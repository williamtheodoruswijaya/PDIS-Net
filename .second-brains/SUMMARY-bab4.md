# Bab 4 Hasil dan Pembahasan: Summary

> Source: `THESIS_v1.docx` (Word upload 16 Nov), Bab 4.1–4.10. Page numbers: ___–___ (filled from Word, not the PDF, so the pages are still to check)
> ⚠️ = in the Word but still needs fixing (see bottom)

---

## 4.1 Spesifikasi Sistem
* Local PC used for: code development, data analysis, re-calculating metrics, and building the web app
* Cloud GPU used for: training all models, hyperparameter search (Optuna), Seg-Eigen-CAM (XAI)

### 4.1.1 Spesifikasi Perangkat Keras
* Local: CPU Intel Core i5-11400H (6 core / 12 thread) · RAM 32,0 GB ⚠️ · GPU NVIDIA RTX 3050 Laptop 4 GB · OS Windows 11
* Cloud: Google Colab + Kaggle (GPU NVIDIA Tesla T4 16 GB)
* Why cloud: 4 GB VRAM is not enough to train at 512 × 512

### 4.1.2 Spesifikasi Perangkat Lunak
* Data: pandas, NumPy, OpenCV, scikit-learn, Albumentations
* Model / training: PyTorch, Segmentation Models PyTorch (SMP), Hugging Face Transformers
* HPO / XAI: Optuna / pytorch-grad-cam (Seg-Eigen-CAM)
* Backend: FastAPI + Uvicorn on Hugging Face Spaces, weights on Hugging Face Hub
* Frontend: NextJS on Vercel

---

## 4.2 Hasil Pra-Pemrosesan Data

### 4.2.1 Hasil Pemeriksaan dan Integrasi Data
* Total: 2.002 images and 2.002 segmentation masks (FloPWD 2025)
* Resolution: 1280 × 720
* Missing values: 0 · duplicate names: 0
* Label "yes": 1.482 (74,03%) · label "no": 520 (25,97%)
* Empty masks: 524 (26,17%)
* Mask binarization: threshold 127 (> 127 → 1 plastik, else 0)
* Mean plastic area: 5,46% · median: 2,44%

### 4.2.2 Hasil Standardisasi dan Encoding Data
* Renamed columns: image_name, presence, fg_pct
* Encoding: presence → has_plastic (yes = 1, no = 0), only used for stratification; the model trains on the mask

### 4.2.3 Hasil Transformasi dan Augmentasi Citra
* Resize: 512 × 512
* Normalize: mean (0,485; 0,456; 0,406) · std (0,229; 0,224; 0,225) (ImageNet)
* Train-only augmentations: HorizontalFlip, VerticalFlip, RandomRotate90 (p 0,5); ShiftScaleRotate (shift 0,1, scale 0,2, rotate 30°, p 0,5); ColorJitter (0,2/0,2/0,2/0,1, p 0,4)
* Why: applied on the fly, so no extra images are added; geometric ones go to image + mask, ColorJitter to the image only; ImageNet stats because every pretrained encoder started from ImageNet

### 4.2.4 Hasil Pembagian Data
* Method: train_test_split (2×) · seed 42 · stratified on has_plastic

| Split | Images | % | Empty mask | Mean plastic area |
|---|---|---|---|---|
| Train | 1.400 | 69,93% | 367 | 5,33% |
| Val | 301 | 15,03% | 78 | 6,12% |
| Test | 301 | 15,03% | 79 | 5,37% |

* pos_weight: 18,37 (from train, cap 50)

---

## 4.3 Hasil Perbandingan Model
* Total configs: 17 (U-Net / DeepLabV3+ / SegFormer × ResNet34/50/101, MiT-B0/B3/B5 × raw / ImageNet / aerial / ADE20K / drone)
* Shared setup: 40 epochs · patience 8 · threshold 0,5
* Metric computed: per image, then averaged over the 301 test images

### 4.3.1 Perbandingan Arsitektur dan Encoder

| Encoder | Arch | IoU plastic | mIoU | Precision | Recall |
|---|---|---|---|---|---|
| ResNet34 | U-Net | 0,5694 | 0,7677 | 0,7205 | 0,7602 |
| ResNet34 | DeepLabV3+ | 0,5999 | 0,7753 | 0,7182 | 0,8094 |
| ResNet34 | SegFormer | 0,5969 | 0,7801 | 0,7414 | 0,7760 |
| MiT-B3 | U-Net | 0,6128 | 0,7918 | 0,7852 | 0,7515 |
| MiT-B3 | DeepLabV3+ | 0,6495 | 0,8092 | 0,7786 | 0,8057 |
| MiT-B3 | SegFormer | **0,6746** | **0,8210** | 0,7847 | 0,8216 |

