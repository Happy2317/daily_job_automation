from scripts.patched_utils import log_success, log_error, log_warning, safe_write, safe_to_csv, deduplicate_offers, parse_date_safe, limit_offers, safe_run
import feedparser
import pandas as pd
from datetime import datetime

def main():
    feed_url = "https://exemple.com/rss"
    log_success(f"Lecture du flux RSS : {feed_url}")
    try:
        feed = feedparser.parse(feed_url)
        offers = []
        for entry in feed.entries:
            offers.append({
                'title': entry.title,
                'link': entry.link,
                'date': entry.get('published', ''),
                'summary': entry.get('summary', ''),
                'site': feed_url
            })
        offers = deduplicate_offers(offers)
        df = pd.DataFrame(offers)
        today = datetime.utcnow().date()
        out_path = f"data/raw/jobs_rss_{today}.csv"
        safe_to_csv(df, out_path)
        log_success(f"{len(df)} offres sauvegardées dans {out_path}")
    except Exception as e:
        log_error(f"Echec récupération RSS: {e}")

if __name__ == "__main__":
    safe_run(main)
