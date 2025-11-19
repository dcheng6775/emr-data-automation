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

    age_str = results.get("Age", "NOT FOUND")
    if age_str != "NOT FOUND":
        try:
            age = int(age_str)
            results["Age_65_74"] = "Y" if 65 <= age <= 74 else "N"
            results["Age_75_plus"] = "Y" if age >= 75 else "N"
        except ValueError:
            results["Age_65_74"] = "N"
            results["Age_75_plus"] = "N"
    else:
        results["Age_65_74"] = "N"
        results["Age_75_plus"] = "N"

    sex = results.get("Sex", "").upper()
    results["Female"] = "Y" if sex == "F" else "N"

    ht_str = results.get("Ht", "NOT FOUND")
    wt_str = results.get("Wt", "NOT FOUND")
    try:
        height_cm = float(ht_str)
        weight_kg = float(wt_str)
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        results["BMI"] = round(bmi, 1)
    except (ValueError, TypeError):
        results["BMI"] = "NOT FOUND"
        
    return results

