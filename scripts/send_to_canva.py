from scripts.patched_utils import log_success, log_error, log_warning, safe_write, safe_to_csv, deduplicate_offers, parse_date_safe, limit_offers, safe_run
import pandas as pd
import os
import json
from datetime import datetime

PROCESSED_DATA_DIR = os.path.join('data', 'processed')
OUTPUT_DIR = os.path.join('outputs')

def load_jobs():
    today = datetime.utcnow().date()
    csv_path = os.path.join(PROCESSED_DATA_DIR, f"jobs_clean_{today}.csv")
    return pd.read_csv(csv_path)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    jobs = load_jobs()
    canva_json = []
    for _, offer in jobs.iterrows():
        block = {
            "poste": offer.get('title', ''),
            "ville": offer.get('location', '').split(',')[0].strip() if offer.get('location', '') else '',
            "province": offer.get('location', '').split(',')[-1].strip() if offer.get('location', '') else '',
            "entreprise": offer.get('site', ''),
            "contrat": "À préciser",
            "salaire": "À préciser",
            "date_limite": offer.get('date', ''),
            "eimt": "À vérifier",
            "logement": "À vérifier",
            "profil": "Étrangers francophones (avec/sans diplôme)",
            "lien": offer.get('link', ''),
            "resume": offer.get('summary', '')[:200]
        }
        canva_json.append(block)
    out_path = os.path.join(OUTPUT_DIR, "canva_blocks.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(canva_json, f, ensure_ascii=False, indent=2)
    print(f"Fichier exporté pour Canva/Make : {out_path}")

if __name__ == "__main__":
    safe_run(main)
