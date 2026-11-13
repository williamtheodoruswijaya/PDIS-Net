# Training pipeline (template `notebooks/v2.ipynb`, same in every run 01-17)

- Split: `train_test_split` seed 42 stratified on `has_plastic`: 15% test, then 15/85 of the rest as val →
  1.400 / 301 / 301. Later runs read the split from `data/clean/manifest.csv` so nothing moves.
- Transforms (Albumentations): Resize 512 → HFlip 0,5 → VFlip 0,5 → RandomRotate90 0,5 →
  ShiftScaleRotate(0,1; 0,2; 30°; p 0,5) → ColorJitter(0,2; 0,2; 0,2; 0,1; p 0,4) → Normalize → ToTensorV2.
  Val/test: Resize → Normalize → ToTensorV2.
- **Normalize = ImageNet mean (0.485, 0.456, 0.406) / std (0.229, 0.224, 0.225) for every run**, including the
  from-scratch ones. A.Normalize also divides by 255 first. The server uses the same constants
  (`deployment/server/core/domain/constants.py`).
- Loss: 0,7 × Dice + 0,3 × weighted CrossEntropy, class weight [1, min(pos_weight, 50)], pos_weight ≈ 18,37.
- AdamW, lr encoder 1e-5 (pretrained) / decoder 3e-4, wd 1e-4, batch 4, 40 epochs, early stop patience 8 on val mIoU,
  AMP fp16. Raw (no pretrained) runs use 3e-4 for the encoder too.
- Metric: per-image IoU at threshold 0,5 averaged over test photos; mIoU = mean of plastic IoU and background IoU;
  mPA = (recall + background accuracy) / 2.

## Pretrained weight sources (`build_model` in the notebooks)
| init | SegFormer checkpoint | Note |
|---|---|---|
| raw | `SegformerConfig.from_pretrained("nvidia/mit-b3")`, random weights | – |
| imagenet | `nvidia/mit-b3` (MiT encoder pretrained on ImageNet-1K); smp `encoder_weights="imagenet"` for U-Net/DeepLabV3+ | – |
| aerial | `restor/tcd-segformer-mit-b3` | OAM-TCD tree canopy, fine-tuned MiT-B3 |
| ade | `nvidia/segformer-b3-finetuned-ade-512-512` | ADE20K 150 classes, fine-tuned MiT-B3 |
| drone | `pablojrios/segformer-b3-finetuned-drones` | Semantic Drone Dataset; code comment says "from nvidia/mit-b3" |

All non-raw SegFormer checkpoints share the MiT-B3 encoder that started from ImageNet-1K weights, which is why one
ImageNet mean/std fits all of them. (Not re-checked live against the HF model cards: huggingface.co was blocked in
the 13 Nov 2026 session.)
