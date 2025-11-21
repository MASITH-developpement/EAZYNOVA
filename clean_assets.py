#!/usr/bin/env python3
import psycopg2
import os

print("Nettoyage des assets orphelins...")

try:
    conn = psycopg2.connect(
        host=os.environ.get('PGHOST'),
        port=os.environ.get('PGPORT'),
        user=os.environ.get('PGUSER'),
        password=os.environ.get('PGPASSWORD'),
        database=os.environ.get('PGDATABASE', 'railway')
    )
    cur = conn.cursor()
    
    # Supprime tous les attachments de type asset
    cur.execute("""
        DELETE FROM ir_attachment 
        WHERE url LIKE '/web/assets/%' 
        OR name LIKE 'web.assets_%'
    """)
    
    conn.commit()
    print(f"✅ {cur.rowcount} assets orphelins supprimés")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Erreur: {e}")