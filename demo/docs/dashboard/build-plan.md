# Dashboard Build Plan

## Phase 0: Contract Verification

- Run the phone demo.
- Save at least one detection.
- Inspect `runs/latest_detection.json`.

## Phase 1: Local API

Create a small API service that:

- reads latest detection JSON
- reads run CSV/JSONL
- serves image files from known folders

## Phase 2: Frontend MVP

Create a frontend that:

- polls latest detection
- displays image and overlay
- displays percentage and metadata
- renders a map marker

## Phase 3: History

Add:

- detection list
- marker list
- click marker to inspect detection
- load historical run data

## Phase 4: Persistence

Add:

- SQLite import
- database-backed API
- filter queries

## Phase 5: Drone Mode

Add:

- flight sessions
- route playback
- heatmap
- GeoJSON export

