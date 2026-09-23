# ADE20K init — `nvidia/segformer-b3-finetuned-ade-512-512`

| | |
|---|---|
| **HF source** | https://huggingface.co/nvidia/segformer-b3-finetuned-ade-512-512 |
| **Trained on** | [ADE20K](https://groups.csail.mit.edu/vision/datasets/ADE20K/) — 150-class scene parsing, 20k images |
| **Task** | semantic segmentation, 150 classes @ 512x512 |
| **Backbone** | MiT-B3 (same as raw / imagenet / aerial runs) |
| **By** | NVIDIA · [SegFormer paper](https://arxiv.org/abs/2105.15203) · 159k downloads |
| **License** | NVIDIA SegFormer research license |

Loaded in `build_model()` as `init="ade"`.

**Why this one — it is the only init so far that pretrains the decoder.**
`nvidia/mit-b3` declares `"architectures": ["SegformerForImageClassification"]`,
i.e. encoder only, so your `imagenet` run starts with a **randomly initialised
decode head**. This checkpoint is a real `SegformerForSemanticSegmentation`, so
`linear_c.*` and `linear_fuse` transfer; only the final 150-wide classifier is
dropped by `ignore_mismatched_sizes`.

Also trained natively at **512x512** — exactly our `img_size`, unlike restor's
1024 px / 10 cm/px.

## Kaggle

Turn on **Internet** (gdown + HF download) and **GPU** in the notebook settings.

Changes vs the Colab notebooks:

| | Colab | here |
|---|---|---|
| dataset | `/content/` | `/kaggle/temp/` |
| results | Drive mount | `/kaggle/working/runs/<run_id>/<version>/` |
| `torchgeo` | installed | dropped — only the smp `aerial` branch imports it, and it can downgrade torch on Kaggle |

Grab `best.pth` + csv + json from the **Output** tab when the run finishes.
