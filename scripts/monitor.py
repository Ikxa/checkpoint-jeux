"""Read-only public health check, separate from collection and deployment."""
import json, sys
from datetime import datetime, timezone, timedelta
from urllib.request import Request, urlopen
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def validate_health(data, now, max_age=12):
    generated=datetime.fromisoformat(data['generated_at'])
    if generated.tzinfo is None: raise ValueError('Horodatage sans fuseau')
    age=now-generated
    if age<timedelta(minutes=-5) or age>timedelta(hours=max_age):
        raise ValueError('Le relevé publié a une date incohérente ou dépasse 12 heures')
    sources=data['sources']
    for name in ('gamerpower','cheapshark'):
        if sources[name]['ok'] is not True:
            raise ValueError('Source indisponible : '+name)
    return True

def main():
    config=json.loads((ROOT/'config.json').read_text(encoding='utf-8'))
    url=config['site_url'].rstrip('/')+'/health.json'
    if not url.startswith('https://'): raise ValueError('Origine publique HTTPS nécessaire')
    with urlopen(Request(url,headers={'User-Agent':'Checkpoint-health/1.0','Cache-Control':'no-cache'}),timeout=25) as response:
        data=json.loads(response.read(100_000))
    validate_health(data,datetime.now(timezone.utc))
    print('Site publié accessible ; sources disponibles ; relevé de moins de 12 heures.')

if __name__=='__main__':
    try:main()
    except Exception as error:
        print('::error::Surveillance du site publiée en échec : '+type(error).__name__)
        sys.exit(1)
