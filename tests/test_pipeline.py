import sys, unittest, tempfile, json
from pathlib import Path
from datetime import datetime,timezone,timedelta
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import collect,build
NOW=datetime(2026,10,10,tzinfo=timezone.utc)
def sale(**kw):
    return dict(dict(gameID='1',storeID='1',title='Test',salePrice='2',normalPrice='10',isOnSale='1',dealID='a&b'),**kw)
def free(**kw):
    return dict(dict(id=1,title='Game',type='Game',status='Active',platforms='PC',end_date='N/A',gamerpower_url='https://www.gamerpower.com/test'),**kw)
class Pipeline(unittest.TestCase):
    def test_discount(self):
        self.assertEqual(collect.normalize('cheapshark',[sale()],NOW)[0]['discount'],80)
    def test_low_discount_excluded(self):self.assertEqual(collect.normalize('cheapshark',[sale(salePrice='8')],NOW),[])
    def test_zero_excluded(self):self.assertEqual(collect.normalize('cheapshark',[sale(salePrice='0')],NOW),[])
    def test_not_on_sale(self):self.assertEqual(collect.normalize('cheapshark',[sale(isOnSale='0')],NOW),[])
    def test_dedup_best_price(self):
        rows=collect.normalize('cheapshark',[sale(),sale(salePrice='1')],NOW)
        self.assertEqual(len(rows),1);self.assertEqual(rows[0]['price'],'1')
    def test_redirect_encoding(self):self.assertIn('a%26b',collect.normalize('cheapshark',[sale()],NOW)[0]['url'])
    def test_preencoded_redirect(self):self.assertTrue(collect.normalize('cheapshark',[sale(dealID='a%2Fb%3D')],NOW)[0]['url'].endswith('a%2Fb%3D'))
    def test_free_and_ttl(self):self.assertEqual(collect.normalize('gamerpower',[free()],NOW)[0]['valid_until'],(NOW+timedelta(hours=12)).isoformat())
    def test_loot_excluded(self):self.assertEqual(collect.normalize('gamerpower',[free(type='Loot')],NOW),[])
    def test_expired_excluded(self):self.assertEqual(collect.normalize('gamerpower',[free(end_date='2026-10-08 10:00:00')],NOW),[])
    def test_unknown_expiry(self):self.assertIsNone(collect.normalize('gamerpower',[free()],NOW)[0]['expiration'])
    def test_untrusted_url(self):
        with self.assertRaises(ValueError):collect.normalize('gamerpower',[free(gamerpower_url='javascript:alert(1)')],NOW)
    def test_bad_contract(self):
        with self.assertRaises(ValueError):collect.normalize('cheapshark',{'error':True},NOW)
    def test_escape(self):self.assertEqual(build.esc('<script>'), '&lt;script&gt;')
    def test_failure_no_stale(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as t:
            root=Path(t);(root/'data').mkdir()
            (root/'data/offers.json').write_text('{"offers":[{"title":"old"}]}')
            with patch.object(collect,'ROOT',root),patch.object(collect,'fetch',side_effect=OSError('offline')):
                self.assertEqual(collect.collect(),1)
            self.assertEqual(json.loads((root/'data/offers.json').read_text())['offers'],[])
if __name__=='__main__':unittest.main()
