from scripts.patched_utils import log_success, log_error, log_warning, safe_write, safe_to_csv, deduplicate_offers, parse_date_safe, limit_offers, safe_run
import pandas as pd
import os
import re
from datetime import datetime

def extract_image(summary):
    if not summary:
        return ""
    urls = re.findall(r'(https?://\S+\.(?:jpg|jpeg|png|webp))', summary)
    return urls[0] if urls else ""

def main():
    today = datetime.utcnow().date()
    csv_path = os.path.join("data", "processed", f"jobs_clean_{today}.csv")
    if not os.path.exists(csv_path):
        log_error("Aucun fichier d'offres à traiter.")
        return
    df = pd.read_csv(csv_path)
    df['image_url'] = df['summary'].apply(extract_image)
    out_path = os.path.join("outputs", f"jobs_with_images_{today}.csv")
    safe_to_csv(df, out_path)
    log_success(f"Export enrichi avec images : {out_path}")

if __name__ == "__main__":
    safe_run(main)
