import os
import logging
from datetime import datetime

LOGS_DIR = os.path.join('outputs', 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)
today = datetime.utcnow().date()
log_path = os.path.join(LOGS_DIR, f'process_{today}.log')

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_success(message):
    logging.info(message)
    print(f"[OK] {message}")

def log_error(message):
    logging.error(message)
    print(f"[ERROR] {message}")

def log_warning(message):
    logging.warning(message)
    print(f"[WARN] {message}")

# Exemple d'utilisation dans d'autres scripts :
if __name__ == "__main__":
    log_success("Traitement du flux RSS terminé avec succès.")
    log_warning("Un champ facultatif est manquant dans certaines offres.")
    log_error("Impossible de se connecter au site cible pour le scraping.")
