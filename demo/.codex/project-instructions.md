# Project Instructions For Codex

## Mission

Help evolve Semantix from research notebooks and trained models into a reliable drone-style plastic-waste detection workflow.

## Current Main Goal

The main goal is still the phone/DroidCam demo. Dashboard work should be planned and contract-driven until the phone prototype is stable.

## What To Protect

Protect these assets:

```text
model/
notebooks/
results/
```

Large model files are important. Do not delete or rewrite them unless explicitly requested.

## What To Improve

Useful improvements:

- Better camera source handling
- Better inference performance
- More robust output records
- Dashboard API prototype
- Better docs and walkthroughs
- Telemetry integration plan

## Model Policy

SegFormer is the default because it runs locally.

DINOv3/EoMT is a supported target but may require package upgrades. Do not make DINOv3 the only runnable path unless it is verified in the environment.

## Dashboard Policy

Do not build a dashboard that invents data. Use the demo output contract:

```text
droidcam-prototype/runs/latest_detection.json
```

If a dashboard mock needs data, create small sample JSON under a documented sample folder, not inside generated `runs/`.

## Verification Policy

For docs-only changes:

- Check links and paths manually.

For Python changes:

```powershell
py -m compileall droidcam-prototype
py droidcam-prototype\run_phone_demo.py --help
```

For inference changes:

- Run a small model-loading smoke test.
- Run the live camera if hardware is available.

