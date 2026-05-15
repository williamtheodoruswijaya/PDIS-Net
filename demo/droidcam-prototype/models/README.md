# Model Folder

The full trained models are already stored in the repository root under `../../model/`.

For a self-contained demo bundle, either:

1. Keep this folder as-is and run the demo from inside the repo, or
2. Copy/link the two model folders here:

```text
droidcam-prototype/models/segformer/
droidcam-prototype/models/dinov3/
```

The demo automatically looks in both places:

- `droidcam-prototype/models/segformer`
- `../../model/20261205 - Segformer (mIoU=0.81)`
- `droidcam-prototype/models/dinov3`
- `../../model/20261305 - DinoV3 (mIoU=0.7916)`

Use `scripts/link_models.ps1` to create local Windows junctions without duplicating the large weight files.
