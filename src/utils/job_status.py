import json
from pathlib import Path
from datetime import datetime
from src.constants import STATUS_FILE


def write_status(job_dir: Path, status: str, message: str = ""):
    status_path = job_dir / STATUS_FILE
    data = {
        "status": status,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }
    with open(status_path, "w") as f:
        json.dump(data, f, indent=2)


def read_status(job_dir: Path):
    status_path = job_dir / STATUS_FILE
    if not status_path.exists():
        return {"status": "unknown"}
    with open(status_path) as f:
        return json.load(f)
