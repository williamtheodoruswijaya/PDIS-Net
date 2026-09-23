# ADE20K init — `nvidia/segformer-b3-finetuned-ade-512-512`

| | |
|---|---|
| **HF source** | https://huggingface.co/nvidia/segformer-b3-finetuned-ade-512-512 |
| **Trained on** | [ADE20K](https://groups.csail.mit.edu/vision/datasets/ADE20K/) — 150-class scene parsing, ~20k images |
| **Task** | semantic segmentation, 150 classes @ 512x512 |
| **Backbone** | MiT-B3 (same as raw / imagenet / aerial runs) |
| **By** | NVIDIA · [SegFormer paper](https://arxiv.org/abs/2105.15203) · 159k downloads |
| **License** | NVIDIA SegFormer research license |

Loaded in `build_model()` as `init="ade"`.

**Why this one — it is the only init so far that pretrains the decoder.**
`nvidia/mit-b3` declares `"architectures": ["SegformerForImageClassification"]`,
i.e. encoder only, so the `imagenet` run starts with a **randomly initialised
decode head**. This checkpoint is a real `SegformerForSemanticSegmentation`, so
`linear_c.*` and `linear_fuse` transfer; only the final 150-wide classifier is
dropped by `ignore_mismatched_sizes`.

It also asks a cleaner question than the other rows: ADE20K is *segmentation*
pretraining, ImageNet is *classification* pretraining. Same MiT-B3 backbone in
both, so any gap is attributable to the pretraining task, not model size.

Also trained natively at **512x512** — exactly our `img_size`, unlike restor's
1024 px / 10 cm/px.

## Environment

Colab, same as the other notebooks: `gdown` to `/content/`, Drive mounted for
output at `/content/drive/MyDrive/THESIS/runs/<run_id>/<version>/`.

Identical to `04-segformer-mitb3-aerial/v1.ipynb` except `CFG["init"]` and the
extra `"ade"` entry in the `src` dict.
