# Contributing

Thank you for improving Semantix. The project is in prototype mode, so the most important contribution style is careful, small, and reproducible.

## Priorities

Highest priority:

1. Keep `droidcam-prototype/` runnable.
2. Preserve trained model artifacts.
3. Keep dashboard output fields stable.
4. Document every workflow that a thesis/demo evaluator needs to repeat.
5. Avoid large refactors unless they unblock the demo or dashboard.

## Development Workflow

1. Check the current state:

```powershell
git status --short
```

2. Read relevant docs before changing behavior:

```text
AGENTS.md
docs/tutorials/00-full-walkthrough.md
docs/architecture/data-flow.md
docs/operations/testing.md
```

3. Make a focused change.
4. Run the smallest useful verification.
5. Update docs if commands, paths, outputs, or assumptions changed.

## Branch Names

Recommended branch names:

```text
codex/phone-demo-fix
codex/dashboard-contract
codex/docs-vibecoding
feature/dashboard-map
fix/droidcam-source
```

## Commit Style

Use short, descriptive commit messages:

```text
docs: add DroidCam walkthrough
prototype: save dashboard detection JSON
dashboard: define map marker contract
```

## Coding Guidelines

- Keep Python simple and explicit.
- Prefer readable model adapters over clever abstractions.
- Keep model loading isolated in `droidcam-prototype/src/drone_phone_demo/models.py`.
- Keep camera logic isolated in `camera.py`.
- Keep output contract logic isolated in `output.py`.
- Do not hard-code secrets or private machine credentials.
- Do not modify trained weight files unless the task is specifically about model packaging.

## Documentation Guidelines

Update docs when:

- A command changes
- A file path changes
- A JSON field changes
- A model requirement changes
- A setup assumption changes
- A dashboard contract changes

Good docs should answer:

- What is this for?
- When should I use it?
- What command do I run?
- What output should I expect?
- What can go wrong?
- How do I verify it worked?

## Testing Expectations

For phone demo changes:

```powershell
py -m compileall droidcam-prototype
py droidcam-prototype\run_phone_demo.py --help
```

For model loading changes, run a small smoke test or a short real camera run.

For dashboard contract changes, inspect:

```text
droidcam-prototype/runs/latest_detection.json
```

## Model Artifact Rules

Treat these as precious artifacts:

```text
model/**/*.safetensors
model/**/*.pth
```

Do not:

- Delete them
- Rename them casually
- Re-save them with unverified code
- Commit generated duplicate copies

If a model is replaced, update:

- [docs/operations/dataset-and-models.md](docs/operations/dataset-and-models.md)
- [docs/research/model-comparison.md](docs/research/model-comparison.md)
- `droidcam-prototype/models/model_manifest.json`

## Review Checklist

Before merging:

- Demo still starts
- README commands still match reality
- Output JSON still contains image path, percentage, latitude, longitude
- Generated `runs/` output is ignored
- Docs are updated
- No unrelated notebook or weight churn is included

