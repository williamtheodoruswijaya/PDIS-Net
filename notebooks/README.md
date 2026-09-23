# notebooks/

Training notebooks, one folder per run:

```
notebooks/<NN>-<architecture>-<backbone>-<init>/v1.ipynb
```

- `<NN>` is the order the run is executed (`01` … `13`), so the folders sort
  themselves in the order the thesis reports them.
- `<architecture>-<backbone>-<init>` names the three variables being compared, e.g.
  `07-segformer-mitb3-imagenet`, `08-segformer-mitb3-raw`, `09-segformer-mitb3-aerial`,
  `01-unet-resnet50-imagenet`.
- Rerunning an experiment adds `v2.ipynb` next to `v1.ipynb`. Nothing is
  overwritten, so an earlier number can always be traced back to the notebook
  that produced it.

The same `<run_id>` folder name is reused in `results/` and `xai/`, so any file
can be traced back to the run that produced it.

Notebooks from before the 3x3 grid restart are kept intact in
`.archive/notebooks/`.
