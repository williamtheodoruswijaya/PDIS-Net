# Phone Demo Preflight Checklist

Use this before running or modifying the phone/DroidCam demo.

## Environment

- Repository root is correct.
- Python launcher works:

```powershell
py --version
```

- Dependencies are installed:

```powershell
cd droidcam-prototype
py -m pip install -r requirements.txt
```

## Models

- SegFormer model folder exists:

```text
model/20261205 - Segformer (mIoU=0.81)
```

- Local model junction exists or fallback path is available:

```text
droidcam-prototype/models/segformer
```

## Camera

- DroidCam app is open on the phone.
- Phone and computer are connected through USB or same Wi-Fi.
- For virtual webcam mode, test `--source 0` then `--source 1`.
- For Wi-Fi mode, use `http://PHONE_IP:4747/video`.

## Run

```powershell
cd droidcam-prototype
py run_phone_demo.py --model segformer --source 0
```

## Verify

- Preview window appears.
- Plastic overlay appears when plastic-like objects are visible.
- Press `s` to save.
- Confirm:

```text
runs/latest_detection.json
runs/YYYYMMDD_HHMMSS/images/
runs/YYYYMMDD_HHMMSS/masks/
runs/YYYYMMDD_HHMMSS/overlays/
```

