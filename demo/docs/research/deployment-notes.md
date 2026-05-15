# Deployment Notes

## Prototype Deployment

Current deployment target:

```text
Windows laptop + DroidCam phone camera
```

This is a ground-station prototype, not an onboard drone deployment.

## Drone Deployment Questions

Before deploying on a drone, answer:

- What compute hardware is available?
- What camera stream format is available?
- What latency is acceptable?
- How will GPS be synchronized to frames?
- Is the model running onboard or on the ground station?

## SegFormer Practicality

SegFormer is the first realistic prototype model because it runs in the current local environment.

## DINOv3 Practicality

DINOv3/EoMT is more likely to require:

- stronger GPU
- ground-station inference
- server inference
- package upgrade

## Field Risks

- Water reflections
- Shadows
- Floating non-plastic objects
- Low altitude motion blur
- Network stream delay
- GPS drift

