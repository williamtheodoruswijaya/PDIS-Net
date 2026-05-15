# Dashboard API Contract

This document defines the first backend contract for a dashboard that reads phone-demo outputs.

## Latest Detection

```text
GET /api/detections/latest
```

Response:

```json
{
  "run_id": "20260515_224500",
  "frame_index": 5,
  "timestamp": "2026-05-15T22:45:30",
  "model": "segformer",
  "plastic_percentage": 12.34,
  "latitude": -6.2088,
  "longitude": 106.8456,
  "altitude_m": 25.0,
  "telemetry_source": "manual",
  "threshold": 0.8,
  "inference_ms": 1520.21,
  "camera_source": "0",
  "image_path": "runs/20260515_224500/images/frame_000005.jpg",
  "mask_path": "runs/20260515_224500/masks/frame_000005_mask.png",
  "overlay_path": "runs/20260515_224500/overlays/frame_000005_overlay.jpg"
}
```

## Detection List

```text
GET /api/detections
```

Query options:

```text
?limit=100
?model=segformer
?min_percentage=5
?max_percentage=20
?from=2026-05-15T00:00:00
?to=2026-05-15T23:59:59
```

## Image Serving

```text
GET /api/images/{run_id}/{kind}/{filename}
```

Where `kind` is:

- `images`
- `masks`
- `overlays`

The backend must restrict access to known run folders and prevent arbitrary file reads.

## Error Cases

No latest detection:

```json
{
  "error": "latest_detection_not_found"
}
```

Image missing:

```json
{
  "error": "image_not_found"
}
```

Invalid coordinate:

```json
{
  "error": "invalid_coordinate"
}
```

