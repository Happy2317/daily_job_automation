from scripts.patched_utils import log_success, log_error, log_warning, safe_write, safe_to_csv, deduplicate_offers, parse_date_safe, limit_offers, safe_run
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def main():
    url = "https://exemple.com/jobs"
    log_success(f"Scraping : {url}")
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        offers = []
        for job in soup.select(".job-offer"):
            offers.append({
                'title': job.select_one(".title").text.strip(),
                'link': job.select_one("a")["href"],
                'date': job.select_one(".date").text.strip(),
                'location': job.select_one(".location").text.strip(),
                'site': url
            })
        offers = deduplicate_offers(offers)
        df = pd.DataFrame(offers)
        today = datetime.utcnow().date()
        out_path = f"data/raw/jobs_scraping_{today}.csv"
        safe_to_csv(df, out_path)
        log_success(f"{len(df)} offres scrapées dans {out_path}")
    except Exception as e:
        log_error(f"Echec scraping : {e}")

if __name__ == "__main__":
    safe_run(main)
