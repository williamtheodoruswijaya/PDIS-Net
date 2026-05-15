# Model Inference Skill

## Use When

Use this skill when changing model loading, preprocessing, inference, thresholds, masks, or percentages.

## Key Files

```text
droidcam-prototype/src/drone_phone_demo/models.py
droidcam-prototype/models/model_manifest.json
model/20261205 - Segformer (mIoU=0.81)/
model/20261305 - DinoV3 (mIoU=0.7916)/
```

## Model Defaults

- SegFormer default threshold: `0.8`
- DINOv3 default threshold: from `training_metadata.json`, usually `0.9`

## Important Compatibility Note

The current local environment supports SegFormer. DINOv3/EoMT needs a Transformers build with `EomtDinov3ForUniversalSegmentation`.

## Workflow

1. Confirm which model is being changed.
2. Read the matching config and processor config.
3. Keep output masks the same size as input frames.
4. Keep plastic percentage as `plastic pixels / total pixels * 100`.
5. Run a synthetic inference smoke test when possible.

## Verification

```powershell
py -m compileall droidcam-prototype
py droidcam-prototype\run_phone_demo.py --help
```

For SegFormer, run a small adapter test or live camera test.

