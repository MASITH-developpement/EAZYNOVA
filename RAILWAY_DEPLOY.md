# 🚂 Déploiement Railway en Un Clic

Déployez EAZYNOVA (Odoo 19) sur Railway automatiquement avec PostgreSQL inclus.

## 🎯 Déploiement Automatique

### Option 1 : Bouton "Deploy on Railway" (Recommandé)

Cliquez sur le bouton ci-dessous pour déployer automatiquement :

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/new?template=https://github.com/MASITH-developpement/EAZYNOVA)

Ce bouton va :
- ✅ Créer un projet Railway
- ✅ Déployer PostgreSQL automatiquement
- ✅ Déployer Odoo 19 avec vos modules EAZYNOVA
- ✅ Configurer toutes les variables d'environnement
- ✅ Lier PostgreSQL à Odoo
- ✅ Initialiser la base de données Odoo automatiquement
- ✅ Générer une URL HTTPS publique

**Temps total : ~5-8 minutes** ⏱️

---

### Option 2 : Via Railway CLI

```bash
# Installer Railway CLI
npm install -g @railway/cli

# Se connecter
railway login

# Créer et déployer depuis le template
railway init --template https://github.com/MASITH-developpement/EAZYNOVA

# Suivre les logs
railway logs
```

---

### Option 3 : Configuration Manuelle

Si vous préférez configurer manuellement, suivez le guide complet : [`RAILWAY_SETUP.md`](./RAILWAY_SETUP.md)

---

## ⚙️ Variables d'Environnement (Configuration Automatique)

Le template Railway configure automatiquement :

### 🔐 Générées Automatiquement

Ces variables sont générées automatiquement de manière sécurisée :

| Variable | Description | Valeur |
|----------|-------------|---------|
| `ODOO_ADMIN_PASSWORD` | Mot de passe maître Odoo | *(secret généré)* |
| `PGPASSWORD` | Mot de passe PostgreSQL | *(secret généré)* |
| `PGHOST` | Hôte PostgreSQL | *(injecté par Railway)* |
| `PGPORT` | Port PostgreSQL | *(injecté par Railway)* |
| `PGUSER` | Utilisateur PostgreSQL | `odoo` |
| `PGDATABASE` | Base de données | `eazynova` |

### 🎨 Personnalisables

Vous pouvez modifier ces variables après le déploiement :

| Variable | Description | Valeur par défaut |
|----------|-------------|-------------------|
| `ENVIRONMENT` | Environnement (production/development) | `production` |
| `AUTO_INIT_DB` | Initialiser la DB automatiquement | `true` |
| `INIT_DB_NAME` | Nom de la base Odoo | `eazynova_prod` |
| `INIT_ADMIN_EMAIL` | Email administrateur | `admin@eazynova.com` |
| `INIT_COMPANY_NAME` | Nom de l'entreprise | `EAZYNOVA` |
| `INIT_COUNTRY` | Code pays | `FR` |
| `INIT_LANG` | Langue | `fr_FR` |

---

## 🚀 Après le Déploiement

### 1. Obtenir Votre URL

Railway génère automatiquement une URL HTTPS :
```
https://eazynova-production-xxxx.up.railway.app
```

Vous la trouverez dans :
- Railway Dashboard → Votre service → **Settings** → **Networking**

### 2. Initialisation Automatique

Si `AUTO_INIT_DB=true` (par défaut), au premier démarrage :

1. ✅ PostgreSQL est créé et configuré
2. ✅ La base de données Odoo est créée automatiquement
3. ✅ L'entreprise et l'admin sont configurés
4. ✅ La langue française est activée

**Vous pouvez vous connecter immédiatement !**

### 3. Connexion Initiale

```
URL: https://votre-url.up.railway.app
Email: admin@eazynova.com (ou votre INIT_ADMIN_EMAIL)
Mot de passe: Consultez la variable ODOO_ADMIN_PASSWORD dans Railway
```

Pour voir le mot de passe :
1. Railway Dashboard → Service Odoo → **Variables**
2. Cherchez `ODOO_ADMIN_PASSWORD`
3. Cliquez sur l'icône œil pour révéler

### 4. Premier Login

