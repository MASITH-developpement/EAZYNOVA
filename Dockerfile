# ============================================
# Dockerfile optimisé pour Railway + Odoo 19
# ============================================

FROM odoo:19

USER root

# === VARIABLES D'ENVIRONNEMENT ===
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# === MISE À JOUR SYSTÈME ===
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    libpq-dev \
    curl \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# === DÉPENDANCES PYTHON SUPPLÉMENTAIRES ===
# Décommentez si vous avez un requirements.txt
# COPY requirements.txt /tmp/
# RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# === COPIER LES MODULES PERSONNALISÉS ===
COPY ./addons /mnt/extra-addons

# === PERMISSIONS ===
RUN chown -R odoo:odoo /mnt/extra-addons \
    && chmod -R 755 /mnt/extra-addons

# === CRÉER LES DOSSIERS NÉCESSAIRES ===
RUN mkdir -p /var/lib/odoo \
    && chown -R odoo:odoo /var/lib/odoo

# === COPIER LA CONFIGURATION PRODUCTION ===
COPY --chown=odoo:odoo odoo.conf.production /etc/odoo/odoo.conf

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