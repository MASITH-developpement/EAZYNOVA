# EAZYNOVA - Odoo 19 SaaS

Plateforme SaaS de gestion d'entreprise basée sur Odoo 19 CE avec modules personnalisés pour la construction, la gestion de chantiers, et l'authentification par reconnaissance faciale.

## 🚀 Déploiement 100% Automatique sur Railway

Déployez EAZYNOVA en **1 clic** avec PostgreSQL inclus - **ZÉRO configuration manuelle !**

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new?template=https://github.com/MASITH-developpement/EAZYNOVA)

**OU copiez ce lien direct dans votre navigateur :**

```
https://railway.app/new?template=https://github.com/MASITH-developpement/EAZYNOVA
```

**Temps : ~5-8 minutes | Configuration : 0 | Clic : 1** ⚡

### Tout est créé automatiquement :

-   ✅ PostgreSQL avec base de données
-   ✅ Odoo 19 configuré
-   ✅ Modules EAZYNOVA installés
-   ✅ **Toutes les variables d'environnement** (mots de passe, DB, admin, etc.)
-   ✅ Base de données Odoo initialisée
-   ✅ Entreprise et administrateur configurés
-   ✅ HTTPS automatique
-   ✅ Prêt à l'emploi !

**Aucune variable à créer manuellement.** Tout est dans le template ! 🎉

➡️ **[🚀 QUICKSTART - Toutes les méthodes de déploiement](./QUICKSTART.md)** ⭐
➡️ [Guide de déploiement automatique](./RAILWAY_AUTO_DEPLOY.md)
➡️ [Guide de déploiement complet](./RAILWAY_DEPLOY.md)

---

## 📋 Fonctionnalités

### Modules EAZYNOVA

-   **Core** - Module de base EAZYNOVA
-   **Planning** - Gestion de chantiers et planning
-   **Reconnaissance Faciale** - Authentification biométrique sans mot de passe
-   **Construction** - Gestion spécifique au secteur du bâtiment
-   **Electrician** - Outils pour électriciens

### Fonctionnalités Clés

-   🏗️ Gestion de chantiers et projets de construction
-   📅 Planning et calendrier Gantt
-   👤 Authentification par reconnaissance faciale
-   📊 Tableaux de bord personnalisés
-   📱 Interface responsive (mobile-friendly)
-   🔐 Sécurité renforcée avec biométrie

---

## 🛠️ Technologies

-   **Odoo 19** Community Edition
-   **Python 3.10+**
-   **PostgreSQL 15**
-   **wkhtmltopdf 0.12.6** (génération PDF Odoo)
-   **Face Recognition** (dlib + OpenCV)
-   **Docker** & **Docker Compose**
-   Compatible **Railway**, **Heroku**, **AWS**, **GCP**

---

## 📚 Documentation

### Déploiement

-   **[QUICKSTART.md](./QUICKSTART.md)** ⭐ - Toutes les méthodes de déploiement (Lien, Script, Auto-provisioning)
-   **[DEPLOY.md](./DEPLOY.md)** - Déploiement via script `deploy.sh` (une commande)
-   **[AUTO_PROVISIONING.md](./AUTO_PROVISIONING.md)** - Système SaaS multi-tenant automatique
-   **[RAILWAY_DIRECT_LINK.md](./RAILWAY_DIRECT_LINK.md)** - Lien direct de configuration Railway
-   **[RAILWAY_DEPLOY.md](./RAILWAY_DEPLOY.md)** - Déploiement en un clic sur Railway
-   **[RAILWAY_QUICKSTART.md](./RAILWAY_QUICKSTART.md)** - Guide rapide Railway (5 min)
-   **[RAILWAY_SETUP.md](./RAILWAY_SETUP.md)** - Configuration Railway détaillée
-   **[RAILWAY_FIX_404.md](./RAILWAY_FIX_404.md)** - Résolution erreur 404
-   **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** - Guide de déploiement général

### Développement

-   **Docker Compose** - Développement local
-   **Tests** - Tests unitaires et d'intégration
-   **Modules** - Documentation des modules personnalisés

---

## 🚦 Démarrage Rapide (Local)

### Prérequis

-   Docker & Docker Compose
-   Git

#### wkhtmltopdf (PDF Odoo)

> **Info :** wkhtmltopdf est installé automatiquement dans l'image Docker (version 0.12.6 recommandée pour Odoo 19 CE). Aucune action manuelle n'est requise pour la génération de PDF.

Si vous développez hors Docker, installez wkhtmltopdf 0.12.6 sur votre machine :

```bash
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb
sudo apt install -y xfonts-75dpi xfonts-base libjpeg-turbo8
sudo dpkg -i wkhtmltox_0.12.6-1.focal_amd64.deb || sudo apt-get -f install -y
```

