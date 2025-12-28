import os
import cv2
import numpy as np


"""
converter.py

Converts RGB segmentation masks into YOLO segmentation (.txt) annotations.

Pipeline:
1. Read RGB segmentation masks
2. Extract regions matching predefined RGB colors
3. Convert each region into polygon contours
4. Normalize polygon coordinates
5. Save annotations in YOLO segmentation format

Output format:
<class_id> x1 y1 x2 y2 x3 y3 ...
"""

# Input directory containing RGB mask images
INPUT_DIR = "data/masks"

# Output directory for YOLO segmentation annotations
OUTPUT_DIR = "data/txt_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# RGB color -> class_id mapping
COLOR_TO_CLASS = {
    (254, 233,   3): 0,
    (201,  19, 223): 1,
    (238, 171, 171): 2,
    (255, 160,   1): 3,
}

for filename in os.listdir(INPUT_DIR):
    image_path = os.path.join(INPUT_DIR, filename)

    # Load image
    image_bgr = cv2.imread(image_path)
    if image_bgr is None:
        continue

    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    height, width, _ = image_rgb.shape

    txt_path = os.path.join(OUTPUT_DIR, filename.rsplit(".", 1)[0] + ".txt")

    with open(txt_path, "w") as file:

        # Process each color as a separate class
        for rgb_color, class_id in COLOR_TO_CLASS.items():

            # Create binary mask for the given RGB color
            binary_mask = (
                np.all(image_rgb == rgb_color, axis=2)
                .astype(np.uint8)
                * 255
            )

            if cv2.countNonZero(binary_mask) == 0:
                continue

            # Extract contours
            contours, _ = cv2.findContours(
                binary_mask,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE,
            )

            for contour in contours:
                if cv2.contourArea(contour) <= 1:
                    continue

                # Convert contour points to normalized polygon coordinates
                polygon = []
                for point in contour:
                    x, y = point[0]
                    polygon.append(x / width)
                    polygon.append(y / height)

                # Write YOLO segmentation line
                file.write(str(class_id) + " ")
                file.write(" ".join(map(str, polygon)))
                file.write("\n")
