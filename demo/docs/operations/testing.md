# Testing

## Syntax Check

```powershell
py -m compileall droidcam-prototype
```

## CLI Check

```powershell
py droidcam-prototype\run_phone_demo.py --help
```

## SegFormer Smoke Test

Use a short live run:

```powershell
cd droidcam-prototype
py run_phone_demo.py --model segformer --source 0 --save-every-seconds 0
```

Press `s` once, then quit.

## Output Check

Confirm:

```text
runs/latest_detection.json
runs/YYYYMMDD_HHMMSS/detections.csv
runs/YYYYMMDD_HHMMSS/detections.jsonl
runs/YYYYMMDD_HHMMSS/images/
runs/YYYYMMDD_HHMMSS/masks/
runs/YYYYMMDD_HHMMSS/overlays/
```

## Dashboard Contract Check

`latest_detection.json` should include:

- timestamp
- model
- plastic percentage
- latitude
- longitude
- image path
- mask path
- overlay path

## Manual Visual Check

Look at the saved overlay. It should align with the original frame and not be blank unless the model detected no plastic.

