# Data Flow

## Current Runtime Flow

```text
Camera frame
  -> OpenCV read
  -> model preprocessing
  -> segmentation model
  -> plastic probability map
  -> thresholded binary mask
  -> plastic percentage
  -> overlay image
  -> saved detection record
```

## Current Output Flow

```text
frame_bgr
  -> images/frame_000001.jpg

mask
  -> masks/frame_000001_mask.png

overlay
  -> overlays/frame_000001_overlay.jpg

metadata
  -> detections.csv
  -> detections.jsonl
  -> runs/latest_detection.json
```

## Dashboard Flow

MVP:

```text
latest_detection.json -> dashboard polling -> image panel + map marker
```

Later:

```text
detections.jsonl/CSV -> backend import -> database -> API -> dashboard
```

## Telemetry Flow

Current:

```text
manual CLI args or telemetry JSON -> DetectionWriter
```

Future:

```text
drone telemetry -> telemetry adapter -> synchronized frame metadata -> DetectionWriter/database
```

## Data Contract Rule

The dashboard should not parse image filenames to infer metadata. It should read structured fields from the JSON/CSV records.

