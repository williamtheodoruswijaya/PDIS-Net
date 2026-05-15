# Map UX

## Main Map

The map should show detections at their latitude and longitude.

If coordinates are missing:

- show the detection in the side panel
- do not place a marker
- show a clear "no coordinates" state

## Marker Color

| Percentage | Meaning |
| --- | --- |
| `< 5%` | low plastic coverage |
| `5-20%` | medium plastic coverage |
| `> 20%` | high plastic coverage |

## Marker Popup

Popup should show:

- plastic percentage
- timestamp
- model
- thumbnail overlay

## Side Panel

The side panel should show:

- latest detection image
- latest overlay
- metadata table
- link to full saved image

## Filters

MVP filters:

- model
- percentage range
- date/time

Later filters:

- flight session
- altitude range
- operator
- confidence/quality score

