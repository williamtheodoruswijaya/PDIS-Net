# .second-brains — context for writing the PDIS-Net thesis

Built 2026-11-05 by traversing the whole repo. Read this first in every session.

## Session context

- **Purpose of these sessions:** writing the **thesis (skripsi) draft** for PDIS-Net, BINUS University.
- **Runs on CLOUD** (claude.ai/code remote container). The container is ephemeral → anything not
  committed + pushed to the dev branch is lost. Commit drafts often.
- Model weights (`*.pth`) are **Git LFS pointers only** in the cloud clone (134-byte text files).
  No GPU here either. Don't plan on re-running training/inference; work from the JSON/CSV/PNG in `results/`, `xai/`.
- The repo `.gitignore` ignores `.second-brain/` (singular, the local one on the user's laptop). This folder
  is `.second-brains/` (plural) so it **can** be committed and survive cloud resets.
- Thesis prose is Indonesian → use the `anthropic-skills:write-like-me` skill when drafting so it sounds
  like the user, not generic AI.

## Files

| File | What's inside | Thesis chapter |
|---|---|---|
| [`project.md`](project.md) | what the project is, dataset, split, repo map, timeline | Bab 1, Bab 3.1 |
| [`methods.md`](methods.md) | exact training recipe, models, loss, metrics, HPO, curriculum, XAI, deployment | Bab 3 |
| [`results.md`](results.md) | every number, grouped into the tables the thesis needs | Bab 4 |
| [`gotchas.md`](gotchas.md) | inconsistencies + caveats to handle before a number goes into the draft | all |
| [`thesis-status.md`](thesis-status.md) | where the thesis + diff artifact live, writing rules, decisions log | all |

## Golden rule

Every number in the draft must trace to a file in the repo (`results/<run>/<ver>/test_metrics.json`,
`history.csv`, `xai/.../xai_summary.json`, ...). If a number only lives in a README (e.g. the bootstrap CIs),
flag it — see `gotchas.md`.
