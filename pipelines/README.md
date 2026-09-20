# Data Validation & Split Pipeline

Deduplicates near-identical frames and produces a leak-free train/val/test split for the
**FloPWD (Dal Lake Floating Plastic Waste Detection)** dataset.

## Quick facts

|                     |                                                                   |
| ------------------- | ----------------------------------------------------------------- |
| Input images        | 2002 (`Raw_Images/`, 1280×720, no EXIF → video frames)            |
| Fingerprint         | dHash, 64-bit                                                     |
| Duplicate threshold | Hamming distance ≤ 5                                              |
| Split method        | `StratifiedGroupKFold` (sklearn), 2 rounds + group-balancing pass |
| Final split         | **train 1496 · val 253 · test 253** (74.7% / 12.6% / 12.6%)       |
| Seed                | 42                                                                |

---

## 1. Pipeline overview

```mermaid
flowchart TD
    A["Raw Images<br/>2002 photos"] --> B["dHash<br/>64-bit fingerprint / image"]
    B --> C["Hamming Distance Matrix<br/>2002 × 2002"]
    C --> D["Union-Find Grouping<br/>threshold ≤ 5"]
    D --> E["StratifiedGroupKFold #1<br/>n_splits=7 → Test fold"]
    E --> F["StratifiedGroupKFold #2<br/>n_splits=6 on remainder → Train / Val"]
    F --> G["Balance Val/Test<br/>move whole groups until equal size"]
    G --> H["Export<br/>train/ val/ test folders (images + masks)"]
```

---

## 2. Why group-aware, not random

```mermaid
flowchart LR
    subgraph R["Random split — LEAKS"]
        direction TB
        r1["frame_100 → TRAIN"]
        r2["frame_101 → TEST"]
        r3["frame_102 → TRAIN"]
        r1 -.->|"near-duplicate"| r2
    end
    subgraph Gp["Group-aware split — CLEAN"]
        direction TB
        g1["frame_100 → TRAIN"]
        g2["frame_101 → TRAIN"]
        g3["frame_102 → TRAIN"]
        g1 --- g2 --- g3
    end
```

Frames 100/101/102 are the same lake, same trash, a fraction of a second apart. Random split
can tear the chain apart; group-aware split locks the whole chain to one side.

---

## 3. Step: dHash fingerprint (64-bit)

```mermaid
flowchart LR
    A["Grayscale<br/>cv2.IMREAD_GRAYSCALE"] --> B["Resize to 9×8<br/>cv2.resize INTER_AREA"]
    B --> C["right > left<br/>9 cols → 8 comparisons/row"]
    C --> D["Flatten<br/>8 rows × 8 bits = 64-bit array"]
```

Real output for `img1.jpg` (first image, `hashes[0]`), 1 = brighter than left neighbor:

```
0 0 0 1 0 0 1 0
0 0 0 0 0 1 1 0
0 0 0 0 0 1 1 1
0 0 1 0 0 1 1 1
0 0 0 0 0 1 0 1
0 0 0 1 0 1 0 1
0 0 0 0 0 1 1 1
0 0 0 0 1 1 0 1
```

---

## 4. Step: Hamming distance matrix

```mermaid
flowchart LR
    A["hashes<br/>(2002, 64) bool"] --> B["hashes[i] != hashes<br/>row-wise XOR vs all"]
    B --> C["dist[i] = differ.sum(axis=1)"]
    C --> D["dist<br/>(2002, 2002) int16<br/>diagonal = 99"]
```

---

## 5. Step: Union-Find grouping

Real chain found in the data — three pairs, one duplicate group:

```mermaid
flowchart LR
    n136((img #136)) -->|"dist ≤ 5"| n811((img #811))
    n136 -->|"dist ≤ 5"| n812((img #812))
    n136 -->|"dist ≤ 5"| n813((img #813))
```

```mermaid
pie title 2002 images → 1714 groups after Union-Find
    "Group representatives" : 1714
    "Duplicate frames merged into a group" : 288
```

---

