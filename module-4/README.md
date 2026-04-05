# Module 4 – Data Loss Prevention (DLP)
### CYBR 445 | Bellevue University

---

## 🎯 Lab Objectives

- Understand the core technologies behind DLP systems
- Use **Regular Expressions (RegEx)** to detect sensitive data patterns
- Apply the **Luhn Algorithm** to validate credit card numbers
- Use **Google Cloud DLP** and **Google Vision API** demos
- Build a **Python OCR script** to extract and detect sensitive data from images

---

## 🧠 Key Concepts Learned

### 1. Regular Expressions for Sensitive Data Detection
RegEx is the core pattern-matching engine behind most DLP systems. It allows automated detection of structured sensitive data like SSNs, credit card numbers, emails, and dates of birth.

**Named capture group regex used:**
```
(?<name>^\w+\s+\w+)\s+(?<ssn>\d{3}-+\d{2}-+\d{4})\s+(?<ccnumber>\d{4}-{0,1}\d{4}-{0,1}\d{4}-{0,1}\d{4}|\d{14,15})
```

**Custom regex written (Name + Date of Birth):**
```
(?<name>^\w+\s+\w+)\s+(?<dob>\d{1,2}\/\d{1,2}\/\d{4})
```

### 2. Luhn Algorithm
The Luhn Algorithm is a checksum validation method used to verify credit card numbers. DLP systems combine RegEx detection with Luhn validation to reduce false positives.

- Fake number `1111-2222-3333-4444` → ❌ FAILS Luhn check
- Generated VISA number → ✅ PASSES Luhn check

### 3. Google Cloud DLP Demo
Enterprise DLP systems use machine learning in addition to RegEx to detect unstructured sensitive data like names and addresses. The Google Cloud DLP API detected:
- PHONE_NUMBER
- EMAIL_ADDRESS
- CREDIT_CARD_NUMBER
- MEDICAL_DATA
- US_HEALTHCARE_NPI
- DRIVERS_LICENSE_NUMBER
- GOVERNMENT_ID (SSNs)

### 4. OCR + DLP Pipeline
Sensitive data can be hidden in images, screenshots, and scanned documents. By chaining **OCR (Tesseract)** with **RegEx**, we can extract and detect sensitive data from image files — a critical capability for modern DLP systems.

---

## 🐍 Python OCR DLP Script

See the full script in [`scripts/dlp_ocr_script.py`](./scripts/dlp_ocr_script.py)

### How it works:
```
Image File → Tesseract OCR → Plain Text → RegEx → Sensitive Data Found
```

### Command line version:
```bash
tesseract dlp_test.png stdout -l eng | grep -oP '\d{3}-\d{2}-\d{4}'
```

### Python version:
```python
import pytesseract
from PIL import Image
import re

img = Image.open('dlp_test.png')
text = pytesseract.image_to_string(img)
pattern = '\d{3}-\d{2}-\d{4}'
matches = re.findall(pattern, text)
print(matches)
```

**Output:** A Python list of every SSN detected in the image file.

---

## 🏗️ DLP System Architecture

A typical enterprise DLP system includes:

| Component | Function |
|-----------|----------|
| DLP Management Server | Central policy management and reporting |
| DLP Network Agent | Monitors network traffic via tap |
| DLP Mail Agent | Inspects outbound email |
| DLP Web Agent | Monitors web proxy traffic |
| DLP Storage Agent | Scans file shares, databases, S3 buckets |
| DLP Endpoint Agent | Monitors USB, clipboard, local file activity |

---

## 🔑 Key Takeaways

1. **RegEx alone is not enough** — names and addresses require ML-based detection
2. **Luhn validation** significantly reduces false positives in CC detection
3. **OCR bridges the gap** between image-based data and text-based DLP inspection
4. **Layered detection** (RegEx + ML + Luhn + OCR) is how real enterprise DLP works
5. **Always use fake test data** — real DLP systems monitor outbound traffic and could capture real sensitive data used in testing

---

## 🛠️ Tools Used

- [regex101.com](https://regex101.com) — RegEx testing
- [dlptest.com](https://dlptest.com/sample-data/) — Sample sensitive data
- [dcode.fr/luhn-algorithm](https://www.dcode.fr/luhn-algorithm) — Luhn validation
- [vccgenerator.org](https://vccgenerator.org) — Valid test CC generation
- [Google Cloud DLP Demo](https://cloud.google.com/dlp/demo/#!/) — Enterprise DLP
- [Google Vision API](https://cloud.google.com/vision/docs/drag-and-drop) — OCR demo
- Python 3, Tesseract, pytesseract, Pillow (PIL)

---

## 📚 References

- CrowdStrike. (2022). *What is data loss prevention (DLP)?* https://www.crowdstrike.com/cybersecurity-101/data-loss-prevention-dlp/
- Devlin, B. (2015). *Data loss protection.* GIAC/SANS Institute.
