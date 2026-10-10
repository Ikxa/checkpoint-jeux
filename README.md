# Checkpoint — MVP français de bons plans jeux

Site statique sans dépendances Python, sans base, sans compte visiteur, sans publicités. Réalisé le 10 octobre 2026. Ce paquet est prêt pour prépublication ; aucun dépôt ni site externe n'a encore été créé.

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

Workflow GitHub livré dans `.github/workflows/refresh.yml` : toutes les 6 heures, à la minute 17 UTC, lancement manuel et à chaque push sur main. Tests, collecte, génération, archive diagnostic et déploiement conditionnel. Aucun achat, inscription d'affiliation ou mail externe automatisé.

Déduplication par identifiant de jeu CheapShark : meilleur prix parmi les boutiques récupérées, pas une garantie de meilleur prix universel. Jeux offerts par identifiant GamerPower. Les éditions différentes restent différentes. Pas de rapprochement hasardeux entre catalogues.

Requêtes avec timeout et trois tentatives maximum pour les erreurs transitoires. Schéma inattendu : source invalidée, exit code d'échec, diagnostic sans secret. Les sources réussies restent affichées. Aucun ancien prix n'est réutilisé après un échec. Les offres disparaissent après 12 heures dans le navigateur (contrôle chaque minute), et au build si périmées. Sans JavaScript, une ancienne page statique peut encore afficher ses anciens relevés : avertissement visible et horodatage. Si l'ordonnanceur ne s'exécute plus, le navigateur masque les offres mais ne peut pas envoyer une alerte.

Expiration GamerPower : date affichée telle que reçue, avec indication du fuseau inconnu. Retrait conservateur à l'instant le plus tôt possible (hypothèse UTC+14) afin de ne pas inventer une heure officielle. Date absente : aucune date fabriquée. CheapShark ne communique pas d'échéance. Les changements entre deux collectes et les ruptures de stock restent possibles.

## Déploiement recommandé : 0 €

GitHub connecté au compte `Ikxa` au moment de la préparation, aucune écriture effectuée. Faire confirmer la création d'un dépôt **public** `checkpoint-jeux` pour bénéficier des exécutions standard gratuites ; un dépôt privé est soumis au quota de minutes du compte.

1. Confirmer dépôt et publication, fournir identité publique de l'éditeur et contact.
2. Créer un projet Cloudflare Pages gratuit, sous-domaine `pages.dev` ; pas de domaine payant requis. [Tarifs](https://www.cloudflare.com/en-gb/developer-platform/products/pages/), [limites](https://developers.cloudflare.com/pages/platform/limits/).
3. Ajouter les secrets GitHub `CLOUDFLARE_API_TOKEN` (limité au déploiement Pages du compte), `CLOUDFLARE_ACCOUNT_ID`, les variables `CLOUDFLARE_PROJECT` et `DEPLOY_ENABLED=true`. Ne jamais envoyer les secrets dans le chat ou les committer.
4. Renseigner `site_url`, `publisher`, `contact` dans config.json. Sans origine définie, prépublication noindex et robots Disallow. Une fois l'origine définie : canonical, sitemap et robots. Ne pas exposer publiquement une identité provisoire.
5. Lancer workflow_dispatch, vérifier la publication et health.json, puis activer les notifications GitHub Actions d'échec dans les préférences du propriétaire. Cela prépare les alertes mais ne prouve pas leur réception.
6. Ajouter, si souhaité, un moniteur externe gratuit pour détecter un health.json de plus de 12 h : seuil sur generated_at, pas seulement HTTP 200. Il faut configurer le service et ses alertes après obtention de l'URL ; aucun moniteur externe n'est actif actuellement.

Le déploiement utilise Wrangler 4 depuis le registre npm. Fixer une version et un SHA des actions après validation de la première exécution distante pour rendre les dépendances reproductibles.

Environ 120 collectes/déploiements par mois (4/jour), sous le quota publié de 500 builds/mois Pages Free. Pas de carte ni offre payante sélectionnée. Coût engagé : **0 €**. Le prix à 0 € dépend du maintien des offres gratuites et des quotas. Ne pas activer d'upgrade automatique.

[GitHub Pages](https://docs.github.com/en/enterprise-cloud%40latest/pages/getting-started-with-github-pages/github-pages-limits) restreint les sites principalement destinés à faciliter les transactions commerciales : il n'est pas retenu pour ce site de bons plans destiné à l'affiliation.

## Monétisation préparée, désactivée

`affiliate_enabled=false` ; mettre true bloque le build tant qu'une intégration approuvée n'existe pas. Aucun revenu prévu ou garanti, aucun identifiant affilié utilisateur, publicité ou cookie marketing. Les liens CheapShark restent ceux imposés par le fournisseur et ne génèrent pas une commission pour l'éditeur de ce MVP.

[Fanatical](https://www.fanatical.com/en/affiliates) propose son programme global via Awin, avec candidature et acceptation. [Epic Support-A-Creator](https://www.epicgames.com/help/c-34406160/a19029301) concerne les créateurs de contenus et les jeux éligibles ; l'éligibilité de ce site n'est pas établie. Pas d'inscription effectuée, pas de taux de commission promis, frais éventuels d'inscription non vérifiés et non engagés.

Avant activation : accord partenaire, droit de réutiliser un flux de prix EUR/France, attribution et divulgation des liens rémunérés, vérification des obligations applicables à l'éditeur. Ne jamais remplacer les liens CheapShark par ses propres tags. Une future source affiliée séparée doit avoir ses propres conditions et son contrat de données.

## Interventions résiduelles

Activation initiale GitHub/Cloudflare et informations d'éditeur ; ensuite lecture des alertes et correction lors d'un changement d'API. Vérifier au moins mensuellement la fraîcheur de health.json, les conditions fournisseurs, quotas et workflow. [GitHub désactive les plannings publics après 60 jours sans activité](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows?tool=webui) et les exécutions peuvent être retardées. Ce workflow ne crée pas de commits artificiels pour contourner cette limite. Réactivation manuelle ou changement d'ordonnanceur peut être nécessaire. La surveillance extérieure de l'arrêt complet reste à activer.

Limites : prix USD, région FR inconnue, catalogues partiels, absence de dates pour certaines offres, pas de contrôle direct du panier ni de disponibilité des clés. Pas de génération vidéo, réseau social, paiement, newsletter, ni revenus automatiques inclus dans ce MVP.
