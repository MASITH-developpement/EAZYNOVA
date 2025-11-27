#!/bin/bash
set -e

echo "=========================================="
echo "EAZYNOVA - Initialisation Railway"
echo "=========================================="

# Variables d'initialisation
AUTO_INIT_DB=${AUTO_INIT_DB:-false}
INIT_DB_NAME=${INIT_DB_NAME:-eazynova_prod}
INIT_ADMIN_EMAIL=${INIT_ADMIN_EMAIL:-admin@eazynova.com}
INIT_ADMIN_PASSWORD=${ODOO_ADMIN_PASSWORD:-admin}
INIT_COMPANY_NAME=${INIT_COMPANY_NAME:-EAZYNOVA}
INIT_COUNTRY=${INIT_COUNTRY:-FR}
INIT_LANG=${INIT_LANG:-fr_FR}

echo "Configuration d'initialisation :"
echo "  - AUTO_INIT_DB: ${AUTO_INIT_DB}"
echo "  - DB Name: ${INIT_DB_NAME}"
echo "  - Admin Email: ${INIT_ADMIN_EMAIL}"
echo "  - Company: ${INIT_COMPANY_NAME}"
echo "  - Country: ${INIT_COUNTRY}"
echo "  - Language: ${INIT_LANG}"
echo "=========================================="

# Vérifier si l'initialisation automatique est activée
if [ "$AUTO_INIT_DB" != "true" ]; then
    echo "⏭️  Initialisation automatique désactivée (AUTO_INIT_DB != true)"
    echo "   Vous devrez créer la base de données manuellement via l'interface web."
    exit 0
fi

# Attendre que PostgreSQL soit prêt
echo "⏳ Attente de PostgreSQL..."
for i in {1..60}; do
    if timeout 2 bash -c "echo > /dev/tcp/${PGHOST}/${PGPORT}" 2>/dev/null; then
        echo "✅ PostgreSQL est prêt !"
        break
    fi
    if [ $i -eq 60 ]; then
        echo "❌ Timeout : PostgreSQL n'est pas accessible après 2 minutes"
        exit 1
    fi
    echo "   Tentative $i/60..."
    sleep 2
done

# Vérifier si la base de données existe déjà
echo ""
echo "🔍 Vérification de l'existence de la base de données '${INIT_DB_NAME}'..."

DB_EXISTS=$(PGPASSWORD=${PGPASSWORD} psql -h ${PGHOST} -p ${PGPORT} -U ${PGUSER} -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='${INIT_DB_NAME}'")

if [ "$DB_EXISTS" = "1" ]; then
    echo "✅ La base de données '${INIT_DB_NAME}' existe déjà"
    echo "   Aucune initialisation nécessaire."
    exit 0
fi

echo "🆕 La base de données '${INIT_DB_NAME}' n'existe pas"
echo "   Création et initialisation en cours..."

# Créer la base de données Odoo
echo ""
echo "📦 Création de la base de données Odoo..."

# Créer un fichier de configuration temporaire pour l'initialisation
cat > /tmp/odoo-init.conf <<EOF
[options]
db_host = ${PGHOST}
db_port = ${PGPORT}
db_user = ${PGUSER}
db_password = ${PGPASSWORD}
admin_passwd = ${INIT_ADMIN_PASSWORD}
addons_path = /opt/odoo/odoo/addons,/opt/odoo/addons,/opt/odoo/custom_addons,/mnt/extra-addons/addons-perso
data_dir = /var/lib/odoo
EOF

# Initialiser Odoo avec la nouvelle base de données
echo "🚀 Initialisation d'Odoo avec la base '${INIT_DB_NAME}'..."
/usr/local/bin/odoo \
    -c /tmp/odoo-init.conf \
    -d ${INIT_DB_NAME} \
    --db_template=template0 \
    --without-demo=all \
    --stop-after-init \
    --init=base

if [ $? -eq 0 ]; then
    echo "✅ Base de données '${INIT_DB_NAME}' créée avec succès !"
else
    echo "❌ Erreur lors de la création de la base de données"
    exit 1
fi

# Configuration post-initialisation via SQL
echo ""
echo "⚙️  Configuration post-initialisation..."

# Créer un script SQL pour configurer l'entreprise et l'admin
cat > /tmp/post-init.sql <<EOF
-- Mise à jour des informations de l'entreprise
UPDATE res_company
SET name = '${INIT_COMPANY_NAME}',
    country_id = (SELECT id FROM res_country WHERE code = '${INIT_COUNTRY}' LIMIT 1)
WHERE id = 1;

-- Mise à jour de l'utilisateur admin
UPDATE res_users
SET login = '${INIT_ADMIN_EMAIL}',
    email = '${INIT_ADMIN_EMAIL}',
    company_id = 1
WHERE id = 2;

-- Configuration de la langue par défaut
UPDATE res_lang
SET active = true
WHERE code = '${INIT_LANG}';

UPDATE res_users
SET lang = '${INIT_LANG}'
WHERE id = 2;

-- Désactiver le mode démo si nécessaire
UPDATE ir_config_parameter
SET value = 'False'
WHERE key = 'base.demo';
EOF

# Exécuter le script SQL
PGPASSWORD=${PGPASSWORD} psql -h ${PGHOST} -p ${PGPORT} -U ${PGUSER} -d ${INIT_DB_NAME} -f /tmp/post-init.sql

if [ $? -eq 0 ]; then
    echo "✅ Configuration post-initialisation terminée !"
else
    echo "⚠️  Avertissement : La configuration post-initialisation a échoué"
    echo "   La base de données est créée mais nécessite une configuration manuelle"
fi

# Nettoyage
rm -f /tmp/odoo-init.conf /tmp/post-init.sql

echo ""
echo "=========================================="
echo "✅ INITIALISATION TERMINÉE AVEC SUCCÈS !"
echo "=========================================="
echo ""
echo "📋 Informations de connexion :"
echo "   URL: https://${RAILWAY_PUBLIC_DOMAIN:-localhost:8069}"
echo "   Base de données: ${INIT_DB_NAME}"
echo "   Email: ${INIT_ADMIN_EMAIL}"
echo "   Mot de passe: ${INIT_ADMIN_PASSWORD}"
echo ""
echo "🔐 IMPORTANT : Changez le mot de passe admin après la première connexion !"
echo ""
echo "=========================================="
