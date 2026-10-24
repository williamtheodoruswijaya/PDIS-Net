# Rebuilds model/README.md from every model/<run>/<version>/test_metrics.json.
import json
from pathlib import Path

root = Path(__file__).parent
rows = {"per-image": [], "dataset": []}
for f in sorted(root.glob("*/*/test_metrics.json")):
    m = json.loads(f.read_text())
    version = f.parts[-2]
    kind = "dataset" if version.startswith("v4") else "per-image"  # the v4 template scores dataset-level IoU at a val-picked threshold
    row = f"| {f.parts[-3]} | {version} | {m['foreground_iou']:.4f} | {m['miou']:.4f} | {m['background_iou']:.4f} | {m['dice']:.4f} | {m.get('mpa', float('nan')):.4f} |"
    rows[kind].append((m["miou"], row + (f" {m['cfg']['threshold']:.2f} |" if kind == "dataset" else "")))

header = "| run | version | foreground IoU | mIoU | background IoU | dice | mPA |"
lines = [
    "# model/",
    "",
    "Weights (`best.pth`, Git LFS) + the `test_metrics.json` they scored, one folder per run and version:",
    "`model/<run_id>/<version>/`. Same `<run_id>` as `notebooks/` and `results/`.",
    "Old models (before the 3x3 grid restart) are in `.archive/model/`.",
    "",
    "Regenerate these tables: `python model/build_index.py`. Sorted by mIoU, best first.",
    "",
    "The two tables score differently, so don't compare numbers across them. For run 02, every model was",
    "re-scored both ways on the same photos; see the results section of the main README.",
    "",
    "## Per-image IoU, threshold 0.5 (templates v1-v3)",
    "",
    header,
    "|---|---|---|---|---|---|---|",
    *[r for _, r in sorted(rows["per-image"], reverse=True)],
    "",
    "## Dataset-level IoU, threshold picked on val (template v4)",
    "",
    header + " threshold |",
    "|---|---|---|---|---|---|---|---|",
    *[r for _, r in sorted(rows["dataset"], reverse=True)],
    "",
]
(root / "README.md").write_text("\n".join(lines))
