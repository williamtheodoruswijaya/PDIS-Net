import os
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Options:
    weights_repo: str
    weights_revision: str
    weights_dir: Path | None
    frontend_origins: list[str]

    @classmethod
    def from_env(cls):
        weights_dir = os.environ.get("WEIGHTS_DIR")
        if weights_dir and not Path(weights_dir).is_dir():
            raise ValueError(f"WEIGHTS_DIR={weights_dir} is not a folder")

        return cls(
            weights_repo=os.environ.get("WEIGHTS_REPO", "adamantix/pdisnet-weights"),
            weights_revision=os.environ.get("WEIGHTS_REVISION", "main"),
            weights_dir=Path(weights_dir) if weights_dir else None,
            frontend_origins=os.environ.get("FRONTEND_ORIGINS", "http://localhost:3000").split(","),
        )

OPTIONS = Options.from_env()