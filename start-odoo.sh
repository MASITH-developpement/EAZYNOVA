
#!/bin/bash
# Script de démarrage Odoo avec affichage de l'IP publique et choix du nom de base

# Vérification et log de la variable DB_HOST
echo "DB_HOST = $DB_HOST"
if [ -z "$DB_HOST" ]; then
  echo "ERREUR : DB_HOST n'est pas défini !"
  exit 1
fi
# Remplacement dynamique du host dans la config Odoo
sed -i "s|db_host = .*|db_host = $DB_HOST|" /etc/odoo/odoo.conf

# Attendre que PostgreSQL soit prêt
echo "Attente de PostgreSQL..."
for i in {1..30}; do
  nc -z $DB_HOST 5432 && break
  echo "PostgreSQL non prêt, tentative $i/30..."
  sleep 2
done

IP=$(curl -s ifconfig.me)
echo "Accédez à Odoo sur : http://$IP:80"

# Affiche la valeur réelle de la variable d'environnement
echo "ODOO_DB_NAME = $ODOO_DB_NAME"

# Nom de la base de données (par défaut 'odoo', peut être surchargé par ODOO_DB_NAME)
DB_NAME=${ODOO_DB_NAME:-odoo}
echo "Nom de la base utilisée : $DB_NAME"

exec odoo --config=/etc/odoo/odoo.conf -d "$DB_NAME" -i base
