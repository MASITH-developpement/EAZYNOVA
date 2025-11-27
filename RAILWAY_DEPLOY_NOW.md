# 🚀 Instructions de Déploiement Railway - MAINTENANT

Vos changements ont été poussés vers GitHub avec succès ! Voici comment déployer sur Railway.

## 📋 Statut des Commits

✅ **Tous les changements ont été committés et poussés vers :**
```
Branch: claude/configure-railway-01BFMjoetfrJMFfTcSHVn5fv
Repository: MASITH-developpement/EAZYNOVA
```

---

## 🎯 Option 1 : Déploiement via Interface Web Railway (Recommandé)

### Étape 1 : Connectez-vous à Railway

1. Allez sur https://railway.app
2. Cliquez sur **"Login"**
3. Connectez-vous avec votre compte GitHub

### Étape 2 : Créer un Nouveau Projet

1. Cliquez sur **"New Project"**
2. Sélectionnez **"Deploy from GitHub repo"**
3. Choisissez le repository **MASITH-developpement/EAZYNOVA**
4. Sélectionnez la branche : **`claude/configure-railway-01BFMjoetfrJMFfTcSHVn5fv`** ou **`main`** (si vous avez mergé)

### Étape 3 : Railway Détecte le Dockerfile

Railway va automatiquement détecter votre `Dockerfile` et configurer le build.

**Important** : Avant de cliquer "Deploy", suivez les étapes suivantes.

### Étape 4 : Ajouter PostgreSQL

**Avant le premier déploiement** :

1. Cliquez sur **"+ New Service"**
2. Sélectionnez **"Database"**
3. Choisissez **"Add PostgreSQL"**
4. Railway crée automatiquement une base PostgreSQL

### Étape 5 : Configurer les Variables d'Environnement

Dans le service **Odoo** (pas PostgreSQL) :

1. Cliquez sur l'onglet **"Variables"**
2. Ajoutez ces variables :

```bash
# OBLIGATOIRE
ODOO_ADMIN_PASSWORD=VotreMotDePasseSecurise123!

# Optionnel (avec valeurs par défaut)
ENVIRONMENT=production
AUTO_INIT_DB=true
INIT_DB_NAME=eazynova_prod
INIT_ADMIN_EMAIL=admin@eazynova.com
INIT_COMPANY_NAME=EAZYNOVA
INIT_COUNTRY=FR
INIT_LANG=fr_FR
```

### Étape 6 : Référencer PostgreSQL dans Odoo

Toujours dans les **Variables** du service Odoo :

1. Cliquez sur **"+ New Variable"** → **"Add Reference"**
2. Sélectionnez le service **PostgreSQL**
3. Référencez ces variables :
   - `PGHOST`
   - `PGPORT`
   - `PGUSER`
   - `PGPASSWORD`
   - `PGDATABASE`

### Étape 7 : Déployer !

1. Cliquez sur **"Deploy"**
2. Railway va :
   - Construire l'image Docker (3-5 minutes)
   - Démarrer PostgreSQL
   - Démarrer Odoo
   - Initialiser la base de données automatiquement
3. Attendez environ **5-8 minutes** pour le premier déploiement

### Étape 8 : Obtenir l'URL

1. Dans le service Odoo, allez dans **Settings** → **Networking**
2. Railway génère automatiquement une URL HTTPS :
   ```
   https://eazynova-production-xxxx.up.railway.app
   ```
3. Copiez cette URL

### Étape 9 : Accéder à Odoo

1. Ouvrez l'URL dans votre navigateur
2. Si `AUTO_INIT_DB=true`, vous serez directement sur la page de connexion
3. Connectez-vous avec :
   - **Email** : `admin@eazynova.com` (ou votre INIT_ADMIN_EMAIL)
   - **Mot de passe** : Voir `ODOO_ADMIN_PASSWORD` dans les variables Railway

4. **Changez immédiatement le mot de passe !**

---

## 🎯 Option 2 : Déploiement via Railway CLI

### Étape 1 : Installer Railway CLI

```bash
npm install -g @railway/cli
```

### Étape 2 : Se Connecter

```bash
railway login
```

Cela ouvrira un navigateur pour vous connecter avec GitHub.

### Étape 3 : Créer le Projet

```bash
cd /home/user/EAZYNOVA

# Lier au repository GitHub
railway link

# Créer un nouveau projet
railway init
```

### Étape 4 : Ajouter PostgreSQL

```bash
# Via l'interface web Railway (plus simple)
# Allez sur railway.app → Votre projet → + New Service → Database → PostgreSQL
```

### Étape 5 : Configurer les Variables

```bash
# Définir les variables
railway variables set ODOO_ADMIN_PASSWORD=VotreMotDePasseSecurise123!
railway variables set ENVIRONMENT=production
railway variables set AUTO_INIT_DB=true
railway variables set INIT_DB_NAME=eazynova_prod
railway variables set INIT_ADMIN_EMAIL=admin@eazynova.com
railway variables set INIT_COMPANY_NAME=EAZYNOVA
railway variables set INIT_COUNTRY=FR
railway variables set INIT_LANG=fr_FR
```

