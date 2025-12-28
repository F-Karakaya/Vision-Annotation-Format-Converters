# COCO to YOLO Format Converter
### Converting COCO Detection Annotations into YOLO-Compatible Labels

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![COCO](https://img.shields.io/badge/Input-COCO-orange.svg)
![YOLO](https://img.shields.io/badge/Output-YOLO-red.svg)
![Computer Vision](https://img.shields.io/badge/Task-Annotation%20Conversion-green.svg)

---

## 📌 Overview

This module provides a **clean and reliable pipeline** for converting  
**COCO-format detection annotations** into **YOLO-format label files**.

It is specifically designed for workflows where:
- Datasets are annotated or exported in **COCO JSON format**
- Models such as **YOLOv5 / YOLOv8 / YOLO-NAS** are used for training
- Annotation formats need to be migrated or standardized
- Quick visual validation of converted labels is required

The converter strictly follows both **COCO** and **YOLO** annotation specifications.

---

## 🧠 Motivation

COCO is a widely adopted standard for object detection datasets,  
but YOLO-based frameworks require annotations in a **lightweight text-based format**.

This module bridges that gap by:
- Parsing COCO JSON files
- Extracting bounding box annotations
- Normalizing coordinates according to image resolution
- Generating YOLO-compatible `.txt` files
- Providing optional visualization for sanity checks

---

## 🗂️ Directory Structure

```text
COCO-to-Yolo-format/
│
├── converter.py
│   (Main conversion logic: COCO JSON → YOLO TXT)
│
├── visualizer.py
│   (Draws YOLO bounding boxes on images for verification)
│
├── input/
│   ├── img/
│   │   └── example.jpg
│   │       (Input image referenced in COCO annotations)
│   │
│   └── json/
│       └── example.json
│           (COCO-format annotation file)
│
└── output/
    ├── example.txt
    │   (Generated YOLO-format annotation file)
    │
    └── image_visualized_with_bboxes.jpg
        (Visualization of YOLO bounding boxes)
```

---

## 🧾 Input Annotation Format (COCO)

The input annotation file strictly follows the **COCO detection format**  
with the following main sections:

- `images`
- `annotations`
- `categories`

### 📥 Example (`example.json` – simplified)

```text
{
  "images": [
    {
      "id": 0,
      "file_name": "example.jpg",
      "width": 1920,
      "height": 1080
    }
  ],
  "annotations": [
    {
      "id": 1,
      "image_id": 0,
      "category_id": 1,
      "bbox": [1394.0, 708.0, 177.0, 303.0],
      "area": 53631,
      "iscrowd": 0
    }
  ],
  "categories": [
    {
      "id": 1,
      "name": "0",
      "supercategory": "Defect"
    }
  ]
}
```

Where:
- `bbox = [xmin, ymin, width, height]` in **pixel coordinates**
- `category_id` starts from **1** (COCO convention)

---

## 🔄 Conversion Logic

For each image in the COCO JSON:

1. Locate the corresponding image file
2. Read image dimensions (from JSON or image metadata)
3. Extract bounding boxes from `annotations`
4. Convert COCO bbox → YOLO bbox:
   - Pixel coordinates → normalized values
   - Top-left → center-based representation
5. Convert `category_id` → YOLO `class_id`:
   - `class_id = category_id - 1`
6. Write YOLO annotations to a `.txt` file

---

## 📤 Output Annotation Format (YOLO)

Each image produces a `.txt` file with one line per object:

```text
<class_id> <x_center> <y_center> <width> <height>
```

All values are **normalized to [0, 1]**.

### 📤 Example (`example.txt`)

```
0 0.772656 0.795833 0.092188 0.280556
0 0.637500 0.687963 0.062500 0.301852
```

This output is directly compatible with YOLO training pipelines.

---

## 🖼️ Visualization Output

After conversion, YOLO bounding boxes can be visualized using `visualizer.py`.

This helps verify:
- Bounding box correctness
- Class assignments
- Coordinate normalization

### Example Visualization

![YOLO Bounding Box Visualization](output/image_visualized_with_bboxes.jpg)

---

## ▶ How to Run

### Step 1 — Convert COCO to YOLO

```text
python converter.py
```

This will:
- Read COCO JSON files from `input/json/`
- Match images from `input/img/`
- Write YOLO labels to `output/`

---

### Step 2 — Visualize YOLO Annotations

```text
python visualizer.py
```

This will generate:
- `image_visualized_with_bboxes.jpg`

---

## 📦 Requirements

- Python **3.8+**
- OpenCV
- NumPy

Installation:

```text
pip install opencv-python numpy
```

---

## ✅ Key Advantages

- Fully COCO-compliant input parsing
- YOLO-standard output formatting
- Handles multiple objects and classes
- Lightweight and dependency-minimal
- Visualization for immediate validation
- Suitable for research and industrial datasets

---

## 📌 Typical Use Cases

- Converting COCO datasets for YOLO training
- Dataset format migration
- Annotation verification
- Computer vision research pipelines
- Industrial inspection datasets

---

## 👤 Author

**Furkan Karakaya**  
AI & Computer Vision Engineer  
📧 se.furkankarakaya@gmail.com  

---

⭐ If you find this module useful, feel free to star the repository or contribute improvements.
