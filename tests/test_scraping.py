import unittest
import yaml
import requests
from bs4 import BeautifulSoup

class TestScraping(unittest.TestCase):
    def setUp(self):
        with open('config/scraping_rules.yaml', 'r', encoding='utf-8') as f:
            self.sites = yaml.safe_load(f)['sites']

    def test_selectors_exist(self):
        for site in self.sites:
            r = requests.get(site['url'], headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(r.text, 'html.parser')
            jobs = soup.select(site['selectors']['job'])
            self.assertIsInstance(jobs, list, f"Aucun bloc offre trouvé pour {site['name']}")
            if jobs:
                job = jobs[0]
                for key, selector in site['selectors'].items():
                    if key == "job" or key == "date_format":
                        continue
                    self.assertIsNotNone(job.select_one(selector), f"{key} manquant sur {site['name']}")

if __name__ == '__main__':
    unittest.main()
