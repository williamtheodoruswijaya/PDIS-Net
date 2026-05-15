# DroidCam Setup

DroidCam lets the phone act like a webcam. This is useful because the phone camera simulates the drone camera before the real drone stream is integrated.

## Setup Modes

There are two common ways to use DroidCam:

- Virtual webcam mode
- Wi-Fi stream mode

## Virtual Webcam Mode

1. Install DroidCam on the phone.
2. Install the DroidCam client on Windows.
3. Connect phone and computer through USB or Wi-Fi.
4. Start DroidCam.
5. Run the prototype with a camera index:

```powershell
cd "D:\BINUS\Semester 6\semantix\demo\droidcam-prototype"
py run_phone_demo.py --model segformer --source 0
```

If source `0` opens the laptop webcam instead, try:

```powershell
py run_phone_demo.py --model segformer --source 1
```

## Wi-Fi Stream Mode

1. Put phone and laptop on the same Wi-Fi.
2. Open DroidCam on the phone.
3. Note the phone IP address.
4. Run:

```powershell
py run_phone_demo.py --model segformer --source http://PHONE_IP:4747/video
```

Example:

```powershell
py run_phone_demo.py --model segformer --source http://192.168.1.24:4747/video
```

## Tips

- Use landscape orientation for drone-like framing.
- Keep the camera stable.
- Avoid dark lighting.
- Test with known plastic objects first.
- Keep the phone cool during longer tests.

## Common Problems

Camera does not open:

- DroidCam app is not started.
- Wrong camera index.
- Phone and laptop are on different Wi-Fi networks.
- Firewall blocks the stream.

Frame is delayed:

- Use USB mode.
- Reduce resolution in DroidCam.
- Close other camera apps.

