"""Translate exact interface text nodes, leaving game titles and URLs untouched."""
from html.parser import HTMLParser
from html import escape

TEXT = {
 'Checkpoint — jeux offerts & fortes promotions': 'Checkpoint — free games & big discounts',
 'Le bon jeu. Au bon moment.': 'The right game. At the right time.',
 'Les offres': 'Deals', 'Notre méthode': 'Our method',
 'LE RADAR DES JOUEURS ÉCONOMES': 'THE RADAR FOR BUDGET GAMERS',
 'Plus de jeux.': 'More games.', 'Moins de dépenses.': 'Less spending.',
 'Jeux offerts pour une durée limitée et promotions d’au moins 70 %. Une sélection issue d’API autorisées, sans abonnement.': 'Limited-time free games and discounts of at least 70%. Selected from authorized APIs, no subscription needed.',
 'À saisir maintenant': 'Available now', 'Rechercher un jeu': 'Search for a game',
 'Type d’offre': 'Deal type', 'Toutes les offres': 'All deals',
 'Jeux offerts': 'Free games', 'Promotions': 'Discounts',
 'Les promotions sont en dollars US. Les sources ne garantissent pas l’activation en France. Vérifie le prix final, les conditions et la région avant de récupérer ou d’acheter.': 'Prices are in US dollars. Regional availability and activation are not guaranteed. Check the final price, terms and your region before claiming or buying.',
 'Jeu offert': 'Free game', 'À récupérer': 'Claim now',
 'Consulter l’offre ↗': 'View deal ↗',
 'Disponibilité en France à confirmer sur la boutique': 'Regional availability must be confirmed with the store',
 'Prix USD • tarif et activation en France à confirmer': 'USD price • confirm local pricing and regional activation',
 'Aucune offre récente à afficher. La prochaine collecte pourra en ajouter.': 'No recent deals to show. The next update may add more.',
 'La recherche nécessite JavaScript. Les offres restent consultables ; vérifie l’heure de relevé avant de cliquer.': 'Search requires JavaScript. Deals remain accessible; check the update time before clicking.',
 'UNE SÉLECTION TRANSPARENTE': 'A TRANSPARENT SELECTION',
 'Une source à chaque offre.': 'A source for every deal.',
 'Nos relevés proviennent de ': 'Our listings come from ', ' et de ': ' and ',
 '. Il s’agit de signalements d’agrégateurs, pas d’une vérification directe en boutique. Les offres de plus de 12 heures sont masquées lorsque JavaScript est actif. Une date absente reste « non communiquée ». Nous ne convertissons pas les dollars en euros.': '. These are aggregator listings, not direct store verification. Listings older than 12 hours are hidden when JavaScript is enabled. Missing expiry dates remain undisclosed. We do not convert currencies.',
 'GamerPower fournit les jeux complets ; les bonus et accès bêta sont exclus. Une offre peut demander un compte, des étapes de récupération ou être limitée en quantité. Les instructions sont sur la page source.': 'GamerPower provides full-game giveaways; bonus items and beta access are excluded. A deal may require an account, claim steps or have limited stock. Instructions are on the source page.',
 'Données : ': 'Data: ', ' et ': ' and ', '. Aucun partenariat revendiqué.': '. No partnership claimed.',
 'Affiliation du site désactivée. Les liens CheapShark conservent leur attribution obligatoire au fournisseur.': 'Site affiliate monetization is disabled. CheapShark links retain the provider’s required attribution.',
 'Mesure d’audience : Cloudflare Web Analytics (visites, pages vues et performances), sans cookie publicitaire. Aucun formulaire ni publicité ajouté. L’hébergeur peut conserver ses journaux techniques.': 'Audience measurement: Cloudflare Web Analytics (visits, page views and performance), without advertising cookies. No forms or ads added. The hosting provider may retain technical logs.',
 'État des collectes': 'Collection status',
}

class Translator(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.out=[]
        self.game_title=False
        self.in_card=False
    def handle_starttag(self, tag, attrs):
        if tag=='article': self.in_card=True
        if tag=='h2': self.game_title=True
        self.out.append(self.get_starttag_text())
    def handle_endtag(self,tag):
        if tag=='article': self.in_card=False
        if tag=='h2': self.game_title=False
        self.out.append(f'</{tag}>')
    def handle_startendtag(self,tag,attrs): self.out.append(self.get_starttag_text())
    def handle_decl(self,decl): self.out.append(f'<!{decl}>')
    def handle_entityref(self,name): self.out.append(f'&{name};')
    def handle_charref(self,name): self.out.append(f'&#{name};')
    def handle_data(self,text):
        # Only exact known UI messages; game names remain their original names.
        if self.game_title and self.in_card:
            self.out.append(text); return
        translated=TEXT.get(text,text)
        if text.endswith(' offres') and text[:-7].isdigit(): translated=text[:-7]+' offers'
        if text.startswith('Fin : '):
            translated=text.replace('Fin : ','Ends: ',1).replace('Non précisée','Not specified').replace('Non communiquée','Not disclosed').replace('(fuseau non précisé par la source)','(time zone not specified by the source)')
        if text.startswith('Relevé API : '): translated=text.replace('Relevé API : ','API checked: ',1)
        if text.startswith('● Collecte '): translated=text.replace('Collecte complète','All sources updated').replace('Collecte partielle : une source est indisponible','Partial update: one source is unavailable')
        if text.startswith('Éditeur : '): translated=text.replace('Éditeur : ','Publisher: ',1)
        self.out.append(translated)

def english_page(page,canonical):
    parser=Translator(); parser.feed(page); parser.close()
    page=''.join(parser.out).replace('<html lang="fr">','<html lang="en">')
    page=page.replace('href="style.css"','href="/style.css"').replace('src="app.js"','src="/app.js"').replace('href="health.json"','href="/health.json"')
    page=page.replace('href="./"','href="/en/"')
    page=page.replace('href="/en/" lang="en" hreflang="en" aria-label="Read in English">English', 'href="/" lang="fr" hreflang="fr" aria-label="Lire en français">Français')
    page=page.replace('placeholder="Un titre, une plateforme…"','placeholder="A title, a platform…"')
    page=page.replace('Les jeux temporairement offerts et les promotions PC de 70 % et plus. Sources, dates et limites affichées pour chaque offre.', 'Limited-time free games and PC discounts of 70% or more. Sources, dates and limitations shown for every deal.')
    if canonical: page=page.replace(f'rel="canonical" href="{escape(canonical,quote=True)}/"', f'rel="canonical" href="{escape(canonical,quote=True)}/en/"')
    return page
