import sys, unittest, tempfile, json
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build
from translations import english_page

class Languages(unittest.TestCase):
    def test_title_escaping_and_translation(self):
        page='<html lang="fr"><head></head><article><h2>Les offres</h2></article><h2>Les offres</h2><p>Fin : Non précisée</p><p>2 offres</p></html>'
        translated=english_page(page,'')
        self.assertIn('<article><h2>Les offres</h2></article>',translated)
        self.assertIn('<h2>Deals</h2><p>Ends: Not specified</p><p>2 offers</p>',translated)
    def test_build_routes_and_assets(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as tmp:
            root=Path(tmp); (root/'data').mkdir(); (root/'static').mkdir()
            (root/'static/favicon.svg').write_text('<svg/>')
            (root/'config.json').write_text(json.dumps(dict(affiliate_enabled=False,site_url='https://example.com',publisher='Ikxa',contact='Contact')))
            (root/'data/offers.json').write_text(json.dumps(dict(offers=[],sources={'source':{'ok':True}},generated_at='2026-10-10T00:00:00+00:00')))
            with patch.object(build,'ROOT',root): build.build()
            fr=(root/'dist/index.html').read_text(encoding='utf-8'); en=(root/'dist/en/index.html').read_text(encoding='utf-8')
            self.assertIn('lang="en"',en)
            self.assertIn('rel="canonical" href="https://example.com/en/"',en)
            self.assertIn('src="/app.js"',en)
            self.assertIn('href="/favicon.svg"',en)
            self.assertIn('href="/en/" lang="en"',fr)
            self.assertIn('href="/" lang="fr"',en)
            self.assertIn('https://example.com/en/',(root/'dist/sitemap.xml').read_text())
            self.assertTrue((root/'dist/favicon.svg').exists())

if __name__=='__main__': unittest.main()