1. Ouvrez votre URL Railway
2. Vous serez directement sur la page de connexion Odoo
3. Entrez vos identifiants
4. **Changez immédiatement le mot de passe !**
   - Menu utilisateur (en haut à droite) → **Préférences** → **Mot de passe**

### 5. Installer les Modules EAZYNOVA

1. Activez le mode développeur :
   - **Paramètres** → Tout en bas : **Activer le mode développeur**

2. Mettez à jour la liste des applications :
   - **Applications** → menu **⋮** (3 points) → **Mettre à jour la liste des applications**

3. Recherchez et installez :
   - **EAZYNOVA Core**
   - **EAZYNOVA Planning** (gestion de chantiers)
   - **EAZYNOVA Reconnaissance Faciale** (authentification biométrique)
   - Autres modules selon vos besoins

---

## 🔧 Configuration Avancée

### Désactiver l'Initialisation Automatique

Si vous préférez créer la base manuellement :

1. Railway Dashboard → Service Odoo → **Variables**
2. Modifiez `AUTO_INIT_DB` → `false`
3. Redéployez

Au démarrage, vous aurez la page Odoo standard de création de DB.

### Activer le Mode Développement

Pour le développement local ou les tests :

1. Modifiez `ENVIRONMENT` → `development`
2. Redéployez

Cela active :
- Mode `--dev=all` d'Odoo
- Logs en niveau `debug`
- 0 workers (meilleur pour le debug)

### Ajouter un Domaine Personnalisé

