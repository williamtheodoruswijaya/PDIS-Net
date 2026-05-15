# Dashboard Preflight Checklist

Use this before building or testing the dashboard.

## Data Contract

Confirm the phone demo has produced:

```text
droidcam-prototype/runs/latest_detection.json
```

Required fields:

- `timestamp`
- `model`
- `plastic_percentage`
- `latitude`
- `longitude`
- `image_path`
- `mask_path`
- `overlay_path`
- `threshold`
- `camera_source`

## MVP Behavior

The first dashboard should:

- Poll latest detection data.
- Show the latest image and overlay.
- Show plastic percentage.
- Place a map marker when latitude and longitude exist.
- Keep a local list of detections seen during the session.

## Do Not Start With

- User accounts
- Cloud deployment
- Complex GIS analysis
- Real-time WebSocket infrastructure

Those are later phases after the local contract is stable.

