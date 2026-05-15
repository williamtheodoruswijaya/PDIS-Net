# Architecture

This section explains how the prototype is structured and how it should evolve into a drone/dashboard system.

## Documents

- [Repository Map](repository-map.md)
- [Data Flow](data-flow.md)
- [Model Inference](model-inference.md)
- [Dashboard Design](dashboard-design.md)
- [Drone Integration](drone-integration.md)

## Current Architecture In One Line

```text
DroidCam/webcam -> OpenCV -> SegFormer/DINOv3 adapter -> mask + percentage -> saved image/JSON -> future dashboard
```

