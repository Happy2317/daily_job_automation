from scripts.patched_utils import log_success, log_error, log_warning, safe_write, safe_to_csv, deduplicate_offers, parse_date_safe, limit_offers, safe_run
import pandas as pd
import os
from datetime import datetime
from jinja2 import Template

PROCESSED_DATA_DIR = os.path.join('data', 'processed')
OUTPUT_DIR = os.path.join('outputs')
TEMPLATE_PATH = os.path.join('templates', 'script_video.txt')

def load_jobs():
    today = datetime.utcnow().date()
    csv_path = os.path.join(PROCESSED_DATA_DIR, f"jobs_clean_{today}.csv")
    return pd.read_csv(csv_path)

def load_template():
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        return Template(f.read())

def render_offer(offer, template):
    return template.render(
        poste=offer.get('title', ''),
        ville=offer.get('location', '').split(',')[0].strip() if offer.get('location', '') else '',
        province=offer.get('location', '').split(',')[-1].strip() if offer.get('location', '') else '',
        entreprise=offer.get('site', ''),
        contrat="À préciser",  # À enrichir si dispo
        salaire="À préciser",  # À enrichir si dispo
        date_limite=offer.get('date', ''),
        eimt="À vérifier",     # À enrichir si dispo
        logement="À vérifier", # À enrichir si dispo
        profil="Étrangers francophones (avec/sans diplôme)",
        lien=offer.get('link', ''),
        image="À imaginer selon le poste",  # Optionnel
        resume=offer.get('summary', '')[:200]  # Résumé court
    )

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    jobs = load_jobs()
    template = load_template()
    scripts = []
    for _, offer in jobs.iterrows():
        txt = render_offer(offer, template)
        scripts.append(txt)
    out_path = os.path.join(OUTPUT_DIR, "video_script.txt")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n\n---\n\n'.join(scripts))
    print(f"{len(scripts)} scripts vidéos générés dans {out_path}")

if __name__ == "__main__":
    main()
