# 🚀 EAZYNOVA - Démarrage Rapide

**3 façons de déployer EAZYNOVA Odoo 19 sur Railway**

---

## 🎯 Quelle Méthode Choisir ?

| Méthode | Temps | Difficulté | Cas d'Usage |
|---------|-------|------------|-------------|
| **1. Lien Direct** | 1 clic + 5-8 min | ⭐ Facile | Déploiement unique |
| **2. Script `deploy.sh`** | 1 commande + 5-8 min | ⭐⭐ Moyen | Multiple instances manuelles |
| **3. Auto-Provisioning** | API + 5-8 min | ⭐⭐⭐ Avancé | SaaS multi-tenant automatique |

---

## 📌 Méthode 1 : Lien Direct (Recommandé pour Débuter)

**Le plus simple - Un seul clic !**

### Étape Unique

Cliquez sur ce lien :

```
https://railway.app/new?template=https://github.com/MASITH-developpement/EAZYNOVA
```

Ou utilisez ce bouton :

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new?template=https://github.com/MASITH-developpement/EAZYNOVA)

**C'est tout !** Railway va :
- ✅ Détecter `railway.json`
- ✅ Créer PostgreSQL + Odoo automatiquement
- ✅ Configurer les 18 variables
- ✅ Générer les secrets
- ✅ Déployer en production

**Documentation complète** : [RAILWAY_DIRECT_LINK.md](RAILWAY_DIRECT_LINK.md)

---

## 📌 Méthode 2 : Script `deploy.sh` (Flexible)

**Pour créer plusieurs instances facilement**

### Prérequis

Node.js seulement : https://nodejs.org/

### Une Seule Commande

```bash
./deploy.sh
```

Le script fait TOUT automatiquement :
- ✅ Installe Railway CLI si nécessaire
- ✅ Se connecte à Railway
- ✅ Lit `railway.json`
- ✅ Crée tous les services
- ✅ Déploie

**Créer plusieurs instances** :

```bash
# Production
./deploy.sh
# Nommez : eazynova-production

# Staging
./deploy.sh
# Nommez : eazynova-staging

# Dev
./deploy.sh
# Nommez : eazynova-dev
```

**Documentation complète** : [DEPLOY.md](DEPLOY.md)

---

## 📌 Méthode 3 : Auto-Provisioning (SaaS Multi-Tenant)

**Pour créer des instances automatiquement depuis un site web**

### Architecture

```
Site Web Client → API → Railway → Instance EAZYNOVA
```

### Installation

```bash
# 1. Obtenir le token Railway
railway whoami --token

# 2. Configurer le token
export RAILWAY_API_TOKEN=your-token-here
```

### Option A : Ligne de Commande

```bash
# Créer une instance pour un client
node create-instance.js acme-corp admin@acme.com
```

### Option B : Serveur API

```bash
# Démarrer le serveur
node api-server.js

# Interface web sur http://localhost:3000
```

### Option C : Intégration Site Web

```javascript
// Depuis votre site web
const response = await fetch('https://votre-api.com/api/instances', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        clientName: 'acme-corp',
        adminEmail: 'admin@acme.com',
        companyName: 'ACME Corporation'
    })
});

const data = await response.json();
// Instance créée automatiquement en 5-8 minutes
```

**Documentation complète** : [AUTO_PROVISIONING.md](AUTO_PROVISIONING.md)

---

## 🔑 Après le Déploiement

### Obtenir l'URL

**Via Interface Web :**
1. Allez sur https://railway.app/dashboard
2. Cliquez sur votre projet
3. Service Odoo → Settings → Networking
4. URL : `https://eazynova-xxxx.up.railway.app`

**Via CLI :**
```bash
railway open
```

### Obtenir le Mot de Passe Admin

**Via Interface Web :**
1. Service Odoo → Variables
2. Cherchez `ODOO_ADMIN_PASSWORD`

**Via CLI :**
```bash
railway variables | grep ODOO_ADMIN_PASSWORD
```

### Se Connecter à Odoo

```
URL: https://eazynova-xxxx.up.railway.app
Email: admin@eazynova.com
Mot de passe: [Voir ci-dessus]
```

---

## 📊 Configuration Automatique

Toutes les méthodes utilisent `railway.json` qui configure automatiquement :

### Services Créés

- ✅ **PostgreSQL 15** : Base de données
- ✅ **Odoo 19** : Application ERP/SaaS

