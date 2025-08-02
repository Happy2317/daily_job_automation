from scripts.patched_utils import log_success, log_error, log_warning, safe_write, safe_to_csv, deduplicate_offers, parse_date_safe, limit_offers, safe_run
import pandas as pd
import os
from datetime import datetime

def main():
    today = datetime.utcnow().date()
    files = [
        f"data/raw/jobs_rss_{today}.csv",
        f"data/raw/jobs_scraping_{today}.csv"
    ]
    dfs = []
    for file in files:
        if os.path.exists(file):
            dfs.append(pd.read_csv(file))
            log_success(f"Fichier trouvé et chargé : {file}")
        else:
            log_warning(f"Fichier non trouvé : {file}")
    if not dfs:
        log_error("Aucun fichier à agréger.")
        return
    df = pd.concat(dfs, ignore_index=True)
    df = df.drop_duplicates(subset=["title", "link", "site"])
    out_path = f"data/processed/jobs_clean_{today}.csv"
    safe_to_csv(df, out_path)
    log_success(f"{len(df)} offres agrégées et nettoyées dans {out_path}")

if __name__ == "__main__":
    safe_run(main)
