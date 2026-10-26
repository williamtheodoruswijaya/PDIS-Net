# Rebuilds model/README.md from every model/<run>/<version>/test_metrics.json.
import json
from pathlib import Path

root = Path(__file__).parent
rows = []
for f in sorted(root.glob("*/*/test_metrics.json")):
    d = json.loads(f.read_text())
    m = d.get("per_image_t05", d)  # v4-template runs store dataset-level scores; their per-image re-score lives here
    rows.append((m["miou"], f"| {f.parts[-3]} | {f.parts[-2]} | {m['foreground_iou']:.4f} | {m['miou']:.4f} | {m['background_iou']:.4f} | {m['dice']:.4f} | {m.get('mpa', float('nan')):.4f} |"))

lines = [
    "# model/",
    "",
    "Weights (`best.pth`, Git LFS) + the `test_metrics.json` they scored, one folder per run and version:",
    "`model/<run_id>/<version>/`. Same `<run_id>` as `notebooks/` and `results/`.",
    "Old models (before the 3x3 grid restart) are in `.archive/model/`.",
    "",
    "Regenerate this table: `python model/build_index.py`. Sorted by mIoU, best first.",
    "All scores are per-image IoU at threshold 0.5 on the same 301 test photos (v2-clean-stage1: its 290 clean ones).",
    "The v4 notebooks store a different (dataset-level) score, so their rows use the per-image re-score saved as",
    "`per_image_t05`.",
    "",
    "| run | version | foreground IoU | mIoU | background IoU | dice | mPA |",
    "|---|---|---|---|---|---|---|",
    *[r for _, r in sorted(rows, reverse=True)],
    "",
]
(root / "README.md").write_text("\n".join(lines))
