from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
from PIL import Image, UnidentifiedImageError


IMAGE_EXTENSIONS = {".bmp", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}
BACKGROUND_LABEL = 0


@dataclass(frozen=True)
class ImagePair:
    image_stem: str
    raw_path: Path
    mask_path: Path


def setup_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def natural_sort_key(path: Path | str) -> list[object]:
    text = Path(path).name.lower()
    return [int(part) if part.isdigit() else part for part in re.split(r"(\d+)", text)]


def ensure_input_dir(path: str | Path) -> Path:
    directory = Path(path)
    if not directory.exists():
        raise FileNotFoundError(f"Missing required directory: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(f"Expected a directory: {directory}")
    return directory


def ensure_output_dir(path: str | Path) -> Path:
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def image_files(directory: str | Path) -> list[Path]:
    directory = ensure_input_dir(directory)
    files = [
        path
        for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    ]
    return sorted(files, key=natural_sort_key)


def canonical_stem(path: Path) -> str:
    stem = path.stem.strip().lower()
    for suffix in ("_mask", "-mask", " mask"):
        if stem.endswith(suffix):
            return stem[: -len(suffix)]
    return stem


def pair_image_files(raw_dir: str | Path, mask_dir: str | Path) -> list[ImagePair]:
    raw_files = image_files(raw_dir)
    mask_files = image_files(mask_dir)

    masks_by_key: dict[str, Path] = {}
    for mask_path in mask_files:
        key = canonical_stem(mask_path)
        if key in masks_by_key:
            logging.warning(
                "Duplicate mask key %s: keeping %s and skipping %s",
                key,
                masks_by_key[key].name,
                mask_path.name,
            )
            continue
        masks_by_key[key] = mask_path

    pairs: list[ImagePair] = []
    raw_keys: set[str] = set()
    used_mask_keys: set[str] = set()
    for raw_path in raw_files:
        key = canonical_stem(raw_path)
        raw_keys.add(key)
        mask_path = masks_by_key.get(key)
        if mask_path is None:
            logging.warning("No mask found for %s", raw_path.name)
            continue
        used_mask_keys.add(key)
        pairs.append(ImagePair(image_stem=raw_path.stem, raw_path=raw_path, mask_path=mask_path))

    for key, mask_path in masks_by_key.items():
        if key not in raw_keys and key not in used_mask_keys:
            logging.warning("No raw image found for %s", mask_path.name)

    return pairs


def markdown_relpath(target: str | Path, markdown_file: str | Path) -> str:
    target_path = Path(target)
    start = Path(markdown_file).parent
    return Path(os.path.relpath(target_path, start=start)).as_posix()


def format_int(value: int | np.integer | float) -> str:
    return f"{int(value):,}"


def format_float(value: float, digits: int = 1) -> str:
    return f"{value:.{digits}f}"


def format_percent(value: float, digits: int = 1) -> str:
    return f"{value:.{digits}f}%"


def load_raw_image(path: Path) -> Image.Image | None:
    try:
        with Image.open(path) as image:
            return image.convert("RGB")
    except (OSError, UnidentifiedImageError) as exc:
        logging.warning("Could not read raw image %s: %s", path.name, exc)
        return None


def load_mask_array(
    path: Path,
    target_size: tuple[int, int] | None = None,
    image_name: str | None = None,
) -> np.ndarray | None:
    try:
        with Image.open(path) as image:
            mask = image.convert("L")
            if target_size is not None and mask.size != target_size:
                name = image_name or path.name
                logging.warning(
                    "Mask size mismatch for %s: mask %dx%d vs raw %dx%d; resizing with nearest neighbor",
                    name,
                    mask.size[0],
                    mask.size[1],
                    target_size[0],
                    target_size[1],
                )
                mask = mask.resize(target_size, Image.Resampling.NEAREST)
            arr = np.array(mask)
    except (OSError, UnidentifiedImageError) as exc:
        logging.warning("Could not read mask %s: %s", path.name, exc)
        return None

    if arr.size == 0:
        logging.warning("Empty mask array for %s", path.name)
        return None
    return arr


def unique_labels(mask_arr: np.ndarray) -> np.ndarray:
    if mask_arr.size == 0:
        return np.array([], dtype=np.uint8)
    return np.unique(mask_arr)


def warn_if_empty_mask(mask_arr: np.ndarray, image_name: str) -> None:
    if not np.any(mask_arr != BACKGROUND_LABEL):
        logging.warning("Mask has no non-background pixels for %s", image_name)


def write_markdown_table(path: str | Path, header: str, divider: str, rows: Iterable[str]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    table = "\n".join([header, divider, *rows]) + "\n"
    output.write_text(table, encoding="utf-8")
