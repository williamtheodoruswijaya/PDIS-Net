# Run The Phone Demo

This tutorial explains the main command and options.

## Basic Command

```powershell
cd "D:\BINUS\Semester 6\semantix\demo\droidcam-prototype"
py run_phone_demo.py --model segformer --source 0
```

## Important Arguments

```text
--model                  segformer or dinov3
--source                 camera index or stream URL
--device                 auto, cpu, or cuda
--threshold              override mask threshold
--lat                    manual latitude
--lon                    manual longitude
--telemetry-file         JSON file with latitude/longitude
--save-every-seconds    auto-save interval
--no-window              headless mode
```

## Recommended First Run

```powershell
py run_phone_demo.py --model segformer --source 0 --lat -6.2088 --lon 106.8456
```

## Use CUDA If Available

```powershell
py run_phone_demo.py --model segformer --source 0 --device cuda
```

If CUDA is not available, use:

```powershell
py run_phone_demo.py --model segformer --source 0 --device cpu
```

## Change Save Interval

Save every 10 seconds:

```powershell
py run_phone_demo.py --model segformer --source 0 --save-every-seconds 10
```

Disable auto-save and only save with `s`:

```powershell
py run_phone_demo.py --model segformer --source 0 --save-every-seconds 0
```

## Headless Run

Useful for remote or embedded testing:

```powershell
py run_phone_demo.py --model segformer --source 0 --no-window
```

## What Success Looks Like

- A preview window appears.
- Text overlay shows model, plastic percentage, threshold, and location.
- Red overlay appears where the model predicts plastic.
- Pressing `s` saves image, mask, overlay, and JSON/CSV records.

