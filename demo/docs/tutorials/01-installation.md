# Installation

This project is currently optimized for a Windows PowerShell workflow.

## Python

Check:

```powershell
py --version
```

If `python --version` fails but `py --version` works, use `py` for this project.

## Dependencies

From the prototype folder:

```powershell
cd "D:\BINUS\Semester 6\semantix\demo\droidcam-prototype"
py -m pip install -r requirements.txt
```

Core packages:

- `torch`
- `transformers`
- `opencv-python`
- `numpy`
- `pillow`
- `safetensors`

## Optional Virtual Environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

## Verify Installation

```powershell
py run_phone_demo.py --help
```

Expected result: command help prints all options.

## Compile Check

From repository root:

```powershell
py -m compileall droidcam-prototype
```

Expected result: no syntax errors.

## DINOv3 Note

The DINOv3/EoMT model artifact exists, but the local package version must include `EomtDinov3ForUniversalSegmentation`. Use SegFormer for the default demo unless DINOv3 support has been verified.

