FROM ubuntu:22.04

USER root

ENV DEBIAN_FRONTEND=noninteractive

# Installation des dépendances système
RUN apt-get update && \
    apt-get install -y python3-pip python3-dev build-essential libpq-dev curl git wget && \
    rm -rf /var/lib/apt/lists/*



# Installation de wheel
RUN pip3 install wheel

# Ajout du dépôt Odoo 19.0 nightly et installation
RUN wget -q -O - https://nightly.odoo.com/odoo.key | gpg --dearmor -o /usr/share/keyrings/odoo-archive-keyring.gpg \
    && echo 'deb [signed-by=/usr/share/keyrings/odoo-archive-keyring.gpg] https://nightly.odoo.com/19.0/nightly/deb/ ./' > /etc/apt/sources.list.d/odoo.list \
    && apt-get update \
    && apt-get install -y odoo \
    && rm -rf /var/lib/apt/lists/*

# Création d'un fichier de configuration minimal
RUN mkdir -p /etc/odoo
COPY odoo.conf /etc/odoo/odoo.conf

# HEALTHCHECK Railway
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8069}/web/health || exit 1

# Exposer le port Railway
EXPOSE 8069

# Point d'entrée
CMD ["odoo", "--config=/etc/odoo/odoo.conf"]
