import sys
from pathlib import Path
from huggingface_hub import HfApi

DEPLOYMENT = Path(__file__).resolve().parents[1]
REPO_ROOT = DEPLOYMENT.parent
sys.path.insert(0, str(DEPLOYMENT / "server"))
from core.domain.options import OPTIONS
from core.entities.trained_models import TRAINED_MODELS

api = HfApi()
for arch, backbone, init, folder in TRAINED_MODELS:
    print(f"uploading {arch}-{backbone}-{init} from model/{folder}")
    api.upload_folder(
        folder_path=REPO_ROOT / "model" / folder,
        path_in_repo=folder,
        repo_id=OPTIONS.weights_repo,
        allow_patterns=["best.pth", "test_metrics.json"],
        commit_message=f"add {folder}",
    )