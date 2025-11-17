#!/bin/bash
set -e

# Affichage des informations de connexion
echo "=========================================="
echo "Démarrage Odoo 19 - EAZYNOVA"
echo "=========================================="
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

# Nom de la base de données
DB_NAME=${ODOO_DB_NAME:-railway}
echo "Base de données: $DB_NAME"

# URL publique
echo "URL publique: https://eazynova.up.railway.app"
echo "=========================================="

# Lancer Odoo avec paramètres en ligne de commande (pas de fichier config)
exec /usr/local/bin/odoo \
  --db_host=${PGHOST} \
  --db_port=${PGPORT} \
  --db_user=${PGUSER} \
  --db_password=${PGPASSWORD} \
  --database=${DB_NAME} \
  --http-port=${PORT:-8069} \
  --workers=2 \
  --max-cron-threads=1 \
  --proxy-mode \
  --addons-path=/opt/odoo/odoo/addons,/opt/odoo/addons \
  --data-dir=/var/lib/odoo \
  --log-level=info \
  --without-demo=all
