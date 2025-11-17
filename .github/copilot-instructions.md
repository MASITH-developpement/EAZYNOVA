## But rapide

Ce dépôt contient une petite extension Odoo nommée `odoo_saas` sous `addons/odoo_saas`. Le but de ce fichier est d'aider un agent automatique à être productif immédiatement : architecture, conventions, workflows de dev, points d'intégration et exemples concrets.

## Architecture & composants clés

-   Module principal : `addons/odoo_saas`.
    -   Manifest : `addons/odoo_saas/__manifest__.py` (métadonnées du module).
    -   Modèles Python : `addons/odoo_saas/models/*.py` (ex. `saas_client.py`, `saas_plan.py`, `saas_subscription.py`).
    -   Vues / menus : `addons/odoo_saas/views/*.xml` (ex. `saas_client_views.xml`, `saas_plan_views.xml`).
    -   Données initiales : `addons/odoo_saas/data/saas_data.xml`.
    -   Sécurité : `addons/odoo_saas/security/ir.model.access.csv` et `saas_security.xml`.
    -   Tests unitaires/integration : `addons/odoo_saas/tests/`.

Conception dominante : extension Odoo classique (models + views + security + data). Les interactions internes se font via les ORM models (classes Python hérité de `models.Model`) et les vues XML exposent l'UI.

## Points d'intégration externes

-   Fichiers de configuration racine : `odoo.conf` et `odoo.conf.production`.
-   Conteneurisation : `Dockerfile` et `docker-compose.yml` présents — le projet est prévu pour être lancé en Docker.
-   Dépendances Python listées dans `requirements.txt`.

## Workflows développeur (découverts / recommandés)

-   Démarrer l'environnement (conteneurs) : exécuter `docker-compose up --build` depuis la racine. (Les services et ports sont définis dans `docker-compose.yml`.)
-   Charger / mettre à jour le module dans une base Odoo : depuis le conteneur Odoo, exécuter la commande Odoo appropriée pour mettre à jour le module (`-u odoo_saas`) ou redémarrer le service pour que le module soit chargé via le `addons` path.
-   Installer dépendances locales : `pip install -r requirements.txt` si vous travaillez hors conteneur.
-   Tests : exécuter les tests unitaires Odoo via la commande Odoo test runner ciblant le module (voir `addons/odoo_saas/tests/`).

Note : README.md n'expose pas (encore) d'instructions détaillées; ces commandes sont les pratiques courantes pour ce type de repo (présence de Dockerfile/docker-compose/requirements.txt).

## Conventions et patterns spécifiques au projet

-   Structure standard d'un module Odoo (manifest, models, views, security, data, tests).
-   Les modèles se trouvent dans `addons/odoo_saas/models/` et utilisent l'ORM Odoo ; chercher des méthodes nommées `create`, `write`, `unlink`, `compute_...`, `@api.*` pour comprendre la logique métier.
-   Les vues XML se trouvent dans `addons/odoo_saas/views/` et référencent les `model` définis dans les fichiers Python.
-   Les données d'amorçage (fixtures) sont sous `data/` et appliquées via le manifest.

## Exemples concrets à utiliser dans les prompts

-   "Où est défini le modèle client ?" → `addons/odoo_saas/models/saas_client.py`.
-   "Modifier l'accès pour le groupe X" → regarder `addons/odoo_saas/security/ir.model.access.csv` et `saas_security.xml`.
-   "Ajouter un champ calculé sur les abonnements" → modifier `addons/odoo_saas/models/saas_subscription.py` et ajouter la référence correspondante dans `views/saas_subscription_views.xml`.

## Limitations / hypothèses raisonnables

-   Le dépôt attend une instance Odoo (la logique métier s'exécute dans ce contexte). Un agent doit éviter d'adopter des changements qui modifient la configuration globale d'Odoo sans tests.
-   README et manifest peuvent être vides/partiels ; vérifier `__manifest__.py` avant d'implémenter des changements de dépendances.

## Vérifications à faire avant une PR

-   Lancer les tests sous `addons/odoo_saas/tests/` et s'assurer qu'ils passent.
-   Vérifier que le `__manifest__.py` contient bien les clefs `data`, `security`, `depends` si vous ajoutez de nouveaux fichiers.
-   Respecter la structure d'accès Odoo (ne pas exposer champs sensibles dans les vues sans contrôle d'accès).

---

Si quelque chose n'est pas clair ou si vous souhaitez que j'inclus des commandes exactes extraites de `docker-compose.yml`/`Dockerfile`/`requirements.txt`, dites-le et je ferai une passe pour intégrer ces détails précis dans ce fichier.
