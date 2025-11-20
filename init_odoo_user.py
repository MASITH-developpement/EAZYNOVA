#!/usr/bin/env python3
import psycopg2
import os
import sys

print("="*60)
print("INITIALISATION UTILISATEUR ODOO")
print("="*60)

try:
    conn = psycopg2.connect(
        host=os.environ.get('PGHOST', 'postgres.railway.internal'),
        port=os.environ.get('PGPORT', '5432'),
        user='postgres',
        password=os.environ.get('PGPASSWORD'),
        database=os.environ.get('PGDATABASE', 'railway')
    )
    conn.autocommit = True
    cur = conn.cursor()
    print("✅ Connecté à PostgreSQL")
    
    try:
        cur.execute("CREATE USER odoo WITH PASSWORD 'odoo_secure_2024' CREATEDB;")
        print("✅ Utilisateur 'odoo' créé")
    except Exception as e:
        print(f"⚠️ Utilisateur existe déjà: {e}")
    
    cur.execute("GRANT ALL PRIVILEGES ON DATABASE railway TO odoo;")
    cur.execute("ALTER DATABASE railway OWNER TO odoo;")
    cur.execute("GRANT ALL ON SCHEMA public TO odoo;")
    print("✅ Droits accordés")
    
    conn.close()
    print("="*60)
    print("✅ CONFIGURATION TERMINÉE")
    print("="*60)
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)