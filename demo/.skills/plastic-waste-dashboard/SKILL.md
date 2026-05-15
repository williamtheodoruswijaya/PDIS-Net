# Plastic Waste Dashboard Skill

## Use When

Use this skill when planning or implementing dashboard behavior for plastic-waste detections.

## Source Data

Primary input:

```text
droidcam-prototype/runs/latest_detection.json
```

Historical run inputs:

```text
droidcam-prototype/runs/YYYYMMDD_HHMMSS/detections.csv
droidcam-prototype/runs/YYYYMMDD_HHMMSS/detections.jsonl
```

## MVP Dashboard

The dashboard should show:

- map marker
- image
- overlay
- plastic percentage
- timestamp
- latitude and longitude
- model name

## Suggested Architecture

- FastAPI local backend for files and JSON
- React or Next.js frontend
- Leaflet for maps
- SQLite first, PostGIS later

## Workflow

1. Read `droidcam-prototype/dashboard_planner.md`.
2. Read `docs/dashboard/api-contract.md`.
3. Preserve the output contract.
4. Implement the smallest visible dashboard step.
5. Add sample data only if needed and document it.

