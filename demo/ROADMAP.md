# Roadmap

## Phase 1: Phone Demo Stabilization

Status: in progress.

Goals:

- Keep DroidCam/webcam inference running.
- Save dashboard-ready records.
- Make setup repeatable.
- Document every step.

Success criteria:

- A new user can run SegFormer with DroidCam from the docs.
- `latest_detection.json` updates during a run.
- Captured image, mask, overlay, and percentage are saved.

## Phase 2: Dashboard MVP

Goals:

- Read phone demo outputs.
- Show latest detection.
- Show map markers from latitude and longitude.
- Show image and overlay preview.
- Keep the API contract stable.

Success criteria:

- A dashboard can poll latest detection data.
- Historical records can be shown from CSV/JSONL.
- Marker color reflects plastic percentage.

## Phase 3: Telemetry Integration

Goals:

- Replace manual coordinates with live telemetry.
- Add altitude and heading.
- Store flight/session identifiers.
- Prepare MAVLink or drone SDK integration.

Success criteria:

- Each frame can be associated with a real GPS point.
- A route can be reconstructed from saved detections.

## Phase 4: Drone Field Trial

Goals:

- Use drone camera stream or recorded drone footage.
- Validate latency and accuracy in outdoor conditions.
- Decide whether inference runs on drone, laptop, or server.

Success criteria:

- Stable field capture workflow.
- Clear performance numbers.
- Dashboard map can explain where detections occurred.

## Phase 5: Deployment Hardening

Goals:

- Package the prototype.
- Add reliable logging.
- Add model versioning.
- Add storage retention rules.
- Add dashboard authentication if hosted.

