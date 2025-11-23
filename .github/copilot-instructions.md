## But rapide

Ce dépôt contient une suite de modules Odoo 19 CE personnalisés nommée **EAZYNOVA** sous `addons/addons-perso/`. Le but de ce fichier est d'aider un agent automatique à être productif immédiatement : architecture, conventions, workflows de dev, points d'intégration et exemples concrets.

## Architecture & composants clés

### Modules EAZYNOVA

-   **Module Core** : `addons/addons-perso/eazynova/`
    -   Infrastructure commune (IA, OCR, Reconnaissance faciale)
    -   Tableau de bord principal
    -   Configuration globale dans `models/res_config_settings.py`

-   **Module Interventions** : `addons/addons-perso/eazynova_intervention/`
    -   Gestion des interventions techniques
    -   Planning et affectation des techniciens

-   **Module Planning** : `addons/addons-perso/eazynova_planning/`
    -   Planification et gestion des tâches

-   **Module Gestion de Chantier** : `addons/addons-perso/eazynova_gestion_chantier/`
    -   Gestion complète des chantiers BTP

-   **Module Import Bancaire** : `addons/addons-perso/eazynova_bank_statement/`
    -   Import des relevés bancaires (QIF, OFX, CSV, PDF)

-   **Module Facture OCR** : `addons/addons-perso/eazynova_facture_ocr/`
    -   Reconnaissance OCR de factures avec IA

### Structure type d'un module EAZYNOVA

-   Manifest : `__manifest__.py` (métadonnées, dépendances, données à charger)
-   Modèles Python : `models/*.py` (logique métier ORM)
-   Vues / menus : `views/*.xml` (interface utilisateur)
-   Sécurité : `security/ir.model.access.csv` et `security/*_security.xml`
-   Données initiales : `data/*.xml`
-   Wizards : `wizard/*.py` et `wizard/*_views.xml`

Conception dominante : extensions Odoo classiques (models + views + security + data). Les interactions internes se font via l'ORM Odoo (classes héritées de `models.Model`) et les vues XML exposent l'UI.

## Points d'intégration externes

-   **Configuration** : `odoo.conf` (configuration Odoo)
-   **Conteneurisation** : `Dockerfile` et `docker-compose.yml` (déploiement Docker)
-   **Dépendances Python** : `requirements.txt` (reconnaissance faciale, OCR, IA, import bancaire)
-   **Déploiement** : Railway (production automatique)

## Workflows développeur

-   **Démarrer l'environnement local** : `docker-compose up --build`
-   **Mettre à jour un module** : Odoo Apps → Update Apps List → Upgrade
-   **Installer dépendances** : `pip install -r requirements.txt`
-   **Commiter des changements** : Toujours sur une branche `claude/*` avec push vers origin

## Conventions et patterns spécifiques au projet

### Compatibilité Odoo 19 CE

-   **IMPORTANT** : Ne plus utiliser `category_id` dans `res.groups` (déprécié dans Odoo 19)
-   **IMPORTANT** : Utiliser `type='jsonrpc'` au lieu de `type='json'` dans les routes
-   **IMPORTANT** : Le fichier menu doit être chargé AVANT les vues qui le référencent dans `__manifest__.py`

### Structure de fichiers

-   Modèles dans `models/` avec méthodes ORM (`create`, `write`, `unlink`, `@api.*`)
-   Vues XML dans `views/` référençant les modèles Python
-   Groupes de sécurité sans `category_id` pour Odoo 19 CE
-   Configuration centralisée dans `res.config.settings` avec `config_parameter`

## Exemples concrets

-   "Ajouter un champ au modèle intervention" → `addons/addons-perso/eazynova_intervention/models/intervention.py`
-   "Modifier les droits d'accès planning" → `addons/addons-perso/eazynova_planning/security/ir.model.access.csv`
-   "Configurer l'IA pour OCR" → `addons/addons-perso/eazynova/models/res_config_settings.py` (champ `eazynova_ai_assistance_enabled`)

## Limitations / hypothèses raisonnables

-   Le dépôt nécessite Odoo 19 CE (la logique métier s'exécute dans ce contexte)
-   Les modules EAZYNOVA dépendent du module `eazynova` (Core)
-   Éviter de modifier la configuration globale Odoo sans tests
-   Vérifier `__manifest__.py` avant de changer les dépendances

## Vérifications avant commit/PR

-   Vérifier que tous les groupes de sécurité n'ont PAS de `category_id` (Odoo 19)
-   Vérifier que les routes utilisent `type='jsonrpc'` et non `type='json'`
-   Vérifier l'ordre de chargement des fichiers dans `__manifest__.py` (menus avant vues)
-   Vérifier que `__manifest__.py` contient `data`, `security`, `depends` si nouveaux fichiers
-   Respecter les contrôles d'accès Odoo (ne pas exposer de données sensibles)

---

**Note** : Ce projet est déployé automatiquement sur Railway. Tous les commits sur les branches `claude/*` déclenchent un build Docker.
