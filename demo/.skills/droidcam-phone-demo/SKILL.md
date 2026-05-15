# DroidCam Phone Demo Skill

## Use When

Use this skill when working on:

- DroidCam setup
- webcam source handling
- live segmentation preview
- saving captures
- phone-as-drone-camera prototype behavior

## Key Files

```text
droidcam-prototype/run_phone_demo.py
droidcam-prototype/src/drone_phone_demo/app.py
droidcam-prototype/src/drone_phone_demo/camera.py
droidcam-prototype/src/drone_phone_demo/output.py
droidcam-prototype/README.md
```

## Workflow

1. Read `AGENTS.md`.
2. Inspect the current prototype files.
3. Keep SegFormer as the default model.
4. Make the smallest useful code or doc change.
5. Verify CLI and syntax.
6. If camera hardware is available, run a short live test.

## Verification

```powershell
py -m compileall droidcam-prototype
py droidcam-prototype\run_phone_demo.py --help
```

Live test:

```powershell
cd droidcam-prototype
py run_phone_demo.py --model segformer --source 0
```

## Output Contract

Do not break:

```text
droidcam-prototype/runs/latest_detection.json
```

