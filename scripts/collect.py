"""Authorized API collection. Python standard library only."""
import json, time, sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import quote, unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
UTC = timezone.utc
def stamp(): return datetime.now(UTC).isoformat()
def safe_url(url, hosts):
    p = urlparse(url)
    if p.scheme != 'https' or p.hostname not in hosts or p.username or p.password:
        raise ValueError('URL non autorisée')
    return url
def fetch(url):
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers={'User-Agent':'BonPlanJeux/1.0 (authorized API consumer)'}), timeout=25) as r:
                if r.status == 201: return []
                return json.loads(r.read(4_000_000))
        except HTTPError as e:
            if e.code not in (429,500,502,503,504) or attempt == 2: raise
            time.sleep(min(30, int(e.headers.get('Retry-After','2'))))
        except (TimeoutError, OSError):
            if attempt == 2: raise
            time.sleep(2 ** attempt)
def normalize(source, rows, now):
    if not isinstance(rows,list): raise ValueError('Réponse API inattendue')
    result=[]
    for r in rows:
        try:
            if source == 'gamerpower':
                if r['type'] != 'Game' or r['status'] != 'Active': continue
                # API has naive dates without documented timezone: never invent UTC.
                end=r.get('end_date','N/A')
                if end != 'N/A':
                    date=datetime.strptime(end,'%Y-%m-%d %H:%M:%S')
                    if date.date() < now.date(): continue
                d=dict(id='gp-'+str(r['id']),title=r['title'],kind='free',price=None,regular=None,discount=None,
                       store=r['platforms'],url=safe_url(r['gamerpower_url'],{'www.gamerpower.com','gamerpower.com'}),
                       expiration=None,expiration_label='Non précisée' if end=='N/A' else end+' (fuseau non précisé par la source)',
                       region='Disponibilité en France à confirmer sur la boutique',source='GamerPower')
            else:
                price=Decimal(r['salePrice']); regular=Decimal(r['normalPrice'])
                if r['isOnSale'] != '1' or price<=0 or regular<=price: continue
                cut=int((regular-price)*100/regular)
                if cut < json.loads((ROOT/'config.json').read_text())['minimum_discount']: continue
                d=dict(id='cs-'+str(r['gameID']),title=r['title'],kind='sale',price=str(price),regular=str(regular),discount=cut,
                       store='Boutique '+str(r['storeID']),url='https://www.cheapshark.com/redirect?dealID='+quote(unquote(r['dealID']),safe=''),
                       expiration=None,expiration_label='Non communiquée',region='Prix USD • tarif et activation en France à confirmer',source='CheapShark')
            until=now+timedelta(hours=12)
            if source=='gamerpower' and end!='N/A':
                # Earliest possible instant for an unspecified civil timezone (+14).
                until=min(until,date.replace(tzinfo=UTC)-timedelta(hours=14))
                if until<=now: continue
            d.update(checked_at=now.isoformat(),valid_until=until.isoformat())
            result.append(d)
        except (KeyError, ValueError, TypeError, ArithmeticError) as e:
            raise ValueError('Contrat API invalide pour '+source) from e
    return deduplicate(result)
def deduplicate(rows):
    out={}
    for d in rows:
        key=d['id']
        if key not in out or (d.get('price') and Decimal(d['price'])<Decimal(out[key]['price'])): out[key]=d
    return sorted(out.values(),key=lambda d:(d['kind']!='free',-(d.get('discount') or 0),d['title'].lower()))
def collect():
    now=datetime.now(UTC); offers=[]; health={}; failed=False
    endpoints={'gamerpower':'https://www.gamerpower.com/api/giveaways?type=game','cheapshark':'https://www.cheapshark.com/api/1.0/deals?lowerPrice=0.01&pageSize=60&onSale=1&sortBy=Savings'}
    for source,url in endpoints.items():
        try:
            raw=fetch(url); normalized=normalize(source,raw,now)
            if source=='cheapshark':
                shops=fetch('https://www.cheapshark.com/api/1.0/stores')
                names={str(shop['storeID']):shop['storeName'] for shop in shops}
                for offer in normalized:
                    offer['store']=names.get(offer['store'].split()[-1],'Boutique indiquée sur CheapShark')
            (ROOT/'data'/f'{source}-raw.json').write_text(json.dumps({'fetched_at':stamp(),'endpoint':url,'rows':raw},ensure_ascii=False),encoding='utf-8')
            offers.extend(normalized); health[source]={'ok':True,'count':len(normalized),'checked_at':stamp()}
        except Exception as e:
            failed=True; health[source]={'ok':False,'error':type(e).__name__,'checked_at':stamp()}
            # No stale fallback: failed source has zero published offers.
    payload={'generated_at':stamp(),'offers':deduplicate(offers),'sources':health}
    temp=ROOT/'data/offers.tmp'; temp.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8');temp.replace(ROOT/'data/offers.json')
    print(json.dumps(health)); return 1 if failed else 0
if __name__=='__main__': sys.exit(collect())
