from scripts.patched_utils import log_success, log_error, log_warning, safe_write, safe_to_csv, deduplicate_offers, parse_date_safe, limit_offers, safe_run
import yaml
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime, timedelta
import random
import time
import json

CONFIG_PATH = os.path.join('config', 'scraping_rules.yaml')
RAW_DATA_DIR = os.path.join('data', 'raw')

# User-Agent pool for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0",
    # Ajoute d'autres user-agents si besoin
]

def load_scraping_rules(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config.get('sites', [])

def fetch_and_parse(site):
    url = site['url']
    headers = {
        'User-Agent': random.choice(USER_AGENTS)
    }
    print(f"Scraping {url} ...")
    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        offers = []
        for job in soup.select(site['selectors']['job']):
            title = job.select_one(site['selectors'].get('title', ''))
            link = job.select_one(site['selectors'].get('link', ''))
            location = job.select_one(site['selectors'].get('location', ''))
            date = job.select_one(site['selectors'].get('date', ''))
            summary = job.select_one(site['selectors'].get('summary', ''))
            offer = {
                'title': title.get_text(strip=True) if title else '',
                'link': link['href'] if link and link.has_attr('href') else '',
                'location': location.get_text(strip=True) if location else '',
                'date': date.get_text(strip=True) if date else '',
                'summary': summary.get_text(strip=True) if summary else '',
                'site': site['name']
            }
            # Garde uniquement les offres publiées aujourd'hui ou hier si possible
            if offer['date']:
                today = datetime.utcnow().date()
                yesterday = today - timedelta(days=1)
                try:
                    # Essaye de parser la date selon le format attendu (ex: "2025-08-01")
                    offer_date = datetime.strptime(offer['date'], site['selectors'].get('date_format', '%Y-%m-%d')).date()
                    if offer_date not in (today, yesterday):
                        continue
                except Exception:
                    pass
            offers.append(offer)
        return offers
    except Exception as e:
        print(f"Erreur sur {url}: {e}")
        return []

def main():
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    sites = load_scraping_rules(CONFIG_PATH)
    all_offers = []
    for site in sites:
        offers = fetch_and_parse(site)
        all_offers.extend(offers)
        time.sleep(random.uniform(2, 5))  # Anti-bot: pause entre chaque site
    out_path = os.path.join(RAW_DATA_DIR, f"scraped_jobs_{datetime.utcnow().date()}.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(all_offers, f, ensure_ascii=False, indent=2)
    print(f"Scraping terminé, {len(all_offers)} offres collectées. Sauvegardé dans {out_path}")

if __name__ == "__main__":
    main()
