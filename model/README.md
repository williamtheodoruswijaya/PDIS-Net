# model/

Weights (`best.pth`, Git LFS) + the `test_metrics.json` they scored, one folder per run and version:
`model/<run_id>/<version>/`. Same `<run_id>` as `notebooks/` and `results/`.
Old models (before the 3x3 grid restart) are in `.archive/model/`.

Regenerate this table: `python model/build_index.py`. Sorted by mIoU, best first.

| run | version | foreground IoU | mIoU | background IoU | dice |
|---|---|---|---|---|---|
| 02-segformer-mitb3-imagenet | v1 | 0.6746 | 0.8210 | 0.9675 | 0.7720 |
| 04-segformer-mitb3-aerial | v1 | 0.6595 | 0.8140 | 0.9685 | 0.7588 |
| 07-segformer-mitb5-imagenet | v1 | 0.6501 | 0.8087 | 0.9673 | 0.7483 |
| 05-segformer-mitb3-ade | v1 | 0.6499 | 0.8077 | 0.9654 | 0.7469 |
| 03-unet-mitb3-imagenet | v1 | 0.6128 | 0.7918 | 0.9709 | 0.7125 |
| 06-segformer-mitb3-drone | v1 | 0.6001 | 0.7809 | 0.9617 | 0.6996 |
| 09-unet-resnet34-imagenet | v1 | 0.5694 | 0.7677 | 0.9661 | 0.6681 |
| 08-unet-resnet34-raw | v1 | 0.3464 | 0.6494 | 0.9524 | 0.4427 |
| 01-segformer-mitb3-raw | v1 | 0.1404 | 0.4725 | 0.8046 | 0.1841 |
