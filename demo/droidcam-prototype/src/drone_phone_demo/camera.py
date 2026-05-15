from __future__ import annotations

from typing import Union

import cv2


CameraSource = Union[int, str]


def parse_camera_source(value: str) -> CameraSource:
    value = str(value).strip()
    if value.isdigit():
        return int(value)
    return value


def open_capture(source: CameraSource) -> cv2.VideoCapture:
    capture = cv2.VideoCapture(source)
    if not capture.isOpened():
        raise RuntimeError(
            "Could not open camera source. For DroidCam, start the app first and use "
            "--source 0/1 for the virtual webcam or --source http://PHONE_IP:4747/video."
        )

    capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    return capture

