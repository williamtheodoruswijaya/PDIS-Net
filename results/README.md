# results/

Metrics produced by the training notebooks, one folder per run:

```
results/<run_id>/v1/
├── test_metrics.json   # final test scores (mIoU, IoU, dice, ...)
├── history.csv         # per-epoch train/val loss and metrics
├── split_{train,val,test}.csv  # image_name -> split used for this run
└── *.png               # sample predictions
```

`<run_id>` is identical to the folder name under `notebooks/`, so
`results/07-segformer-imagenet/` belongs to
`notebooks/07-segformer-imagenet/`.

Results from before the 3x3 grid restart are kept in `.archive/results/`.
