import json
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict

from src.constants import DATASET_METADATA_FILE, IMAGE_EXTENSIONS, ANNOTATION_EXTENSION


def compute_data_fingerprint(images: list[Path]) -> str:
    """
    Lightweight dataset fingerprint based on filenames + sizes.
    """
    sha = hashlib.sha256()
    for img in sorted(images, key=lambda x: x.name):
        sha.update(img.name.encode())
        sha.update(str(img.stat().st_size).encode())
    return sha.hexdigest()


def generate_dataset_metadata(job_dir: Path, extracted_dir: Path):
    images = [p for p in extracted_dir.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS]
    xmls = [p for p in extracted_dir.iterdir() if p.suffix.lower() == ANNOTATION_EXTENSION]

    class_counts = defaultdict(int)
    total_boxes = 0

    for xml in xmls:
        text = xml.read_text(errors="ignore")
        for line in text.splitlines():
            if "<name>" in line:
                label = line.replace("<name>", "").replace("</name>", "").strip()
                class_counts[label] += 1
                total_boxes += 1

    resolutions = []
    for xml in xmls:
        text = xml.read_text(errors="ignore")
        if "<width>" in text and "<height>" in text:
            try:
                w = int(text.split("<width>")[1].split("</width>")[0])
                h = int(text.split("<height>")[1].split("</height>")[0])
                resolutions.append((w, h))
            except Exception:
                pass

    metadata = {
        "job_id": job_dir.name,
        "created_at_utc": datetime.utcnow().isoformat(),
        "num_images": len(images),
        "num_annotations": total_boxes,
        "classes": dict(class_counts),
        "image_resolution_summary": {
            "min": list(min(resolutions)) if resolutions else None,
            "max": list(max(resolutions)) if resolutions else None,
        },
        "data_fingerprint": compute_data_fingerprint(images),
    }

    metadata_path = job_dir / DATASET_METADATA_FILE
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    return metadata_path
