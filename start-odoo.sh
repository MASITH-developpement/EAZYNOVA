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

# Nettoyer les assets orphelins
echo "Nettoyage des assets..."
python3 /opt/clean_assets.py

# Nom de la base de données
echo "Base de données: ${PGDATABASE}"

# URL publique
echo "URL publique: https://eazynova.up.railway.app"
echo "=========================================="

exec /usr/local/bin/odoo -c /etc/odoo/odoo.conf --dev=all --addons-path=/opt/odoo/odoo/addons,/opt/odoo/addons,/mnt/extra-addons/addons-perso,/opt/odoo/custom_addons
