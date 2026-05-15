from __future__ import annotations

import argparse
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import cv2

from .camera import open_capture, parse_camera_source
from .geo import TelemetryProvider
from .models import load_segmenter
from .output import DetectionWriter
from .visualization import draw_hud, make_overlay


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run plastic-waste segmentation on a webcam or DroidCam stream."
    )
    parser.add_argument(
        "--model",
        choices=["segformer", "dinov3"],
        default="segformer",
        help="Model adapter to use. SegFormer is the practical default for this environment.",
    )
    parser.add_argument(
        "--model-path",
        type=Path,
        default=None,
        help="Optional explicit model folder. If omitted, the demo searches local and repo model paths.",
    )
    parser.add_argument(
        "--source",
        default="0",
        help="OpenCV camera index such as 0/1, or a DroidCam URL like http://PHONE_IP:4747/video.",
    )
    parser.add_argument(
        "--device",
        default="auto",
        choices=["auto", "cpu", "cuda"],
        help="Inference device.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=None,
        help="Override mask threshold. Defaults are 0.8 for SegFormer and 0.9 for DINOv3.",
    )
    parser.add_argument(
        "--lat",
        type=float,
        default=None,
        help="Manual latitude to attach to saved detections.",
    )
    parser.add_argument(
        "--lon",
        type=float,
        default=None,
        help="Manual longitude to attach to saved detections.",
    )
    parser.add_argument(
        "--telemetry-file",
        type=Path,
        default=None,
        help="Optional JSON file containing latitude/longitude. Updated values are read while running.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "runs",
        help="Directory for captures and dashboard logs.",
    )
    parser.add_argument(
        "--save-every-seconds",
        type=float,
        default=5.0,
        help="Automatically save a dashboard sample every N seconds. Set 0 to disable auto-save.",
    )
    parser.add_argument(
        "--display-width",
        type=int,
        default=1280,
        help="Max preview width for the OpenCV window.",
    )
    parser.add_argument(
        "--no-window",
        action="store_true",
        help="Run headless and only write outputs. Useful for remote/embedded tests.",
    )
    return parser


def resize_for_display(frame, max_width: int):
    height, width = frame.shape[:2]
    if width <= max_width:
        return frame
    scale = max_width / float(width)
    return cv2.resize(frame, (max_width, int(height * scale)), interpolation=cv2.INTER_AREA)


def should_save(
    last_save_at: Optional[float],
    save_every_seconds: float,
    manual_requested: bool,
) -> bool:
    if manual_requested:
        return True
    if save_every_seconds <= 0:
        return False
    now = time.monotonic()
    return last_save_at is None or (now - last_save_at) >= save_every_seconds


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    source = parse_camera_source(args.source)
    segmenter = load_segmenter(
        model_name=args.model,
        model_path=args.model_path,
        device=args.device,
        threshold=args.threshold,
    )
    telemetry = TelemetryProvider(
        manual_latitude=args.lat,
        manual_longitude=args.lon,
        telemetry_file=args.telemetry_file,
    )
    writer = DetectionWriter(args.output_dir, model_name=args.model, camera_source=str(args.source))

    cap = open_capture(source)
    window_name = "Drone Phone Plastic Waste Demo"
    last_save_at = None
    frame_index = 0

    if not args.no_window:
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    print("Phone camera demo is running.")
    print("Press 's' to save a capture, 'q' or Esc to quit.")
    print(f"Model: {args.model} | threshold: {segmenter.threshold:.2f} | source: {args.source}")

    try:
        while True:
            ok, frame_bgr = cap.read()
            if not ok or frame_bgr is None:
                print("Camera frame was not available. Check DroidCam/webcam connection.")
                time.sleep(0.5)
                continue

            result = segmenter.predict(frame_bgr)
            overlay = make_overlay(frame_bgr, result.mask, result.probability)
            location = telemetry.read()
            timestamp = datetime.now().replace(microsecond=0).isoformat()
            display = draw_hud(
                overlay,
                plastic_percentage=result.plastic_percentage,
                model_name=args.model,
                threshold=segmenter.threshold,
                latitude=location.latitude,
                longitude=location.longitude,
                timestamp=timestamp,
            )

            key = -1
            if not args.no_window:
                cv2.imshow(window_name, resize_for_display(display, args.display_width))
                key = cv2.waitKey(1) & 0xFF

            manual_save = key == ord("s")
            if should_save(last_save_at, args.save_every_seconds, manual_save):
                writer.write(
                    frame_index=frame_index,
                    timestamp=timestamp,
                    frame_bgr=frame_bgr,
                    mask=result.mask,
                    overlay_bgr=overlay,
                    plastic_percentage=result.plastic_percentage,
                    threshold=segmenter.threshold,
                    latitude=location.latitude,
                    longitude=location.longitude,
                    altitude_m=location.altitude_m,
                    telemetry_source=location.source,
                    inference_ms=result.inference_ms,
                )
                last_save_at = time.monotonic()

            frame_index += 1

            if key in (ord("q"), 27):
                break

    except KeyboardInterrupt:
        print("Stopping demo.")
    finally:
        cap.release()
        if not args.no_window:
            cv2.destroyAllWindows()

    print(f"Run saved at: {writer.run_dir}")
    print(f"Dashboard latest JSON: {writer.latest_json_path}")
    return 0

