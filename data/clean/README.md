# data/clean/ - FloPWD, curriculum step 1 (bad annotations set aside)

`FloPWD-clean-stage1.zip` is the raw FloPWD dataset with **94 of 2002 photos (4.7%) moved out**
because their masks teach the model the wrong thing. Nothing is deleted: the removed photos
and masks sit in `removed/<category>/` inside the zip, and `data/raw/` is untouched.

| | train | val | test | total |
|---|---|---|---|---|
| original (seed-42 split of v2.ipynb) | 1400 | 301 | 301 | 2002 |
| removed - `coarse_zone` | 63 | 17 | 11 | 91 |
| removed - `missing_mask` | 2 | 1 | 0 | 3 |
| **kept** | **1335** | **283** | **290** | **1908** |

## Zip layout

```
Dal Lake Floating Plastic Waste Detection Dataset (FloPWD 2025)/   <- same name as the original zip
├── Raw_Images/            1908 .jpg  (kept)
├── Segmentation_Masks/    1908 .png  (kept)
├── Image_labels_Binary Classification Task.csv        removed rows dropped, other rows byte-identical
├── Mask_foreground_percentages_Regression Task.csv    removed rows dropped, other rows byte-identical
├── removed/
│   ├── coarse_zone/       91 photos + masks
│   └── missing_mask/       3 photos + masks
└── cleaning/
    ├── manifest.csv       all 2002 photos: split, status, category, fg_pct, biggest_blob_pct
    ├── README.md          this file
    ├── build_clean.py     the script that built the zip
    └── audit/*.jpg        overlay sheets of every flagged photo (removed and kept-with-note)
```

## What was removed and why

- **`coarse_zone`** (img1199-1219, img1418-1487): two continuous video runs where the annotator
  drew one big zone over a whole bank or field. Most pixels inside are grass, soil or water with
  small scattered litter (see img1484). Elsewhere in the dataset each item or pile gets its own
  outline, so these frames tell the model "grass = plastic". Both runs have a clear style break at
  each end: img1198/1220 and img1417/1488 go back to per-pile outlines.
- **`missing_mask`** (img96, img340, img772): plastic is clearly visible but the mask is empty,
  so the model is punished for finding it.

## Checked but kept (`category` filled, `status = kept`)

- **`rough_polygon`**: loose outlines that still follow a real litter pile or strip. This is the
  normal style for dense piles in this dataset, so removing these would be arbitrary. Candidates
  for a later curriculum stage.
- **`yes_label_empty_mask`** (img762, 947, 1633-1635): labelled "yes", but nothing clearly
  plastic is visible, so the empty mask is defensible.
- **`no_label_nonempty_mask`** (img447, 614, 1000, 1797): small correct mask; only the yes/no CSV
  is wrong. Training never uses that column except for split stratification.

## How photos were screened

Every photo matching one of these was looked at on an overlay sheet:
`fg_pct >= 20`, or `5 <= fg_pct < 20` with `biggest_blob_pct >= 5`, or the yes/no label disagrees
with the mask. That is 124 + 140 + 12 photos. Photos outside that net were not eye-checked.

Compared with the first pass (`.second-brain/bad-annotations.md`, 111 photos): img1440 and
img1443 were added (same run, just under 20%). img1285-1287, 1375-1379, 1492-1495, 1508-1510,
1545-1548, 1789-1790 and 1888-1889 were moved to `rough_polygon` because their unflagged
neighbours in the same run use the same style.

## Using it in a notebook

1. Upload the zip to Drive and put its id in `file_id`. Paths stay the same.
2. Take the split from `cleaning/manifest.csv` instead of calling `train_test_split` again.
   Re-splitting 1908 photos would reshuffle everything, and the test set would no longer be a
   subset of the old one.
3. The test set is now 290 of the old 301. To compare with older runs, re-score their `best.pth`
   on the same 290 photos.

## Rebuild

```
python data/clean/build_clean.py      # from the repo root; needs data/raw, pandas, opencv, scikit-learn
```
