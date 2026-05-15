# Agent Playbooks

## Phone Demo Playbook

Use when changing camera, inference loop, output writer, or CLI behavior.

Read:

```text
.skills/droidcam-phone-demo/SKILL.md
droidcam-prototype/README.md
docs/tutorials/03-run-phone-demo.md
```

Verify:

```powershell
py -m compileall droidcam-prototype
py droidcam-prototype\run_phone_demo.py --help
```

## Dashboard Playbook

Use when planning or building map/data features.

Read:

```text
.skills/plastic-waste-dashboard/SKILL.md
droidcam-prototype/dashboard_planner.md
docs/dashboard/api-contract.md
```

Rule:

```text
Do not break latest_detection.json.
```

## Model Inference Playbook

Use when changing model logic.

Read:

```text
.skills/model-inference/SKILL.md
docs/architecture/model-inference.md
droidcam-prototype/src/drone_phone_demo/models.py
```

Rule:

```text
Output mask size must match input frame size.
```

## Docs Playbook

Use when adding docs.

Read:

```text
.skills/project-docs/SKILL.md
.codex/checklists/docs-preflight.md
docs/README.md
```

Rule:

```text
Use actual paths and verified commands.
```

