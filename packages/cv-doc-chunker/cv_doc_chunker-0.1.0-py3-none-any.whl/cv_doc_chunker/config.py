"""
Configuration settings for the PDF parser.

This module loads configuration from environment variables or default values.
"""

import os
import logging
from pathlib import Path
# from dotenv import load_dotenv

# load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = os.getenv("MODEL_DIR", os.path.join(BASE_DIR, "models"))
OUTPUT_DIR = os.getenv("OUTPUT_DIR", os.path.join(BASE_DIR, "output"))
DEBUG_DIR = os.getenv("DEBUG_DIR", os.path.join(OUTPUT_DIR, "debug"))
TEMP_DIR = os.getenv("TEMP_DIR", os.path.join(BASE_DIR, "temp"))

# Ensure directories exist
os.makedirs(MODEL_DIR, exist_ok = True)
os.makedirs(OUTPUT_DIR, exist_ok = True)
os.makedirs(TEMP_DIR, exist_ok = True)

# Model paths
YOLO_MODEL_PATH = os.path.join(MODEL_DIR, "doclayout_yolo_docstructbench_imgsz1024.pt")

# Image Processing Settings
ZOOM_FACTOR = float(os.getenv("ZOOM_FACTOR", "2.0"))
IOU_THRESHOLD = float(os.getenv("IOU_THRESHOLD", "0.45"))
CONTAINMENT_THRESHOLD = float(os.getenv("CONTAINMENT_THRESHOLD", "0.90"))

# Box Processing Settings
AUTOMATIC_ROW_DETECTION = os.getenv("AUTOMATIC_ROW_DETECTION", "True").lower() in ("true", "1", "yes")
ROW_SIMILARITY_THRESHOLD = int(os.getenv("ROW_SIMILARITY_THRESHOLD", "10"))
CONTAINER_THRESHOLD = int(os.getenv("CONTAINER_THRESHOLD", "2"))

# Memory Management Settings
MEMORY_EFFICIENT = os.getenv("MEMORY_EFFICIENT", "True").lower() in ("true", "1", "yes")
PAGE_BATCH_SIZE = int(os.getenv("PAGE_BATCH_SIZE", "1"))
ENABLE_GC = os.getenv("ENABLE_GC", "True").lower() in ("true", "1", "yes")
CLEAR_CUDA_CACHE = os.getenv("CLEAR_CUDA_CACHE", "True").lower() in ("true", "1", "yes")

# Text label categories (elements that should be preserved during processing)
TEXT_LABELS = ["title", "plain_text"] #"table_caption", "table_footnote", "formula_caption"]

# Debug mode settings
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() in ("true", "1", "yes")
if DEBUG_MODE:
    logging.basicConfig(level = logging.DEBUG)

else:
    logging.basicConfig(level = logging.INFO)