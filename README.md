# Invoice & Receipt Extractor

OCR receipt parser that extracts dates and totals from images using Tesseract and regex.

## Features

- OCR (via Tesseract) to extract text from receipt images
- Automatic parsing of vendor, invoice number, date, and total
- Exports results to a structured Excel file
- Simple folder-based input/output system

## Folder Structure

```text
receipt-extractor/
├── app/                # Core logic
├── receipts/           # Drop your .jpg/.png/.pdf receipts here
├── output/             # Excel results will appear here
├── main.py             # Run this file
└── requirements.txt    # Install dependencies
```

## Usage

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/receipt-extractor.git
cd receipt-extractor
```

### 2. Install dependencies
```bash
    pip install -r requirements.txt
```

### 3. Add receipt images
Place your .jpg, .png, or .pdf files in the receipts/ folder.

### 4. Run the script
```bash
python main.py
```
### 5. Check the output
Results will appear in:
```bash
output/receipt_summary.xlsx
```
### Dependencies
Python 3.8+

OpenCV

pytesseract

dateparser

pdf2image

Note: Ensure Tesseract OCR is installed and available in your system path.
