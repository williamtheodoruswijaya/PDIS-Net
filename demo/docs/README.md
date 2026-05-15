# Documentation Index

This documentation turns the project into a repeatable workflow for humans and coding agents.

## Start Here

- [Full Walkthrough](tutorials/00-full-walkthrough.md)
- [Installation](tutorials/01-installation.md)
- [DroidCam Setup](tutorials/02-droidcam-setup.md)
- [Run The Phone Demo](tutorials/03-run-phone-demo.md)

## Main Sections

- [Tutorials](tutorials/README.md): step-by-step walkthroughs.
- [Architecture](architecture/README.md): how the system is shaped.
- [Operations](operations/README.md): runbooks, testing, release, retention.
- [Dashboard](dashboard/README.md): dashboard contract and map planning.
- [Research](research/README.md): model notes and metrics context.
- [Codex](codex/README.md): vibecoding, MCP, skills, and agent workflows.

## Most Important Project Truths

- The runnable demo is in `droidcam-prototype/`.
- SegFormer is the current default model for local demo runs.
- DINOv3 is available as a model artifact, but local package support may need upgrading.
- The dashboard should consume `droidcam-prototype/runs/latest_detection.json`.
- Generated camera runs should not be committed.

