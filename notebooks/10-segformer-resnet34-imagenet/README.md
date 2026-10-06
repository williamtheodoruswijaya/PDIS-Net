# SegFormer decoder + ResNet34 encoder, ImageNet init

| | |
|---|---|
| **Model** | `smp.Segformer("resnet34", decoder_segmentation_channels=768)` |
| **Encoder** | ResNet34, smp `imagenet` weights. Byte-identical to the starting encoder of run 09 |
| **Decoder** | SegFormer All-MLP head, width 768 (= HF SegFormer-B3 `decoder_hidden_size`) |
| **Params** | 25.0M (vs 47.2M SegFormer-B3, 24.4M UNet-ResNet34) |

Set in `CFG` as `arch="segformer-smp"`, `backbone="resnet34"`, `init="imagenet"`.

**Why this one:** it completes a 2x2 that separates encoder from decoder. Every other
row changes both at once.

| | UNet decoder | SegFormer decoder |
|---|---|---|
| **MiT-B3 encoder** (transformer) | 03: 0.792 | 02: 0.821 |
| **ResNet34 encoder** (CNN) | 09: 0.768 | **10: ?** |

- 10 vs 09: same encoder and weights, only the decoder changes.
- 10 vs 02: same decoder, only the encoder changes (CNN vs transformer).
- So it answers whether SegFormer wins because of its transformer encoder or
  its lightweight MLP decoder. The B5 run (07) already showed that making
  the encoder bigger doesn't help.

**Caveats:**
- Run 03 came from an older notebook (same split and CFG values, different code),
  so the MiT-B3 row is slightly less controlled than the ResNet34 row.
- smp's MLP decoder also reads ResNet's 1/2-resolution stem features (5 inputs);
  MiT has only 4. That's 0.6M extra decoder params, so the head isn't byte-identical
  to run 02's.
- Weight decay and learning rates are the ones tuned for MiT; CNN encoders are
  usually fine with them, but they weren't tuned for this run.
