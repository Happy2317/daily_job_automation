import os
import logging
import sys
from datetime import datetime

# --- Logging centralisé ---
LOGS_DIR = os.path.join('outputs', 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)
today = datetime.utcnow().date()
log_path = os.path.join(LOGS_DIR, f'process_{today}.log')

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_success(msg): logging.info(msg); print(f"[OK] {msg}")
def log_error(msg): logging.error(msg); print(f"[ERROR] {msg}", file=sys.stderr)
def log_warning(msg): logging.warning(msg); print(f"[WARN] {msg}")

# --- Sauvegarde sécurisée ---
def safe_write(path, content, mode='w', encoding='utf-8'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode, encoding=encoding) as f:
        f.write(content)

def safe_to_csv(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False, encoding='utf-8')

# --- Dédoublonnage robuste ---
def deduplicate_offers(offers):
    seen = set()
    unique = []
    for o in offers:
        key = (o.get('title','').lower(), o.get('location','').lower(), o.get('site','').lower(), o.get('link','').lower())
        if key not in seen: seen.add(key); unique.append(o)
    return unique

# --- Parsing date tolérant ---
def parse_date_safe(date_str, fmt='%Y-%m-%d'):
    from datetime import datetime
    try: return datetime.strptime(date_str, fmt).date()
    except Exception: return None

# --- Limiter le nombre d'offres ---
def limit_offers(offers, max_offers=100):
    return offers[:max_offers]

# --- Gestion interruption propre ---
def safe_run(main_func):
    try: main_func()
    except KeyboardInterrupt: log_warning("Arrêt manuel du script (Ctrl+C)")
    except Exception as e: log_error(f"Erreur inattendue : {e}")
