from scripts.patched_utils import log_success, log_error, log_warning, safe_write, safe_to_csv, deduplicate_offers, parse_date_safe, limit_offers, safe_run
import json
import os
import pandas as pd
from datetime import datetime

RAW_DATA_DIR = os.path.join('data', 'raw')
PROCESSED_DATA_DIR = os.path.join('data', 'processed')
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

def load_json(filename):
    path = os.path.join(RAW_DATA_DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def normalize_rss_entries(entries):
    # RSS extraction standardisation
    norm = []
    for e in entries:
        norm.append({
            'title': e.get('title', ''),
            'link': e.get('link', ''),
            'location': e.get('raw', {}).get('location', '') or e.get('summary', ''),
            'date': e.get('published', ''),
            'site': e.get('raw', {}).get('site', ''),
            'summary': e.get('summary', ''),
        })
    return norm

def normalize_scraped_entries(entries):
    # Scraping extraction standardisation
    norm = []
    for e in entries:
        norm.append({
            'title': e.get('title', ''),
            'link': e.get('link', ''),
            'location': e.get('location', ''),
            'date': e.get('date', ''),
            'site': e.get('site', ''),
            'summary': e.get('summary', ''),
        })
    return norm

def deduplicate(offers):
    seen = set()
    unique = []
    for offer in offers:
        key = (offer['title'].lower(), offer['location'].lower(), offer['site'])
        if key not in seen:
            seen.add(key)
            unique.append(offer)
    return unique

def main():
    today = datetime.utcnow().date()
    rss_file = f"rss_jobs_{today}.json"
    scraping_file = f"scraped_jobs_{today}.json"
    offers = []

    # Charger RSS
    if os.path.exists(os.path.join(RAW_DATA_DIR, rss_file)):
        rss_entries = load_json(rss_file)
        offers.extend(normalize_rss_entries(rss_entries))
    # Charger Scraping
    if os.path.exists(os.path.join(RAW_DATA_DIR, scraping_file)):
        scraping_entries = load_json(scraping_file)
        offers.extend(normalize_scraped_entries(scraping_entries))

    # Dédoublonnage
    offers = deduplicate(offers)
    print(f"{len(offers)} offres uniques après fusion et dédoublonnage.")

    # Sauvegarde CSV
    df = pd.DataFrame(offers)
    out_path = os.path.join(PROCESSED_DATA_DIR, f"jobs_clean_{today}.csv")
    df.to_csv(out_path, index=False, encoding='utf-8')
    print(f"Fichier final nettoyé : {out_path}")

if __name__ == "__main__":
    main()
