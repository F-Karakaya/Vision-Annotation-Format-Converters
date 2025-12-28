import cv2
import os
import matplotlib.pyplot as plt

"""
visualizer.py

Visualizes YOLO bounding box annotations on images.

Features:
- Reads YOLO-format bounding boxes
- Converts normalized coordinates to pixel space
- Draws bounding boxes and class labels
- Saves and displays the visualization result
"""

# ===============================
# PATH CONFIGURATION
# ===============================
IMAGE_PATH = "image/image.jpg"
TXT_PATH = "converter/mask.txt"
OUTPUT_DIR = "visualizer_data"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "image_visualized_with_bboxes.jpg")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===============================
# CLASS COLORS (BGR)
# ===============================
CLASS_COLORS = {
    0: (0,   0, 255),   # Red
    1: (0, 255,   0),   # Green
    2: (255, 0,   0),   # Blue
    3: (0, 255, 255),   # Yellow
}

# ===============================
# LOAD IMAGE
# ===============================
image = cv2.imread(IMAGE_PATH)
if image is None:
    raise FileNotFoundError(f"Image not found: {IMAGE_PATH}")

image_height, image_width, _ = image.shape

# ===============================
# READ YOLO ANNOTATIONS
# ===============================
with open(TXT_PATH, "r") as file:
    lines = file.readlines()

for line in lines:
    class_id, x, y, w, h = map(float, line.split())
    class_id = int(class_id)

    # Convert YOLO → pixel coordinates
    left = int((x - w / 2) * image_width)
    right = int((x + w / 2) * image_width)
    top = int((y - h / 2) * image_height)
    bottom = int((y + h / 2) * image_height)

    # Clamp bounding box to image boundaries
    left = max(0, left)
    right = min(image_width - 1, right)
    top = max(0, top)
    bottom = min(image_height - 1, bottom)

    color = CLASS_COLORS.get(class_id, (255, 255, 255))

    # Draw bounding box
    cv2.rectangle(image, (left, top), (right, bottom), color, 2)

    # Draw class label
    label_text = f"class {class_id}"
    cv2.putText(
        image,
        label_text,
        (left, max(top - 5, 15)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        color,
        1,
        cv2.LINE_AA,
    )

# ===============================
# SAVE RESULT
# ===============================
cv2.imwrite(OUTPUT_PATH, image)
print(f"Saved visualization to: {OUTPUT_PATH}")

# ===============================
# DISPLAY IMAGE (RGB for matplotlib)
# ===============================
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.imshow(image_rgb)
plt.axis("off")
plt.show()
