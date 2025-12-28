from pathlib import Path

"""
create_annotations.py

Helper utilities for building COCO-format annotations
from YOLO bounding boxes.
"""


def create_image_annotation(file_path: Path, width: int, height: int, image_id: int):
    """
    Create a COCO image entry.
    """
    return {
        "file_name": file_path.name,
        "width": width,
        "height": height,
        "id": image_id,
    }


def create_annotation_from_yolo_format(
    min_x, min_y, width, height,
    image_id, category_id, annotation_id,
    segmentation=True
):
    """
    Convert a YOLO bounding box to a COCO annotation.
    """

    bbox = [float(min_x), float(min_y), float(width), float(height)]
    area = width * height

    if segmentation:
        x2 = min_x + width
        y2 = min_y + height
        seg = [[min_x, min_y, x2, min_y, x2, y2, min_x, y2]]
    else:
        seg = []

    return {
        "id": annotation_id,
        "image_id": image_id,
        "category_id": category_id,
        "bbox": bbox,
        "area": area,
        "iscrowd": 0,
        "segmentation": seg,
    }


def create_annotation_from_yolo_results_format(
    min_x, min_y, width, height,
    image_id, category_id, confidence
):
    """
    Convert YOLO inference results into COCO results format.
    """
    return [{
        "image_id": image_id,
        "category_id": category_id,
        "bbox": [float(min_x), float(min_y), float(width), float(height)],
        "score": confidence,
    }]


# COCO base template
coco_format = {
    "images": [],
    "annotations": [],
    "categories": [],
}
