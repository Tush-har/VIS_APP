from fastapi import FastAPI, UploadFile, File, HTTPException
import uuid
import zipfile
import shutil
from pathlib import Path
from src.utils.job_status import read_status
from src.utils.versioning import get_latest_version
from src.constants import RUNS_DIR
from src.constants import DATASET_METADATA_FILE
from src.utils.s3_utils import download_file_from_s3
from tempfile import TemporaryDirectory
from src.utils.s3_utils import download_file_from_s3
from tempfile import TemporaryDirectory


from tempfile import TemporaryDirectory
from src.utils.s3_utils import download_file_from_s3
from src.constants import DATASET_METADATA_FILE, S3_DATASET_PREFIX

from src.constants import (
    BASE_UPLOAD_DIR,
    RAW_ZIP_DIR,
    EXTRACTED_DIR
)
from src.components.data_validation import validate_extracted_dataset
from src.components.data_transformation import transform_dataset

from src.components.model_trainer import train_yolo_model
from src.constants import (
    DEFAULT_EPOCHS,
    DEFAULT_IMGSZ,
    DEFAULT_BATCH,
    DEFAULT_MODEL
)

from fastapi.responses import FileResponse
from src.constants import ARTIFACTS_DIR


from fastapi import BackgroundTasks
from src.pipelines.train_pipeline import run_training_job
from src.utils.job_status import write_status
from src.constants import (
    BASE_UPLOAD_DIR,
    STATUS_PENDING,
    DEFAULT_EPOCHS,
    DEFAULT_IMGSZ,
    DEFAULT_BATCH,
    DEFAULT_MODEL
)



