import shutil
import random
from pathlib import Path

from src.constants import *
from src.utils.xml_parser import parse_voc_xml
from src.utils.yolo_converter import voc_to_yolo
from src.utils.yaml_generator import generate_data_yaml
from src.utils.dataset_metadata import generate_dataset_metadata
from src.utils.s3_utils import upload_file_to_s3
from src.constants import DATASET_METADATA_FILE, S3_DATASET_PREFIX


def transform_dataset(job_id: str, class_map: dict):

    job_dir = BASE_UPLOAD_DIR / job_id
    extracted_dir = job_dir / EXTRACTED_DIR
    processed_dir = job_dir / PROCESSED_DIR

    # Create YOLO directory structure
    for split in [TRAIN_DIR, VAL_DIR]:
        (processed_dir / IMAGES_DIR / split).mkdir(parents=True, exist_ok=True)
        (processed_dir / LABELS_DIR / split).mkdir(parents=True, exist_ok=True)

    images = [p for p in extracted_dir.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS]

    if len(images) == 0:
        raise ValueError("No images found in extracted dataset")

    random.seed(RANDOM_SEED)
    random.shuffle(images)

    split_idx = int(len(images) * TRAIN_SPLIT_RATIO)
    train_imgs = images[:split_idx]
    val_imgs = images[split_idx:]

    def process_split(image_list, split):
        for img_path in image_list:
            xml_path = img_path.with_suffix(ANNOTATION_EXTENSION)

            if not xml_path.exists():
                continue

            img_w, img_h, objects = parse_voc_xml(xml_path)

            if len(objects) == 0:
                continue

            label_file = processed_dir / LABELS_DIR / split / f"{img_path.stem}.txt"

            with open(label_file, "w") as f:
                for obj in objects:
                    if obj["label"] not in class_map:
                        continue

                    class_id = class_map[obj["label"]]
                    x, y, w, h = voc_to_yolo(obj["bbox"], img_w, img_h)
                    f.write(f"{class_id} {x} {y} {w} {h}\n")

            shutil.copy(
                img_path,
                processed_dir / IMAGES_DIR / split / img_path.name
            )

    process_split(train_imgs, TRAIN_DIR)
    process_split(val_imgs, VAL_DIR)
    generate_data_yaml(processed_dir, class_map)


# After dataset processing + data.yaml generation
    generate_dataset_metadata(job_dir=job_dir, extracted_dir=extracted_dir)
    metadata_path = job_dir / DATASET_METADATA_FILE

    upload_file_to_s3(
        metadata_path,
        f"{job_dir.name}/{S3_DATASET_PREFIX}/{DATASET_METADATA_FILE}"
    )

