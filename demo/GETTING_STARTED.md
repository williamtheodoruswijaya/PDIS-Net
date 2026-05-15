# Getting Started

This guide gets you from a fresh clone to a working phone-camera plastic-waste segmentation demo.

## 1. Requirements

Use Windows PowerShell from the repository root.

Needed:

- Python available through `py`
- Phone with DroidCam installed, or any normal webcam
- Existing trained model folders in `model/`
- Enough RAM for SegFormer inference

Recommended:

- NVIDIA GPU with CUDA for faster inference
- Good lighting for camera testing
- Stable phone mount or tripod

## 2. Verify The Repository

From the root:

```powershell
Get-ChildItem
```

You should see:

```text
model/
notebooks/
results/
droidcam-prototype/
docs/
```

## 3. Enter The Prototype

```powershell
cd "D:\BINUS\Semester 6\semantix\demo\droidcam-prototype"
```

## 4. Install Python Dependencies

Optional virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

If you already have the dependencies in your global Python environment, you can run directly with `py`.

## 5. Link Models

The prototype can read models directly from `../../model/` when run from `droidcam-prototype/`. It also supports local model paths under `droidcam-prototype/models/`.

To create Windows junctions without duplicating model weights:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\link_models.ps1
```

Expected links:

```text
droidcam-prototype/models/segformer -> ../../model/20261205 - Segformer (mIoU=0.81)
droidcam-prototype/models/dinov3    -> ../../model/20261305 - DinoV3 (mIoU=0.7916)
```

## 6. Run With A Normal Webcam

```powershell
py run_phone_demo.py --model segformer --source 0
```

If camera `0` is not correct, try:

```powershell
py run_phone_demo.py --model segformer --source 1
```

## 7. Run With DroidCam

For DroidCam virtual webcam mode:

```powershell
py run_phone_demo.py --model segformer --source 0
```

For DroidCam Wi-Fi stream:

```powershell
py run_phone_demo.py --model segformer --source http://PHONE_IP:4747/video
```

Replace `PHONE_IP` with the IP shown in the DroidCam app.

## 8. Add Location Metadata

Manual location:

```powershell
py run_phone_demo.py --model segformer --source 0 --lat -6.2088 --lon 106.8456
```

Telemetry file:

```powershell
py run_phone_demo.py --model segformer --source 0 --telemetry-file telemetry.sample.json
```

The telemetry file can be updated while the demo is running.

## 9. Understand Outputs

Every run creates:

```text
runs/YYYYMMDD_HHMMSS/
  detections.csv
  detections.jsonl
  images/
  masks/
  overlays/
```

The latest dashboard record is:

```text
runs/latest_detection.json
```

## 10. Next Reading

- [Full Walkthrough](docs/tutorials/00-full-walkthrough.md)
- [Output Tutorial](docs/tutorials/04-capture-and-outputs.md)
- [Troubleshooting](docs/tutorials/07-troubleshooting.md)
