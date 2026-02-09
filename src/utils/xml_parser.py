import xml.etree.ElementTree as ET
from pathlib import Path


def parse_voc_xml(xml_path: Path):
    """
    Parses a Pascal VOC XML file.

    Returns:
        image_width (int)
        image_height (int)
        objects (list of dicts)
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    size = root.find("size")
    if size is None:
        raise ValueError(f"Missing <size> tag in {xml_path.name}")

    img_w = int(size.find("width").text)
    img_h = int(size.find("height").text)

    objects = []

    for obj in root.findall("object"):
        label = obj.find("name").text.strip()

        bndbox = obj.find("bndbox")
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)

        # Skip invalid boxes
        if xmax <= xmin or ymax <= ymin:
            continue

        objects.append({
            "label": label,
            "bbox": (xmin, ymin, xmax, ymax)
        })

    return img_w, img_h, objects
