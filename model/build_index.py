# Rebuilds model/README.md from every model/<run>/<version>/test_metrics.json.
import json
from pathlib import Path

root = Path(__file__).parent
rows = []
for f in sorted(root.glob("*/*/test_metrics.json")):
    m = json.loads(f.read_text())
    rows.append((m["miou"], f"| {f.parts[-3]} | {f.parts[-2]} | {m['foreground_iou']:.4f} | {m['miou']:.4f} | {m['background_iou']:.4f} | {m['dice']:.4f} |"))

lines = [
    "# model/",
    "",
    "Weights (`best.pth`, Git LFS) + the `test_metrics.json` they scored, one folder per run and version:",
    "`model/<run_id>/<version>/`. Same `<run_id>` as `notebooks/` and `results/`.",
    "Old models (before the 3x3 grid restart) are in `.archive/model/`.",
    "",
    "Regenerate this table: `python model/build_index.py`. Sorted by mIoU, best first.",
    "",
    "| run | version | foreground IoU | mIoU | background IoU | dice |",
    "|---|---|---|---|---|---|",
    *[r for _, r in sorted(rows, reverse=True)],
    "",
]
(root / "README.md").write_text("\n".join(lines))
