from scripts.patched_utils import log_success, log_error, log_warning, safe_write, safe_to_csv, deduplicate_offers, parse_date_safe, limit_offers, safe_run
import pandas as pd
from jinja2 import Template
import os
from datetime import datetime

def main():
    today = datetime.utcnow().date()
    csv_path = os.path.join("outputs", f"jobs_with_images_{today}.csv")
    if not os.path.exists(csv_path):
        log_error("Aucune offre enrichie à traiter.")
        return
    df = pd.read_csv(csv_path)
    template_path = os.path.join("templates", "video_script.txt")
    if not os.path.exists(template_path):
        log_error("Template vidéo manquant.")
        return
    with open(template_path, "r", encoding="utf-8") as f:
        template = Template(f.read())
    scripts = []
    for _, row in df.iterrows():
        scripts.append(template.render(**row.to_dict()))
    out_path = os.path.join("outputs", f"video_scripts_{today}.txt")
    safe_write(out_path, "\n\n".join(scripts))
    log_success(f"{len(scripts)} scripts vidéo générés dans {out_path}")

if __name__ == "__main__":
    safe_run(main)
