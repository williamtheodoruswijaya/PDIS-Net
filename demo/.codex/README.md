# Codex Project Setup

This folder contains project-specific context for Codex-style coding sessions.

## Purpose

Use `.codex/` to keep agent-facing instructions close to the repository without mixing them into application code.

This folder covers:

- Project context
- Repeatable prompts
- Preflight checklists
- MCP configuration mirror
- Vibecoding workflow notes

## Suggested Reading Order For Agents

1. `../AGENTS.md`
2. `.codex/project-instructions.md`
3. `.codex/checklists/phone-demo-preflight.md`
4. Relevant prompt from `.codex/prompts/`
5. Relevant skill from `.skills/`

## Important Defaults

- Canonical demo folder: `droidcam-prototype/`
- Default runnable model: SegFormer
- Dashboard contract: `droidcam-prototype/runs/latest_detection.json`
- Local command style: PowerShell with `py`

