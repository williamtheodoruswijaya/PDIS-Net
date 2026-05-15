# Dashboard

The dashboard will turn detection records into a map-based operational view.

## MVP Goal

Show the latest detection from the phone demo with:

- original image
- segmentation overlay
- plastic percentage
- latitude
- longitude
- map marker
- timestamp

## Source Of Truth

```text
droidcam-prototype/runs/latest_detection.json
```

## Documents

- [API Contract](api-contract.md)
- [Database Schema](database-schema.md)
- [Map UX](map-ux.md)
- [Dashboard Build Plan](build-plan.md)

## First Dashboard Rule

Build around the existing demo output contract. Do not invent a separate shape unless the phone demo and docs are updated together.

