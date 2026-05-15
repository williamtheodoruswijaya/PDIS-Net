# Runbook

## Normal Demo Run

1. Start DroidCam or connect webcam.
2. Open PowerShell.
3. Run:

```powershell
cd "D:\BINUS\Semester 6\semantix\demo\droidcam-prototype"
py run_phone_demo.py --model segformer --source 0 --lat -6.2088 --lon 106.8456
```

4. Confirm preview.
5. Press `s` to save a sample.
6. Confirm `runs/latest_detection.json`.
7. Quit with `q`.

## Before A Presentation

- Test camera source.
- Test model load.
- Test save output.
- Clean distracting old run folders if needed.
- Prepare sample plastic object.
- Use stable lighting.

## During A Presentation

Explain:

- phone camera simulates drone camera
- red overlay is model prediction
- percentage is image area covered by predicted plastic
- latitude/longitude is currently manual or telemetry-file based
- dashboard will map these records

## After A Presentation

- Keep useful sample outputs if needed.
- Remove accidental private images.
- Record any failure in troubleshooting docs.

