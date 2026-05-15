# Drone Integration Architecture

## Current Prototype

The phone camera is a replacement for the drone camera during early prototyping.

```text
phone camera -> DroidCam -> OpenCV -> model -> output files
```

## Target Drone Architecture

```text
drone camera stream -> ground station inference -> detection records -> dashboard
drone telemetry ----/
```

## Telemetry Adapter

The current telemetry provider reads:

- manual latitude/longitude
- JSON file latitude/longitude

Future telemetry provider should read:

- GPS latitude
- GPS longitude
- altitude
- heading
- camera pitch
- flight ID
- drone ID

## Synchronization

The hard part is matching video frames to telemetry timestamps.

Minimum viable approach:

- read latest telemetry when frame is saved
- record both frame timestamp and telemetry source

Better future approach:

- maintain telemetry buffer
- match nearest telemetry timestamp to frame timestamp

## Inference Placement

| Location | Pros | Cons |
| --- | --- | --- |
| Drone onboard | lower network dependency | limited compute |
| Laptop ground station | easy debugging | needs video link |
| Remote server | stronger compute | latency and network risk |

Start with laptop ground station.

