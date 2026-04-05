"""
=============================================================
 CYBR 445 – Module 4: Simple OCR Data Loss Prevention Script
 Author: Tren Patterson | Bellevue University
 Description:
   Extracts text from an image using Tesseract OCR and uses
   regular expressions to detect sensitive data patterns
   including Social Security Numbers and credit card numbers.

 Requirements:
   pip install pytesseract pillow
   sudo apt install tesseract-ocr  (Linux)

 Usage:
   python3 dlp_ocr_script.py
=============================================================
"""

import pytesseract
from PIL import Image
import re

# ── Step 1: Open the image ──────────────────────────────────
img = Image.open('dlp_test.png')

# ── Step 2: Extract text using OCR ─────────────────────────
text = pytesseract.image_to_string(img)

print("=" * 60)
print(" EXTRACTED TEXT (via Tesseract OCR)")
print("=" * 60)
print(text)

# ── Step 3: Detect Social Security Numbers ──────────────────
ssn_pattern = r'\d{3}-\d{2}-\d{4}'
ssn_matches = re.findall(ssn_pattern, text)

print("=" * 60)
print(f" SSNs DETECTED: {len(ssn_matches)} found")
print("=" * 60)
for ssn in ssn_matches:
    print(f"  [SSN] {ssn}")

# ── Step 4: Detect Credit Card Numbers ─────────────────────
cc_pattern = r'\d{4}-{0,1}\d{4}-{0,1}\d{4}-{0,1}\d{4}|\d{14,15}'
cc_matches = re.findall(cc_pattern, text)

print("=" * 60)
print(f" CREDIT CARD NUMBERS DETECTED: {len(cc_matches)} found")
print("=" * 60)
for cc in cc_matches:
    print(f"  [CC] {cc}")

# ── Step 5: Summary ─────────────────────────────────────────
print("=" * 60)
print(" DLP SCAN SUMMARY")
print("=" * 60)
print(f"  Total SSNs found:          {len(ssn_matches)}")
print(f"  Total CC numbers found:    {len(cc_matches)}")
print(f"  Total sensitive items:     {len(ssn_matches) + len(cc_matches)}")
print("=" * 60)
