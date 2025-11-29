# 🚂 Guide de Configuration Railway - EAZYNOVA Odoo 19

Ce guide vous aidera à déployer votre application EAZYNOVA (Odoo 19) sur Railway.app avec PostgreSQL.

## 📋 Pré-requis

- Un compte Railway.app (gratuit ou payant)
- Git installé localement
- Accès à ce repository GitHub
- Variables d'environnement à préparer

---

## 🎯 Architecture du Déploiement

Sur Railway, vous aurez **2 services** :

1. **PostgreSQL Database** - Base de données gérée par Railway
2. **Odoo Application** - Votre application EAZYNOVA

---

## 📦 Étape 1 : Créer un Nouveau Projet Railway

### Via l'interface web Railway :

1. Connectez-vous sur [railway.app](https://railway.app)
2. Cliquez sur **"New Project"**
3. Choisissez **"Deploy from GitHub repo"**
4. Sélectionnez votre repository **EAZYNOVA**
5. Railway détectera automatiquement le `Dockerfile`

---

## 🗄️ Étape 2 : Ajouter PostgreSQL

### Dans votre projet Railway :

1. Cliquez sur **"+ New Service"**
2. Sélectionnez **"Database"**
3. Choisissez **"Add PostgreSQL"**
4. Railway créera automatiquement une base de données PostgreSQL

### Variables automatiques créées :

Railway créera automatiquement ces variables pour vous :
- `DATABASE_URL`
- `PGHOST`
- `PGPORT`
- `PGUSER`
- `PGPASSWORD`
- `PGDATABASE`

**Important** : Ces variables sont automatiquement injectées dans votre service Odoo.

---

## ⚙️ Étape 3 : Configurer les Variables d'Environnement

### Dans le service Odoo :

1. Cliquez sur votre service **Odoo**
2. Allez dans l'onglet **"Variables"**
3. Ajoutez les variables suivantes :

#### Variables OBLIGATOIRES :

```bash
# Mot de passe admin Odoo (IMPORTANT!)
ODOO_ADMIN_PASSWORD=VotreMotDePasseSecurise123!

# Port (fourni automatiquement par Railway, mais vous pouvez le définir)
PORT=8069
```

#### Variables PostgreSQL (Référencez celles de votre service PostgreSQL) :

Si Railway ne les injecte pas automatiquement, vous pouvez les référencer manuellement :

1. Dans l'onglet "Variables" du service Odoo
2. Cliquez sur **"+ New Variable"** → **"Add Reference"**
3. Sélectionnez votre service PostgreSQL
4. Choisissez les variables suivantes :
   - `PGHOST`
   - `PGPORT`
   - `PGUSER`
   - `PGPASSWORD`
   - `PGDATABASE`

#### Variables optionnelles :

```bash
# Environnement
ENVIRONMENT=production

# Nom de base de données personnalisé (optionnel)
# PGDATABASE=eazynova_prod

# Configuration Email (optionnel)
# SMTP_SERVER=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USER=votre-email@gmail.com
# SMTP_PASSWORD=votre-mot-de-passe-app
```

---

## 🔧 Étape 4 : Configuration des Settings Railway

### Dans le service Odoo :

#### 1. **Settings** → **General** :
- **Service Name** : `eazynova-odoo` (ou votre nom préféré)
- **Branch** : `main` ou `claude/configure-railway-01BFMjoetfrJMFfTcSHVn5fv`

#### 2. **Settings** → **Networking** :
- Railway génèrera automatiquement une URL publique
- Format : `https://votre-projet.up.railway.app`
- Vous pouvez aussi configurer un domaine personnalisé

#### 3. **Settings** → **Deploy** :
- **Watch Paths** : Laissez vide pour déployer sur chaque commit
- **Build Command** : Automatique (utilise le Dockerfile)
- **Start Command** : `/start-odoo.sh` (défini dans railway.toml)

#### 4. **Settings** → **Health Check** :
- **Health Check Path** : `/web/health`
- **Health Check Timeout** : `100` secondes
- Railway utilisera cela pour vérifier que Odoo démarre correctement

---

## 🚀 Étape 5 : Premier Déploiement

### Méthode automatique (via GitHub) :

1. Railway détecte automatiquement les commits sur votre branche
2. Pushez vos changements :
   ```bash
   git add .
   git commit -m "Configuration Railway"
   git push origin claude/configure-railway-01BFMjoetfrJMFfTcSHVn5fv
   ```
3. Railway commencera le build automatiquement
4. Attendez 3-5 minutes (première installation d'Odoo)

### Suivre le déploiement :

1. Dans Railway, cliquez sur votre service Odoo
2. Allez dans l'onglet **"Deployments"**
3. Cliquez sur le déploiement en cours
4. Vous verrez les logs en temps réel

### Logs typiques d'un démarrage réussi :

```
Step 1/15 : FROM ubuntu:22.04
Step 2/15 : USER root
...
Step 15/15 : CMD ["/start-odoo.sh"]
Successfully built abc123def456
==========================================
Démarrage Odoo 19 - EAZYNOVA
==========================================
PostgreSQL Host: postgres.railway.internal
PostgreSQL Port: 5432
✓ PostgreSQL est prêt !
Nettoyage des assets...
Base de données: railway
URL publique: https://eazynova.up.railway.app
==========================================
Odoo server is running...
```

---

## 🔍 Étape 6 : Vérification et Tests

### 1. Accéder à votre application :

Ouvrez l'URL fournie par Railway (ex: `https://votre-projet.up.railway.app`)

### 2. Premier accès - Initialisation de la base de données :

Odoo affichera une page pour créer la base de données :

1. **Database Name** : `eazynova_prod` (ou votre choix)
2. **Email** : Votre email admin
3. **Password** : Le mot de passe défini dans `ODOO_ADMIN_PASSWORD`
4. **Language** : Français
5. **Country** : France
6. Cliquez sur **"Create Database"**

### 3. Installer les modules EAZYNOVA :

Après la création de la DB :

1. Connectez-vous avec vos identifiants
2. Allez dans **Applications**
3. Activez le **mode développeur** : Paramètres → Activer le mode développeur
4. Mettez à jour la liste : Applications → ⋮ → Mettre à jour la liste des applications
5. Recherchez **"EAZYNOVA"**
6. Installez les modules :
   - **EAZYNOVA Core**
   - **EAZYNOVA Planning** (si disponible)
   - **EAZYNOVA Reconnaissance Faciale** (si disponible)
   - Autres modules selon vos besoins

### 4. Vérifier le Health Check :

Testez l'endpoint de santé :
```bash
curl https://votre-projet.up.railway.app/web/health
```

Réponse attendue :
```
OK
```

---

## 📊 Étape 7 : Monitoring et Logs

### Consulter les logs :

1. Dans Railway, cliquez sur votre service Odoo
2. Allez dans l'onglet **"Logs"**
3. Vous verrez les logs en temps réel

### Logs utiles pour débugger :

```bash
# Rechercher des erreurs
Grep "ERROR" dans les logs Railway

# Vérifier la connexion PostgreSQL
Grep "PostgreSQL" dans les logs

# Vérifier le démarrage Odoo
Grep "Odoo server" dans les logs
```

### Métriques :

Railway fournit automatiquement :
- **CPU Usage**
- **Memory Usage**
- **Network Traffic**
- **Response Times**

Consultez-les dans l'onglet **"Metrics"** de votre service.

---

## 🔐 Étape 8 : Sécurité et Best Practices

### 1. Sécuriser le mot de passe admin :

**IMPORTANT** : Changez `ODOO_ADMIN_PASSWORD` après le premier déploiement

```bash
# Dans Railway Variables, utilisez un générateur de mot de passe
# Exemple : openssl rand -base64 32
```

### 2. Configurer un domaine personnalisé (optionnel) :

1. Dans Railway, allez dans **Settings** → **Networking**
2. Cliquez sur **"Add Custom Domain"**
3. Suivez les instructions pour configurer vos DNS

### 3. Activer HTTPS :

Railway active automatiquement HTTPS pour tous les domaines (gratuit avec Let's Encrypt)

### 4. Limiter l'accès à la base de données :

Dans les settings PostgreSQL :
- Notez que seul votre service Odoo peut y accéder (réseau interne Railway)
- Pas d'accès public par défaut (sécurisé)

### 5. Backups de la base de données :

Railway Pro propose des backups automatiques. Sinon, configurez des backups manuels :

```bash
# Installer Railway CLI
npm install -g @railway/cli

# Se connecter
railway login

# Dumper la base de données
railway run pg_dump $DATABASE_URL > backup.sql
```

---

## 🐛 Résolution de Problèmes

### Problème 1 : "Build Failed"

**Causes possibles** :
- Erreur dans le Dockerfile
- Dépendances manquantes

**Solution** :
1. Vérifiez les logs de build dans Railway
2. Assurez-vous que tous les fichiers nécessaires sont commités
3. Vérifiez que `requirements.txt` est à jour

### Problème 2 : "Application Crashed"

**Causes possibles** :
- Variables d'environnement manquantes
- PostgreSQL non accessible
- Port incorrect

**Solution** :
1. Vérifiez que toutes les variables sont définies
2. Vérifiez les logs : recherchez "ERROR" ou "CRITICAL"
3. Vérifiez que PostgreSQL est bien démarré et accessible

### Problème 3 : "Health Check Failed"

**Causes possibles** :
- Odoo met trop de temps à démarrer
- Route `/web/health` non accessible

**Solution** :
1. Augmentez `healthcheckTimeout` à 200 dans `railway.toml`
2. Vérifiez les logs de démarrage
3. Testez manuellement : `curl https://votre-url/web/health`

### Problème 4 : "Database Connection Error"

**Causes possibles** :
- Variables PostgreSQL incorrectes
- Service PostgreSQL non démarré

**Solution** :
1. Vérifiez que le service PostgreSQL est actif dans Railway
2. Vérifiez les variables : `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`
3. Testez la connexion dans les logs : recherchez "PostgreSQL est prêt"

### Problème 5 : "Module Not Found"

**Causes possibles** :
- Addons non copiés dans l'image Docker
- Chemin `addons_path` incorrect

**Solution** :
1. Vérifiez le Dockerfile : ligne `COPY addons/addons-perso /opt/odoo/custom_addons`
2. Vérifiez `start-odoo.sh` : paramètre `--addons-path`
3. Reconstruisez l'image : dans Railway, allez dans Deployments → Redeploy

---

## 📈 Optimisation pour Production

### 1. Activer les Workers :

Dans `start-odoo.sh`, remplacez :
```bash
--workers=0
```
Par :
```bash
--workers=2
```

**Note** : Les workers nécessitent plus de RAM. Vérifiez votre plan Railway.

### 2. Configurer les limites de mémoire :

Railway ajuste automatiquement selon votre plan :
- **Starter** : 512 MB RAM
- **Developer** : 8 GB RAM
- **Team** : 32 GB RAM

Pour Odoo, recommandé : minimum 2 GB RAM

### 3. Activer le mode production :

Dans `start-odoo.sh`, retirez :
```bash
--dev=all
```

Cela désactive le mode développeur et améliore les performances.

### 4. Configurer le cron :

Les crons Odoo fonctionnent automatiquement. Pour ajuster :
```bash
--max-cron-threads=2
```

---

## 🎉 Checklist Finale

Avant de mettre en production :

- [ ] PostgreSQL déployé et accessible
- [ ] Service Odoo déployé et démarré
- [ ] Variables d'environnement configurées (surtout `ODOO_ADMIN_PASSWORD`)
- [ ] Health check réussi (`/web/health` retourne "OK")
- [ ] Base de données créée et initialisée
- [ ] Modules EAZYNOVA installés
- [ ] Tests de connexion (login/logout)
- [ ] Tests des fonctionnalités clés (reconnaissance faciale, etc.)
- [ ] HTTPS actif (automatique avec Railway)
- [ ] Domaine personnalisé configuré (optionnel)
- [ ] Backups configurés
- [ ] Monitoring actif (vérifier les métriques Railway)

---

## 📞 Support et Ressources

### Documentation officielle :
- [Railway Docs](https://docs.railway.app/)
- [Odoo 19 Documentation](https://www.odoo.com/documentation/19.0/)

### Commandes Railway CLI utiles :

```bash
# Installer Railway CLI
npm install -g @railway/cli

# Se connecter
railway login

# Lister les projets
railway list

# Se connecter à un projet
railway link

# Voir les logs en temps réel
railway logs

# Ouvrir l'interface web
railway open

# Exécuter une commande dans le container
railway run bash
```

### Liens utiles :
- Dashboard Railway : https://railway.app/dashboard
- Status Railway : https://status.railway.app/
- Community Railway : https://discord.gg/railway

---

## 🔄 Mises à Jour et Redéploiements

### Déploiement automatique :

Chaque push sur la branche configurée déclenchera un redéploiement automatique.

### Déploiement manuel :

1. Dans Railway, allez dans **Deployments**
2. Cliquez sur **"Deploy"** → **"Redeploy"**

### Rollback :

1. Dans **Deployments**, trouvez un déploiement précédent réussi
2. Cliquez sur **⋮** → **"Redeploy"**

---

**Version** : 1.0.0
**Date** : 2025-11-27
**Auteur** : Claude Code
**Projet** : EAZYNOVA - Odoo 19 SaaS
