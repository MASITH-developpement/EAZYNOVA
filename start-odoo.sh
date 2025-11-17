#!/bin/bash
# Script de démarrage Odoo avec affichage de l'IP publique et choix du nom de base


IP=$(curl -s ifconfig.me)
echo "Accédez à Odoo sur : http://$IP:8069"

# Affiche la valeur réelle de la variable d'environnement
echo "ODOO_DB_NAME = $ODOO_DB_NAME"

# Nom de la base de données (par défaut 'odoo', peut être surchargé par ODOO_DB_NAME)
DB_NAME=${ODOO_DB_NAME:-odoo}
echo "Nom de la base utilisée : $DB_NAME"

exec odoo --config=/etc/odoo/odoo.conf -d "$DB_NAME" -i base
