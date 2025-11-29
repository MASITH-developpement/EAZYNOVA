# ⚡ Railway Quick Start - EAZYNOVA

Guide rapide pour déployer EAZYNOVA sur Railway en 5 minutes.

## 🚀 Déploiement en 5 étapes

### 1️⃣ Créer le Projet Railway (2 min)

```bash
# Aller sur https://railway.app
# Se connecter avec GitHub
# Cliquer sur "New Project"
# Sélectionner "Deploy from GitHub repo"
# Choisir le repo EAZYNOVA
```

### 2️⃣ Ajouter PostgreSQL (1 min)

```bash
# Dans le projet Railway :
# Cliquer "+ New Service"
# Sélectionner "Database" → "PostgreSQL"
# Railway crée automatiquement la DB
```

### 3️⃣ Configurer les Variables (1 min)

Dans le service **Odoo**, onglet **Variables**, ajouter :

```bash
ODOO_ADMIN_PASSWORD=VotreMotDePasseSecurise123!
ENVIRONMENT=production
```

Les autres variables (PGHOST, PGPORT, etc.) sont **automatiquement injectées** par Railway.

### 4️⃣ Connecter PostgreSQL au Service Odoo (30 sec)

```bash
# Dans le service Odoo, onglet "Variables"
# Cliquer "+ New Variable" → "Add Reference"
# Sélectionner le service PostgreSQL
# Choisir toutes les variables PG* (PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE)
```

### 5️⃣ Déployer ! (30 sec)

```bash
# Railway déploie automatiquement
# Ou cliquer sur "Deploy" dans l'interface
# Attendre 3-5 minutes (build + démarrage)
```

## ✅ Vérification

### Obtenir l'URL :

Dans Railway, onglet **Settings** → **Networking**, vous verrez :
```
https://votre-projet.up.railway.app
```

### Tester :

```bash
# Health check
curl https://votre-projet.up.railway.app/web/health
# Devrait retourner: OK

# Ouvrir dans le navigateur
# https://votre-projet.up.railway.app
```

## 🎉 Initialiser Odoo

1. Ouvrir l'URL de votre application
2. Vous verrez la page de création de base de données
3. Remplir :
   - **Database Name** : `eazynova_prod`
   - **Email** : votre email admin
   - **Password** : le mot de passe défini dans `ODOO_ADMIN_PASSWORD`
   - **Language** : Français
   - **Country** : France
4. Cliquer **"Create Database"**
5. Attendre 1-2 minutes

## 📦 Installer les Modules EAZYNOVA

1. Se connecter avec vos identifiants
2. Aller dans **Applications**
3. Activer le mode développeur : **Paramètres** → **Activer le mode développeur**
4. Mettre à jour la liste : **Applications** → menu **⋮** → **Mettre à jour la liste des applications**
5. Rechercher **"EAZYNOVA"**
6. Cliquer **"Installer"** sur les modules souhaités

## 🔧 Configuration Avancée (Optionnel)

### Domaine Personnalisé :

```bash
# Dans Railway : Settings → Networking
# Cliquer "Add Custom Domain"
# Entrer : odoo.votredomaine.com
# Configurer vos DNS comme indiqué
```

### Activer les Workers (Production) :

Dans le fichier `.env.railway` ou les variables Railway :
```bash
ENVIRONMENT=production
```

Le script `start-odoo.sh` activera automatiquement :
- 2 workers
- 2 threads cron
- Mode production (pas de --dev)

### Consulter les Logs :

```bash
# Dans Railway : Onglet "Logs"
# Ou via CLI :
railway logs
```

## 🐛 Problèmes Courants

### "Application Crashed" ?

1. Vérifier que PostgreSQL est bien démarré
2. Vérifier les variables d'environnement (surtout PGHOST, PGUSER, etc.)
3. Consulter les logs pour voir l'erreur exacte

### "Health Check Failed" ?

1. Attendre 2-3 minutes (Odoo prend du temps à démarrer)
2. Si ça persiste, vérifier les logs
3. Tester manuellement : `curl https://votre-url/web/health`

### "Database Connection Error" ?

1. Vérifier que le service PostgreSQL est actif
2. Vérifier que les variables PG* sont bien injectées dans le service Odoo
3. Dans Railway, vérifier l'onglet "Variables" du service Odoo

## 📚 Documentation Complète

Pour plus de détails, consultez :
- [`RAILWAY_SETUP.md`](./RAILWAY_SETUP.md) - Guide complet
- [`DEPLOYMENT_GUIDE.md`](./DEPLOYMENT_GUIDE.md) - Guide de déploiement général

## 🆘 Support

- Railway Docs : https://docs.railway.app/
- Railway Discord : https://discord.gg/railway
- Odoo Docs : https://www.odoo.com/documentation/19.0/

---

**Version** : 1.0.0
**Temps total** : ~5 minutes
**Difficulté** : Facile 🟢
