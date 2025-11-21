# 🚀 EAZYNOVA - Solution de Gestion d'Entreprise Intelligente

[![Odoo Version](https://img.shields.io/badge/Odoo-19.0-brightgreen.svg)](https://www.odoo.com/)
[![License](https://img.shields.io/badge/License-LGPL--3-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

**EAZYNOVA** est une solution complète de gestion d'entreprise développée pour Odoo 19 Community Edition, spécialement conçue pour les entreprises du BTP et de la construction.

## 🌟 Fonctionnalités Principales

### 🤖 Intelligence Artificielle
- Assistant IA intégré (Anthropic Claude / OpenAI)
- Suggestions contextuelles pour l'optimisation
- Analyse budgétaire automatique
- Prédictions de délais et coûts

### 👤 Reconnaissance Faciale
- Authentification biométrique sécurisée
- Conforme RGPD avec consentement utilisateur
- Chiffrement des données sensibles
- Droit à l'effacement garanti

### 📄 OCR (Reconnaissance de Caractères)
- Extraction automatique de données depuis documents
- Support PDF et images (JPG, PNG, TIFF)
- Reconnaissance multi-langues
- Extraction intelligente selon le type de document

### 🏗️ Gestion de Chantiers
- Planification et suivi complets
- Géolocalisation GPS
- Gestion d'équipes
- Suivi budgétaire en temps réel

### 💰 Facturation Avancée
- Situations de travaux
- Acomptes et retenues de garantie
- Génération automatique
- Intégration comptable

## 📦 Modules Complémentaires

| Module | Description | Statut |
|--------|-------------|--------|
| **eazynova** | Module principal | ✅ Stable |
| **eazynova_chantier** | Gestion de chantiers | 🚧 En développement |
| **eazynova_facture** | Facturation avancée | 📅 Planifié |
| **eazynova_frais** | Notes de frais | 📅 Planifié |
| **eazynova_compta** | Comptabilité analytique | 📅 Planifié |
| **eazynova_stock** | Gestion de stock | 📅 Planifié |

## 🔧 Installation

### Prérequis

#### Système
- Ubuntu 22.04+ / Debian 11+
- Python 3.10+
- PostgreSQL 13+
- Node.js 18+

#### Odoo
- Odoo 19 Community Edition

#### Bibliothèques Python
```bash
pip install -r requirements.txt
```

#### Tesseract OCR
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-fra

# macOS
brew install tesseract tesseract-lang
```

#### Face Recognition (optionnel)
```bash
# Installation des dépendances système
sudo apt-get install cmake libboost-all-dev

# Installation de dlib et face_recognition
pip install dlib face_recognition opencv-python
```

### Installation du Module

1. **Cloner le dépôt**
```bash
cd /path/to/odoo/addons
git clone https://github.com/your-repo/eazynova.git
```

2. **Installer les dépendances**
```bash
cd eazynova
pip install -r requirements.txt
```

3. **Mettre à jour la liste des modules Odoo**
```bash
# Via l'interface Odoo
# Apps > Update Apps List
```

4. **Installer le module**
```bash
# Via l'interface Odoo
# Apps > Search "EAZYNOVA" > Install
```

## ⚙️ Configuration

### 1. Paramètres Généraux

Accédez à : **EAZYNOVA > Configuration > Paramètres**

#### Intelligence Artificielle
- ✅ Activer l'assistance IA
- Choisir le fournisseur (Anthropic / OpenAI)
- Saisir la clé API

#### Reconnaissance Faciale
- ✅ Activer la reconnaissance faciale
- Définir la tolérance (0.0 à 1.0)
- ⚠️ Nécessite HTTPS en production

#### OCR
- ✅ Activer l'OCR
- Vérifier l'installation de Tesseract

### 2. Configuration Utilisateur

Chaque utilisateur peut configurer :
- **Reconnaissance faciale** : Préférences > EAZYNOVA
- **Capture de visage** : Via le wizard d'enregistrement
- **Consentement RGPD** : Obligatoire pour activer

### 3. Variables d'Environnement

Pour le déploiement sur Railway :
```bash
# .env
DATABASE_URL=postgresql://user:password@host:5432/database
ODOO_ADMIN_PASSWORD=your_secure_password
EAZYNOVA_AI_PROVIDER=anthropic
EAZYNOVA_AI_API_KEY=your_api_key
```

## 🚀 Déploiement

### Déploiement Local
```bash
# Démarrer Odoo avec le module
python odoo-bin -c odoo.conf -d database_name -i eazynova
```

### Déploiement Railway

1. **Connecter votre dépôt GitHub**
2. **Configurer les variables d'environnement**
3. **Déployer automatiquement**

URL de production : https://eazynova-production.up.railway.app/

## 🧪 Tests

### Lancer les tests unitaires
```bash
# Tous les tests
python odoo-bin -c odoo.conf -d test_database --test-enable --stop-after-init -i eazynova

# Tests spécifiques
python odoo-bin -c odoo.conf -d test_database --test-enable --stop-after-init -i eazynova --test-tags eazynova
```

### Coverage
```bash
pip install coverage
coverage run odoo-bin -c odoo.conf -d test_database --test-enable --stop-after-init -i eazynova
coverage report
coverage html
```

## 📚 Documentation

### Documentation Utilisateur
- [Guide de démarrage rapide](docs/user/quick_start.md)
- [Gestion des chantiers](docs/user/chantiers.md)
- [Facturation](docs/user/facturation.md)
- [Assistant IA](docs/user/ai_assistant.md)

### Documentation Technique
- [Architecture](docs/technical/architecture.md)
- [API](docs/technical/api.md)
- [Modèles de données](docs/technical/models.md)
- [Sécurité](docs/technical/security.md)

### Documentation Développeur
- [Contribuer](CONTRIBUTING.md)
- [Standards de code](docs/developer/coding_standards.md)
- [Tests](docs/developer/testing.md)

## 🔒 Sécurité et Conformité

### RGPD
- ✅ Consentement explicite pour données biométriques
- ✅ Droit d'accès aux données
- ✅ Droit de rectification
- ✅ Droit à l'effacement
- ✅ Droit à la portabilité
- ✅ Chiffrement des données sensibles

### Sécurité
- ✅ Protection CSRF
- ✅ Protection XSS
- ✅ Validation des entrées
- ✅ Logs d'audit
- ✅ Backups automatiques

## 🤝 Contribution

Les contributions sont les bienvenues ! Veuillez consulter [CONTRIBUTING.md](CONTRIBUTING.md) pour plus de détails.

### Workflow
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Changelog

### Version 19.0.1.0.0 (2025-11-21)
- ✨ Module principal EAZYNOVA
- ✨ Reconnaissance faciale
- ✨ Assistant IA (Anthropic/OpenAI)
- ✨ OCR multi-format
- ✨ Tableau de bord intelligent
- 🏗️ Module Chantier (en cours)

## 📄 Licence

Ce projet est sous licence LGPL-3. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👥 Auteurs

- **EAZYNOVA Team** - *Développement initial*

## 🙏 Remerciements

- Odoo SA pour le framework
- Anthropic pour l'API Claude
- OpenAI pour l'API GPT
- La communauté open source

## 📞 Support

- 📧 Email: support@eazynova.com
- 🌐 Site web: https://eazynova-production.up.railway.app/
- 📖 Documentation: https://docs.eazynova.com
- 🐛 Issues: https://github.com/your-repo/eazynova/issues

## 🗺️ Roadmap

### Phase 1 - Q4 2025 ✅
- [x] Module principal
- [x] Reconnaissance faciale
- [x] Assistant IA
- [x] OCR
- [ ] Module Chantier

### Phase 2 - Q1 2026
- [ ] Module Facture
- [ ] Module Frais
- [ ] Module Compta
- [ ] Module Stock
- [ ] Application mobile

### Phase 3 - Q2 2026
- [ ] Signature électronique
- [ ] Géofencing
- [ ] IoT capteurs
- [ ] Réalité augmentée
- [ ] Blockchain

---

**⭐ Si vous aimez ce projet, n'hésitez pas à lui donner une étoile !**