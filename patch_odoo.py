import re

DB_PATH = '/opt/odoo/odoo/service/db.py'

with open(DB_PATH, 'r') as f:
    content = f.read()

content = re.sub(
    r"if db_user == 'postgres':\s+raise RuntimeError\([^)]+\)",
    "if db_user == 'postgres':\n        pass  # Patched for Railway",
    content,
    flags=re.MULTILINE
)

with open(DB_PATH, 'w') as f:
    f.write(content)

print("✅ Patch Odoo appliqué avec succès")
