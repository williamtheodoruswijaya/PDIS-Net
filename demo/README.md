# Semantix Plastic Waste Segmentation

Semantix is a plastic-debris image segmentation project focused on turning trained computer-vision models into a drone-ready field workflow. The current practical prototype uses a phone camera through DroidCam as a stand-in for a drone camera, runs a segmentation model, estimates plastic-waste coverage, and writes dashboard-ready outputs.

## What Is In This Repository

```text
model/                 Trained model artifacts and configs
notebooks/             Training and evaluation notebooks
results/               Training histories and test metrics
droidcam-prototype/    Phone-camera inference prototype
docs/                  Project documentation and walkthroughs
.codex/                Codex/vibecoding project setup notes
.skills/               Local workflow skills for agents
```

## Current Working Prototype

The main runnable prototype is:

```text
droidcam-prototype/
```

It supports:

- Webcam or DroidCam video input
- SegFormer inference as the default working model
- DINOv3/EoMT adapter scaffolding
- Plastic mask overlay
- Plastic percentage calculation
- Optional latitude and longitude metadata
- Saved original images, masks, overlays, CSV, JSONL, and latest dashboard JSON

Start here:

- [Getting Started](GETTING_STARTED.md)
- [Full Walkthrough](docs/tutorials/00-full-walkthrough.md)
- [DroidCam Setup](docs/tutorials/02-droidcam-setup.md)
- [Phone Demo Run Guide](docs/tutorials/03-run-phone-demo.md)

## Quick Run

```powershell
cd "D:\BINUS\Semester 6\semantix\demo\droidcam-prototype"
py run_phone_demo.py --model segformer --source 0
```

For DroidCam Wi-Fi:

```powershell
py run_phone_demo.py --model segformer --source http://PHONE_IP:4747/video --lat -6.2088 --lon 106.8456
```

## Models

Current usable model folders:

- `model/20261205 - Segformer (mIoU=0.81)`
- `model/20261305 - DinoV3 (mIoU=0.7916)`

SegFormer is the default demo model because it works with the local Python package versions already available in this workspace. DINOv3/EoMT requires a Transformers version that includes `EomtDinov3ForUniversalSegmentation`.

## Dashboard Direction

The demo writes the live dashboard contract here:

```text
droidcam-prototype/runs/latest_detection.json
```

The planned dashboard should read this file during the MVP stage, then later move to a FastAPI backend and spatial database.

Dashboard docs:

- [Dashboard Planner](droidcam-prototype/dashboard_planner.md)
- [Dashboard Overview](docs/dashboard/README.md)
- [Dashboard API Contract](docs/dashboard/api-contract.md)
- [Dashboard Database Schema](docs/dashboard/database-schema.md)

## For Contributors And Agents

- [Contributing Guide](CONTRIBUTING.md)
- [Agent Instructions](AGENTS.md)
- [Codex Setup](docs/codex/README.md)
- [Vibecoding Setup](docs/codex/vibecoding-setup.md)
- [MCP Setup](docs/codex/mcp-setup.md)

## Repository Status

This project is currently in prototype mode. The highest-value path is:

1. Keep the phone demo stable.
2. Make the output contract reliable.
3. Build the dashboard around the output contract.
4. Replace manual telemetry with drone telemetry.
5. Optimize deployment for field hardware.

