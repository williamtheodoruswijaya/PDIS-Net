# ImageNet init, MiT-B5: `nvidia/mit-b5`

| | |
|---|---|
| **HF source** | https://huggingface.co/nvidia/mit-b5 |
| **Trained on** | ImageNet-1k (same data as the `imagenet` run) |
| **Backbone** | MiT-B5: depths `[3,6,40,3]` vs B3 `[3,4,18,3]`; same widths `[64,128,320,512]` and decoder size (768) |
| **Params** | ~85M vs ~47M for B3 |

Loaded in `build_model()` as `init="imagenet-b5"`.

**Why this one:** a one-variable ablation against `02-segformer-mitb3-imagenet`.
Same pretraining data, same decoder, same recipe. Only the encoder depth changes, so any
gap is down to capacity.

**Why a new init name:** `run_id = f"{arch}-{init}"` sets the Drive save path. Reusing
`"imagenet"` would overwrite run 02's `best.pth`.

**Caveat:** batch 4 at 512 with AMP is untested for B5. If Colab runs out of memory, use
batch 2 and record it as a deviation.

Identical to `06-segformer-mitb3-drone/v1.ipynb` except `CFG["init"]` and the
extra `"imagenet-b5"` entry in the `src` dict. Outputs cleared.
