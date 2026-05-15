# Dashboard Walkthrough

This is the planned path for building the dashboard after the phone demo is stable.

## MVP Goal

Show the latest plastic-waste detection on a map with image evidence.

The dashboard should display:

- latest camera frame
- segmentation overlay
- plastic percentage
- latitude and longitude
- map marker
- timestamp
- model name

## Data Source

Read:

```text
droidcam-prototype/runs/latest_detection.json
```

The file updates each time the phone demo saves a detection.

## First Implementation Shape

Use a tiny local backend:

```text
FastAPI
  GET /api/detections/latest
  GET /api/detections
  GET /api/images/{run_id}/{kind}/{filename}
```

Use a frontend:

```text
React or Next.js
Leaflet map
Image preview panel
Detection list
```

## Map Behavior

Marker colors:

- low: `< 5%`
- medium: `5-20%`
- high: `> 20%`

If latitude or longitude is missing, show the detection in the list but do not place it on the map.

## Phase 1 Build Order

1. Create backend that reads latest JSON.
2. Serve saved images safely from the run folder.
3. Create frontend card for latest detection.
4. Add Leaflet map.
5. Add marker color by plastic percentage.
6. Add list of historical detections from JSONL or CSV.

## Later Phases

- Persistent database
- Route playback
- Heatmap
- GeoJSON export
- Flight/session grouping
- Real drone telemetry

