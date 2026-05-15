# Dashboard Design

## Purpose

The dashboard should make model results understandable in the context of location.

It should answer:

- Where was plastic detected?
- How much plastic did the model estimate?
- What did the original frame look like?
- What did the model mask look like?
- Which model produced the result?

## MVP Layout

Suggested sections:

```text
Top bar:
  project name, model, latest timestamp

Main area:
  map on the left
  latest detection panel on the right

Bottom:
  detection table or timeline
```

## Marker Design

Marker color by percentage:

| Plastic Percentage | Marker |
| --- | --- |
| `< 5%` | low |
| `5-20%` | medium |
| `> 20%` | high |

## Image Panel

Show:

- original image
- overlay image
- plastic percentage
- timestamp
- model
- threshold
- location

## Backend Boundary

The frontend should not read arbitrary local file paths directly in a deployed version. A backend should serve approved image files from the run directory.

## Future Layers

- heatmap
- route playback
- flight sessions
- GeoJSON export
- model comparison overlays

