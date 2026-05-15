# Drone Phone Camera Plastic-Waste Demo

This folder is the first prototype for showing how the drone flow will work using a normal webcam or a phone camera through DroidCam.

The default path is:

1. Phone camera streams into Windows through DroidCam.
2. Python reads the camera with OpenCV.
3. A segmentation model predicts the plastic-waste mask.
4. The demo overlays the mask on the live frame.
5. Captures are saved with plastic percentage and optional GPS coordinates.
6. A future dashboard can read `runs/latest_detection.json` or the run CSV.

## Models

The repo currently has two usable model folders:

- SegFormer: `../../model/20261205 - Segformer (mIoU=0.81)`
- DINOv3 / EoMT: `../../model/20261305 - DinoV3 (mIoU=0.7916)`

This demo defaults to SegFormer because the local environment already supports it with `transformers==4.41.2`. DINOv3 support needs a Transformers build that includes `EomtDinov3ForUniversalSegmentation`; the saved config notes `transformers_version: 5.8.1`.

## Setup

From the repo root:

```powershell
cd "D:\BINUS\Semester 6\semantix\drone_phone_demo"
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

If you already have the repo Python environment with `torch`, `transformers`, `opencv-python`, and `safetensors`, you can run with `py` directly.

For DINOv3/EoMT support, use the optional requirements file once your package source has a Transformers build with that architecture:

```powershell
py -m pip install -r requirements-dinov3.txt
```

## DroidCam Camera Source

Use one of these:

- USB DroidCam / virtual webcam: `--source 0`, `--source 1`, etc.
- Wi-Fi DroidCam stream: `--source http://PHONE_IP:4747/video`

Open DroidCam on the phone first, start the connection, then run the demo.

## Run The Demo

SegFormer, default camera:

```powershell
py run_phone_demo.py --model segformer --source 0
```

DroidCam Wi-Fi:

```powershell
py run_phone_demo.py --model segformer --source http://192.168.1.24:4747/video
```

With manual location metadata:

```powershell
py run_phone_demo.py --model segformer --source 0 --lat -6.2088 --lon 106.8456
```

With a telemetry file that another process can update:

```powershell
py run_phone_demo.py --model segformer --source 0 --telemetry-file telemetry.sample.json
```

## Keyboard Controls

- `s`: save a capture now
- `q` or `Esc`: quit

The demo also auto-saves every few seconds. Change it with `--save-every-seconds`.

## Outputs

Each run writes to:

```text
runs/YYYYMMDD_HHMMSS/
  detections.csv
  detections.jsonl
  images/
  masks/
  overlays/
```

The dashboard-friendly pointer is:

```text
runs/latest_detection.json
```

That JSON contains:

- timestamp
- model
- plastic percentage
- latitude
- longitude
- image path
- mask path
- overlay path

## Notes For Drone Framing

This is a ground-station prototype. The phone stands in for the drone camera, and manual or file-based location stands in for flight telemetry. When the drone integration starts, replace the camera source with the drone video stream and replace the telemetry file with MAVLink/GPS data.
