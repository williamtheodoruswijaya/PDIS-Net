# Builds data/clean/FloPWD-clean-stage1.zip = raw FloPWD minus the hand-checked bad annotations below.
# Curriculum learning step 1. Run from the repo root:  python data/clean/build_clean.py
import zipfile
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

RAW = Path("data/raw")
OUT = Path("data/clean")
ZIP = OUT / "FloPWD-clean-stage1.zip"
ZIP_ROOT = "Dal Lake Floating Plastic Waste Detection Dataset (FloPWD 2025)"  # same folder name as the original zip, so notebook paths still work
LABELS = "Image_labels_Binary Classification Task.csv"
REG = "Mask_foreground_percentages_Regression Task.csv"

# Every photo number below was checked by eye on an overlay sheet (audit/*.jpg, rules in README.md).
REMOVE = {
    "coarse_zone": [*range(1199, 1220), *range(1418, 1488)],  # two video runs drawn as one big zone over grass/soil/water
    "missing_mask": [96, 340, 772],                            # plastic clearly visible, mask is empty
}
KEEP_NOTE = {
    "rough_polygon": [*range(1222, 1229), 1285, 1286, 1287, 1336, *range(1375, 1380),  # loose outline, but around a real litter pile
                      *range(1492, 1496), 1508, 1509, 1510, 1545, 1547, 1548, 1789, 1790, 1888, 1889],
    "yes_label_empty_mask": [762, 947, 1633, 1634, 1635],  # nothing clearly plastic visible, so the empty mask is defensible
    "no_label_nonempty_mask": [447, 614, 1000, 1797],      # small correct mask; only the yes/no CSV is off, segmentation unaffected
}

lab = pd.read_csv(RAW / LABELS)
reg = pd.read_csv(RAW / REG)
df = lab.merge(reg, on="image name", how="inner")  # same row order as the notebook's labels_df.merge(reg_df)
df["has_plastic"] = (df["Presence of plastic waste?"].astype(str).str.lower() == "yes").astype(int)

# the exact split notebooks/v2.ipynb makes on all 2002 photos, frozen here so dropping photos can't reshuffle it
tv, te = train_test_split(df, test_size=0.15, random_state=42, stratify=df["has_plastic"])
tr, va = train_test_split(tv, test_size=15/85, random_state=42, stratify=tv["has_plastic"])

m = pd.DataFrame({"image_name": df["image name"], "split": "train", "status": "kept", "category": ""})
m.loc[va.index, "split"] = "val"
m.loc[te.index, "split"] = "test"
num = m["image_name"].str[3:-4].astype(int)
for cat, nums in KEEP_NOTE.items():
    m.loc[num.isin(nums), "category"] = cat
for cat, nums in REMOVE.items():
    m.loc[num.isin(nums), ["status", "category"]] = ["removed", cat]
assert num.isin([n for v in [*REMOVE.values(), *KEEP_NOTE.values()] for n in v]).sum() == \
    sum(len(v) for v in [*REMOVE.values(), *KEEP_NOTE.values()]), "a listed photo number is missing or listed twice"

# biggest_blob_pct = area of the largest connected mask region, % of the photo; used to pick which photos to eye-check
masks = {n: cv2.imread(str(RAW / "Segmentation_Masks" / f"{n[:-4]}_mask.png"), cv2.IMREAD_GRAYSCALE) > 127 for n in m["image_name"]}
def biggest_blob(mask):
    k, _, st, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8))
    return st[1:, cv2.CC_STAT_AREA].max() / mask.size * 100 if k > 1 else 0.0
m["fg_pct"] = df["plastic waste accumulation (in percentage)"]
m["biggest_blob_pct"] = m["image_name"].map(lambda n: round(biggest_blob(masks[n]), 2))
m.to_csv(OUT / "manifest.csv", index=False)

# audit sheets: every flagged photo, mask filled red + yellow outline, 4x4 per page
(OUT / "audit").mkdir(exist_ok=True)
for cat in [*REMOVE, *KEEP_NOTE]:
    tiles = []
    for r in m[m["category"] == cat].itertuples():
        img = cv2.resize(cv2.imread(str(RAW / "Raw_Images" / r.image_name)), (360, 203))
        mk = cv2.resize(masks[r.image_name].astype(np.uint8), (360, 203), interpolation=cv2.INTER_NEAREST)
        red = img.copy()
        red[mk > 0] = (0, 0, 255)
        t = cv2.addWeighted(img, 0.55, red, 0.45, 0)
        cv2.drawContours(t, cv2.findContours(mk, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0], -1, (0, 255, 255), 1)
        label = f"{r.image_name[:-4]} {r.fg_pct:.0f}% {r.split}"
        cv2.putText(t, label, (4, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 3)
        cv2.putText(t, label, (4, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
        tiles.append(cv2.copyMakeBorder(t, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=(40, 40, 40)))
    for i in range(0, len(tiles), 16):
        page = tiles[i:i + 16] + [np.zeros_like(tiles[0])] * (16 - len(tiles[i:i + 16]))
        sheet = np.vstack([np.hstack(page[j:j + 4]) for j in range(0, 16, 4)])
        cv2.imwrite(str(OUT / "audit" / f"{m.loc[m.category == cat, 'status'].iloc[0]}_{cat}_{i // 16:02d}.jpg"), sheet, [cv2.IMWRITE_JPEG_QUALITY, 80])

# the zip: kept photos + masks, CSVs with removed rows dropped (other rows byte-identical), plus the audit trail
kept = set(m.loc[m["status"] == "kept", "image_name"])
def keep_rows(name):
    lines = (RAW / name).read_bytes().splitlines(keepends=True)
    return lines[0] + b"".join(l for l in lines[1:] if l.split(b",")[0].decode() in kept)
with zipfile.ZipFile(ZIP, "w") as z:  # ponytail: ZIP_STORED, jpg/png are already compressed
    for n in sorted(kept):
        z.write(RAW / "Raw_Images" / n, f"{ZIP_ROOT}/Raw_Images/{n}")
        z.write(RAW / "Segmentation_Masks" / f"{n[:-4]}_mask.png", f"{ZIP_ROOT}/Segmentation_Masks/{n[:-4]}_mask.png")
    for r in m[m["status"] == "removed"].itertuples():  # bad photos are set aside, not thrown away
        z.write(RAW / "Raw_Images" / r.image_name, f"{ZIP_ROOT}/removed/{r.category}/{r.image_name}")
        z.write(RAW / "Segmentation_Masks" / f"{r.image_name[:-4]}_mask.png", f"{ZIP_ROOT}/removed/{r.category}/{r.image_name[:-4]}_mask.png")
    z.writestr(f"{ZIP_ROOT}/{LABELS}", keep_rows(LABELS))
    z.writestr(f"{ZIP_ROOT}/{REG}", keep_rows(REG))
    for f in [OUT / "manifest.csv", OUT / "README.md", OUT / "build_clean.py",*sorted((OUT / "audit").glob("*.jpg"))]:
        z.write(f, f"{ZIP_ROOT}/cleaning/{f.relative_to(OUT).as_posix()}")

with zipfile.ZipFile(ZIP) as z:
    names = z.namelist()
assert sum("/Raw_Images/" in n for n in names) == sum("/Segmentation_Masks/" in n for n in names) == len(kept)
assert sum("/removed/" in n for n in names) == 2 * (m["status"] == "removed").sum()
print(pd.crosstab(m["category"].where(m["status"] == "removed", "kept"), m["split"], margins=True))
print(f"{ZIP}: {len(kept)} pairs, {ZIP.stat().st_size / 1e6:.0f} MB")
