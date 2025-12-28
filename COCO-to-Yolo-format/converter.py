import json
import cv2
from pathlib import Path

"""
converter.py

Converts COCO-format annotations into YOLO-format annotation files.

Supported:
- Standard COCO JSON structure
- Bounding-box based annotations
- Multiple categories
"""


# --------------------------------------------------
# Utility Functions
# --------------------------------------------------

def read_json(json_file):
    with open(json_file, "r") as f:
        return json.load(f)


def get_image_shape(image_path):
    img = cv2.imread(str(image_path))
    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    return img.shape[:2]  # (height, width)


def coco_bbox_to_yolo(bbox, img_width, img_height):
    """
    COCO bbox: [xmin, ymin, width, height]
    YOLO bbox: [x_center, y_center, width, height] (normalized)
    """
    xmin, ymin, w, h = bbox

    x_center = (xmin + w / 2) / img_width
    y_center = (ymin + h / 2) / img_height
    w /= img_width
    h /= img_height

    return (
        round(x_center, 6),
        round(y_center, 6),
        round(w, 6),
        round(h, 6),
    )


def find_image_by_name(file_name, img_dir):
    """
    Locate image file using its file_name from COCO JSON.
    """
    candidate = Path(img_dir) / file_name
    if candidate.exists():
        return candidate

    raise FileNotFoundError(f"Image file not found: {file_name}")


# --------------------------------------------------
# Main Conversion Logic
# --------------------------------------------------

def process_coco_json(json_file, img_dir, output_dir):
    coco = read_json(json_file)

    images = coco.get("images", [])
    annotations = coco.get("annotations", [])

    # Map image_id -> image info
    image_map = {img["id"]: img for img in images}

    # Group annotations by image_id
    ann_by_image = {}
    for ann in annotations:
        ann_by_image.setdefault(ann["image_id"], []).append(ann)

    for image_id, image_info in image_map.items():
        file_name = image_info["file_name"]
        img_width = image_info["width"]
        img_height = image_info["height"]

        image_path = find_image_by_name(file_name, img_dir)

        yolo_lines = []

        for ann in ann_by_image.get(image_id, []):
            category_id = ann["category_id"] - 1  # COCO → YOLO index
            bbox = ann["bbox"]

            x, y, w, h = coco_bbox_to_yolo(
                bbox,
                img_width,
                img_height,
            )

            yolo_lines.append(f"{category_id} {x} {y} {w} {h}")

        output_dir.mkdir(parents=True, exist_ok=True)
        output_txt = output_dir / (Path(file_name).stem + ".txt")

        with open(output_txt, "w") as f:
            f.write("\n".join(yolo_lines))

        print(f"Converted: {file_name} → {output_txt}")


def convert_all_coco_to_yolo(json_dir, img_dir, output_dir):
    json_dir = Path(json_dir)
    img_dir = Path(img_dir)
    output_dir = Path(output_dir)

    json_files = sorted(json_dir.glob("*.json"))

    for json_file in json_files:
        process_coco_json(json_file, img_dir, output_dir)


# --------------------------------------------------
# Entry Point
# --------------------------------------------------

if __name__ == "__main__":
    json_dir = "input/json"      # COCO JSON files
    img_dir = "input/img"        # Image directory
    output_dir = "output/"   # YOLO TXT output

    convert_all_coco_to_yolo(json_dir, img_dir, output_dir)