1. Railway Dashboard → Service Odoo → **Settings** → **Networking**
2. Cliquez **Add Custom Domain**
3. Entrez votre domaine : `odoo.votredomaine.com`
4. Configurez vos DNS comme indiqué
5. HTTPS est automatique (Let's Encrypt)

---

## 📊 Monitoring et Logs

### Consulter les Logs en Temps Réel

```bash
# Via Railway CLI
railway logs

# Ou dans l'interface web
# Railway Dashboard → Service Odoo → Onglet "Logs"
```

### Logs d'Initialisation

Au premier démarrage, vous verrez :

```
==========================================
EAZYNOVA - Initialisation Railway
==========================================
Configuration d'initialisation :
  - AUTO_INIT_DB: true
  - DB Name: eazynova_prod
  - Admin Email: admin@eazynova.com
  - Company: EAZYNOVA
  - Country: FR
  - Language: fr_FR
==========================================
⏳ Attente de PostgreSQL...
✅ PostgreSQL est prêt !
🔍 Vérification de l'existence de la base de données 'eazynova_prod'...
🆕 La base de données 'eazynova_prod' n'existe pas
   Création et initialisation en cours...
📦 Création de la base de données Odoo...
🚀 Initialisation d'Odoo avec la base 'eazynova_prod'...
✅ Base de données 'eazynova_prod' créée avec succès !
⚙️  Configuration post-initialisation...
✅ Configuration post-initialisation terminée !
==========================================
✅ INITIALISATION TERMINÉE AVEC SUCCÈS !
==========================================
```

### Métriques

Railway fournit automatiquement :
- CPU Usage
- Memory Usage (RAM)
- Network Traffic
- Disk Usage
- Response Times

Consultez-les : Railway Dashboard → Service → **Metrics**

---

## 🐛 Dépannage

### "Application Crashed" au démarrage

**Vérifications** :
1. PostgreSQL est-il démarré ? (Railway Dashboard → Service PostgreSQL)
2. Les variables sont-elles injectées ? (Service Odoo → Variables)
3. Consultez les logs : cherchez "ERROR" ou "CRITICAL"

**Solution** :
```bash
# Redéployer
railway up --detach
```

### "Health Check Failed"

**Cause** : Odoo met 2-3 minutes à démarrer (surtout au premier lancement).

**Solution** : Attendez 3-5 minutes. Si ça persiste :

```bash
# Tester manuellement
curl https://votre-url.up.railway.app/web/health

# Devrait retourner : OK
```

### Impossible de se connecter

**Vérifications** :
1. La base de données est-elle créée ?
   - Logs : cherchez "Base de données 'eazynova_prod' créée"
2. Le mot de passe est-il correct ?
   - Railway → Variables → `ODOO_ADMIN_PASSWORD`

**Solution** :
```bash
# Voir les variables
railway variables

# Réinitialiser le mot de passe (en modifiant la variable)
railway variables set ODOO_ADMIN_PASSWORD=NouveauMotDePasse123!
```

### Base de données non initialisée

**Cause** : `AUTO_INIT_DB` est à `false` ou l'initialisation a échoué.

**Solution** :

Option A - Initialisation manuelle :
1. Ouvrez votre URL
2. Vous verrez la page de création de DB
3. Créez la base manuellement

Option B - Réactiver l'auto-init :
```bash
railway variables set AUTO_INIT_DB=true
railway up --detach
```

---

## 🔄 Mises à Jour et Redéploiements

### Déploiement Automatique

Chaque commit sur votre branche `main` déclenche un redéploiement automatique.

```bash
git add .
git commit -m "Mise à jour des modules EAZYNOVA"
git push origin main

# Railway redéploie automatiquement
```

### Déploiement Manuel

```bash
# Via CLI
railway up

# Ou dans l'interface web
# Railway Dashboard → Deployments → Deploy
```

### Rollback

Si un déploiement échoue :

1. Railway Dashboard → **Deployments**
2. Trouvez un déploiement précédent réussi (✅)
3. Cliquez **⋮** → **Redeploy**

---

## 💰 Coûts Railway

### Plan Gratuit (Hobby)

- ✅ $5/mois de crédit gratuit
- ✅ 500 heures d'exécution/mois
- ✅ 1 GB RAM
- ✅ 1 GB Disk
- ✅ HTTPS inclus
- ⚠️ Peut être limité pour production intensive

### Plan Payant (Developer+)

- ✅ $5/mois de base + utilisation
- ✅ RAM illimitée (payant à l'usage)
- ✅ Disk jusqu'à 100 GB
- ✅ Backups automatiques
- ✅ Support prioritaire

**Estimation pour EAZYNOVA** :
- Petit usage : ~$5-10/mois (plan gratuit suffisant)
- Usage moyen : ~$15-25/mois
- Usage intensif : ~$40-60/mois

---

## 🔐 Sécurité et Best Practices

### ✅ Checklist de Sécurité

Après le déploiement :

- [ ] Changez le mot de passe admin
- [ ] Configurez un domaine personnalisé (HTTPS)
- [ ] Activez l'authentification à deux facteurs (Railway)
- [ ] Limitez les accès à votre projet Railway (Team settings)
- [ ] Configurez des backups réguliers
- [ ] Surveillez les logs pour détecter les anomalies

### 🔒 Variables Sensibles

**JAMAIS** :
- ❌ Commiter `.env` ou `.env.railway` dans Git
- ❌ Partager `ODOO_ADMIN_PASSWORD` publiquement
- ❌ Utiliser des mots de passe faibles

**TOUJOURS** :
- ✅ Utiliser les secrets générés par Railway
- ✅ Activer l'authentification à deux facteurs
- ✅ Changer les mots de passe régulièrement

---

## 📚 Ressources

- [RAILWAY_SETUP.md](./RAILWAY_SETUP.md) - Guide complet étape par étape
- [RAILWAY_QUICKSTART.md](./RAILWAY_QUICKSTART.md) - Guide rapide (5 min)
- [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) - Guide de déploiement général
- [Railway Documentation](https://docs.railway.app/)
- [Odoo 19 Documentation](https://www.odoo.com/documentation/19.0/)

---

## 🆘 Support

**Problème avec Railway** :
- Railway Discord : https://discord.gg/railway
- Railway Docs : https://docs.railway.app/
- Railway Status : https://status.railway.app/

**Problème avec Odoo/EAZYNOVA** :
- Consultez les logs Railway
- Vérifiez le fichier `RAILWAY_SETUP.md` (section Troubleshooting)
- Odoo Community : https://www.odoo.com/forum

---

**Prêt à déployer ?** Cliquez sur le bouton ci-dessous ! 👇

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/new?template=https://github.com/MASITH-developpement/EAZYNOVA)

---

**Version** : 1.0.0
**Date** : 2025-11-27
**Auteur** : MASITH Développement
**Projet** : EAZYNOVA - Odoo 19 SaaS
