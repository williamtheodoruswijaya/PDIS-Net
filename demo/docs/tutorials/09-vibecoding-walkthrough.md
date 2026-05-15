# Vibecoding Walkthrough

This tutorial explains how to use Codex-style agent work safely in this repository.

## What Vibecoding Means Here

Vibecoding means using an AI coding agent as a fast collaborator while keeping the project grounded with docs, checklists, and verification commands.

For this repo, vibecoding should be:

- context-aware
- small-step
- verified
- documented
- respectful of model artifacts

## Read Before Prompting

Read:

```text
AGENTS.md
.codex/README.md
.codex/project-instructions.md
.skills/README.md
```

## Pick The Right Prompt

Phone demo:

```text
.codex/prompts/phone-demo.md
```

Dashboard:

```text
.codex/prompts/dashboard.md
```

Debugging:

```text
.codex/prompts/debugging.md
```

Research summary:

```text
.codex/prompts/research-summary.md
```

## Example Prompt

```text
Use the droidcam-phone-demo local skill.
Improve the camera source error message when DroidCam is not connected.
Keep SegFormer as the default model.
Verify with compileall and --help.
Update docs if a command changes.
```

## Good Agent Tasks

- Add a CLI option.
- Improve output JSON.
- Write a dashboard API plan.
- Add a troubleshooting section.
- Refactor a small module.
- Add a smoke test.

## Risky Agent Tasks

- Replace model weights.
- Rewrite notebooks.
- Change dashboard contract silently.
- Make DINOv3 the only model path.
- Add cloud services with secrets.

## Verification Habit

Always ask for the verification result in the final response:

```powershell
py -m compileall droidcam-prototype
py droidcam-prototype\run_phone_demo.py --help
```

