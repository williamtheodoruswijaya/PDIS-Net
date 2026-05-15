# Full Walkthrough

This is the end-to-end path from repository to phone-camera plastic-waste demo and dashboard planning.

## What You Are Building

The prototype simulates a drone camera by using a phone camera through DroidCam. The model sees each camera frame, predicts where plastic waste appears, estimates the percentage of the frame covered by plastic, and saves the result with optional GPS coordinates.

The future dashboard reads those saved results and maps them.

## Step 1: Understand The Folders

Important folders:

```text
model/                 trained model artifacts
notebooks/             research and training notebooks
results/               metrics and training histories
droidcam-prototype/    runnable phone-camera prototype
docs/                  documentation
.codex/                agent/vibecoding setup
.skills/               local workflow skills
```

The main folder for the demo is:

```text
droidcam-prototype/
```

## Step 2: Check Python

From the repository root:

```powershell
py --version
```

Use `py` on Windows because `python` may point to the Microsoft Store launcher instead of the real installed Python.

## Step 3: Install Dependencies

```powershell
cd "D:\BINUS\Semester 6\semantix\demo\droidcam-prototype"
py -m pip install -r requirements.txt
```

Optional virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

## Step 4: Check Model Access

The demo can read models from the root `model/` folder. It also supports junctions under `droidcam-prototype/models/`.

Create junctions:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\link_models.ps1
```

This avoids copying large weight files.

## Step 5: Prepare Camera

Normal webcam:

```powershell
py run_phone_demo.py --model segformer --source 0
```

DroidCam virtual camera usually also appears as a camera index:

```powershell
py run_phone_demo.py --model segformer --source 1
```

DroidCam Wi-Fi stream:

```powershell
py run_phone_demo.py --model segformer --source http://PHONE_IP:4747/video
```

## Step 6: Add Location

Manual location:

```powershell
py run_phone_demo.py --model segformer --source 0 --lat -6.2088 --lon 106.8456
```

Telemetry file:

```powershell
py run_phone_demo.py --model segformer --source 0 --telemetry-file telemetry.sample.json
```

## Step 7: Use The Demo

Keyboard:

- `s`: save a capture
- `q`: quit
- `Esc`: quit

Auto-save happens every few seconds by default.

## Step 8: Inspect Outputs

After running, inspect:

```text
droidcam-prototype/runs/latest_detection.json
droidcam-prototype/runs/YYYYMMDD_HHMMSS/detections.csv
droidcam-prototype/runs/YYYYMMDD_HHMMSS/images/
droidcam-prototype/runs/YYYYMMDD_HHMMSS/masks/
droidcam-prototype/runs/YYYYMMDD_HHMMSS/overlays/
```

The dashboard should start with `latest_detection.json`.

## Step 9: Dashboard Plan

Read:

```text
droidcam-prototype/dashboard_planner.md
docs/dashboard/README.md
docs/dashboard/api-contract.md
```

The dashboard MVP should show:

- latest image
- overlay
- plastic percentage
- latitude and longitude
- map marker

## Step 10: Codex/Vibecoding Setup

Read:

```text
AGENTS.md
.codex/README.md
docs/codex/vibecoding-setup.md
.skills/README.md
```

Use the local prompts in `.codex/prompts/` when asking agents to modify the project.

## Done Means

You have a complete prototype loop when:

- Camera opens.
- SegFormer loads.
- Overlay preview appears.
- `latest_detection.json` is created.
- Images, masks, and overlays are saved.
- The dashboard contract has latitude, longitude, and plastic percentage.

