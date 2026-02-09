from pathlib import Path
from src.components.model_trainer import train_yolo_model
from src.utils.job_status import write_status
from src.constants import (
    BASE_UPLOAD_DIR,
    STATUS_RUNNING,
    STATUS_COMPLETED,
    STATUS_FAILED
)


def run_training_job(job_id: str, epochs: int, imgsz: int, batch: int, model: str):
    job_dir = BASE_UPLOAD_DIR / job_id

    try:
        write_status(job_dir, STATUS_RUNNING, "Training started")

        train_yolo_model(
            job_id=job_id,
            epochs=epochs,
            imgsz=imgsz,
            batch=batch,
            model_name=model
        )

        write_status(job_dir, STATUS_COMPLETED, "Training completed successfully")

    except Exception as e:
        write_status(job_dir, STATUS_FAILED, str(e))
