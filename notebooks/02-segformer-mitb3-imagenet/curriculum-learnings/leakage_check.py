# Leakage check: did phase 1 or the curriculum put any photo somewhere new compared with baseline v1?
# Compares each run's train/val/test with v1's saved split, checks the three splits never share a photo, and
# counts test photos whose neighbouring video frame is in the photos being trained on. That count is the
# dataset's own near-duplicate level; a run that moved photos around could raise it above v1's.
# Run from the repo root:  python notebooks/02-segformer-mitb3-imagenet/curriculum-learnings/leakage_check.py
import pandas as pd

RES = "results/02-segformer-mitb3-imagenet"
MANIFEST = "https://raw.githubusercontent.com/williamtheodoruswijaya/PDIS-Net/447897111b2ad8ceb014fd99f1e06976da3bb9af/data/clean/manifest.csv"
SPLITS = ["train", "val", "test"]


def saved_split(run):
    return {s: set(pd.read_csv(f"{RES}/{run}/split_{s}.csv")["image_name"]) for s in SPLITS}


m = pd.read_csv(MANIFEST)
v1 = saved_split("v1")
curriculum = {s: set(m.loc[m["split"] == s, "image_name"]) for s in SPLITS}
easy = set(m.loc[(m["split"] == "train") & (m["status"] == "kept"), "image_name"])
runs = {
    "v1 baseline": v1,
    "phase 1 clean": saved_split("v2-clean-stage1"),
    "curriculum, epochs 1-20": {**curriculum, "train": easy},
    "curriculum, epochs 21-40": curriculum,
}

frames = lambda names: {int(n[3:-4]) for n in names}
print(f"{'run':26s} {'train':>5s} {'val':>4s} {'test':>4s} {'moved vs v1':>12s} {'shared':>7s} {'test w/ neighbour in train':>27s}")
for name, r in runs.items():
    moved = sum(len(r[s] - v1[s]) for s in SPLITS)  # photos in a different split than in v1
    shared = len(r["train"] & r["val"]) + len(r["train"] & r["test"]) + len(r["val"] & r["test"])
    train = frames(r["train"])
    near = sum(n - 1 in train or n + 1 in train for n in frames(r["test"]))
    print(f"{name:26s} {len(r['train']):5d} {len(r['val']):4d} {len(r['test']):4d} {moved:12d} {shared:7d} {near:>19d} of {len(r['test'])}")
    assert moved == 0 and shared == 0, name
print("no run moved a photo or shared one between splits")
