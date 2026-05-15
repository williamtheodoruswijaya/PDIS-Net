# Prompt Recipes

## Improve Phone Demo

```text
Use the local droidcam-phone-demo skill.
Improve [specific behavior] in droidcam-prototype/.
Keep SegFormer as default.
Preserve latest_detection.json fields.
Verify with compileall and --help.
Update docs if needed.
```

## Build Dashboard MVP

```text
Use the local plastic-waste-dashboard skill.
Create the smallest dashboard step that reads droidcam-prototype/runs/latest_detection.json.
Show image, overlay, percentage, timestamp, and map marker.
Do not change the output contract without updating docs.
```

## Debug A Failure

```text
Use the debugging prompt in .codex/prompts/debugging.md.
Find the failing layer first: environment, camera, model loading, inference, output, or dashboard.
Use the smallest reproducing command.
Explain the verification result.
```

## Summarize Research

```text
Use the research summary prompt.
Summarize results from model configs and results files.
Separate measured metrics from deployment assumptions.
```

