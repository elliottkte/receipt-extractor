import pandas as pd
import os

def export_to_excel(data, output_path="output/receipt_summary.xlsx"):
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_excel(output_path, index=False)
    return output_path