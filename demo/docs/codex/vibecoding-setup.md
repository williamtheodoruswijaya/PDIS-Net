# Vibecoding Setup

Vibecoding setup means configuring the repository so a coding agent can understand the project quickly and act safely.

## Files Added For This

```text
AGENTS.md
.codex/README.md
.codex/project-instructions.md
.codex/mcp.json
.codex/checklists/
.codex/prompts/
.skills/
docs/codex/
```

## What Agents Should Read

For any task:

1. `AGENTS.md`
2. `.codex/project-instructions.md`
3. the relevant `.skills/*/SKILL.md`
4. the relevant docs section

## Good Vibecoding Loop

```text
context -> small plan -> edit -> verify -> explain -> update docs
```

## Example Agent Request

```text
Use the local droidcam-phone-demo skill.
Add a CLI flag to change preview width.
Keep SegFormer as the default.
Run compileall and --help.
Update docs if command behavior changes.
```

## Why This Matters

The project mixes research artifacts, large model files, prototype code, and future dashboard planning. Without a shared context layer, agents can easily optimize the wrong thing.

