# Database Schema

The first dashboard can read JSON files directly. A database becomes useful once detections need filtering, persistence, and map queries.

## SQLite MVP

Table: `detections`

| Column | Type | Notes |
| --- | --- | --- |
| `id` | integer primary key | local ID |
| `run_id` | text | run folder name |
| `frame_index` | integer | frame counter |
| `timestamp` | text | ISO timestamp |
| `model` | text | `segformer` or `dinov3` |
| `plastic_percentage` | real | 0-100 |
| `latitude` | real nullable | GPS latitude |
| `longitude` | real nullable | GPS longitude |
| `altitude_m` | real nullable | altitude |
| `telemetry_source` | text | manual/file/drone |
| `threshold` | real | model threshold |
| `inference_ms` | real | runtime |
| `camera_source` | text | camera index or stream |
| `image_path` | text | original frame |
| `mask_path` | text | binary mask |
| `overlay_path` | text | overlay |

## Future PostGIS

Add:

```text
geom GEOGRAPHY(Point, 4326)
flight_id
drone_id
heading_deg
camera_pitch_deg
```

## Indexes

Useful indexes:

```text
timestamp
model
plastic_percentage
latitude, longitude
flight_id
```

## Import Strategy

Initial:

```text
detections.jsonl -> database import script
```

Later:

```text
phone/drone service -> API insert -> database
```

