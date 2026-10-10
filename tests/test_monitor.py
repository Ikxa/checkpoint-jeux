import sys, unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from monitor import validate_health
NOW=datetime(2026,10,10,tzinfo=timezone.utc)
def health(hours=0):
    return {'generated_at':(NOW-timedelta(hours=hours)).isoformat(),'sources':{'gamerpower':{'ok':True},'cheapshark':{'ok':True}}}
class Monitor(unittest.TestCase):
    def test_fresh(self):self.assertTrue(validate_health(health(),NOW))
    def test_old(self):
        with self.assertRaises(ValueError):validate_health(health(13),NOW)
    def test_future(self):
        with self.assertRaises(ValueError):validate_health(health(-1),NOW)
    def test_source_failure(self):
        data=health();data['sources']['cheapshark']['ok']=False
        with self.assertRaises(ValueError):validate_health(data,NOW)
    def test_missing_source(self):
        data=health();del data['sources']['cheapshark']
        with self.assertRaises(KeyError):validate_health(data,NOW)
    def test_naive_date(self):
        data=health();data['generated_at']='2026-10-10T00:00:00'
        with self.assertRaises(ValueError):validate_health(data,NOW)
