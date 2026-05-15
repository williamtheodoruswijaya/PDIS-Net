# Repository Map

## Root Files

```text
README.md              project overview
GETTING_STARTED.md     first setup path
CONTRIBUTING.md        contribution rules
AGENTS.md              coding agent instructions
mcp.json               MCP server template
```

## Prototype

```text
droidcam-prototype/
  run_phone_demo.py
  requirements.txt
  requirements-dinov3.txt
  telemetry.sample.json
  dashboard_planner.md
  models/
  scripts/
  src/drone_phone_demo/
```

## Prototype Modules

```text
app.py             CLI and main loop
camera.py          OpenCV camera source opening
geo.py             manual/file telemetry
models.py          SegFormer and DINOv3 adapters
output.py          image/mask/overlay/CSV/JSON writer
visualization.py   preview overlay and HUD
```

## Research Assets

```text
notebooks/         training notebooks
results/           metrics and histories
model/             trained artifacts
```

## Agent Setup

```text
.codex/            project instructions, prompts, checklists, MCP mirror
.skills/           local workflow playbooks
docs/codex/        human-readable Codex setup documentation
```

