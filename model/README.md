# model/

Weights (`best.pth`, Git LFS) + the `test_metrics.json` they scored, one folder per run and version:
`model/<run_id>/<version>/`. Same `<run_id>` as `notebooks/` and `results/`.
Old models (before the 3x3 grid restart) are in `.archive/model/`.

Regenerate this table: `python model/build_index.py`. Sorted by mIoU, best first.

| run | version | foreground IoU | mIoU | background IoU | dice |
|---|---|---|---|---|---|
| 02-segformer-mitb3-imagenet | v1 | 0.6746 | 0.8210 | 0.9675 | 0.7720 |
| 04-segformer-mitb3-aerial | v1 | 0.6595 | 0.8140 | 0.9685 | 0.7588 |
| 03-unet-mitb3-imagenet | v1 | 0.6128 | 0.7918 | 0.9709 | 0.7125 |
| 01-segformer-mitb3-raw | v1 | 0.1404 | 0.4725 | 0.8046 | 0.1841 |
