# notebooks/

Training notebooks, one folder per run:

```
notebooks/<NN>-<architecture>-<init>/v1.ipynb
```

- `<NN>` is the order the run is executed (`01` … `13`), so the folders sort
  themselves in the order the thesis reports them.
- `<architecture>-<init>` names the two variables being compared, e.g.
  `07-segformer-imagenet`, `08-segformer-raw`, `09-segformer-aerial`.
- Rerunning an experiment adds `v2.ipynb` next to `v1.ipynb`. Nothing is
  overwritten, so an earlier number can always be traced back to the notebook
  that produced it.

The same `<run_id>` folder name is reused in `results/` and `xai/`, so any file
can be traced back to the run that produced it.

Notebooks from before the 3x3 grid restart are kept intact in
`.archive/notebooks/`.