## 6. Step: two-round `StratifiedGroupKFold`

```mermaid
flowchart TD
    subgraph R1["Round 1 — n_splits=7"]
        A["2002 images"] --> B["6/7 remainder"]
        A --> C["1/7 → TEST fold"]
    end
    subgraph R2["Round 2 — n_splits=6, applied to remainder only"]
        B --> D["5/6 → TRAIN"]
        B --> E["1/6 → VAL"]
    end
```

---

## 7. Step: balance val/test

Fold sizes aren't equal by default — whole groups get handed back to train until val and test match.

```
Before balancing:  train 1475  val 253  test 274   (test is bigger, gap = 21)
Groups moved:       5 whole groups, 21 images, test → train
After balancing:   train 1496  val 253  test 253   (gap closed to 0)
```

```mermaid
flowchart LR
    T["TEST fold<br/>274 images"] -->|"move 5 groups<br/>(21 images)"| Tr["TRAIN<br/>1475 → 1496"]
    T --> Tf["TEST<br/>274 → 253"]
```

---

## 8. Final result

```mermaid
pie title Final split (2002 images)
    "Train — 1496" : 1496
    "Validation — 253" : 253
    "Test — 253" : 253
```

| Split | Images | %     | Groups | has_plastic |
| ----- | ------ | ----- | ------ | ----------- |
| Train | 1496   | 74.7% | 1271   | 73.8%       |
| Val   | 253    | 12.6% | 200    | 74.7%       |
| Test  | 253    | 12.6% | 243    | 74.7%       |

```
Train  74.7% ███████████████████████████████████░░░░░░░░░░░░░
Val    12.6% ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
Test   12.6% ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
```

No group appears in more than one split — that's what makes the split leak-free.

---

## 9. Evidence this matters (literature)

Accuracy inflation caused by random (non-grouped) splitting, Yagis et al. (2021):

```
OASIS      +30%  ██████
ADNI       +29%  ██████
PPMI       +48%  ██████████
Versilia   +55%  ███████████
```

Random-label control experiment (label is unlearnable noise — correct score is 50%):

```
Slice-level split (leaked)     96%  ███████████████████
Subject-level split (grouped)  50%  ██████████
```

---

## References (APA 7)

Adimoolam, M., Poullis, C., & Averkiou, M. (2023). _Data leakage detection and de-duplication in
large scale geospatial image datasets_. arXiv. https://arxiv.org/abs/2304.02296

Barz, B., & Denzler, J. (2020). Do we train on test data? Purging CIFAR of near-duplicates.
_Journal of Imaging_, _6_(6), 41. https://doi.org/10.3390/jimaging6060041

Karasiak, N., Dejoux, J.-F., Monteil, C., & Sheeren, D. (2021). Spatial dependence between
training and test sets: Another pitfall of classification accuracy assessment in remote sensing.
_Machine Learning_, _111_(7), 2715–2740. https://doi.org/10.1007/s10994-021-05972-1

Kapoor, S., & Narayanan, A. (2023). Leakage and the reproducibility crisis in machine-learning-based
science. _Patterns_, _4_(9), Article 100804. https://doi.org/10.1016/j.patter.2023.100804

Tampu, I. E., Eklund, A., & Haj-Hosseini, N. (2022). Inflation of test accuracy due to data
leakage in deep learning-based classification of OCT images. _Scientific Data_, _9_, Article 580.
https://doi.org/10.1038/s41597-022-01618-6

Yagis, E., Atnafu, S. W., García Seco de Herrera, A., Marzi, C., Scheda, R., Giannelli, M., Tessa,
C., Citi, L., & Diciotti, S. (2021). Effect of data leakage in brain MRI classification using 2D
convolutional neural networks. _Scientific Reports_, _11_, Article 22544.
https://doi.org/10.1038/s41598-021-01681-w

Glazner, C. et al. (2025). _Find the leak, fix the split: Cluster-based method to prevent leakage
in video-derived datasets_. arXiv. https://arxiv.org/abs/2511.13944 — supplementary; abstract-only reference.
