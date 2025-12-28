import os

"""
converter.py

Converts polygon-based annotations into YOLO bounding box format.

Key Features:
- Computes bounding boxes from polygon coordinates
- Filters out very small objects using pixel-based size thresholds
- Outputs YOLO-compatible normalized bounding boxes
- Supports batch processing of annotation files

Expected Input Format (per line):
<class_id> x1 y1 x2 y2 x3 y3 ...

Output Format (YOLO):
<class_id> x_center y_center width height
"""

# ===============================
# IMAGE & FILTER PARAMETERS
# ===============================
IMAGE_WIDTH_PX = 1920
IMAGE_HEIGHT_PX = 1080
MIN_BOX_SIZE_PX = 15  # minimum allowed edge length in pixels


def convert_to_yolo(txt_file_path):
    """
    Convert a single polygon annotation file to YOLO bounding box format.

    Args:
        txt_file_path (str): Path to polygon annotation file

    Returns:
        list[dict]: List of YOLO bounding box annotations
    """

    with open(txt_file_path, "r") as file:
        lines = file.readlines()

    converted_annotations = []

    for line in lines:
        parts = line.strip().split(" ")
        class_id = int(parts[0])

        # Separate x and y coordinates
        x_coords = [float(parts[i]) for i in range(1, len(parts), 2)]
        y_coords = [float(parts[i]) for i in range(2, len(parts), 2)]

        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)

        width = max_x - min_x
        height = max_y - min_y

        # ===============================
        # PIXEL-BASED SIZE FILTER
        # ===============================
        box_width_px = width * IMAGE_WIDTH_PX
        box_height_px = height * IMAGE_HEIGHT_PX

        short_edge = min(box_width_px, box_height_px)
        long_edge = max(box_width_px, box_height_px)

        # Skip very small objects
        if short_edge < MIN_BOX_SIZE_PX and long_edge < MIN_BOX_SIZE_PX:
            continue
        # ===============================

        # YOLO normalized bounding box
        x_center = min_x + width / 2
        y_center = min_y + height / 2

        converted_annotations.append({
            "class": class_id,
            "x_center": x_center,
            "y_center": y_center,
            "width": width,
            "height": height,
        })

    return converted_annotations


def write_to_yolo_txt(data, output_file_path):
    """
    Write YOLO bounding box annotations to a .txt file.

    Args:
        data (list[dict]): YOLO annotations
        output_file_path (str): Output file path
    """

    with open(output_file_path, "w") as file:
        for item in data:
            line = (
                f"{item['class']} "
                f"{item['x_center']} "
                f"{item['y_center']} "
                f"{item['width']} "
                f"{item['height']}\n"
            )
            file.write(line)


def convert_all_txt_files(input_folder, output_folder):
    """
    Convert all polygon annotation files in a folder to YOLO format.

    Args:
        input_folder (str): Folder containing polygon .txt files
        output_folder (str): Output folder for YOLO annotations
    """

    os.makedirs(output_folder, exist_ok=True)

    txt_files = [f for f in os.listdir(input_folder) if f.endswith(".txt")]

    for txt_file in txt_files:
        input_path = os.path.join(input_folder, txt_file)
        output_path = os.path.join(output_folder, txt_file)

        yolo_data = convert_to_yolo(input_path)
        write_to_yolo_txt(yolo_data, output_path)


# ===============================
# EXAMPLE USAGE
# ===============================
if __name__ == "__main__":
    INPUT_FOLDER = "data"
    OUTPUT_FOLDER = "converter"

    convert_all_txt_files(INPUT_FOLDER, OUTPUT_FOLDER)