> wkhtmltopdf doit être dans le PATH système pour que la génération de PDF Odoo fonctionne.

### Installation

```bash
# Cloner le repository
git clone https://github.com/MASITH-developpement/EAZYNOVA.git
cd EAZYNOVA

# Copier les variables d'environnement
cp .env.example .env

# Démarrer avec Docker Compose
docker-compose up -d

# Accéder à Odoo
# http://localhost:8069
```

### Première Connexion

1. Ouvrez http://localhost:8069
2. Créez une base de données
3. Installez les modules EAZYNOVA
4. Profitez !

---

## 🌐 Déploiement Production

### Railway (Recommandé)

**3 Méthodes de Déploiement :**

| Méthode                                            | Temps      | Cas d'Usage                   |
| -------------------------------------------------- | ---------- | ----------------------------- |
| **1. [Lien Direct](./RAILWAY_DIRECT_LINK.md)**     | 1 clic     | Instance unique               |
| **2. [Script `deploy.sh`](./DEPLOY.md)**           | 1 commande | Instances multiples manuelles |
| **3. [Auto-Provisioning](./AUTO_PROVISIONING.md)** | API REST   | SaaS multi-tenant automatique |

➡️ **[Voir le QUICKSTART pour choisir](./QUICKSTART.md)**

### Auto-Provisioning SaaS Multi-Tenant

Pour créer des instances EAZYNOVA automatiquement depuis un site web :

```bash
# Créer une instance pour un client
node create-instance.js acme-corp admin@acme.com

# Ou démarrer le serveur API
node api-server.js
```

**Parfait pour :**

-   Sites web SaaS avec inscription client
-   Plateformes de partenaires
-   Démonstrations automatiques
-   Gestion de centaines de clients isolés

➡️ **[Guide complet Auto-Provisioning](./AUTO_PROVISIONING.md)**

### Autres Plateformes

-   **Heroku** - Compatible via Dockerfile
-   **AWS ECS/EKS** - Déploiement containerisé
-   **Google Cloud Run** - Déploiement serverless
-   **Serveur VPS** - Via Docker ou installation manuelle

Consultez [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) pour plus de détails.

---

## 🔒 Sécurité

-   Authentification par reconnaissance faciale (optionnelle)
-   HTTPS obligatoire en production (géré par Railway)
-   Mots de passe sécurisés (générés automatiquement)
-   Conformité RGPD pour les données biométriques
-   Logs d'audit complets

---

## 📦 Structure du Projet

```
EAZYNOVA/
├── addons/
│   └── addons-perso/          # Modules personnalisés EAZYNOVA
│       ├── eazynova-core/
│       ├── eazynova-planning/
│       ├── construction/
│       ├── electrician/
│       └── ...
├── base_industry_data/         # Données de base (secteur)
├── Dockerfile                  # Image Docker Odoo 19
├── docker-compose.yml          # Développement local
├── start-odoo.sh              # Script de démarrage
├── init-railway.sh            # Initialisation automatique Railway
├── deploy.sh                  # Script de déploiement une commande
├── railway.json               # Configuration Railway (auto-détectée)
├── railway.toml               # Configuration Railway
├── railway.template.json      # Template Railway (déploiement en un clic)
├── create-instance.js         # Auto-provisioning via Railway API
├── api-server.js              # Serveur API pour création d'instances
├── package.json               # Configuration Node.js
├── requirements.txt           # Dépendances Python
├── QUICKSTART.md              # ⭐ Guide de démarrage rapide
├── AUTO_PROVISIONING.md       # Guide auto-provisioning SaaS
└── DEPLOY.md                  # Guide script deploy.sh
```

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Consultez nos guidelines de contribution.

1. Fork le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

---

## 📄 Licence

Ce projet est sous licence propriétaire. Tous droits réservés à MASITH Développement.

---

## 📞 Support

-   **Email** : contact@masith.fr
-   **GitHub Issues** : [Créer une issue](https://github.com/MASITH-developpement/EAZYNOVA/issues)
-   **Documentation** : [Wiki du projet](https://github.com/MASITH-developpement/EAZYNOVA/wiki)

---

## 🙏 Remerciements

-   [Odoo](https://www.odoo.com/) - Plateforme ERP open source
-   [Railway](https://railway.app/) - Hébergement et déploiement
-   [Face Recognition](https://github.com/ageitgey/face_recognition) - Bibliothèque de reconnaissance faciale

---

**Prêt à commencer ?** Déployez maintenant ! 👇

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/new?template=https://github.com/MASITH-developpement/EAZYNOVA)
