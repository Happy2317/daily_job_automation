from scripts.patched_utils import log_success, log_error, log_warning, safe_write, safe_to_csv, deduplicate_offers, parse_date_safe, limit_offers, safe_run
import pandas as pd
import os
from datetime import datetime

def main():
    today = datetime.utcnow().date()
    csv_path = os.path.join("outputs", f"jobs_with_images_{today}.csv")
    if not os.path.exists(csv_path):
        log_error("Aucune offre enrichie à exporter.")
        return
    df = pd.read_csv(csv_path)
    out_path = os.path.join("outputs", f"canva_jobs_{today}.csv")
    safe_to_csv(df, out_path)
    log_success(f"Export Canva prêt : {out_path}")

if __name__ == "__main__":
    safe_run(main)
