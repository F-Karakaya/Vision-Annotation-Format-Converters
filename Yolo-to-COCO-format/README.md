# YOLO to COCO Format Converter
### Converting YOLO Detection Annotations into COCO-Compliant Datasets

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![YOLO](https://img.shields.io/badge/Format-YOLO-red.svg)
![COCO](https://img.shields.io/badge/Format-COCO-orange.svg)
![Dataset](https://img.shields.io/badge/Task-Annotation%20Conversion-green.svg)

---

## 📌 Overview

This module provides a **robust and production-ready pipeline** for converting  
**YOLO-format object detection annotations** into the **COCO dataset format**.

It is designed for practitioners who:
- Annotate datasets using YOLO-style `.txt` files
- Want to train or evaluate models that require **COCO JSON annotations**
- Need optional **debug visualization** and **segmentation generation**
- Require support for both **training datasets** and **inference results**

The implementation follows the official COCO specification and is suitable for:
- Research
- Industrial datasets
- Model benchmarking
- Dataset migration pipelines

---

## 🧠 Motivation

YOLO is widely used due to its simplicity and speed, but many modern detection and
segmentation frameworks (e.g. Detectron2, EfficientDet, MMDetection) require
annotations in **COCO format**.

This module bridges that gap by:
- Parsing YOLO annotations
- Converting normalized bounding boxes into pixel-based COCO annotations
- Preserving category consistency
- Generating valid COCO JSON files with minimal dependencies

---

## 🗂️ Directory Structure

```text
Yolo-to-COCO-format/
│
├── main.py
│   (Main entry point: parses YOLO data and generates COCO JSON)
│
├── create_annotations.py
│   (Helper utilities for building COCO image and annotation entries)
│
├── input/
│   ├── dataset/
│   │   ├── example.jpg
│   │   │   (Example input image)
│   │   └── example.txt
│   │       (YOLO annotation file for the image)
│   │
│   ├── dataset.txt
│   │   (List of absolute image paths used as input)
│   │
│   └── obj.names
│       (Class name definitions corresponding to YOLO labels)
│
└── output/
    └── dataset_coco.json
        (Generated COCO-format annotation file)
```

---

## 🧾 Input Annotation Format (YOLO)

YOLO annotations are stored in `.txt` files, one per image.

Each line follows the format:

```text
<class_id> <x_center> <y_center> <width> <height>
```

Where:
- Coordinates are **normalized to [0, 1]**
- `(x_center, y_center)` represent the bounding box center
- `width` and `height` represent box dimensions

### 📥 Example (`example.txt`)

```text
0 0.512 0.487 0.182 0.264
1 0.732 0.401 0.098 0.143
```

---

## 🔄 Conversion Logic

The conversion pipeline performs the following steps:

1. Read image paths from a directory or `dataset.txt`
2. Read image dimensions using lightweight metadata parsing
3. Parse YOLO bounding box annotations
4. Convert normalized coordinates to absolute pixel values
5. Generate COCO-compliant annotation dictionaries
6. Assign unique image and annotation IDs
7. Export the result as a valid COCO `.json` file

---

## 📤 Output Annotation Format (COCO)

The generated COCO file contains three main sections:
- `images`
- `annotations`
- `categories`

### 📤 Example (`dataset_coco.json` – excerpt)

```
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
      "bbox": [820, 385, 350, 285],
      "area": 99750,
      "iscrowd": 0,
      "segmentation": []
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

This output is fully compatible with COCO-based training and evaluation pipelines.

---

## ▶ How to Run

### Default Usage

If no arguments are provided, the script automatically uses:

```text
input/dataset.txt
```

Run:

```text
python main.py
```

---

### Custom Path Usage

You can override the default input:

```text
python main.py --path input/dataset.txt --output dataset_coco.json
```

---

### Debug Mode (Visualization)

To visually inspect bounding boxes and annotation values:

```text
python main.py --path input/dataset.txt --debug
```

This opens images with drawn bounding boxes and prints annotation details to the console.

---

### Optional Arguments

- `--yolo-subdir`  
  Use if annotations are stored in a nested `YOLO_darknet/` directory

- `--box2seg`  
  Generates COCO-style segmentation polygons from bounding boxes

- `--results`  
  Converts YOLO inference results (with confidence scores) into COCO results format

---

## 📦 Requirements

### Python Version
- Python **3.8 or higher**

### Required Packages

```text
pip install numpy opencv-python imagesize
```

No deep learning frameworks are required.

---

## ✅ Key Advantages

- Fully COCO-compliant output
- Supports YOLO training and inference formats
- Minimal dependencies
- Debug visualization support
- Clean and extensible codebase
- Suitable for research and industrial workflows

---

## 📌 Typical Use Cases

- Migrating YOLO datasets to COCO format
- Training COCO-based detection frameworks
- Dataset standardization
- Annotation validation
- Research and benchmarking

---

## 👤 Author

**Furkan Karakaya**  
AI & Computer Vision Engineer  
📧 se.furkankarakaya@gmail.com  

---

⭐ If you find this module useful, feel free to star the repository or contribute improvements.
