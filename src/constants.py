from pathlib import Path

# Base directory MUST be a Path object
BASE_UPLOAD_DIR = Path("data/uploads")

RAW_ZIP_DIR = "raw_zip"
EXTRACTED_DIR = "extracted"
PROCESSED_DIR = "processed"
ARTIFACTS_DIR = "artifacts"

IMAGES_DIR = "images"
LABELS_DIR = "labels"

TRAIN_DIR = "train"
VAL_DIR = "val"

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]
ANNOTATION_EXTENSION = ".xml"

TRAIN_SPLIT_RATIO = 0.8
RANDOM_SEED = 42
MIN_IMAGES_REQUIRED = 5


# ---------- Training Defaults ----------
DEFAULT_EPOCHS = 50
DEFAULT_IMGSZ = 640
DEFAULT_BATCH = 16
DEFAULT_MODEL = "yolov8n.pt"

# ---------- MLflow ----------
MLFLOW_EXPERIMENT_NAME = "VIS_APP_YOLO"
MLFLOW_TRACKING_URI = "http://localhost:5000"

# ---------- Job Status ----------
STATUS_PENDING = "pending"
STATUS_RUNNING = "running"
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"

STATUS_FILE = "status.json"
# ---------- Versioning ----------
RUNS_DIR = "runs"
LATEST_FILE = "latest.json"
VERSION_PREFIX = "v"

# ---------- Dataset Metadata ----------
DATASET_METADATA_FILE = "dataset_metadata.json"
# ---------- S3 ----------
S3_BUCKET_NAME = "vis-app-ml-artifacts"
S3_ARTIFACT_PREFIX = ""
S3_DATASET_PREFIX = "dataset"
