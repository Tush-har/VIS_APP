from ultralytics import YOLO
from pathlib import Path
import mlflow
import json
import time
import shutil
from src.utils.versioning import get_next_version, update_latest_version
from src.constants import RUNS_DIR

from src.constants import (
    BASE_UPLOAD_DIR,
    PROCESSED_DIR,
    ARTIFACTS_DIR,
    DEFAULT_EPOCHS,
    DEFAULT_IMGSZ,
    DEFAULT_BATCH,
    DEFAULT_MODEL,
    MLFLOW_EXPERIMENT_NAME,
    MLFLOW_TRACKING_URI,
)


def train_yolo_model(
    job_id: str,
    epochs: int = DEFAULT_EPOCHS,
    imgsz: int = DEFAULT_IMGSZ,
    batch: int = DEFAULT_BATCH,
    model_name: str = DEFAULT_MODEL
):

    # -----------------------------
    # Paths
    # -----------------------------
    job_dir = BASE_UPLOAD_DIR / job_id
    dataset_dir = job_dir / PROCESSED_DIR
    artifacts_dir = job_dir / ARTIFACTS_DIR
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    data_yaml = dataset_dir / "data.yaml"
    if not data_yaml.exists():
        raise FileNotFoundError("data.yaml not found. Dataset not ready.")

    # -----------------------------
    # MLflow setup
    # -----------------------------
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

    start_time = time.time()

    with mlflow.start_run(run_name=job_id):

        # -----------------------------
        # Log params
        # -----------------------------
        params = {
            "epochs": epochs,
            "imgsz": imgsz,
            "batch": batch,
            "model": model_name
        }
        mlflow.log_params(params)

        # -----------------------------
        # Train YOLO
        # -----------------------------
        model = YOLO(model_name)

        results = model.train(
            data=str(data_yaml),
            epochs=epochs,
            imgsz=imgsz,
            batch=batch,
            project=str(artifacts_dir),
            name="train",
            exist_ok=True
        )

        # -----------------------------
        # Resolve best.pt
        # -----------------------------
        save_dir = Path(results.save_dir)
        best_model_path = save_dir / "weights" / "best.pt"


        # version
        version = get_next_version(artifacts_dir)

        run_dir = artifacts_dir / RUNS_DIR / version
        model_dir = run_dir / "model"
        model_dir.mkdir(parents=True, exist_ok=True)

        registry_model_path = model_dir / "best.pt"
        shutil.copy(best_model_path, registry_model_path)

        if not best_model_path.exists():
            raise RuntimeError(
                f"Training completed but best.pt not found at {best_model_path}"
            )

        # -----------------------------
        # Copy model to registry
        # -----------------------------
        model_registry_dir = artifacts_dir / "model"
        model_registry_dir.mkdir(exist_ok=True)
        registry_model_path = model_registry_dir / "best.pt"

        shutil.copy(best_model_path, registry_model_path)

        # -----------------------------
        # Create metadata (DEFINE FIRST)
        # -----------------------------
        metrics = {
            "version": version,
            "training_time_sec": round(time.time() - start_time, 2),
            "best_model_path": str(registry_model_path)
        }


        # -----------------------------
        # Write metadata to disk
        # -----------------------------
        # metrics_path = artifacts_dir / "metrics.json"
        # params_path = artifacts_dir / "params.json"
        metrics_path = run_dir / "metrics.json"
        params_path = run_dir / "params.json"


        with open(metrics_path, "w") as f:
            json.dump(metrics, f, indent=2)

        with open(params_path, "w") as f:
            json.dump(params, f, indent=2)

        update_latest_version(artifacts_dir, version)


        # -----------------------------
        # Log artifacts to MLflow
        # -----------------------------
        mlflow.log_artifact(str(registry_model_path), artifact_path="model")
        mlflow.log_artifact(str(metrics_path), artifact_path="metadata")
        mlflow.log_artifact(str(params_path), artifact_path="metadata")

        # -----------------------------
        # FINAL RETURN (last line)
        # -----------------------------
        return {
        "status": "training_completed",
        "version": version,
        "model_path": str(registry_model_path),
        "metrics_path": str(metrics_path),
        "params_path": str(params_path)
         }

