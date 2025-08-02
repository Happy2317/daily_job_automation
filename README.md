# Daily Job Automation

## Architecture

```
/daily-job-automation/
│
├── /config/               # Flux RSS & règles de scraping
├── /data/                 # Données brutes et nettoyées
├── /scripts/              # Toute l'automatisation
├── /templates/            # Templates vidéo et Canva
├── /outputs/              # Résultats, logs, exports
├── /tests/                # Tests unitaires scraping/RSS
└── README.md
```

## Pipeline

1. **Collecte**  
   - `fetch_rss.py` : Agrège offres via RSS
   - `fetch_scraping.py` : Scrape les sites sans RSS

2. **Fusion & Nettoyage**  
   - `aggregate_jobs.py` : Fusionne, nettoie, dédoublonne

3. **Génération de scripts vidéos**  
   - `generate_script_gpt.py` : Génère le texte prêt à publier (Jinja2)

4. **Export Canva/Make**  
   - `send_to_canva.py` : Prépare JSON/CSV pour Canva, Make, Zapier

5. **Images**  
   - `extract_image_url.py` : Tente d'extraire une image pour chaque offre

6. **Publication & Simulation**  
   - `publish_reels.py` : Simulation ou automatisation de la diffusion

7. **Logs & Monitoring**  
   - `logs_and_monitoring.py` : Centralise et formate les logs

## Configuration

- Ajoute/édite les sources dans `/config/rss_feeds.yaml` et `/config/scraping_rules.yaml`
- Adapte les templates dans `/templates/`

## Tests

- Lancer `python -m unittest tests/test_scraping.py` pour valider les sélecteurs

---

**Ce projet fonctionne sans aucune API propriétaire, uniquement RSS et scraping.**  
Pour toute extension (plus de sources, automatisation publication, etc.), adapte simplement la config ou les scripts concernés.
