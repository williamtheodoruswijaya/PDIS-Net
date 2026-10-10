# model/

Weights (`best.pth`, Git LFS) + the `test_metrics.json` they scored, one folder per run and version:
`model/<run_id>/<version>/`. Same `<run_id>` as `notebooks/` and `results/`.
Old models (before the 3x3 grid restart) are in `.archive/model/`.

Regenerate this table: `python model/build_index.py`. Sorted by mIoU, best first.

| run | version | foreground IoU | mIoU | background IoU | dice | mPA |
|---|---|---|---|---|---|---|
| 02-segformer-mitb3-imagenet | v1 | 0.6746 | 0.8210 | 0.9675 | 0.7720 | 0.8975 |
| 04-segformer-mitb3-aerial | v1 | 0.6595 | 0.8140 | 0.9685 | 0.7588 | 0.9022 |
| 13-deeplabv3plus-mitb3-imagenet | v2 | 0.6495 | 0.8092 | 0.9688 | 0.7470 | 0.8908 |
| 07-segformer-mitb5-imagenet | v1 | 0.6501 | 0.8087 | 0.9673 | 0.7483 | 0.8886 |
| 05-segformer-mitb3-ade | v1 | 0.6499 | 0.8077 | 0.9654 | 0.7469 | 0.9006 |
| 03-unet-mitb3-imagenet | v1 | 0.6128 | 0.7918 | 0.9709 | 0.7125 | 0.8666 |
| 06-segformer-mitb3-drone | v1 | 0.6001 | 0.7809 | 0.9617 | 0.6996 | 0.8822 |
| 10-segformer-resnet34-imagenet | v1 | 0.5969 | 0.7801 | 0.9632 | 0.6950 | 0.8741 |
| 14-deeplabv3plus-resnet34-imagenet | v2 | 0.5999 | 0.7753 | 0.9506 | 0.7016 | 0.8824 |
| 09-unet-resnet34-imagenet | v1 | 0.5694 | 0.7677 | 0.9661 | 0.6681 | 0.8705 |
| 12-segformer-mitb0-imagenet | v2 | 0.5521 | 0.7552 | 0.9583 | 0.6509 | 0.8725 |
| 11-segformer-resnet34-raw | v2 | 0.3779 | 0.6535 | 0.9292 | 0.4580 | 0.8274 |
| 08-unet-resnet34-raw | v1 | 0.3464 | 0.6494 | 0.9524 | 0.4427 | 0.8346 |
| 15-deeplabv3plus-resnet34-raw | v2 | 0.2727 | 0.5867 | 0.9007 | 0.3562 | 0.8237 |
| 01-segformer-mitb3-raw | v1 | 0.1404 | 0.4725 | 0.8046 | 0.1841 | 0.6958 |
