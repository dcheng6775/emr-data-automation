import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import re
import os
from patterns import PATTERNS
from io import BytesIO

def extract_pdf_text(uploaded_file):
    pdf_bytes = uploaded_file.read()
    images = convert_from_bytes(pdf_bytes, dpi=700)
    full_text = ""
    for page in images:
        full_text += pytesseract.image_to_string(page) + "\n"
    return full_text

def extract_image_text(uploaded_file):
    img_bytes = uploaded_file.read()
    image = Image.open(BytesIO(img_bytes))
    text = pytesseract.image_to_string(image)
    return text

def extract_text(uploaded_file, file_type=None):
    if file_type is None:
        filename= getattr(uploaded_file, 'filename', '')
        if filename.lower().endswith(".pdf"):
            file_type = "pdf"
        elif filename.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp")):
            file_type = "image"
        else: 
            file_type = "text"
    if file_type == "text":
        text = uploaded_file.read().decode("utf-8")  # or another encoding
        return text
    elif file_type == "pdf":
        return extract_pdf_text(uploaded_file)
    elif file_type == "image":
        return extract_image_text(uploaded_file)

def extract_data(report_text):
    results = {}
    for label, pattern in PATTERNS.items():
        match = re.search(pattern, report_text, re.IGNORECASE | re.DOTALL)
        if match:
            groups = [g for g in match.groups() if g]
            value = groups[0].strip() if groups else "NOT FOUND"
            results[label] = value
        else: 
            results[label] = "NOT FOUND"
    return results