# Ensure base directory exists
BASE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# -------------------------------
# Upload Dataset API
# -------------------------------
app = FastAPI(title="VIS_APP – Vision Training Platform")
@app.post("/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):

    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only ZIP files are allowed")

    job_id = f"job_{uuid.uuid4().hex[:8]}"
    job_dir = BASE_UPLOAD_DIR / job_id

    raw_zip_dir = job_dir / RAW_ZIP_DIR
    extracted_dir = job_dir / EXTRACTED_DIR

    raw_zip_dir.mkdir(parents=True, exist_ok=True)
    extracted_dir.mkdir(parents=True, exist_ok=True)

    zip_path = raw_zip_dir / file.filename

    # Save ZIP
    with open(zip_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Validate ZIP
    if not zipfile.is_zipfile(zip_path):
        shutil.rmtree(job_dir)
        raise HTTPException(status_code=400, detail="Invalid ZIP file")

    # Extract ZIP
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extracted_dir)

    return {
        "job_id": job_id,
        "message": "Dataset uploaded and extracted successfully"
    }


# -------------------------------
# Preprocess Dataset API
# -------------------------------
@app.post("/preprocess/{job_id}")
def preprocess_dataset(job_id: str):

    job_dir = BASE_UPLOAD_DIR / job_id
    extracted_dir = job_dir / EXTRACTED_DIR

    if not extracted_dir.exists():
        raise HTTPException(status_code=404, detail="Job not found")

    validate_extracted_dataset(extracted_dir)

    # TODO: Make dynamic later
    class_map = {
        "teeth_good": 0,
        "1D": 1,
        "1G":2,
        "1J":3
    }

    transform_dataset(job_id, class_map)

    return {"status": "dataset processed successfully"}


# # training API

# @app.post("/train/{job_id}")
# def start_training(
#     job_id: str,
#     epochs: int = DEFAULT_EPOCHS,
#     imgsz: int = DEFAULT_IMGSZ,
#     batch: int = DEFAULT_BATCH,
#     model: str = DEFAULT_MODEL
# ):
#     result = train_yolo_model(
#         job_id=job_id,
#         epochs=epochs,
#         imgsz=imgsz,
#         batch=batch,
#         model_name=model
#     )

#     return result



# download model API


# @app.get("/download/model/{job_id}")
# def download_model(job_id: str):
#     model_path = (
#         BASE_UPLOAD_DIR
#         / job_id
#         / ARTIFACTS_DIR
#         / "model"
#         / "best.pt"
#     )

#     if not model_path.exists():
#         raise HTTPException(status_code=404, detail="Model not found")

#     return FileResponse(
#         path=model_path,
#         filename="best.pt",
#         media_type="application/octet-stream"
#     )





@app.get("/download/model/{job_id}")
def download_latest_model(job_id: str):
    artifacts_dir = BASE_UPLOAD_DIR / job_id / ARTIFACTS_DIR
    version = get_latest_version(artifacts_dir)

    model_path = (
        artifacts_dir
        / RUNS_DIR
        / version
        / "model"
        / "best.pt"
    )

    if not model_path.exists():
        raise HTTPException(status_code=404, detail="Model not found")

    return FileResponse(model_path, filename="best.pt")




# download metrices API
@app.get("/download/metrics/{job_id}")
def download_metrics(job_id: str):
    metrics_path = (
        BASE_UPLOAD_DIR
        / job_id
        / ARTIFACTS_DIR
        / "metrics.json"
    )

    if not metrics_path.exists():
        raise HTTPException(status_code=404, detail="Metrics not found")

    return FileResponse(
        path=metrics_path,
        filename="metrics.json",
        media_type="application/json"
    )



# async training

@app.post("/train-async/{job_id}")
def start_training_async(
    job_id: str,
    background_tasks: BackgroundTasks,
    epochs: int = DEFAULT_EPOCHS,
    imgsz: int = DEFAULT_IMGSZ,
    batch: int = DEFAULT_BATCH,
    model: str = DEFAULT_MODEL
):
    job_dir = BASE_UPLOAD_DIR / job_id

    if not job_dir.exists():
        raise HTTPException(status_code=404, detail="Job not found")

    write_status(job_dir, STATUS_PENDING, "Queued for training")

    background_tasks.add_task(
        run_training_job,
        job_id,
        epochs,
        imgsz,
        batch,
        model
    )

    return {
        "status": "accepted",
        "message": "Training started in background"
    }


# status of training
@app.get("/status/{job_id}")
def get_job_status(job_id: str):
    job_dir = BASE_UPLOAD_DIR / job_id

    if not job_dir.exists():
        raise HTTPException(status_code=404, detail="Job not found")

    return read_status(job_dir)



@app.get("/download/model/{job_id}/{version}")
def download_versioned_model(job_id: str, version: str):
    model_path = (
        BASE_UPLOAD_DIR
        / job_id
        / ARTIFACTS_DIR
        / RUNS_DIR
        / version
        / "model"
        / "best.pt"
    )

    if not model_path.exists():
        raise HTTPException(status_code=404, detail="Model not found")

    return FileResponse(model_path, filename=f"{version}_best.pt")




# @app.get("/dataset/metadata/{job_id}")
# def get_dataset_metadata(job_id: str):
#     metadata_path = (
#         BASE_UPLOAD_DIR
#         / job_id
#         / DATASET_METADATA_FILE
#     )

#     if not metadata_path.exists():
#         raise HTTPException(status_code=404, detail="Dataset metadata not found")

#     return FileResponse(
#         path=metadata_path,
#         filename=DATASET_METADATA_FILE,
#         media_type="application/json"
#     )



# @app.get("/download/model/{job_id}")
# def download_latest_model(job_id: str):
#     artifacts_dir = BASE_UPLOAD_DIR / job_id / ARTIFACTS_DIR
#     version = get_latest_version(artifacts_dir)

#     s3_key = f"{job_id}/runs/{version}/model/best.pt"

#     with TemporaryDirectory() as tmp:
#         local_path = Path(tmp) / "best.pt"
#         download_file_from_s3(local_path, s3_key)
#         return FileResponse(local_path, filename="best.pt")



# s3 metadata fetch
@app.get("/download/model/{job_id}")
def download_latest_model(job_id: str):
    artifacts_dir = BASE_UPLOAD_DIR / job_id / ARTIFACTS_DIR
    version = get_latest_version(artifacts_dir)

    s3_key = f"{job_id}/runs/{version}/model/best.pt"

    with TemporaryDirectory() as tmp:
        local_path = Path(tmp) / "best.pt"
        download_file_from_s3(local_path, s3_key)
        return FileResponse(local_path, filename="best.pt")



@app.get("/dataset/metadata/{job_id}")
def get_dataset_metadata(job_id: str):

    s3_key = f"{job_id}/{S3_DATASET_PREFIX}/{DATASET_METADATA_FILE}"

    with TemporaryDirectory() as tmp:
        local_path = Path(tmp) / DATASET_METADATA_FILE
        download_file_from_s3(local_path, s3_key)
        return FileResponse(
            local_path,
            filename=DATASET_METADATA_FILE,
            media_type="application/json"
        )

