from pathlib import Path
import argparse
import json
import cv2
import numpy as np
import imagesize

from create_annotations import (
    create_image_annotation,
    create_annotation_from_yolo_format,
    create_annotation_from_yolo_results_format,
    coco_format,
)

"""
main.py

Converts YOLO-format annotations into COCO dataset format.

Supported input:
- A directory containing images (.jpg / .png)
- A text file listing absolute image paths (train.txt / test.txt)

Supported output:
- COCO detection annotations
- Optional COCO-style segmentation from bounding boxes
- Optional YOLO result format with confidence scores
"""

# --------------------------------------------------
# Dataset Configuration
# --------------------------------------------------

YOLO_DARKNET_SUB_DIR = "YOLO_darknet"

# IMPORTANT:
# Update class names according to your dataset
# Do NOT change the variable name "classes"
classes = [
    "0",
    "1",
    "2",
    "3",
]


def get_images_info_and_annotations(opt):
    """
    Parse images and corresponding YOLO annotations,
    then convert them into COCO-compatible structures.
    """

    if opt.path is None:
        raise ValueError("No input path provided.")

    path = Path(opt.path)
    if not path.exists():
        raise FileNotFoundError(f"Provided path does not exist: {path}")

    images_annotations = []
    annotations = []

    # --------------------------------------------------
    # Resolve image file paths
    # --------------------------------------------------
    if path.is_dir():
        image_paths = []
        image_paths += sorted(path.rglob("*.jpg"))
        image_paths += sorted(path.rglob("*.jpeg"))
        image_paths += sorted(path.rglob("*.png"))
    else:
        with open(path, "r") as f:
            image_paths = [Path(line.strip()) for line in f.readlines()]

    image_id = 0
    annotation_id = 1  # COCO annotation IDs must start from 1

    # --------------------------------------------------
    # Process each image
    # --------------------------------------------------
    for img_path in image_paths:
        print(f"\rProcessing image {image_id}", end="")

        # Get image size without full decoding
        width, height = imagesize.get(str(img_path))

        image_annotation = create_image_annotation(
            file_path=img_path,
            width=width,
            height=height,
            image_id=image_id,
        )
        images_annotations.append(image_annotation)

        label_name = f"{img_path.stem}.txt"

        if opt.yolo_subdir:
            label_path = img_path.parent / YOLO_DARKNET_SUB_DIR / label_name
        else:
            label_path = img_path.parent / label_name

        if not label_path.exists():
            image_id += 1
            continue

        # --------------------------------------------------
        # Read YOLO labels
        # --------------------------------------------------
        with open(label_path, "r") as f:
            label_lines = f.readlines()

        for line in label_lines:
            parts = line.strip().split()

            category_id = int(parts[0]) + 1  # COCO category IDs start from 1
            x_center, y_center, w, h = map(float, parts[1:5])

            # Convert normalized YOLO → pixel space
            px = x_center * width
            py = y_center * height
            pw = w * width
            ph = h * height

            min_x = int(px - pw / 2)
            min_y = int(py - ph / 2)

            if opt.results:
                conf = float(parts[5])
                annotation = create_annotation_from_yolo_results_format(
                    min_x, min_y, int(pw), int(ph),
                    image_id, category_id, conf
                )
            else:
                annotation = create_annotation_from_yolo_format(
                    min_x, min_y, int(pw), int(ph),
                    image_id, category_id, annotation_id,
                    segmentation=opt.box2seg,
                )

            annotations.append(annotation)
            annotation_id += 1

        image_id += 1

    return images_annotations, annotations


def debug(opt):
    """
    Visual debugging utility for YOLO annotations.
    Draws bounding boxes on images and prints details.
    """

    color_map = np.random.randint(0, 255, (len(classes), 3)).tolist()

    with open(opt.path, "r") as f:
        image_list = f.readlines()

    for line in image_list:
        image_path = line.strip()
        img = cv2.imread(image_path)

        label_path = image_path.replace(".jpg", ".txt")
        with open(label_path, "r") as f:
            labels = f.readlines()

        for label in labels:
            cls, xc, yc, w, h = map(float, label.split())
            cls = int(cls)

            iw, ih = img.shape[1], img.shape[0]
            px = int(xc * iw)
            py = int(yc * ih)
            pw = int(w * iw)
            ph = int(h * ih)

            x1 = int(px - pw / 2)
            y1 = int(py - ph / 2)
            x2 = int(px + pw / 2)
            y2 = int(py + ph / 2)

            cv2.rectangle(img, (x1, y1), (x2, y2), color_map[cls], 2)
            cv2.putText(
                img,
                classes[cls],
                (x1, max(y1 - 5, 15)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color_map[cls],
                1,
            )

        cv2.imshow("Debug", img)
        if cv2.waitKey(0) in [27, ord("q")]:
            break

    cv2.destroyAllWindows()


def get_args():
    """
    Parse command-line arguments.
    """

    parser = argparse.ArgumentParser(
        description="Convert YOLO annotations to COCO dataset format"
    )

    parser.add_argument(
        "-p", "--path",
        type=str,
        default="input/dataset.txt",
        help="Path to image directory or train/test txt file."
    )
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--output", default="dataset_coco.json")
    parser.add_argument("--yolo-subdir", action="store_true")
    parser.add_argument("--box2seg", action="store_true")
    parser.add_argument("--results", action="store_true")

    return parser.parse_args()


def main(opt):
    print("Start!")

    if opt.debug:
        debug(opt)
        print("Debug finished.")
        return

    images, anns = get_images_info_and_annotations(opt)
    coco_format["images"] = images
    coco_format["annotations"] = anns

    for idx, name in enumerate(classes):
        coco_format["categories"].append({
            "id": idx + 1,
            "name": name,
            "supercategory": "Defect",
        })

    Path("output").mkdir(exist_ok=True)
    output_path = Path("output") / opt.output

    if opt.results:
        results = [a[0] for a in coco_format["annotations"]]
        with open(output_path, "w") as f:
            json.dump(results, f, indent=4)
    else:
        with open(output_path, "w") as f:
            json.dump(coco_format, f, indent=4)

    print("\nFinished!")


if __name__ == "__main__":
    args = get_args()
    main(args)
