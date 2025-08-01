import yaml
import feedparser
import os
from datetime import datetime, timedelta

CONFIG_PATH = os.path.join('config', 'rss_feeds.yaml')
RAW_DATA_DIR = os.path.join('data', 'raw')
PROCESSED_DATA_DIR = os.path.join('data', 'processed')

def load_rss_sources(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config.get('feeds', [])

def fetch_and_filter_today_entries(feed_url):
    d = feedparser.parse(feed_url)
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    results = []
    for entry in d.entries:
        # Try multiple date fields
        published = getattr(entry, 'published', None) or getattr(entry, 'updated', None)
        if not published:
            continue
        try:
            pubdate = datetime(*entry.published_parsed[:6]).date()
        except Exception:
            continue
        if pubdate in (today, yesterday):
            results.append({
                'title': entry.title,
                'link': entry.link,
                'published': str(pubdate),
                'summary': getattr(entry, 'summary', ''),
                'raw': dict(entry)
            })
    return results

def main():
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    feeds = load_rss_sources(CONFIG_PATH)
    all_entries = []
    for feed in feeds:
        url = feed.get('url')
        if not url:
            continue
        print(f"Fetching {url} ...")
        entries = fetch_and_filter_today_entries(url)
        all_entries.extend(entries)
    # Save raw to JSON
    out_path = os.path.join(RAW_DATA_DIR, f"rss_jobs_{datetime.utcnow().date()}.json")
    import json
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(all_entries, f, ensure_ascii=False, indent=2)
    print(f"Fetched {len(all_entries)} offers from RSS. Saved to {out_path}")

if __name__ == "__main__":
    main()
