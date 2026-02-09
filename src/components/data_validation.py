from pathlib import Path
from src.constants import IMAGE_EXTENSIONS, ANNOTATION_EXTENSION, MIN_IMAGES_REQUIRED

def validate_extracted_dataset(extracted_dir: Path):
    images = []
    xmls = []

    for file in extracted_dir.rglob("*"):
        if file.suffix.lower() in IMAGE_EXTENSIONS:
            images.append(file)
        elif file.suffix.lower() == ANNOTATION_EXTENSION:
            xmls.append(file)

    if len(images) < MIN_IMAGES_REQUIRED:
        raise ValueError("Not enough images for training")

    if len(xmls) == 0:
        raise ValueError("No XML annotations found")

    return images, xmls
