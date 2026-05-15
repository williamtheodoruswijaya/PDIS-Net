# Prompt: Phone Demo Work

Use this prompt when asking Codex to work on the DroidCam prototype.

```text
Work on the Semantix phone-camera prototype in droidcam-prototype/.

Goal:
- Keep SegFormer as the default runnable model.
- Preserve the dashboard output contract.
- Make the change small and verifiable.

Before editing:
- Read AGENTS.md.
- Read droidcam-prototype/README.md.
- Check droidcam-prototype/src/drone_phone_demo/.

Verify:
- py -m compileall droidcam-prototype
- py droidcam-prototype\run_phone_demo.py --help

Do not modify model weights.
```

