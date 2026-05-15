# DINOv3 Optional Setup

DINOv3/EoMT is available as a trained model artifact, but it is not the default runnable path for this workspace.

## Why It Is Optional

The saved config uses:

```text
EomtDinov3ForUniversalSegmentation
```

The local environment checked during prototype setup had `transformers==4.41.2`, which did not expose that class.

## Current Recommendation

Use SegFormer for:

- phone demo
- first dashboard testing
- thesis demonstration flow

Use DINOv3 for:

- comparison
- research notes
- future higher-end inference
- server or GPU ground-station experiments

## Install Attempt

The prototype includes:

```text
droidcam-prototype/requirements-dinov3.txt
```

Install only when your package source has a compatible Transformers build:

```powershell
cd droidcam-prototype
py -m pip install -r requirements-dinov3.txt
```

## Run

```powershell
py run_phone_demo.py --model dinov3 --source 0
```

If the architecture is missing, the demo should fail with a clear message and tell you to use SegFormer.

## Practical Drone Note

DINOv3/EoMT is heavier than SegFormer. It may be better as:

- a research comparison model
- a ground-station/server inference model
- a teacher model for improving labels

It is less likely to be the first model deployed directly on a small drone.

