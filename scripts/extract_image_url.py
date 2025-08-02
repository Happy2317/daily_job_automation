from scripts.patched_utils import log_success, log_error, log_warning, safe_write, safe_to_csv, deduplicate_offers, parse_date_safe, limit_offers, safe_run
import pandas as pd
import os
import re
from datetime import datetime

PROCESSED_DATA_DIR = os.path.join('data', 'processed')
OUTPUT_DIR = os.path.join('outputs')

def extract_image(summary):
    # Extraction naïve d'URL d'image depuis le résumé (pour Canva ou vignette)
    # Peut être adapté si tu veux crawler l'image de l'entreprise ou du poste
    if not summary:
        return ""
    urls = re.findall(r'(https?://\S+\.(?:jpg|jpeg|png|webp))', summary)
    return urls[0] if urls else ""

def main():
    today = datetime.utcnow().date()
    csv_path = os.path.join(PROCESSED_DATA_DIR, f"jobs_clean_{today}.csv")
    if not os.path.exists(csv_path):
        print("Aucun fichier d'offres à traiter.")
        return
    df = pd.read_csv(csv_path)
    df['image_url'] = df['summary'].apply(extract_image)
    out_path = os.path.join(OUTPUT_DIR, f"jobs_with_images_{today}.csv")
    df.to_csv(out_path, index=False, encoding='utf-8')
    print(f"Export enrichi avec images : {out_path}")

if __name__ == "__main__":
    safe_run(main)
