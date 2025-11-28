#!/bin/bash

# ==========================================
# EAZYNOVA - Déploiement Automatique Railway
# UNE SEULE COMMANDE POUR TOUT DÉPLOYER
# ==========================================

set -e

echo "🚀 EAZYNOVA - Déploiement Automatique sur Railway"
echo "=================================================="
echo ""

# Fonction pour installer Railway CLI automatiquement
install_railway_cli() {
    echo "📦 Installation de Railway CLI..."

    # Détecter l'OS
    OS="$(uname -s)"
    case "${OS}" in
        Linux*)
            if command -v npm &> /dev/null; then
                npm install -g @railway/cli
            else
                echo "❌ npm n'est pas installé. Installation de Node.js requise."
                echo "Installez Node.js depuis: https://nodejs.org/"
                exit 1
            fi
            ;;
        Darwin*)
            if command -v brew &> /dev/null; then
                brew install railway
            elif command -v npm &> /dev/null; then
                npm install -g @railway/cli
            else
                echo "❌ Homebrew ou npm requis sur macOS"
                echo "Installez Homebrew: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
                exit 1
            fi
            ;;
        MINGW*|MSYS*|CYGWIN*)
            if command -v npm &> /dev/null; then
                npm install -g @railway/cli
            else
                echo "❌ npm n'est pas installé. Installation de Node.js requise."
                echo "Installez Node.js depuis: https://nodejs.org/"
                exit 1
            fi
            ;;
        *)
            echo "❌ Système d'exploitation non supporté: ${OS}"
            exit 1
            ;;
    esac

    echo "✅ Railway CLI installé avec succès"
}

# Vérifier si Railway CLI est installé
if ! command -v railway &> /dev/null; then
    echo "⚠️  Railway CLI n'est pas installé"
    read -p "Voulez-vous l'installer automatiquement ? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        install_railway_cli
    else
        echo "❌ Installation annulée"
        echo "Installez manuellement: npm install -g @railway/cli"
        exit 1
    fi
fi

echo "✅ Railway CLI détecté"
echo ""

# Connexion à Railway
echo "🔐 Connexion à Railway..."
echo "Votre navigateur va s'ouvrir pour l'authentification."
echo ""
railway login

if [ $? -ne 0 ]; then
    echo "❌ Échec de la connexion à Railway"
    exit 1
fi

echo ""
echo "✅ Connecté à Railway"
echo ""

# Aller dans le dossier du script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

echo "📂 Répertoire du projet: $SCRIPT_DIR"
echo ""

# Vérifier que railway.json existe
if [ ! -f "railway.json" ]; then
    echo "❌ Fichier railway.json non trouvé dans $SCRIPT_DIR"
    exit 1
fi

echo "✅ Fichier railway.json détecté"
echo ""

# Initialisation du projet Railway
echo "🔧 Initialisation du projet Railway..."
echo "Railway va détecter automatiquement railway.json"
echo "et créer PostgreSQL + Odoo avec toutes les variables."
echo ""

railway init

if [ $? -ne 0 ]; then
    echo "❌ Échec de l'initialisation du projet"
    exit 1
fi

echo ""
echo "✅ Projet Railway initialisé"
echo ""

# Déploiement
echo "🚀 Déploiement sur Railway..."
echo "Cela va prendre 5-8 minutes (build Docker + initialisation DB)"
echo ""

railway up

if [ $? -ne 0 ]; then
    echo "❌ Échec du déploiement"
    exit 1
fi

echo ""
echo "✅ Déploiement lancé avec succès !"
echo ""

# Attendre un peu
sleep 5

# Afficher les informations
echo "=================================================="
echo "🎉 DÉPLOIEMENT TERMINÉ AVEC SUCCÈS"
echo "=================================================="
echo ""

# Obtenir les informations du projet
echo "📊 Informations du déploiement:"
echo ""
railway status || echo "Exécutez 'railway status' pour voir l'état"
echo ""

# Instructions finales
echo "=================================================="
echo "📋 PROCHAINES ÉTAPES"
echo "=================================================="
echo ""
echo "1️⃣  Suivre les logs en temps réel:"
echo "    railway logs -f"
echo ""
echo "2️⃣  Ouvrir le dashboard Railway:"
echo "    railway open"
echo ""
echo "3️⃣  Obtenir l'URL de votre application:"
echo "    - Dans Railway Dashboard → Service Odoo → Settings → Networking"
echo "    - URL: https://eazynova-production-xxxx.up.railway.app"
echo ""
echo "4️⃣  Obtenir le mot de passe admin:"
echo "    railway variables | grep ODOO_ADMIN_PASSWORD"
echo ""
echo "5️⃣  Se connecter à Odoo:"
echo "    - Email: admin@eazynova.com"
echo "    - Mot de passe: (voir étape 4)"
echo ""
echo "=================================================="
echo ""
echo "✅ Configuration détectée depuis railway.json:"
echo "   - PostgreSQL: Base 'eazynova', User 'odoo'"
echo "   - Odoo: 18 variables d'environnement configurées"
echo "   - Initialisation automatique de la DB Odoo"
echo "   - Entreprise: EAZYNOVA (France, Français)"
echo ""
echo "🎉 Votre SaaS Odoo est en cours de déploiement !"
echo ""
echo "Pour voir les logs:"
echo "  railway logs -f"
echo ""
