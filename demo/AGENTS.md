# Agent Instructions

This file is for Codex and other coding agents working in this repository.

## Project Summary

Semantix is a plastic-waste segmentation project. The current engineering target is a phone-camera prototype that simulates a drone camera using DroidCam, runs a segmentation model, saves results, and feeds a future dashboard.

## Canonical Prototype Folder

Use this folder for runnable prototype work:

```text
droidcam-prototype/
```

Important files:

```text
droidcam-prototype/run_phone_demo.py
droidcam-prototype/src/drone_phone_demo/app.py
droidcam-prototype/src/drone_phone_demo/models.py
droidcam-prototype/src/drone_phone_demo/output.py
droidcam-prototype/dashboard_planner.md
```

## Model Rules

Existing trained models:

```text
model/20261205 - Segformer (mIoU=0.81)
model/20261305 - DinoV3 (mIoU=0.7916)
```

Default to SegFormer for local runnable demos. It is currently compatible with the installed environment.

DINOv3/EoMT is wired in but requires a newer Transformers package that exposes `EomtDinov3ForUniversalSegmentation`.

Do not delete, rename, or regenerate model weights unless the user explicitly asks.

## Output Contract

The dashboard contract centers on:

```text
droidcam-prototype/runs/latest_detection.json
```

Required fields include:

- `timestamp`
- `model`
- `plastic_percentage`
- `latitude`
- `longitude`
- `image_path`
- `mask_path`
- `overlay_path`
- `threshold`
- `camera_source`

Any change to these fields must update dashboard docs.

## Coding Style

- Keep edits focused.
- Preserve existing user work.
- Use clear Python and avoid unnecessary frameworks in the prototype.
- Keep generated outputs ignored.
- Prefer PowerShell commands in docs because this workspace is Windows-based.
- Use `py` instead of `python` in commands unless verifying a cross-platform note.

## Documentation Style

This repo intentionally has detailed docs. When adding or changing behavior, update the nearest relevant document:

- `GETTING_STARTED.md`
- `docs/tutorials/`
- `docs/architecture/`
- `docs/operations/`
- `docs/dashboard/`
- `docs/codex/`

## Verification Commands

Useful checks:

```powershell
py -m compileall droidcam-prototype
py droidcam-prototype\run_phone_demo.py --help
```

If a camera is available:

```powershell
cd droidcam-prototype
py run_phone_demo.py --model segformer --source 0
```

## Do Not

- Do not commit generated `runs/` data.
- Do not duplicate large model weights into docs or examples.
- Do not rely on DINOv3 as the default runnable path until the Transformers requirement is satisfied.
- Do not change dashboard JSON fields silently.

