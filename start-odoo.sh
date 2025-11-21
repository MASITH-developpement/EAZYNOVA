#!/bin/bash
set -e

# Affichage des informations de connexion
echo "=========================================="
echo "Démarrage Odoo 19 - EAZYNOVA"
echo "=========================================="
echo "PostgreSQL Host: ${DB_HOST}"
echo "PostgreSQL Port: ${DB_PORT}"
echo "PostgreSQL User: ${DB_USER}"
echo "PostgreSQL Database: ${DB_NAME}"
echo "HTTP Port: ${PORT:-8069}"
echo "=========================================="

# Attendre que PostgreSQL soit prêt (avec timeout)
echo "Vérification de PostgreSQL..."
for i in {1..30}; do
  if timeout 2 bash -c "echo > /dev/tcp/${DB_HOST}/${DB_PORT}" 2>/dev/null; then
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
DB_NAME=${DB_NAME:-railway}
echo "Base de données: $DB_NAME"

# URL publique
echo "URL publique: https://eazynova.up.railway.app"
echo "=========================================="

# Lancer Odoo avec paramètres en ligne de commande
exec /usr/local/bin/odoo \
  --db_host=${DB_HOST} \
  --db_port=${DB_PORT} \
  --db_user=${DB_USER} \
  --db_password=${DB_PASSWORD} \
  --database=${DB_NAME} \
  --http-interface=0.0.0.0 \
  --http-port=${PORT:-8069} \
  --workers=0 \
  --max-cron-threads=1 \
  --proxy-mode \
  --no-database-list \
  --addons-path=/opt/odoo/odoo/addons,/opt/odoo/addons,/opt/odoo/custom_addons \
  --data-dir=/var/lib/odoo \
  --log-level=info \
  --dev=all