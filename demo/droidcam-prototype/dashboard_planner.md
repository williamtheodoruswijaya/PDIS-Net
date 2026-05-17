# Dashboard Planner

## Goal

Build a dashboard that maps each plastic-waste detection from the phone/drone demo with the captured image, segmentation overlay, plastic percentage, latitude, and longitude.

## Demo Data Contract

The phone demo writes one latest JSON file for live dashboard polling:

```text
droidcam-prototype/runs/latest_detection.json
```

It also writes durable run logs:

```text
droidcam-prototype/runs/YYYYMMDD_HHMMSS/detections.csv
droidcam-prototype/runs/YYYYMMDD_HHMMSS/detections.jsonl
```

Required dashboard fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `timestamp` | string | ISO-like local timestamp for detection |
| `model` | string | `segformer` or `dinov3` |
| `plastic_percentage` | number | Predicted plastic pixels divided by total pixels |
| `latitude` | number/null | GPS latitude from manual input, telemetry file, or drone |
| `longitude` | number/null | GPS longitude from manual input, telemetry file, or drone |
| `image_path` | string | Saved original frame |
| `mask_path` | string | Saved binary plastic mask |
| `overlay_path` | string | Saved frame with mask overlay |
| `threshold` | number | Mask binarization threshold |
| `camera_source` | string | Camera index or stream URL |

## MVP Dashboard Flow

1. Read `runs/latest_detection.json` every 1-2 seconds.
2. Append new detections into local state when the timestamp changes.
3. Show a map with markers at latitude/longitude.
4. Color markers by plastic percentage:
   - low: `< 5%`
   - medium: `5-20%`
   - high: `> 20%`
5. Show a side panel with:
   - latest original image
   - overlay image
   - plastic percentage
   - model name
   - timestamp
   - latitude and longitude

## Suggested Stack

For the next implementation stage:

- Frontend: Next.js or Vite React
- Map: Leaflet with OpenStreetMap tiles
- Local live bridge: small FastAPI service that reads the JSON/CSV and serves image files
- Storage later: PostgreSQL/PostGIS or SQLite + SpatiaLite

## API Shape

Initial FastAPI endpoints:

```text
GET /api/detections/latest
GET /api/detections
GET /api/images/{run_id}/{kind}/{filename}
```

Example latest response:

```json
{
  "timestamp": "2026-05-15T22:45:30",
  "model": "segformer",
  "plastic_percentage": 12.34,
  "latitude": -6.2088,
  "longitude": 106.8456,
  "image_path": "runs/20260515_224500/images/frame_000005.jpg",
  "mask_path": "runs/20260515_224500/masks/mask_000005.png",
  "overlay_path": "runs/20260515_224500/overlays/overlay_000005.jpg",
  "threshold": 0.8,
  "camera_source": "0"
}
```

## Implementation Phases

### Phase 1: Local viewer

- Read the JSON output from the phone demo.
- Render latest detection and a marker map.
- Use local file serving for images.

### Phase 2: Persistent backend

- Insert every detection into a database.
- Store images under a stable media directory.
- Add filters by date, model, percentage range, and area.

### Phase 3: Drone telemetry

- Replace manual latitude/longitude with MAVLink GPS.
- Add altitude and heading.
- Store flight session ID and camera frame ID.

### Phase 4: Operational dashboard

- Add heatmap layer.
- Add route playback.
- Add export to CSV/GeoJSON.
- Add confidence/quality indicators.

## Open Decisions

- Whether the dashboard should run locally beside the model or on a remote server.
- Whether inference should run on the drone, laptop ground station, or cloud.
- Whether GPS should come from drone telemetry, phone GPS, or manual test coordinates during the prototype.

