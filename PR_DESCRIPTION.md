# Pull Request - Module eazynova_bank_statement

## 🎯 Objectif

Ajout d'un nouveau module pour l'import automatisé de relevés bancaires avec rapprochement intelligent par IA.

## ✨ Fonctionnalités Principales

### 🔄 Import Multi-Format
- **CSV** : Détection automatique des colonnes (date, libellé, montant, référence)
- **OFX** : Support complet OFX 1.x et 2.x
- **PDF** : Extraction OCR avec Tesseract + analyse par IA (Claude/OpenAI)

### 🤖 Rapprochement Intelligent
- Correspondance exacte par référence
- Correspondance par montant et date (±7 jours)
- Analyse sémantique du libellé par IA
- Règles de rapprochement personnalisables
- Score de confiance pour chaque rapprochement (0-1)

### 🚨 Système d'Alertes
- Alertes automatiques pour rapprochements incertains
- Alertes pour transactions non rapprochées
- Détection de doublons
- Gestion des priorités (faible, normal, élevé, urgent)
- Workflow complet (new → in_progress → resolved/ignored)

### 📊 Statistiques et Rapports
- Tableaux de bord avec statistiques
- Graphiques par journal et état
- Vue pivot pour analyses
- Historique complet des imports

## 📦 Contenu du Module

**Statistiques :**
- 27 fichiers créés
- 3412 lignes de code
- 6 modèles de données
- 3 wizards interactifs
- 10 vues XML
- 7 règles pré-configurées

**Structure :**
```
eazynova_bank_statement/
├── models/           # 6 modèles Python
│   ├── bank_statement_import.py      # Import principal
│   ├── bank_statement_line.py        # Lignes avec suggestions
│   ├── bank_statement_parser.py      # Parser CSV/OFX/PDF
│   ├── reconciliation_rule.py        # Règles personnalisables
│   ├── reconciliation_alert.py       # Système d'alertes
│   └── account_bank_statement.py     # Extension modèle Odoo
├── wizard/           # 3 assistants
│   ├── bank_statement_import_wizard.py
│   └── reconciliation_suggestion_wizard.py
├── views/            # 6 vues XML
├── security/         # Groupes et droits
├── data/             # Données et règles
├── README.md         # Documentation complète
└── INSTALL.md        # Guide d'installation
```

## 🔧 Technologies Utilisées

**Dépendances Python :**
- ofxparse : Parser OFX
- pandas : Traitement CSV
- PyPDF2 : Extraction PDF
- pytesseract : OCR
- Pillow : Traitement images
- pdf2image : Conversion PDF→images

**Dépendances Système :**
- Tesseract OCR
- Poppler utils

## 📚 Documentation

- ✅ README.md complet (300+ lignes)
- ✅ INSTALL.md avec guide pas à pas
- ✅ Docstrings dans tous les modèles
- ✅ Exemples d'utilisation

## 🔒 Sécurité

- Groupes d'accès : Utilisateur / Manager
- Règles multi-sociétés activées
- 13 droits d'accès configurés

## ✅ Compatibilité

- Odoo 19 Community Edition
- Pas de dépendance Enterprise
- Compatible avec l'architecture EAZYNOVA existante

## 🚀 Installation

```bash
# 1. Dépendances système
sudo apt-get install tesseract-ocr tesseract-ocr-fra poppler-utils

# 2. Dépendances Python
pip install ofxparse pandas PyPDF2 pytesseract Pillow pdf2image

# 3. Installer le module dans Odoo
Applications → Mettre à jour → "EAZYNOVA - Import Relevés Bancaires"
```

## 📝 Utilisation Rapide

1. Menu : Comptabilité → Imports Bancaires → Nouvel Import
2. Sélectionner le journal bancaire
3. Charger le fichier (CSV/OFX/PDF)
4. Configurer et cliquer "Importer"

## 🎁 Règles Pré-configurées

7 règles de rapprochement incluses :
- Virements avec référence
- Prélèvements SEPA
- Paiements carte bancaire
- Chèques
- Frais bancaires
- Petits montants (<50€)
- Gros montants (>5000€)

## 📸 Aperçu

Le module inclut :
- Interface d'import intuitive
- Tableau de bord de rapprochement
- Gestion des alertes
- Configuration des règles
- Rapports et statistiques

---

**Prêt à être mergé et utilisé !** 🎉