* Best: SegFormer MiT-B3 (ImageNet), mIoU 0,8210
* Key finding: MiT-B3 beats ResNet34 on every architecture (+0,0241 to +0,0409 mIoU), mostly through higher precision

### 4.3.2 Pengaruh Bobot Awal
* Random vs ImageNet gain: +0,1183 to +0,3485 mIoU
* Why random init fails: underfits, train loss stays 0,56–0,78 vs 0,19–0,33 with pretrained; a transformer has no built-in locality bias, so it needs pretraining the most
* Other pretrained weights: aerial 0,8140 and ADE20K 0,8077 = setara with ImageNet; drone 0,7809 (early-stopped at epoch 17)

### 4.3.3 Pengaruh Ukuran Encoder
* SegFormer MiT-B0 / B3 / B5: 0,7552 / 0,8210 / 0,8087
* DeepLabV3+ ResNet34 / 50 / 101: 0,7753 / 0,7533 / 0,7816
* Conclusion: a bigger encoder is not automatically better; size only hurts when the encoder is too small (B0)
* Winner for 4.4: SegFormer MiT-B3 ImageNet (test 0,8210, val 0,8164)

---

## 4.4 Optimasi Model Terbaik
* Model optimized: SegFormer MiT-B3, ImageNet
* Two parts: hyperparameter search with Optuna + Learning Rate Scheduler (Polynomial LR)

### 4.4.1 Hasil Pencarian Hyperparameter
* Tool / method: Optuna, TPE sampler + MedianPruner, 12 epochs per trial, scored on validation mIoU

| Hyperparameter | Range | Start | Best |
|---|---|---|---|
| LR encoder | 1e-6 – 1e-4 (log) | 1e-5 | 2,68e-5 |
| LR decoder | 3e-5 – 3e-3 (log) | 3e-4 | 3,38e-5 |
| Weight decay | 1e-5 – 5e-2 (log) | 1e-4 | 1,65e-3 |
| Dice loss weight | 0,3 – 0,9 | 0,70 | 0,76 |

