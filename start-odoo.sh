#!/bin/bash
set -e

# Détection de l'environnement
ENVIRONMENT=${ENVIRONMENT:-production}

# Affichage des informations de connexion
echo "=========================================="
echo "Démarrage Odoo 19 - EAZYNOVA"
echo "=========================================="
echo "Environnement: ${ENVIRONMENT}"
echo "PostgreSQL Host: ${PGHOST}"
echo "PostgreSQL Port: ${PGPORT}"
echo "PostgreSQL User: ${PGUSER}"
echo "PostgreSQL Database: ${PGDATABASE}"
echo "HTTP Port: ${PORT:-8069}"
echo "=========================================="

# Attendre que PostgreSQL soit prêt (avec timeout)
echo "Vérification de PostgreSQL..."
for i in {1..30}; do
  if timeout 2 bash -c "echo > /dev/tcp/${PGHOST}/${PGPORT}" 2>/dev/null; then
    echo "✓ PostgreSQL est prêt !"
    break
  fi
  echo "PostgreSQL non prêt, tentative $i/30..."
  sleep 2
done

# Nettoyer les assets orphelins
echo "Nettoyage des assets..."
python3 /opt/clean_assets.py

# Nom de la base de données
echo "Base de données: ${PGDATABASE}"

# URL publique (Railway fournit RAILWAY_PUBLIC_DOMAIN)
if [ -n "$RAILWAY_PUBLIC_DOMAIN" ]; then
  echo "URL publique: https://${RAILWAY_PUBLIC_DOMAIN}"
else
  echo "URL publique: http://localhost:${PORT:-8069}"
fi
echo "=========================================="

# Configuration selon l'environnement
if [ "$ENVIRONMENT" = "production" ]; then
  echo "Mode PRODUCTION activé"
  WORKERS=2
  MAX_CRON=2
  DEV_MODE=""
  LOG_LEVEL="info"
else
  echo "Mode DÉVELOPPEMENT activé"
  WORKERS=0
  MAX_CRON=1
  DEV_MODE="--dev=all"
  LOG_LEVEL="debug"
fi

# Lancer Odoo avec paramètres en ligne de commande
exec /usr/local/bin/odoo \
  --db_host=${PGHOST} \
  --db_port=${PGPORT} \
  --db_user=${PGUSER} \
  --db_password=${PGPASSWORD} \
  --database=${PGDATABASE} \
  --http-interface=0.0.0.0 \
  --http-port=${PORT:-8069} \
  --workers=${WORKERS} \
  --max-cron-threads=${MAX_CRON} \
  --proxy-mode \
  --addons-path=/opt/odoo/odoo/addons,/opt/odoo/addons,/opt/odoo/custom_addons,/mnt/extra-addons/addons-perso \
  --data-dir=/var/lib/odoo \
  --log-level=${LOG_LEVEL} \
  ${DEV_MODE}