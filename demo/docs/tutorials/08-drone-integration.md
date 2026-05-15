# Drone Integration Tutorial

This tutorial explains how the phone prototype becomes a drone workflow.

## Current Prototype Mapping

| Prototype | Drone Equivalent |
| --- | --- |
| Phone camera through DroidCam | Drone camera stream |
| Manual latitude/longitude | Drone GPS telemetry |
| Laptop inference | Ground station or onboard computer |
| Local JSON/CSV outputs | Backend database |
| Manual demo run | Flight session |

## Step 1: Replace Camera Source

The current command:

```powershell
py run_phone_demo.py --model segformer --source 0
```

Future drone stream:

```powershell
py run_phone_demo.py --model segformer --source DRONE_VIDEO_STREAM_URL
```

The camera module already accepts OpenCV-compatible stream URLs.

## Step 2: Replace Location Source

Current manual coordinates:

```powershell
--lat -6.2088 --lon 106.8456
```

Current file telemetry:

```powershell
--telemetry-file telemetry.sample.json
```

Future drone telemetry can update a JSON file or feed a dedicated telemetry provider.

## Step 3: Add Flight Metadata

Future fields:

- flight ID
- drone ID
- altitude
- heading
- camera pitch
- frame timestamp
- GPS timestamp

## Step 4: Decide Inference Location

Options:

- onboard drone computer
- laptop ground station
- remote server

Start with laptop ground station because it is easiest to debug and can use the existing prototype.

## Step 5: Validate Field Conditions

Field tests should record:

- lighting
- altitude
- speed
- camera angle
- water reflection
- inference latency
- false positives
- false negatives

