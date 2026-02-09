import json
from pathlib import Path
from src.constants import RUNS_DIR, VERSION_PREFIX, LATEST_FILE


def get_next_version(artifacts_dir: Path) -> str:
    runs_dir = artifacts_dir / RUNS_DIR
    runs_dir.mkdir(exist_ok=True)

    versions = [
        int(p.name.replace(VERSION_PREFIX, ""))
        for p in runs_dir.iterdir()
        if p.is_dir() and p.name.startswith(VERSION_PREFIX)
    ]

    next_version = max(versions) + 1 if versions else 1
    return f"{VERSION_PREFIX}{next_version}"


def update_latest_version(artifacts_dir: Path, version: str):
    latest_path = artifacts_dir / RUNS_DIR / LATEST_FILE
    with open(latest_path, "w") as f:
        json.dump({"latest_version": version}, f, indent=2)


def get_latest_version(artifacts_dir: Path) -> str:
    latest_path = artifacts_dir / RUNS_DIR / LATEST_FILE
    if not latest_path.exists():
        raise FileNotFoundError("No latest version found")
    with open(latest_path) as f:
        return json.load(f)["latest_version"]
