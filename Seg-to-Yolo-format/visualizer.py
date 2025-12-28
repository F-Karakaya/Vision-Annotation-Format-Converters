from PIL import Image, ImageDraw


"""
visualizer.py

Visualizes YOLO segmentation annotations by drawing colored polygons
on the corresponding image.

- Each class is rendered with a distinct color
- Useful for annotation validation and debugging
"""

# class_id -> RGB color mapping for visualization
CLASS_COLORS = {
    0: (255,   0,   0),   # Red
    1: (0,   255, 255),   # Turquoise
    2: (0,     0, 255),   # Blue
    3: (255, 255,   0),   # Yellow
}


def draw_polygons(image_path, txt_path, output_path=None):
    """
    Draw YOLO segmentation polygons on an image.

    Args:
        image_path (str): Path to the original image
        txt_path (str): Path to YOLO segmentation annotation file
        output_path (str, optional): Output image path
    """

    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    with open(txt_path, "r") as file:
        lines = file.readlines()

    for line in lines:
        values = list(map(float, line.split()))
        class_id, *coords = values
        class_id = int(class_id)

        if len(coords) < 4 or len(coords) % 2 != 0:
            continue

        # Convert normalized coordinates to pixel coordinates
        points = [
            (
                int(coords[i] * image.width),
                int(coords[i + 1] * image.height),
            )
            for i in range(0, len(coords), 2)
        ]

        color = CLASS_COLORS.get(class_id, (255, 255, 255))

        draw.polygon(points, outline=color, width=2)

    if output_path:
        image.save(output_path)
    else:
        image.show()


# Example usage
if __name__ == "__main__":
    IMAGE_PATH = "data/images/image.jpg"
    TXT_PATH = "data/txt_data/mask.txt"
    OUTPUT_PATH = "data/visualizer_data/image_visualized_with_polygons.jpg"

    draw_polygons(IMAGE_PATH, TXT_PATH, OUTPUT_PATH)
