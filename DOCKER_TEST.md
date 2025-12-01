# 🐳 Guide de Test Docker - EAZYNOVA

Guide complet pour tester EAZYNOVA avec Docker, incluant le nouveau module `eazynova_website`.

## 📋 Prérequis

- **Docker Desktop** installé ([Télécharger ici](https://www.docker.com/products/docker-desktop))
- **Docker Compose** (inclus avec Docker Desktop)
- Au minimum **4 GB de RAM** disponible pour Docker
- Au minimum **10 GB d'espace disque** libre

## 🚀 Démarrage rapide (1 commande)

```bash
./test-docker.sh
```

Cette commande :
1. ✅ Crée le fichier `.env` automatiquement
2. ✅ Construit les images Docker
3. ✅ Démarre PostgreSQL, Odoo, PgAdmin et MailHog
4. ✅ Affiche toutes les informations de connexion
5. ✅ Propose d'ouvrir le navigateur automatiquement

## 🔧 Démarrage manuel

Si vous préférez contrôler chaque étape :

### 1. Créer le fichier de configuration

```bash
cp .env.test .env
```

Éditez `.env` si vous voulez changer les ports ou mots de passe.

### 2. Construire les images

```bash
docker-compose -f docker-compose.dev.yml build
```

### 3. Démarrer les services

```bash
docker-compose -f docker-compose.dev.yml up -d
```

### 4. Vérifier le statut

```bash
docker-compose -f docker-compose.dev.yml ps
```

Vous devriez voir 4 conteneurs :
- ✅ `eazynova_test_db` (PostgreSQL)
- ✅ `eazynova_test_odoo` (Odoo 19)
- ✅ `eazynova_test_pgadmin` (PgAdmin)
- ✅ `eazynova_test_mailhog` (MailHog)

## 🌐 Accès aux services

### Odoo 19
- **URL**: http://localhost:8069
- **Base de données**: `eazynova_test`
- **Login**: `admin`
- **Mot de passe**: `admin`

### PgAdmin (Interface PostgreSQL)
- **URL**: http://localhost:5050
- **Email**: `admin@eazynova.local`
- **Mot de passe**: `admin`

Pour se connecter à PostgreSQL dans PgAdmin :
1. Cliquer sur "Add New Server"
2. **Name**: EAZYNOVA Test
3. Dans l'onglet "Connection" :
   - **Host**: `db`
   - **Port**: `5432`
   - **Database**: `eazynova_test`
   - **Username**: `odoo`
   - **Password**: `odoo_password_2024`

### MailHog (Serveur SMTP de test)
- **URL Web**: http://localhost:8025
- **Port SMTP**: `1025`

MailHog capture tous les emails envoyés par Odoo. Parfait pour tester :
- Les emails d'essai gratuit
- Les credentials de connexion
- Les notifications d'expiration
- Etc.

## 📦 Installation du module eazynova_website

### Méthode 1 : Via l'interface Odoo

1. Aller sur http://localhost:8069
2. Créer une base de données ou se connecter à `eazynova_test`
3. Aller dans **Apps** (Applications)
4. Cliquer sur **Mettre à jour la liste des applications**
5. Dans la barre de recherche, taper : `EAZYNOVA`
6. Vous verrez :
   - **EAZYNOVA - Principal** (module de base)
   - **EAZYNOVA - Site Web SaaS** (nouveau module)
7. Cliquer sur **Installer** pour `eazynova_website`

### Méthode 2 : Via la ligne de commande

```bash
docker exec -it eazynova_test_odoo odoo -d eazynova_test -i eazynova_website --stop-after-init
docker-compose -f docker-compose.dev.yml restart odoo
```

## 🧪 Tester les fonctionnalités SaaS

Une fois le module installé :

### 1. Visiter le site web SaaS

- **Page d'accueil**: http://localhost:8069/
- **Tarifs**: http://localhost:8069/saas/pricing
- **Fonctionnalités**: http://localhost:8069/saas/features
- **Inscription**: http://localhost:8069/saas/signup

### 2. Créer un abonnement de test

1. Aller sur http://localhost:8069/saas/signup
2. Remplir le formulaire :
   - Nom entreprise : `Test SaaS Company`
   - Contact : `John Doe`
   - Email : `test@example.com`
   - Téléphone : `+33 1 23 45 67 89`
   - Nombre d'utilisateurs : `5`
3. Soumettre le formulaire
4. Vérifier l'email dans MailHog : http://localhost:8025

### 3. Gérer les abonnements (Backend)

1. Se connecter à Odoo en tant qu'admin
2. Aller dans **SaaS EAZYNOVA** (menu principal)
3. Voir :
   - **Abonnements** : Liste des abonnements clients
   - **Instances** : Instances Odoo provisionnées
   - **Configuration → Plans** : Plans d'abonnement

### 4. Portail client

1. Se connecter avec un compte client
2. Aller dans **Mon compte**
3. Voir **Mes abonnements**
4. Tester :
   - Modification du nombre d'utilisateurs
   - Activation de l'abonnement
   - Annulation

## 📊 Commandes utiles

### Voir les logs

```bash
# Tous les conteneurs
docker-compose -f docker-compose.dev.yml logs -f

# Seulement Odoo
docker-compose -f docker-compose.dev.yml logs -f odoo

# Seulement PostgreSQL
docker-compose -f docker-compose.dev.yml logs -f db
```

### Entrer dans un conteneur

```bash
# Odoo
docker exec -it eazynova_test_odoo bash

# PostgreSQL
docker exec -it eazynova_test_db psql -U odoo -d eazynova_test
```

### Redémarrer les services

```bash
# Tous
docker-compose -f docker-compose.dev.yml restart

# Seulement Odoo
docker-compose -f docker-compose.dev.yml restart odoo
```

### Arrêter les services

```bash
# Arrêter sans supprimer les volumes
docker-compose -f docker-compose.dev.yml stop

# Arrêter et tout supprimer
docker-compose -f docker-compose.dev.yml down -v
```

### Nettoyer et redémarrer

```bash
./test-docker.sh --clean
```

Cette commande :
1. Arrête tous les conteneurs
2. Supprime les volumes (données perdues !)
3. Reconstruit les images
4. Redémarre tout

## 🔍 Déboguer

### Odoo ne démarre pas

1. Vérifier les logs :
```bash
docker-compose -f docker-compose.dev.yml logs odoo
```

2. Vérifier que PostgreSQL est prêt :
```bash
docker-compose -f docker-compose.dev.yml ps db
```

3. Redémarrer Odoo :
```bash
docker-compose -f docker-compose.dev.yml restart odoo
```

### Module non visible dans Apps

1. Mettre à jour la liste des modules :
```bash
docker exec -it eazynova_test_odoo odoo -d eazynova_test -u all --stop-after-init
docker-compose -f docker-compose.dev.yml restart odoo
```

2. Vérifier que le module est bien copié :
```bash
docker exec -it eazynova_test_odoo ls -la /opt/odoo/custom_addons/eazynova_website
```

### Problèmes de permissions

```bash
# Depuis le répertoire du projet
sudo chown -R $(whoami):$(whoami) .
```

### Reset complet

```bash
# Arrêter et supprimer TOUT
docker-compose -f docker-compose.dev.yml down -v

# Supprimer les images
docker rmi $(docker images -q eazynova*)

# Redémarrer
./test-docker.sh --clean
```

## 📝 Configuration avancée

### Changer les ports

Éditez `.env` et changez :
```env
ODOO_PORT=8069          # Port Odoo
POSTGRES_PORT=5432      # Port PostgreSQL
PGADMIN_PORT=5050       # Port PgAdmin
MAILHOG_WEB_PORT=8025   # Port MailHog Web
MAILHOG_SMTP_PORT=1025  # Port MailHog SMTP
```

Puis redémarrez :
```bash
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml up -d
```

### Activer le mode développement

Le mode développement est activé par défaut avec rechargement automatique des modules.

Pour le désactiver, éditez `odoo.conf.dev` :
```ini
dev_mode =
```

### Installer d'autres modules

Éditez `odoo.conf.dev` et ajoutez :
```ini
init = website,eazynova,eazynova_website,eazynova_businessplan
```

Puis reconstruisez :
```bash
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml up -d --build
```

## 🎯 Cas d'usage de test

### Test du workflow complet SaaS

1. ✅ Inscription client (essai gratuit 30 jours)
2. ✅ Réception email de bienvenue dans MailHog
3. ✅ Provisioning de l'instance (simulé)
4. ✅ Réception des credentials par email
5. ✅ Connexion au portail client
6. ✅ Modification du nombre d'utilisateurs
7. ✅ Activation de l'abonnement payant
8. ✅ Génération de la facture de configuration
9. ✅ Facturation mensuelle automatique
10. ✅ Annulation de l'abonnement
11. ✅ Suppression de l'instance après 30 jours

### Test des crons (tâches planifiées)

Les crons s'exécutent automatiquement. Pour les tester manuellement :

```bash
docker exec -it eazynova_test_odoo odoo shell -d eazynova_test
```

Puis dans le shell Python :
```python
# Vérifier les périodes d'essai expirées
env['saas.subscription']._cron_check_trial_expiration()

# Générer les factures mensuelles
env['saas.subscription']._cron_generate_invoices()

# Supprimer les bases inactives
env['saas.subscription']._cron_check_unpaid_subscriptions()
```

## 🛠️ Développement

### Modifier le code en direct

Les modules sont montés en volume, donc toute modification dans `addons/addons-perso/` est immédiatement visible.

Pour recharger un module :
```bash
# Via l'interface Odoo : Apps → Rechercher le module → Mettre à jour

# Via la ligne de commande
docker exec -it eazynova_test_odoo odoo -d eazynova_test -u eazynova_website --stop-after-init
docker-compose -f docker-compose.dev.yml restart odoo
```

### Ajouter un nouveau module

1. Créer votre module dans `addons/addons-perso/`
2. Redémarrer Odoo :
```bash
docker-compose -f docker-compose.dev.yml restart odoo
```
3. Mettre à jour la liste des applications dans Odoo

## 📚 Ressources

- **Documentation Odoo 19** : https://www.odoo.com/documentation/19.0/
- **Docker Documentation** : https://docs.docker.com/
- **PostgreSQL Documentation** : https://www.postgresql.org/docs/

## ⚠️ Notes importantes

### ⚠️ Mode développement uniquement

Ce docker-compose est conçu pour le **développement et les tests**, PAS pour la production.

Pour la production, utilisez :
- `docker-compose.yml` (avec workers, limites mémoire, etc.)
- Railway, Heroku ou autre plateforme PaaS

### 🔒 Sécurité

Les mots de passe par défaut sont **faibles** et doivent être changés en production :
- PostgreSQL : `odoo_password_2024` → Mot de passe fort
- Odoo admin : `admin` → Mot de passe fort
- PgAdmin : `admin` → Mot de passe fort

### 💾 Sauvegarde des données

Les données sont stockées dans des volumes Docker :
- `eazynova-test-db-data` : Base de données PostgreSQL
- `eazynova-test-data` : Filestore Odoo (fichiers uploadés)

Pour sauvegarder :
```bash
docker run --rm -v eazynova-test-db-data:/data -v $(pwd):/backup ubuntu tar czf /backup/db-backup.tar.gz /data
docker run --rm -v eazynova-test-data:/data -v $(pwd):/backup ubuntu tar czf /backup/odoo-backup.tar.gz /data
```

## 🆘 Support

En cas de problème :
1. Vérifier les logs : `docker-compose -f docker-compose.dev.yml logs`
2. Consulter cette documentation
3. Créer une issue GitHub : https://github.com/MASITH-developpement/EAZYNOVA/issues

## 🎉 Bon test !

Amusez-vous bien avec EAZYNOVA ! 🚀
