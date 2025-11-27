# EAZYNOVA - Odoo 19 SaaS

Plateforme SaaS de gestion d'entreprise basée sur Odoo 19 CE avec modules personnalisés pour la construction, la gestion de chantiers, et l'authentification par reconnaissance faciale.

## 🚀 Déploiement 100% Automatique sur Railway

Déployez EAZYNOVA en **2 clics** avec PostgreSQL inclus - **ZÉRO configuration manuelle !**

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/new?template=https://github.com/MASITH-developpement/EAZYNOVA)

**Temps : ~5-8 minutes | Configuration : 0 | Clics : 2** ⚡

### Tout est créé automatiquement :
- ✅ PostgreSQL avec base de données
- ✅ Odoo 19 configuré
- ✅ Modules EAZYNOVA installés
- ✅ **Toutes les variables d'environnement** (mots de passe, DB, admin, etc.)
- ✅ Base de données Odoo initialisée
- ✅ Entreprise et administrateur configurés
- ✅ HTTPS automatique
- ✅ Prêt à l'emploi !

**Aucune variable à créer manuellement.** Tout est dans le template ! 🎉

➡️ **[Guide de déploiement automatique](./RAILWAY_AUTO_DEPLOY.md)** ⭐
➡️ [Guide de déploiement complet](./RAILWAY_DEPLOY.md)

---

## 📋 Fonctionnalités

### Modules EAZYNOVA

- **Core** - Module de base EAZYNOVA
- **Planning** - Gestion de chantiers et planning
- **Reconnaissance Faciale** - Authentification biométrique sans mot de passe
- **Construction** - Gestion spécifique au secteur du bâtiment
- **Electrician** - Outils pour électriciens

### Fonctionnalités Clés

- 🏗️ Gestion de chantiers et projets de construction
- 📅 Planning et calendrier Gantt
- 👤 Authentification par reconnaissance faciale
- 📊 Tableaux de bord personnalisés
- 📱 Interface responsive (mobile-friendly)
- 🔐 Sécurité renforcée avec biométrie

---

## 🛠️ Technologies

- **Odoo 19** Community Edition
- **Python 3.10+**
- **PostgreSQL 15**
- **Face Recognition** (dlib + OpenCV)
- **Docker** & **Docker Compose**
- Compatible **Railway**, **Heroku**, **AWS**, **GCP**

---

## 📚 Documentation

### Déploiement

- **[RAILWAY_DEPLOY.md](./RAILWAY_DEPLOY.md)** - Déploiement en un clic sur Railway
- **[RAILWAY_QUICKSTART.md](./RAILWAY_QUICKSTART.md)** - Guide rapide Railway (5 min)
- **[RAILWAY_SETUP.md](./RAILWAY_SETUP.md)** - Configuration Railway détaillée
- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** - Guide de déploiement général

### Développement

- **Docker Compose** - Développement local
- **Tests** - Tests unitaires et d'intégration
- **Modules** - Documentation des modules personnalisés

---

## 🚦 Démarrage Rapide (Local)

### Prérequis

- Docker & Docker Compose
- Git

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

Cliquez sur le bouton "Deploy on Railway" ci-dessus ou suivez le [guide complet](./RAILWAY_DEPLOY.md).

### Autres Plateformes

- **Heroku** - Compatible via Dockerfile
- **AWS ECS/EKS** - Déploiement containerisé
- **Google Cloud Run** - Déploiement serverless
- **Serveur VPS** - Via Docker ou installation manuelle

Consultez [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) pour plus de détails.

---

## 🔒 Sécurité

- Authentification par reconnaissance faciale (optionnelle)
- HTTPS obligatoire en production (géré par Railway)
- Mots de passe sécurisés (générés automatiquement)
- Conformité RGPD pour les données biométriques
- Logs d'audit complets

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
├── railway.toml               # Configuration Railway
├── railway.template.json      # Template Railway (déploiement en un clic)
└── requirements.txt           # Dépendances Python
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

- **Email** : contact@masith.fr
- **GitHub Issues** : [Créer une issue](https://github.com/MASITH-developpement/EAZYNOVA/issues)
- **Documentation** : [Wiki du projet](https://github.com/MASITH-developpement/EAZYNOVA/wiki)

---

## 🙏 Remerciements

- [Odoo](https://www.odoo.com/) - Plateforme ERP open source
- [Railway](https://railway.app/) - Hébergement et déploiement
- [Face Recognition](https://github.com/ageitgey/face_recognition) - Bibliothèque de reconnaissance faciale

---

**Prêt à commencer ?** Déployez maintenant ! 👇

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/new?template=https://github.com/MASITH-developpement/EAZYNOVA)
