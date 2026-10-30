---
title: PDIS-Net API
emoji: 🌊
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 6.22.0
python_version: "3.12"
app_file: main.py
pinned: false
license: mit
---

# PDIS-Net API

Floating plastic segmentation on aerial photos (FloPWD 2025). 16 trained models: pick arch, backbone and pretrained weights.
Best: SegFormer MiT-B3 (ImageNet), test mIoU **0.832**.

Weights: [adamantix/pdisnet-weights](https://huggingface.co/adamantix/pdisnet-weights).

## Endpoints

- `GET /health` — status, device, how many models are available
- `GET /models` — every trained combo with its test mIoU and threshold
- `POST /predict` — multipart: `file`, `arch`, `backbone`, `init` → mask (base64 PNG), coverage %, category, recommendation
- `/ui` — small Gradio test page

## Layout

- `main.py` — entry point, starts the API on port 7860
- `api/` — API host: one file per endpoint, no model logic
- `core/` — everything about models: domain (constants, options), entities (trained model list),
  infrastructure (where weights come from), application (load models, segment a photo, coverage category)
