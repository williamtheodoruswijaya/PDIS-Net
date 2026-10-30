from pathlib import Path
from huggingface_hub import hf_hub_download
from core.domain.options import OPTIONS

def weights_file(folder, filename):
    if OPTIONS.weights_dir:
        return OPTIONS.weights_dir / folder / filename

    path = hf_hub_download(OPTIONS.weights_repo, f"{folder}/{filename}", revision=OPTIONS.weights_revision)

    return Path(path)