Pour les variables PostgreSQL, utilisez l'interface web (plus simple).

### Étape 6 : Déployer

```bash
# Déployer depuis la branche actuelle
railway up

# Ou spécifier une branche
railway up --branch claude/configure-railway-01BFMjoetfrJMFfTcSHVn5fv
```

### Étape 7 : Suivre les Logs

```bash
railway logs
```

### Étape 8 : Obtenir l'URL

```bash
railway open
```

Cela ouvrira votre projet dans le navigateur.

---

## 🎯 Option 3 : Déploiement en Un Clic (Template)

**⚠️ Important** : Pour utiliser cette option, vous devez d'abord :

1. **Merger** la branche `claude/configure-railway-01BFMjoetfrJMFfTcSHVn5fv` dans `main`
2. **Pousser** vers GitHub

### Étapes :

```bash
# Merger dans main
git checkout main
git pull origin main
git merge claude/configure-railway-01BFMjoetfrJMFfTcSHVn5fv
git push origin main
```

### Ensuite :

Cliquez sur ce bouton depuis le README :

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/new?template=https://github.com/MASITH-developpement/EAZYNOVA)

Railway va automatiquement :
- Créer le projet
- Configurer PostgreSQL
- Configurer Odoo
- Générer les secrets
- Déployer tout automatiquement

---

## 📊 Vérifications Post-Déploiement

### 1. Vérifier que PostgreSQL fonctionne

Dans Railway → Service PostgreSQL → **Logs** :
```
PostgreSQL init process complete; ready for start up.
database system is ready to accept connections
```

### 2. Vérifier les Logs Odoo

Dans Railway → Service Odoo → **Logs**, vous devriez voir :

```
==========================================
EAZYNOVA - Initialisation Railway
==========================================
⏳ Attente de PostgreSQL...
✅ PostgreSQL est prêt !
🔍 Vérification de l'existence de la base de données 'eazynova_prod'...
🆕 La base de données 'eazynova_prod' n'existe pas
   Création et initialisation en cours...
📦 Création de la base de données Odoo...
✅ Base de données 'eazynova_prod' créée avec succès !
⚙️  Configuration post-initialisation...
✅ Configuration post-initialisation terminée !
==========================================
✅ INITIALISATION TERMINÉE AVEC SUCCÈS !
==========================================
Odoo server is running...
```

### 3. Vérifier le Health Check

```bash
curl https://votre-url.up.railway.app/web/health
```

Doit retourner : `OK`

### 4. Accéder à l'Interface

Ouvrez : `https://votre-url.up.railway.app`

---

## 🐛 Problèmes Courants

### "Build Failed"

**Cause** : Erreur dans le Dockerfile ou dépendances manquantes.

**Solution** :
1. Vérifiez les logs de build dans Railway
2. Assurez-vous que tous les fichiers sont bien poussés
3. Vérifiez que `init-railway.sh` et `start-odoo.sh` sont exécutables

### "Application Crashed"

**Cause** : Variables manquantes ou PostgreSQL non accessible.

**Solution** :
1. Vérifiez que PostgreSQL est démarré
2. Vérifiez les variables : `PGHOST`, `PGPORT`, etc.
3. Consultez les logs Odoo

### "Database Connection Error"

**Cause** : PostgreSQL non référencé dans Odoo.

**Solution** :
1. Allez dans Service Odoo → Variables
2. Assurez-vous que les variables PG* sont bien référencées
3. Redéployez

### "Health Check Failed"

**Cause** : Odoo prend du temps à démarrer.

**Solution** : Attendez 3-5 minutes. Le premier démarrage est long.

---

## 📞 Besoin d'Aide ?

Consultez :
- [`RAILWAY_DEPLOY.md`](./RAILWAY_DEPLOY.md) - Guide complet
- [`RAILWAY_SETUP.md`](./RAILWAY_SETUP.md) - Configuration détaillée
- Railway Discord : https://discord.gg/railway
- Railway Docs : https://docs.railway.app/

---

## ✅ Checklist Finale

Avant de déployer, vérifiez :

- [ ] Branche poussée vers GitHub
- [ ] Compte Railway créé et connecté à GitHub
- [ ] PostgreSQL ajouté au projet
- [ ] Variables d'environnement configurées
- [ ] Variables PostgreSQL référencées dans Odoo
- [ ] Prêt à attendre 5-8 minutes pour le build

**Tout est prêt ? Lancez le déploiement !** 🚀

---

**Date** : 2025-11-27
**Statut** : ✅ Prêt pour déploiement
**Branch** : `claude/configure-railway-01BFMjoetfrJMFfTcSHVn5fv`
