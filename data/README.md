# data/

```
data/
├── raw/                  # the original dataset, exactly as downloaded
│   ├── Raw_Images/                 2002 .jpg (1280x720 UAV frames)
│   ├── Segmentation_Masks/         2002 .png (binary: plastic vs background)
│   ├── Image_labels_Binary Classification Task.csv
│   └── Mask_foreground_percentages_Regression Task.csv
├── splits/               # produced by pipelines/split.ipynb — regenerable
│   ├── train/{images,masks}        1496 pairs
│   ├── val/{images,masks}           253 pairs
│   └── test/{images,masks}          253 pairs
└── samples/              # a couple of photos for quick manual tests
```

Source: FloPWD 2025 (Dal Lake Floating Plastic Waste Detection).

`raw/` keeps the original folder names on purpose — they are evidence the images
were not altered. Never write into it.

`splits/` is generated, not hand-made. The frames come from video, so many images
are near-duplicates; a random split would put the same scene in both train and
test. `pipelines/split.ipynb` fingerprints every image with a 64-bit dHash, groups
images within Hamming distance 5, and splits whole groups with
`StratifiedGroupKFold` (seed 42). Rerunning it reproduces the same 1496/253/253
split; see `pipelines/README.md` for the full procedure.
