#!/bin/bash

###############################################################################
# Script de Création d'Instance EAZYNOVA via Railway CLI
# Alternative plus simple et fiable à l'API GraphQL
###############################################################################

set -e  # Arrêter en cas d'erreur

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction d'affichage
print_step() {
    echo -e "${BLUE}$1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Vérifier les arguments
if [ $# -lt 2 ]; then
    print_error "Usage: $0 <client-name> <admin-email> [company-name]"
    echo ""
    echo "Exemples :"
    echo "  $0 acme-corp admin@acme.com"
    echo "  $0 client1 admin@client1.com \"Client 1 Inc\""
    exit 1
fi

CLIENT_NAME=$1
ADMIN_EMAIL=$2
COMPANY_NAME=${3:-$CLIENT_NAME}
PROJECT_NAME="eazynova-${CLIENT_NAME}"

echo ""
print_step "🚀 Création d'une instance EAZYNOVA pour ${CLIENT_NAME}"
echo ""

# Vérifier Railway CLI
if ! command -v railway &> /dev/null; then
    print_error "Railway CLI n'est pas installé"
    echo ""
    echo "Installation :"
    echo "  npm install -g @railway/cli"
    echo "OU"
    echo "  brew install railway"
    exit 1
fi

# Vérifier la connexion Railway
print_step "🔐 Vérification de la connexion Railway..."
if ! railway whoami &> /dev/null; then
    print_error "Vous n'êtes pas connecté à Railway"
    echo ""
    echo "Connectez-vous avec :"
    echo "  railway login"
    exit 1
fi

RAILWAY_USER=$(railway whoami 2>&1 | grep -v "Logged in as" | head -1 || echo "unknown")
print_success "Connecté en tant que : $RAILWAY_USER"
echo ""

# Créer un dossier temporaire pour le projet
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

print_step "📦 Création du projet Railway '${PROJECT_NAME}'..."

# Initialiser un nouveau projet Railway
railway init --name "$PROJECT_NAME" 2>&1

print_success "Projet créé"
echo ""

# Lier au repository GitHub
print_step "🔗 Connexion au repository GitHub..."
railway link

print_success "Repository connecté"
echo ""

# Créer le service PostgreSQL
print_step "🗄️  Ajout de PostgreSQL..."
railway add --database postgres

print_success "PostgreSQL ajouté"
echo ""

# Les variables seront configurées automatiquement par railway.json
print_step "⚙️  Railway.json va configurer toutes les variables automatiquement..."
print_success "Configuration automatique activée (via railway.json)"
echo ""

# Déployer depuis GitHub
print_step "🚀 Déploiement en cours..."
print_warning "Cela va prendre 5-8 minutes..."
echo ""

railway up

print_success "Déploiement lancé !"
echo ""

# Obtenir l'URL du projet
print_step "📡 Récupération de l'URL..."
sleep 5  # Attendre que le déploiement commence

PROJECT_URL=$(railway status 2>&1 | grep -o 'https://.*\.railway\.app' || echo "URL non disponible")

echo ""
echo "================================================================="
print_success "Instance EAZYNOVA créée !"
echo "================================================================="
echo ""
echo "📋 Informations :"
echo "  - Projet     : $PROJECT_NAME"
echo "  - Client     : $CLIENT_NAME"
echo "  - Email      : $ADMIN_EMAIL"
echo "  - Entreprise : $COMPANY_NAME"
echo ""
echo "🌐 Accès :"
if [ "$PROJECT_URL" != "URL non disponible" ]; then
    echo "  - URL        : $PROJECT_URL"
else
    echo "  - Dashboard  : https://railway.app/dashboard"
    echo "               (Cherchez le projet '$PROJECT_NAME')"
fi
echo ""
echo "🔑 Mot de passe admin :"
echo "  railway variables | grep ODOO_ADMIN_PASSWORD"
echo ""
echo "⏳ Le déploiement complet prend 5-8 minutes"
echo "   Vérifiez l'état sur : https://railway.app/dashboard"
echo ""
echo "================================================================="
echo ""

# Nettoyer
cd - > /dev/null
rm -rf "$TEMP_DIR"

print_success "Terminé !"
