# Capture And Outputs

The phone demo writes both visual evidence and dashboard-ready metadata.

## Output Folder

Each run creates:

```text
droidcam-prototype/runs/YYYYMMDD_HHMMSS/
```

Inside:

```text
detections.csv
detections.jsonl
images/
masks/
overlays/
```

## Latest Dashboard File

The live dashboard pointer is:

```text
droidcam-prototype/runs/latest_detection.json
```

This file is overwritten with the newest saved detection.

## Saved Image Types

Original image:

```text
images/frame_000001.jpg
```

Binary mask:

```text
masks/frame_000001_mask.png
```

Overlay:

```text
overlays/frame_000001_overlay.jpg
```

## Plastic Percentage

Plastic percentage is calculated from the binary segmentation mask:

```text
plastic pixels / total pixels * 100
```

This is a frame-level estimate. It is not yet a real-world area measurement because camera altitude, camera angle, and lens calibration are not included.

## Location Fields

Location can come from:

- manual CLI arguments
- telemetry JSON file
- future drone telemetry

Manual:

```powershell
--lat -6.2088 --lon 106.8456
```

Telemetry file:

```json
{
  "latitude": -6.2088,
  "longitude": 106.8456,
  "altitude_m": 25.0,
  "source": "manual-sample"
}
```

## Dashboard Record Example

```json
{
  "run_id": "20260515_224500",
  "frame_index": 5,
  "timestamp": "2026-05-15T22:45:30",
  "model": "segformer",
  "plastic_percentage": 12.34,
  "latitude": -6.2088,
  "longitude": 106.8456,
  "altitude_m": 25.0,
  "telemetry_source": "manual",
  "threshold": 0.8,
  "inference_ms": 1520.21,
  "camera_source": "0",
  "image_path": "runs/20260515_224500/images/frame_000005.jpg",
  "mask_path": "runs/20260515_224500/masks/frame_000005_mask.png",
  "overlay_path": "runs/20260515_224500/overlays/frame_000005_overlay.jpg"
}
```

## Do Not Commit Outputs

`runs/` is generated data. Keep it local unless a specific sample is intentionally added.

