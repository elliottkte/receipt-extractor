import re
import dateparser

def parse_receipt_text(text):
    lines = text.split('\n')
    result = {
        "Date": "",
        "Total": "",
        "Amounts Used": [],
        "Extracted Text": text.strip()
    }

    date_pattern = re.compile(r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2}|\d{1,2} \w+ \d{4})\b', re.IGNORECASE)
    money_pattern = re.compile(r'[$£€]?\s?[\d,]+\.\d{2}')
    fallback_number_pattern = re.compile(r'\b\d{3,5}\b')  # e.g. "511" instead of "5.11"
    total_keywords = ['total', 'amount due', 'net total', 'grand total', 'purchase total', 'balance due', 'subtotal']

    total_found = False
    all_amounts = []

    for line in lines:
        clean_line = line.strip().lower()

        # Date extraction
        if not result["Date"]:
            date_match = date_pattern.search(line)
            if date_match:
                parsed_date = dateparser.parse(date_match.group())
                if parsed_date:
                    result["Date"] = parsed_date.strftime('%Y-%m-%d')

        # Total detection (look for keywords, try to find real or OCR-failed amount)
        if not total_found and any(keyword in clean_line for keyword in total_keywords):
            money_match = money_pattern.search(line)
            if money_match:
                result["Total"] = money_match.group().replace(' ', '')
                total_found = True
            else:
                # Attempt OCR correction: e.g. "511" => "5.11"
                fallback_match = fallback_number_pattern.search(line)
                if fallback_match:
                    raw = fallback_match.group()
                    if len(raw) >= 3:
                        corrected = float(raw) / 100
                        result["Total"] = f"£{corrected:.2f}"
                        total_found = True

        # Collect all potential monetary values
        for m in money_pattern.finditer(line):
            amount_text = m.group().replace('£', '').replace('$', '').replace('€', '').replace(',', '').strip()
            try:
                amount = float(amount_text)
                all_amounts.append(amount)
            except ValueError:
                continue

    # Fallback: use last realistic value if no total line found
    if not result["Total"] and all_amounts:
        sensible_amounts = [amt for amt in all_amounts if 0.3 < amt < 500]
        if sensible_amounts:
            last_amount = sensible_amounts[-1]
            result["Total"] = f"£{last_amount:.2f}"
            result["Amounts Used"] = [last_amount]

    return result
