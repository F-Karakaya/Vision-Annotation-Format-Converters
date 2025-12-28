import cv2


"""
mask_rgb_picker.py

An interactive RGB color picker for segmentation mask images.

- Displays the RGB value of the pixel under the mouse cursor in real time
- Prints the selected RGB value to the console on left mouse click
- Useful for identifying exact color values in color-coded segmentation masks

Controls:
- Move mouse  → show (x, y) and RGB value
- Left click  → print RGB value to console
- ESC         → exit
"""

# Path to the segmentation mask image
IMAGE_PATH = "data/masks/mask.png"

# Load image (OpenCV loads images in BGR format by default)
image_bgr = cv2.imread(IMAGE_PATH)
if image_bgr is None:
    raise FileNotFoundError(f"Image not found: {IMAGE_PATH}")

# Convert to RGB for correct color interpretation
image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

WINDOW_NAME = "Mask RGB Picker"


def mouse_callback(event, x, y, flags, param):
    """
    Mouse callback function for displaying and selecting RGB values.
    """
    if event == cv2.EVENT_MOUSEMOVE:
        r, g, b = image_rgb[y, x]
        display = image_bgr.copy()

        text = f"x: {x}, y: {y} | RGB: ({r}, {g}, {b})"
        cv2.putText(
            display,
            text,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )

        cv2.imshow(WINDOW_NAME, display)

    elif event == cv2.EVENT_LBUTTONDOWN:
        r, g, b = image_rgb[y, x]
        print(f"SELECTED RGB -> ({r}, {g}, {b})")


# Create window and register mouse callback
cv2.namedWindow(WINDOW_NAME)
cv2.setMouseCallback(WINDOW_NAME, mouse_callback)

cv2.imshow(WINDOW_NAME, image_bgr)
cv2.waitKey(0)
cv2.destroyAllWindows()
