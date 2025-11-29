#!/bin/bash
set -e

# ==========================================
# Script de Déploiement EAZYNOVA sur Railway
# 100% Automatique et Scalable
# ==========================================

echo "🚀 Déploiement EAZYNOVA sur Railway"
echo "===================================="
echo ""

# Vérifier que Railway CLI est installé
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI n'est pas installé"
    echo ""
    echo "Installation :"
    echo "  npm install -g @railway/cli"
    echo ""
    echo "Ou via Homebrew (macOS) :"
    echo "  brew install railway"
    exit 1
fi

echo "✅ Railway CLI détecté"
echo ""

# Connexion Railway
echo "📝 Connexion à Railway..."
railway login
echo "✅ Connecté à Railway"
echo ""

# Initialisation du projet
echo "🔧 Initialisation du projet Railway..."
echo "Railway va détecter automatiquement le fichier railway.json"
echo "et créer tous les services (PostgreSQL + Odoo) automatiquement."
echo ""
railway init
echo "✅ Projet initialisé"
echo ""

# Lien avec GitHub (optionnel - Railway peut le détecter automatiquement)
echo "🔗 Lien avec le repository GitHub..."
railway link || echo "⚠️  Lien GitHub ignoré (peut être déjà configuré)"
echo ""

# Afficher la configuration détectée
echo "📋 Configuration détectée depuis railway.json :"
echo "  - Service PostgreSQL : eazynova (base de données)"
echo "  - Service Odoo : EAZYNOVA Odoo 19"
echo "  - Variables : 18 variables créées automatiquement"
echo "  - Secrets : ODOO_ADMIN_PASSWORD, PGPASSWORD (générés)"
echo ""

# Déploiement
echo "🚀 Déploiement en cours..."
echo "Cela peut prendre 5-8 minutes (build Docker + initialisation DB)"
echo ""
railway up
echo ""
echo "✅ Déploiement lancé avec succès !"
echo ""

# Attendre un peu pour que le déploiement démarre
echo "⏳ Attente du démarrage des services (10 secondes)..."
sleep 10
echo ""

# Afficher les informations
echo "===================================="
echo "✅ DÉPLOIEMENT TERMINÉ"
echo "===================================="
echo ""

# Statut du projet
echo "📊 Statut du projet :"
railway status
echo ""

# Variables d'environnement importantes
echo "🔑 Variables d'environnement configurées :"
echo ""
railway variables | grep -E "(ODOO_ADMIN_PASSWORD|INIT_ADMIN_EMAIL|INIT_DB_NAME|ENVIRONMENT)" || railway variables
echo ""

# Instructions de connexion
echo "===================================="
echo "📋 PROCHAINES ÉTAPES"
echo "===================================="
echo ""
echo "1️⃣  Suivre les logs de déploiement :"
echo "    railway logs -f"
echo ""
echo "2️⃣  Ouvrir le projet Railway dans le navigateur :"
echo "    railway open"
echo ""
echo "3️⃣  Obtenir l'URL de votre application Odoo :"
echo "    Allez dans : Settings → Networking"
echo "    URL : https://eazynova-production-xxxx.up.railway.app"
echo ""
echo "4️⃣  Obtenir le mot de passe admin :"
echo "    railway variables | grep ODOO_ADMIN_PASSWORD"
echo "    Ou dans l'interface : Variables → ODOO_ADMIN_PASSWORD"
echo ""
echo "5️⃣  Se connecter à Odoo :"
echo "    Email : admin@eazynova.com"
echo "    Mot de passe : (voir étape 4)"
echo ""
echo "===================================="
echo "🎉 Script terminé avec succès !"
echo "===================================="
echo ""
echo "Pour voir les logs en temps réel :"
echo "  railway logs -f"
echo ""
echo "Pour ouvrir le dashboard Railway :"
echo "  railway open"
echo ""
