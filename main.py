import os
from app.ocr import process_receipt
from app.parser import parse_receipt_text
from app.exporter import export_to_excel
from app.utils import get_image_files

RECEIPT_FOLDER = "receipts"
OUTPUT_FILE = "output/receipt_summary.xlsx"

def main():
    files = get_image_files(RECEIPT_FOLDER)
    data = []

    for file in files:
        file_path = os.path.join(RECEIPT_FOLDER, file)
        text = process_receipt(file_path)
        parsed = parse_receipt_text(text)
        parsed["Filename"] = file
        data.append(parsed)

    output_path = export_to_excel(data, OUTPUT_FILE)
    print(f"✅ Exported receipt summary to: {output_path}")

if __name__ == "__main__":
    main()