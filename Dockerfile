FROM ubuntu:22.04

USER root

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --allow-downgrades libpq5=16.10-0ubuntu0.24.04.1 && \
    apt-get install -y python3-pip python3-dev build-essential curl git wget && \
    rm -rf /var/lib/apt/lists/*
    
# === HEALTHCHECK (pour Railway) ===
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8069}/web/health || exit 1

# === PASSER À L'UTILISATEUR ODOO ===
USER odoo

# === EXPOSER LE PORT ===
# Railway utilise la variable d'environnement PORT
EXPOSE 8069

# === POINT D'ENTRÉE ===
# Railway injecte automatiquement DATABASE_URL
CMD ["odoo", "--config=/etc/odoo/odoo.conf"]