### Variables d'Environnement (18 au total)

| Variable | Valeur par Défaut | Type |
|----------|------------------|------|
| `ODOO_ADMIN_PASSWORD` | *Généré automatiquement* | Secret |
| `ENVIRONMENT` | `production` | String |
| `AUTO_INIT_DB` | `true` | Boolean |
| `INIT_DB_NAME` | `eazynova_prod` | String |
| `INIT_ADMIN_EMAIL` | `admin@eazynova.com` | Email |
| `INIT_COMPANY_NAME` | `EAZYNOVA` | String |
| `INIT_COMPANY_COUNTRY` | `FR` | Country Code |
| `INIT_LANG` | `fr_FR` | Locale |
| `PGDATABASE` | Référence PostgreSQL | Reference |
| `PGHOST` | Référence PostgreSQL | Reference |
| `PGPORT` | Référence PostgreSQL | Reference |
| `PGUSER` | Référence PostgreSQL | Reference |
| `PGPASSWORD` | Référence PostgreSQL | Reference |
| ... | ... | ... |

---

## 🛠️ Dépannage

### Problème : 404 sur le Lien Direct

**Solution** : Assurez-vous que le code est dans la branche `main` du repository.

### Problème : "File too large"

**Solution** : Déployez depuis GitHub (automatique avec lien direct et `deploy.sh`)

### Problème : Railway CLI non installé

**Solution** :
```bash
# Via npm
npm install -g @railway/cli

# Via Homebrew (macOS)
brew install railway
```

### Problème : Variables non définies

**Solution** : Elles sont créées automatiquement par `railway.json`. Vérifiez que Railway a bien détecté le fichier.

---

## 📈 Scalabilité

### Coût par Instance

- PostgreSQL : ~$3-5/mois
- Odoo : ~$5-10/mois
- **Total : ~$8-15/mois**

### Modèle SaaS Recommandé

- Client paie : **$49/mois**
- Coût instance : **$10/mois**
- **Marge : $39/mois par client**

### Capacité

- **Instances simultanées** : Illimitées (limité par compte Railway)
- **Temps de création** : 5-8 minutes
- **Isolation** : Chaque client a sa propre instance

---

## 📚 Documentation Complète

| Fichier | Description |
|---------|-------------|
| [DEPLOY.md](DEPLOY.md) | Déploiement via script `deploy.sh` |
| [RAILWAY_DIRECT_LINK.md](RAILWAY_DIRECT_LINK.md) | Lien direct Railway |
| [AUTO_PROVISIONING.md](AUTO_PROVISIONING.md) | Système d'auto-provisioning |
| [RAILWAY_FIX_404.md](RAILWAY_FIX_404.md) | Résolution erreur 404 |

---

## ✅ Checklist de Production

Avant de lancer en production :

- [ ] Token Railway sécurisé (variable d'environnement)
- [ ] Rate limiting configuré (si auto-provisioning)
- [ ] Base de données pour tracking des instances
- [ ] Système de queue pour créations multiples
- [ ] Emails de notification configurés
- [ ] Monitoring et alertes
- [ ] Backup et récupération
- [ ] Documentation client
- [ ] Support technique

---

## 🎓 Exemples Complets

### Déploiement Simple

```bash
# Cloner le repo
git clone https://github.com/MASITH-developpement/EAZYNOVA.git
cd EAZYNOVA

# Déployer
./deploy.sh
```

### Multi-Tenant SaaS

```bash
# Installer les dépendances
npm install

# Obtenir le token Railway
export RAILWAY_API_TOKEN=$(railway whoami --token)

# Créer une instance pour un client
node create-instance.js client1 admin@client1.com

# Ou démarrer le serveur API
node api-server.js
```

---

## 🚀 Commencer Maintenant

**Choix Rapide :**

1. **Je veux tester rapidement** → [Lien Direct](#-méthode-1--lien-direct-recommandé-pour-débuter)
2. **Je veux plusieurs instances** → [Script deploy.sh](#-méthode-2--script-deploysh-flexible)
3. **Je veux un SaaS multi-tenant** → [Auto-Provisioning](#-méthode-3--auto-provisioning-saas-multi-tenant)

---

**Version** : 1.0.0
**Date** : 2025-11-28
**Repository** : https://github.com/MASITH-developpement/EAZYNOVA
**Temps de déploiement** : 5-8 minutes
**Configuration manuelle** : 0
**Scalabilité** : ♾️
