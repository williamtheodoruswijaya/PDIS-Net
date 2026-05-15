# Safety Rules For Agent Work

## Protect Model Artifacts

Do not delete, rename, or rewrite:

```text
model/**/*.pth
model/**/*.safetensors
```

## Protect Output Contract

Do not silently change:

```text
droidcam-prototype/runs/latest_detection.json
```

## Avoid Secrets

Do not commit:

- API keys
- private tokens
- real sensitive GPS logs
- private camera captures

## Keep Changes Focused

Small, verified changes are better than broad rewrites.

## Document Reality

Docs must describe what works now and clearly label future plans.

Do not claim DINOv3 runs locally unless verified after the required package upgrade.

