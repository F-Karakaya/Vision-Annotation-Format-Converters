# Vision Annotation Format Converters
### A Unified Toolkit for Detection & Segmentation Annotation Transformation

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Computer Vision](https://img.shields.io/badge/Domain-Computer%20Vision-green.svg)
![YOLO](https://img.shields.io/badge/Format-YOLO-red.svg)
![COCO](https://img.shields.io/badge/Format-COCO-orange.svg)
![Segmentation](https://img.shields.io/badge/Task-Segmentation-purple.svg)

---

## 📌 Project Overview

**Vision Annotation Format Converters** is a modular and extensible toolkit designed to
**convert, normalize, and validate computer vision annotation formats** commonly used
in **object detection** and **segmentation** pipelines.

The repository addresses one of the most common and time-consuming problems in
computer vision workflows:

> *“My dataset annotations are in the wrong format for the model I want to train.”*

This project provides **reliable, visual, and production-ready solutions** to bridge
annotation formats such as **YOLO**, **COCO**, **polygon-based annotations**, and
**segmentation masks** — without relying on heavy deep learning frameworks.

---

## 🎯 Core Objectives

The main goals of this repository are:

- Standardize dataset annotations across **YOLO** and **COCO**
- Convert **segmentation masks and polygons** into YOLO-compatible formats
- Preserve class consistency and geometric correctness
- Enable **visual verification** of converted annotations
- Support both **research** and **industrial dataset pipelines**

---

## 🧩 Supported Conversion Modules

This repository consists of **four independent but complementary modules**:

### 1️⃣ COCO → YOLO (Detection)

Converts **COCO JSON detection annotations** into **YOLO `.txt` files**  
with normalized bounding boxes.

Use case:
- Training YOLOv5 / YOLOv8 on COCO-annotated datasets
- Migrating datasets between frameworks

📂 Module:
COCO-to-Yolo-format

---

### 2️⃣ YOLO → COCO (Detection & Optional Segmentation)

Converts **YOLO detection annotations** into **fully COCO-compliant JSON files**.

Supports:
- Detection datasets
- Optional box-to-segmentation polygon generation
- Training and inference result formats

📂 Module:
Yolo-to-COCO-format

---

### 3️⃣ Polygon → Rectangle (Detection)

Transforms **polygon-based annotations** into **axis-aligned bounding boxes**
compatible with YOLO detection models.

Includes:
- Tight bounding box extraction
- Pixel-based noise filtering
- Visual inspection tools

📂 Module:
Polygon-to-Rectangle-format

---

### 4️⃣ Segmentation Mask → YOLO Polygon (Segmentation)

Converts **color-coded segmentation masks** into **YOLOv8 polygon annotations**.

Features:
- RGB-based class extraction
- Contour-to-polygon conversion
- Fully YOLOv8-compatible segmentation output

📂 Module:
Seg-to-Yolo-format

---

## 🧠 Detection vs Segmentation — What’s Covered?

This repository explicitly supports **both major annotation paradigms**:

### 🟩 Object Detection
- Bounding boxes
- YOLO detection format
- COCO detection format
- Rectangle-based annotations

### 🟦 Segmentation
- Polygon annotations
- RGB segmentation masks
- YOLOv8 segmentation format
- Pixel-accurate contour extraction

This makes the toolkit suitable for **hybrid datasets** that mix detection and
segmentation tasks.

---

## 🖼️ Example Outputs (Visual Verification)

Visual inspection is a **first-class citizen** in this project.

### 🔴 YOLO Bounding Box Visualization (from COCO → YOLO)

![YOLO Bounding Box Visualization](COCO-to-Yolo-format/output/image_visualized_with_bboxes.jpg)

This image demonstrates:
- Correct COCO → YOLO bounding box conversion
- Proper normalization and placement
- Class-aware rectangle rendering

---

### 🟣 YOLO Segmentation Polygon Visualization (from Mask → YOLO)

![YOLO Segmentation Visualization](Seg-to-Yolo-format/data/visualizer_data/image_visualized_with_polygons.jpg)

This image demonstrates:
- Accurate segmentation mask conversion
- Polygon extraction from contours
- YOLOv8-compatible segmentation output

---

## 🧪 Why Visualization Matters

Annotation conversion without visualization is **risky**.

This repository ensures:
- Geometry correctness
- Class consistency
- Early detection of annotation bugs
- High confidence before model training

Every conversion module includes or supports **visual sanity checks**.

---

## ⚙️ Design Philosophy

- Minimal dependencies
- Deterministic conversions
- Readable and maintainable code
- Modular structure
- Dataset-first mindset
- No framework lock-in

---

## 📌 Typical Use Cases

- Dataset migration between YOLO and COCO
- Preparing industrial inspection datasets
- Converting segmentation masks to train YOLOv8-Seg
- Cleaning and validating noisy annotations
- Academic research and benchmarking
- Automated dataset pipelines

---

## 👤 Author

**Furkan Karakaya**  
AI & Computer Vision Engineer  
📧 se.furkankarakaya@gmail.com  

---

⭐ If this toolkit helps your workflow, feel free to star the repository or contribute improvements.
