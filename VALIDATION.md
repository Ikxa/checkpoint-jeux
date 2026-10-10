# Bilan final — 10 octobre 2026

## Résultat

- Site public : https://checkpoint-jeux.pages.dev
- Dépôt public : https://github.com/Ikxa/checkpoint-jeux
- 70 offres lors de la validation : 17 jeux signalés comme offerts, 53 promotions après déduplication. Données d'agrégateurs, prix USD et activation en France non vérifiée directement.
- Coût engagé : 0 €. Cloudflare Pages, sous-domaine gratuit, GitHub Actions sur dépôt public. Aucun achat, abonnement payant ou domaine ajouté. Affiliation de l'éditeur désactivée.

## Vérifications réussies

- 21 tests Python : remises, exclusion des prix zéro/hors promotion, doublons, meilleur prix parmi les offres récupérées, encodage des liens, jeux complets, exclusion loot, expiration, fraîcheur, URL dangereuse, schéma inattendu, échappement HTML, panne réseau sans réutilisation de données anciennes, contrôle du site publié et panne d'une source dans son diagnostic.
- Collectes HTTPS réelles réussies auprès de GamerPower et CheapShark.
- GitHub Actions : trois lancements de collecte réussis, publication des données par le bot dans le dépôt, et un lancement de surveillance réussi.
- Cloudflare : premier déploiement puis redéploiements Git automatiques réussis, dont un déclenché par un commit du bot. Aucune clé API Cloudflare créée ; application GitHub autorisée uniquement pour checkpoint-jeux après confirmation explicite.
- Site public : filtre jeux offerts = 17, recherche sans résultat, retour aux 70 offres, contenu statique, canonical et suppression du noindex confirmés. Responsive contrôlé auparavant à 390 × 844, aucun débordement horizontal détecté.
- Diagnostic HTTPS public : deux sources disponibles et relevé récent à 04:03 Europe/Paris lors du contrôle final.
- Notifications GitHub : préférences existantes lues et conservées, workflows en échec uniquement, sur GitHub et par email.

## Automatisation active

- Collecte : toutes les 6 h, minute 17 UTC, et lancement manuel/à chaque push de main. Tests puis collecte, construction, diagnostic, commit utile des données et déploiement Git Cloudflare.
- Surveillance indépendante du workflow de collecte : toutes les 6 h, minute 47 UTC. Vérifie HTTPS, JSON, fraîcheur < 12 h, horodatage cohérent et état des deux sources. Un échec marque le workflow en erreur.
- Les plannings peuvent être retardés par GitHub. Le contrôle ne couvre pas un arrêt total de GitHub Actions lui-même. Les préférences d'email sont actives, mais aucune panne artificielle ni réception d'email n'a été provoquée pour ce test.

## Limites et entretien résiduel

- Prix USD, région FR non garantie, API partielles, fins parfois inconnues, quantités et conditions propres à chaque boutique. Aucun prix panier ni activation de clé contrôlé directement.
- Titres fournis par les sources parfois en anglais ; interface française.
- Les dates GamerPower sans fuseau restent explicitement telles quelles et entraînent un retrait conservateur ; aucun fuseau officiel inventé.
- Sans JavaScript, une ancienne page statique peut afficher d'anciens relevés avec leur date. Avec JavaScript, retrait après 12 h ou plus tôt selon l'échéance conservatrice.
- Les pannes et changements d'API peuvent demander une correction ; vérifier mensuellement le planning, les alertes, conditions fournisseurs et quotas. Réactivation manuelle potentielle si GitHub désactive un workflow pour inactivité.
- Identité publique utilisée faute d'autre choix : pseudonyme GitHub Ikxa, contact via les issues du dépôt. À adapter avec les informations requises avant activation commerciale.
- Panne partielle du collecteur, HTTP 429 réel et arrêt global de l'ordonnanceur non testés directement. Le contrôle de santé dégradée est couvert par les tests.

## Preuves distantes

- Collecte et tests : https://github.com/Ikxa/checkpoint-jeux/actions/runs/38015537642
- Surveillance du site : https://github.com/Ikxa/checkpoint-jeux/actions/runs/38015537646
- État public : https://checkpoint-jeux.pages.dev/health.json
