import yaml
from pathlib import Path

def generate_data_yaml(dataset_dir: Path, class_map: dict):
    data = {
        "path": str(dataset_dir),
        "train": "images/train",
        "val": "images/val",
        "nc": len(class_map),
        "names": list(class_map.keys())
    }

    yaml_path = dataset_dir / "data.yaml"
    with open(yaml_path, "w") as f:
        yaml.safe_dump(data, f)

    return yaml_path
