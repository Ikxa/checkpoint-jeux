# Checkpoint — MVP français de bons plans jeux

Site statique sans dépendances Python, sans base, sans compte visiteur, sans publicités. Réalisé le 10 octobre 2026. Dépôt public : https://github.com/Ikxa/checkpoint-jeux. Site publié : https://checkpoint-jeux.pages.dev.

## Démarrer

Python 3.12+ :

```
python -m unittest discover -s tests -v
python scripts/collect.py
python scripts/build.py
python -m http.server 8765 --directory dist
```

Ouvrir http://localhost:8765. Une collecte en échec renvoie 1 mais écrit les données des sources réussies et leur diagnostic. Lancer ensuite le build pour publier l'état dégradé ; ne jamais déployer les fichiers d'un ancien build à sa place.

## Sources et décisions

Vérification documentaire du 10 octobre 2026, pas un avis juridique ni une autorisation individuelle des boutiques.

| Source | Conditions documentées | Décision |
|---|---|---|
| [GamerPower API](https://www.gamerpower.com/api-read) | Usage personnel et commercial gratuit, lien d'attribution actif, pas de revente des données ; maximum 10 requêtes/s | Activée, une requête par collecte. Jeux complets actifs uniquement ; loot et bêta exclus |
| [CheapShark API](https://apidocs.cheapshark.com/) | API gratuite sans clé, User-Agent nécessaire, liens de redirection CheapShark obligatoires ; prix USD | Activée, deux requêtes par collecte (offres et noms des boutiques), 60 résultats bruts maximum. Redirections réservées aux visiteurs, aucune visite automatisée |
| [IsThereAnyDeal](https://docs.isthereanydeal.com/) | Interdit les applications concurrentes, impose de conserver prix et tags d'affiliation | Non intégrée ; demander une autorisation écrite pour ce comparateur avant toute intégration |
| Epic / Steam / GOG internes | Aucun contrat d'API publique de collecte de promotions établi pendant cette recherche | Aucun scraping ni endpoint interne utilisé ; offres éventuellement relayées via GamerPower |

Les API utilisées sont officielles **chez les agrégateurs**, pas des API officielles des boutiques. Aucun prix ni accès en France n'est présenté comme vérifié directement chez le marchand. Les titres sont conservés tels que fournis, parfois en anglais. L'interface est française.

## Architecture et autonomie

`API → collect.py → data/offers.json → build.py → dist/ → Cloudflare Pages`.

Workflow GitHub livré dans `.github/workflows/refresh.yml` : toutes les 6 heures, à la minute 17 UTC, lancement manuel et à chaque push sur main. Tests, collecte, génération, archive diagnostic, commit des relevés et déploiement Git automatique Cloudflare. Le jeton GitHub éphémère du workflow possède uniquement contents:write ; aucun secret Cloudflare requis. Aucun achat, inscription d'affiliation ou mail externe automatisé.

Déduplication par identifiant de jeu CheapShark : meilleur prix parmi les boutiques récupérées, pas une garantie de meilleur prix universel. Jeux offerts par identifiant GamerPower. Les éditions différentes restent différentes. Pas de rapprochement hasardeux entre catalogues.

Requêtes avec timeout et trois tentatives maximum pour les erreurs transitoires. Schéma inattendu : source invalidée, exit code d'échec, diagnostic sans secret. Les sources réussies restent affichées. Aucun ancien prix n'est réutilisé après un échec. Les offres disparaissent après 12 heures dans le navigateur (contrôle chaque minute), et au build si périmées. Sans JavaScript, une ancienne page statique peut encore afficher ses anciens relevés : avertissement visible et horodatage. Si l'ordonnanceur ne s'exécute plus, le navigateur masque les offres mais ne peut pas envoyer une alerte.

Expiration GamerPower : date affichée telle que reçue, avec indication du fuseau inconnu. Retrait conservateur à l'instant le plus tôt possible (hypothèse UTC+14) afin de ne pas inventer une heure officielle. Date absente : aucune date fabriquée. CheapShark ne communique pas d'échéance. Les changements entre deux collectes et les ruptures de stock restent possibles.

## Déploiement recommandé : 0 €

Le dépôt public `Ikxa/checkpoint-jeux` est créé. L'application GitHub Cloudflare est autorisée uniquement pour ce dépôt.

Configuration Cloudflare Pages : branche `main`, aucun framework, commande `python -m unittest discover -s tests -v && python scripts/build.py`, sortie `dist`. GitHub Actions effectue la collecte toutes les 6 heures et pousse les données actualisées ; Cloudflare reconstruit sur chaque push. Les actions officielles sont figées sur leur SHA.

Aucun token Cloudflare ni mot de passe dans le dépôt. Le workflow GitHub éphémère peut écrire les relevés dans ce dépôt uniquement. Les commits du bot ne relancent pas le workflow GitHub via GITHUB_TOKEN ; Cloudflare reçoit les événements Git.

Identité publique provisoire : pseudonyme GitHub `Ikxa`, contact via les issues du dépôt. Aucun nom réel ou email privé publié. Remplacer ces champs si nécessaire avant activation commerciale. Renseigner `site_url` après confirmation de l'origine ; canonical, robots et sitemap sont alors générés.

Vérifier dans Actions les échecs de collecte et dans Cloudflare les échecs de publication. Le diagnostic public `health.json` doit avoir moins de 12 h. Un second workflow read-only `monitor.yml` vérifie toutes les 6 heures, à la minute 47 UTC, la disponibilité HTTPS de health.json, la fraîcheur inférieure à 12 h et les deux sources. Il ne dépend pas du succès de la collecte. Son premier lancement distant a réussi. Les préférences GitHub existantes sont activées pour les workflows en échec uniquement, sur GitHub et par email ; réception effective d'une alerte non simulée. Un arrêt total de GitHub Actions reste indétectable par un autre workflow GitHub ; aucun service de surveillance tiers n'est utilisé.

Environ 120 collectes/déploiements par mois (4/jour), sous le quota publié de 500 builds/mois Pages Free. Pas de carte ni offre payante sélectionnée. Coût engagé : **0 €**. Le prix à 0 € dépend du maintien des offres gratuites et des quotas. Ne pas activer d'upgrade automatique.

[GitHub Pages](https://docs.github.com/en/enterprise-cloud%40latest/pages/getting-started-with-github-pages/github-pages-limits) restreint les sites principalement destinés à faciliter les transactions commerciales : il n'est pas retenu pour ce site de bons plans destiné à l'affiliation.

## Monétisation préparée, désactivée

`affiliate_enabled=false` ; mettre true bloque le build tant qu'une intégration approuvée n'existe pas. Aucun revenu prévu ou garanti, aucun identifiant affilié utilisateur, publicité ou cookie marketing. Les liens CheapShark restent ceux imposés par le fournisseur et ne génèrent pas une commission pour l'éditeur de ce MVP.

[Fanatical](https://www.fanatical.com/en/affiliates) propose son programme global via Awin, avec candidature et acceptation. [Epic Support-A-Creator](https://www.epicgames.com/help/c-34406160/a19029301) concerne les créateurs de contenus et les jeux éligibles ; l'éligibilité de ce site n'est pas établie. Pas d'inscription effectuée, pas de taux de commission promis, frais éventuels d'inscription non vérifiés et non engagés.

Avant activation : accord partenaire, droit de réutiliser un flux de prix EUR/France, attribution et divulgation des liens rémunérés, vérification des obligations applicables à l'éditeur. Ne jamais remplacer les liens CheapShark par ses propres tags. Une future source affiliée séparée doit avoir ses propres conditions et son contrat de données.

## Interventions résiduelles

Activation initiale GitHub/Cloudflare et informations d'éditeur ; ensuite lecture des alertes et correction lors d'un changement d'API. Vérifier au moins mensuellement la fraîcheur de health.json, les conditions fournisseurs, quotas et workflow. [GitHub désactive les plannings publics après 60 jours sans activité](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows?tool=webui) et les exécutions peuvent être retardées. Ce workflow ne crée pas de commits artificiels pour contourner cette limite. Réactivation manuelle ou changement d'ordonnanceur peut être nécessaire. La surveillance par un second workflow est active après son push, mais ne couvre pas un arrêt total de GitHub Actions. Les mises à jour des données créent de vrais commits utiles au déploiement, pas des commits vides de maintien d'activité.

Limites : prix USD, région FR inconnue, catalogues partiels, absence de dates pour certaines offres, pas de contrôle direct du panier ni de disponibilité des clés. Pas de génération vidéo, réseau social, paiement, newsletter, ni revenus automatiques inclus dans ce MVP.

## Audience et récap mensuel
Cloudflare Web Analytics activé le 10 octobre 2026 : injection automatique au déploiement Pages, script et destination autorisés par la CSP. La mention de mesure d’audience figure au pied de page. Tableau de bord privé dans Cloudflare, rubrique Web Analytics pour checkpoint-jeux.pages.dev. Les mesures commencent à l’activation, ne reconstituent pas le passé et peuvent être bloquées par les navigateurs. Elles ne mesurent pas les clics sortants ni les revenus.
Un bilan mensuel est programmé dans cette conversation Codex le 1er à 10 h (heure locale). Il requiert l’application ouverte, un ordinateur allumé et les accès disponibles ; une session expirée sera signalée. La collecte et la surveillance GitHub restent indépendantes de cette tâche locale.

## Langues et identité visuelle
Version française à / et anglaise à /en/, navigation réciproque, canonical propre à chaque langue et hreflang fr/en. Les titres des jeux restent inchangés. Les ressources et le favicon SVG (drapeau checkpoint avec coche) sont communs. Les deux versions sont générées à chaque collecte. Aucun changement de disponibilité régionale ni conversion monétaire n’est déduit de la langue.
