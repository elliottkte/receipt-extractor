import os
import cv2
import numpy as np
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

def preprocess_image_cv2(img):
    """Preprocess an OpenCV image array for better OCR."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)

    # Adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        blockSize=15,
        C=11
    )

    return thresh


def extract_text(image):
    """Extract text using Tesseract with custom config."""
    custom_config = r'--oem 3 --psm 6'
    return pytesseract.image_to_string(image, config=custom_config)


def process_receipt(image_path):
    """Handle image or PDF, apply OCR with preprocessing."""
    images = []

    if image_path.lower().endswith('.pdf'):
        images = convert_from_path(image_path)
    else:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File not found: {image_path}")
        images = [Image.open(image_path)]

    full_text = ''
    for img in images:
        # Convert to OpenCV format
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # Preprocess and OCR
        preprocessed = preprocess_image_cv2(img_cv)
        full_text += extract_text(preprocessed)

    return full_text