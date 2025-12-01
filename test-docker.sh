#!/bin/bash

# ========================================
# Script de démarrage rapide EAZYNOVA Test
# ========================================

set -e

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
print_message() {
    echo -e "${2}${1}${NC}"
}

print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

# Vérifier que Docker est installé
if ! command -v docker &> /dev/null; then
    print_message "❌ Docker n'est pas installé. Veuillez installer Docker Desktop." "$RED"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    print_message "❌ Docker Compose n'est pas installé." "$RED"
    exit 1
fi

print_header "🚀 Démarrage EAZYNOVA en mode test"

# Copier le fichier .env.test si .env n'existe pas
if [ ! -f .env ]; then
    print_message "📝 Création du fichier .env à partir de .env.test..." "$YELLOW"
    cp .env.test .env
fi

# Créer le dossier logs s'il n'existe pas
mkdir -p logs

# Nettoyer les anciens conteneurs si demandé
if [ "$1" == "--clean" ] || [ "$1" == "-c" ]; then
    print_message "🧹 Nettoyage des anciens conteneurs et volumes..." "$YELLOW"
    docker-compose -f docker-compose.dev.yml down -v
    print_message "✅ Nettoyage terminé" "$GREEN"
fi

# Construire les images
print_header "🔨 Construction des images Docker"
docker-compose -f docker-compose.dev.yml build --no-cache

# Démarrer les conteneurs
print_header "🚀 Démarrage des conteneurs"
docker-compose -f docker-compose.dev.yml up -d

# Attendre que les services soient prêts
print_message "⏳ Attente du démarrage des services..." "$YELLOW"
sleep 10

# Vérifier le statut
print_header "📊 Statut des conteneurs"
docker-compose -f docker-compose.dev.yml ps

# Afficher les logs en direct pendant 30 secondes
print_header "📜 Logs de démarrage (30 secondes)"
timeout 30 docker-compose -f docker-compose.dev.yml logs -f || true

# Afficher les informations d'accès
print_header "✅ EAZYNOVA est prêt !"

print_message "🌐 Accès Odoo:" "$GREEN"
print_message "   URL: http://localhost:8069" "$BLUE"
print_message "   Base de données: eazynova_test" "$BLUE"
print_message "   Login: admin" "$BLUE"
print_message "   Mot de passe: admin" "$BLUE"

echo ""
print_message "🗄️  Accès PgAdmin:" "$GREEN"
print_message "   URL: http://localhost:5050" "$BLUE"
print_message "   Email: admin@eazynova.local" "$BLUE"
print_message "   Mot de passe: admin" "$BLUE"

echo ""
print_message "📧 Accès MailHog (emails de test):" "$GREEN"
print_message "   URL: http://localhost:8025" "$BLUE"

echo ""
print_message "📝 Commandes utiles:" "$YELLOW"
echo "   Voir les logs:        docker-compose -f docker-compose.dev.yml logs -f"
echo "   Arrêter:             docker-compose -f docker-compose.dev.yml down"
echo "   Redémarrer:          docker-compose -f docker-compose.dev.yml restart"
echo "   Entrer dans Odoo:    docker exec -it eazynova_test_odoo bash"
echo "   Nettoyer tout:       ./test-docker.sh --clean"

echo ""
print_message "🧪 Pour installer le module eazynova_website:" "$YELLOW"
echo "   1. Aller sur http://localhost:8069"
echo "   2. Créer une base de données 'eazynova_test' (ou utiliser celle existante)"
echo "   3. Aller dans Apps → Mettre à jour la liste des applications"
echo "   4. Rechercher 'EAZYNOVA - Site Web SaaS'"
echo "   5. Cliquer sur Installer"

echo ""
print_message "📚 Documentation complète: ./DOCKER_TEST.md" "$BLUE"

# Proposer d'ouvrir le navigateur
read -p "Voulez-vous ouvrir Odoo dans votre navigateur ? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:8069
    elif command -v open &> /dev/null; then
        open http://localhost:8069
    else
        print_message "⚠️  Impossible d'ouvrir le navigateur automatiquement. Ouvrez http://localhost:8069 manuellement." "$YELLOW"
    fi
fi
