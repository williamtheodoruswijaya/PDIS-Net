from pathlib import Path
from huggingface_hub import HfApi

MODEL_DIR = Path(__file__).resolve().parents[2] / "model"

api = HfApi()
api.create_repo("adamantix/pdisnet-weights", repo_type="model", exist_ok=True)

api.upload_folder(
    folder_path = MODEL_DIR / "segformer",
    path_in_repo = "segformer",
    repo_id = "adamantix/pdisnet-weights",
    ignore_patterns = ["*.pth"],
)

'''
# for name, skip in UPLOAD.items():
#     api.upload_folder(
#         folder_path = MODEL_DIR/name,
#         path_in_repo = name,
#         repo_id = "adamantix/pdisnet-weights",
#         ignore_patterns = skip,
#     )
'''