---
title: PDIS-Net Inference API
emoji: 🌊
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# PDIS-Net Inference API

SegFormer (MiT-B3) fine-tuned on FloPWD 2025. Binary segmentation: floating plastic vs background.
Test mIoU **0.811**.

Weights pulled at startup from [adamantix/pdisnet-weights](https://huggingface.co/adamantix/pdisnet-weights).

## Endpoints

- `GET /health` — device + whether model finished loading
- `POST /predict` — multipart upload, field `file`. Returns raw probability map as base64 PNG.
