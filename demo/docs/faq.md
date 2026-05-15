# FAQ

## Why Use DroidCam?

DroidCam lets a phone camera act as the drone camera during early prototyping. It is cheaper and easier than testing with a real drone immediately.

## Which Model Should I Use First?

Use SegFormer:

```powershell
py run_phone_demo.py --model segformer --source 0
```

## Why Not DINOv3 First?

DINOv3/EoMT is heavier and needs a newer Transformers architecture class. It is useful, but SegFormer is the practical default for the local demo.

## What Does Plastic Percentage Mean?

It is the percentage of image pixels classified as plastic:

```text
plastic pixels / total pixels * 100
```

It is not yet real-world area.

## Where Are Outputs?

```text
droidcam-prototype/runs/
```

Latest dashboard record:

```text
droidcam-prototype/runs/latest_detection.json
```

## Can This Run On A Drone?

Eventually. The current prototype runs on a laptop/ground station. Drone integration needs camera stream and telemetry integration.

