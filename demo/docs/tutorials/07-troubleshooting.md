# Troubleshooting

Use this guide when the demo does not run.

## Python Not Found

Problem:

```text
Python was not found
```

Try:

```powershell
py --version
```

Use `py` commands from the docs.

## Camera Does Not Open

Try another camera index:

```powershell
py run_phone_demo.py --model segformer --source 1
```

For DroidCam Wi-Fi, confirm the URL:

```powershell
py run_phone_demo.py --model segformer --source http://PHONE_IP:4747/video
```

Check:

- DroidCam phone app is running.
- DroidCam Windows client is connected.
- Phone and laptop are on same Wi-Fi.
- Firewall is not blocking the stream.

## Model Does Not Load

Confirm model folders:

```text
model/20261205 - Segformer (mIoU=0.81)
model/20261305 - DinoV3 (mIoU=0.7916)
```

Try linking models:

```powershell
cd droidcam-prototype
powershell -ExecutionPolicy Bypass -File .\scripts\link_models.ps1
```

## DINOv3 Fails

If the error mentions `EomtDinov3ForUniversalSegmentation`, use SegFormer:

```powershell
py run_phone_demo.py --model segformer --source 0
```

The DINOv3 model needs a newer Transformers architecture implementation.

## Preview Is Slow

Try:

- Use `--device cuda` if CUDA is available.
- Lower DroidCam resolution.
- Close other apps.
- Use USB mode instead of Wi-Fi.
- Increase auto-save interval.

## No Plastic Detected

Try:

- Better lighting.
- Closer plastic objects.
- Lower threshold:

```powershell
py run_phone_demo.py --model segformer --source 0 --threshold 0.5
```

Lower thresholds may create more false positives.

## Outputs Missing

Press `s` while the preview is open, then check:

```text
droidcam-prototype/runs/
```

If `--save-every-seconds 0` was used, auto-save is disabled.

