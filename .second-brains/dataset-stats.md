# FloPWD dataset stats (as used in thesis Bab 4.2.1 / Tabel 4.4 / Tabel 4.7)

Recompute: `python .second-brains/scripts/plastic_coverage_stats.py` (from repo root, needs numpy + Pillow).

## Basic counts
- 2.002 .jpg + 2.002 .png masks, all 1280×720. 0 missing values, 0 duplicate names.
- Label CSV: 1.482 "yes" (74,03%), 520 "no" (25,97%).
- Empty masks (0 plastic pixels after binarizing): 524 (26,17%). Non-empty: 1.478.
- Label vs mask disagree on 8 + 4 photos (yes-but-empty, no-but-nonempty), hence 1.482 vs 1.478.

## Plastic coverage ("luas plastik")
Method: read each mask as grayscale, binarize `> 127` → 1 = plastic, then
`coverage_i = plastic_pixels_i / (1280 × 720) × 100`.

| Stat | Value | Thesis |
|---|---|---|
| Mean over all 2.002 images | 5,4560% | **5,46%** |
| Median over all 2.002 images | 1,0624% | – |
| Mean over the 1.478 non-empty masks | 7,3904% | – |
| Median over the 1.478 non-empty masks | 2,4406% | **2,44%** |
| Median over the 1.482 "yes"-label images | 2,4207% | (not used) |
| 90th percentile / max | 13,15% / 81,91% | – |
| Images with < 5% plastic | 1.536 of 2.002 | – |

- All images are the same size, so the per-image mean (5,46%) is also the dataset-wide share of plastic
  pixels → background 94,54%, about 17,3 background pixels per plastic pixel.
- `pos_weight` 18,37 in the notebooks comes from 200 random **train** photos (seed 42), not from this full count;
  it is close to 17,3, as expected.
- The dataset's own `Mask_foreground_percentages_Regression Task.csv` gives mean 5,38% (values are rounded to
  2 decimals and may use another threshold). The thesis numbers come from the masks, not the CSV.
- Per split (Tabel 4.7): train 5,33%, val 6,12%, test 5,37%.

## RGB stats of FloPWD (computed on all 2.002 photos, downsized to 320×180)
- mean (0,456; 0,467; 0,413), std (0,174; 0,173; 0,177).
- ImageNet: mean (0,485; 0,456; 0,406), std (0,229; 0,224; 0,225). Means are close, FloPWD std is smaller.
