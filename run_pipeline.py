```python
# run_pipeline.py

from scripts.fetch_rss import main as rss
from scripts.fetch_scraping import main as scraping
from scripts.aggregate_jobs import main as aggregate
from scripts.extract_image_url import main as images
from scripts.generate_script_gpt import main as generate
from scripts.send_to_canva import main as export_canva
from scripts.publish_reels import main as publish
from scripts.patched_utils import safe_run, log_success

def run_all():
    log_success("🔁 Lancement de la pipeline Daily Job Automation")
    safe_run(rss)
    safe_run(scraping)
    safe_run(aggregate)
    safe_run(images)
    safe_run(generate)
    safe_run(export_canva)
    safe_run(publish)
    log_success("✅ Pipeline exécutée sans erreur")

if __name__ == "__main__":
    run_all()
```
