import os

PROJECT_STRUCTURE = {
    "data": {
        "raw": {},
        "processed": {}
    },
    "src": {
        "components": {
            "data_ingestion.py": "",
            "data_validation.py": "",
            "data_transformation.py": "",
            "model_trainer.py": "",
            "model_evaluation.py": "",
            "model_pusher.py": "",
        },
        "pipelines": {
            "train_pipeline.py": "",
            "predict_pipeline.py": "",
        },
        "config": {
            "config.yaml": "",
            "schema.yaml": "",
        },
        "utils": {
            "logger.py": "",
            "common.py": "",
            "s3_utils.py": "",
        },
        "__init__.py": ""
    },
    "app": {
        "main.py": ""
    },
    "notebooks": {},
    "tests": {},
    ".github": {
        "workflows": {
            "ci-cd.yaml": ""
        }
    },
    "Dockerfile": "",
    "requirements.txt": "",
    "README.md": "",
    ".gitignore": ""
}


def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)

        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            if not os.path.exists(path):
                with open(path, "w") as f:
                    f.write(content)


if __name__ == "__main__":
    project_root = "./"
    os.makedirs(project_root, exist_ok=True)
    create_structure(project_root, PROJECT_STRUCTURE)
    print("✅ YOLO MLOps project structure created successfully.")