* The thesis now tells **one search only**: 25 trials, best trial ke-15 (val 0,8136); first 10 trials random (val 0,7554–0,8068), from trial 12 on tighter (0,8045–0,8136)
* Retrained with these, 40 epochs + patience 8 → test mIoU 0,7810 (best epoch 8, stopped 16) (Tabel 4.13)
* (The old "Search 1: 12 trials → 0,8177" is no longer in the text, so don't bring it up)
* Why it dropped: early stopping fired at epoch 16 while the LR was still high, before the model settled ⚠️ the Word doesn't explain Tabel 4.13 yet

### 4.4.2 Pengaruh Jadwal Pelatihan (Learning Rate)
* Scheduler: Polynomial LR (power 1,0, down to ~0) · epochs 80 · early stopping: none

| Model | Hyperparameter | LR | Early stop | Best/stop | mIoU |
|---|---|---|---|---|---|
| Model awal | Awal | Tetap | Patience 8, max 40 | 36/40 | 0,8210 |
| Model dengan early stopping | Awal | Tetap | Patience 8, max 80 | 25/33 | 0,8005 |
| Model dengan LR Scheduler | Awal | Poly 80 | No | 78/80 | 0,8258 |
| Model akhir | Hasil pencarian | Poly 80 | No | 80/80 | **0,8320** |

* Scheduler gain: +0,0253 (0,8005 → 0,8258, same hyperparameters); val mIoU still climbing 0,7908 (ep 20) → 0,8223 (ep 80)
* Optuna gain on same schedule: +0,0062 (0,8258 → 0,8320, setara)
* Total optimization gain: 0,8210 → 0,8320 (+0,0110)
* Insight: the model can still train with a big LR at the start, but needs a small LR at the end so validation stays stable
* Why only this model: one search ≈ 9,5 h → 17 configs ≈ 160 h

---

## 4.5 Evaluasi Model

### 4.5.1 Hasil Evaluasi Metrik
* IoU plastic: 0,6926
* IoU background: 0,9715
* mIoU: 0,8320
* Dice: 0,7839
* Precision: 0,7816 · Recall: 0,8515
* mPA: 0,9138
* Why mIoU > IoU plastic: plastic is only 5,37% of the test pixels, so background (0,9715) lifts the average; also the 79 empty masks predicted empty count as IoU 1; small objects shrink after the 512 resize and lose a big share of IoU from a few edge pixels
* Why recall > precision: pos_weight 18,37 punishes missed plastic much more than false plastic → the model over-marks; fine for monitoring (missing trash is worse)

### 4.5.2 Analisis Kualitatif Hasil Prediksi
* Good cases: img1892 (trash pile on the lake edge, boat NOT marked), img29 (small objects on calm water)
* Error cases: img1220 (dry grass marked as plastic), img729 (transparent bag missed), img1697 (bush marked, no plastic in the image) → needs more training data with these conditions

---

## 4.6 Interpretasi Model Menggunakan Seg-Eigen-CAM
* Purpose: check whether the prediction comes from the plastic itself or from what's around it (red = high influence, blue = low)

### 4.6.1 Hasil Seg-Eigen-CAM pada Citra Uji
* img1892: hottest on the trash pile along the wall + floating trash → prediction driven by the trash itself
* img1220: hottest near the real plastic piece; the grass it wrongly marked is cooler → found the right plastic, then spread to the grass ⚠️ still has "31,76% … 9,00%"
* img1697: hottest on some leaves in the bush → model treats that leaf colour/texture as plastic → add plant-only training images
* img729: hot only on the bright bag it detected; the missed transparent bag is not explained
* Limitation: the heatmap only explains the area predicted as plastic, so it can't explain missed plastic

---

## 4.7 Pengujian Aplikasi ⚠️ (title swapped with 4.8)
* Frontend: NextJS on Vercel · Backend: FastAPI on Hugging Face Spaces (CPU) · Weights: Hugging Face Hub, loaded into memory once at startup
* Models served: 16 (best model + 15 others)

### 4.7.1 Halaman Dasbor
* One page following the 3.8.2 wireframe: left = model choice, Upload Image, Photo, Result; right = Category, How Much Plastic Coverage, Recommendation; hint messages before upload (Gambar 4.6)

### 4.7.2 Pemilihan Model
* 3 dropdowns (Model, Backbone, Pretrained weights), only combos actually trained, each with its test mIoU; default SegFormer MiT-B3 ImageNet (0,832); changing the model re-runs the uploaded image (Gambar 4.7)

### 4.7.3 Hasil Segmentasi
* JPG/PNG upload → backend resizes to 512 × 512 + ImageNet normalization (same as training) → back to original size → threshold 0,5 → shown as Mask or Overlay mode (Gambar 4.8, 4.9)

### 4.7.4 Kategori Cakupan dan Rekomendasi
* Thresholds: 1,1% and 4,5%
* Why those: tertiles of plastic coverage over the 1.474 FloPWD images with plastic (4,47 rounded to 4,5); most images have small coverage, so bigger cut-offs would put almost everything in Low

| Category | Coverage | Recommendation |
|---|---|---|
| None | 0% | "No plastic detected in this photo." |
| Low | < 1,1% | "A little plastic. Check this spot again on the next routine flight." |
| Moderate | 1,1% – < 4,5% | "Visible plastic patches. Add this spot to the next cleanup round." |
| High | ≥ 4,5% | "Among the most plastic-covered spots in FloPWD. Prioritise it for cleanup." |

* Note under Recommendation: category only compares to FloPWD, not water quality; also shows model name + inference time. Example img100.jpg = 8,12% → High (Gambar 4.10)

---

## 4.8 Hasil Aplikasi ⚠️ (title swapped with 4.7)
* Method: black box testing by the team, on the hosted app, with img100.jpg (plastic) and img999.jpg (no plastic); tests 8–10 sent straight to the backend API
* Result: 10 / 10 pass
* Inference time: 1,7–3,2 s on CPU for 1280 × 720 (3–5 s total, upload to result)

## 4.9 Evaluasi Aplikasi
* ⚠️ still `[PLACEHOLDER]` (plan: Eight Golden Rules questionnaire, 20 BINUS students, 6-point Likert)

## 4.10 Poster
* Poster with a QR code to the app (Gambar 4.11)

---

## TL;DR

| What | Number |
|---|---|
| Dataset | FloPWD 2025, 2.002 images (1.400 / 301 / 301) |
| Configs tested | 17 |
| Best baseline | SegFormer MiT-B3 ImageNet, mIoU 0,8210 |
| Final model | + Optuna + Poly LR 80 epochs → mIoU 0,8320 (IoU plastik 0,6926) |
| App | NextJS + FastAPI, 16 models, black box 10/10 pass |

---

## ⚠️ Still to fix in the Word
1. Tabel 4.1 RAM says 32,0 GB, but the notes say 16 GB. Check which laptop it is.
2. 4.4.2 opening sentence is broken, and Tabel 4.13 (0,7810) is never explained (one sentence about early stopping at epoch 16 is enough).
3. The "Tahap optimasi hanya dilakukan …" paragraph appears twice. Delete the long one.
4. 4.6.1 still has "31,76% … 9,00%" (breaks the no-numbers-from-Seg-Eigen-CAM rule).
5. 4.7 / 4.8 titles are swapped.
6. 4.9 is still a placeholder, and Bab 5 is not written yet.
