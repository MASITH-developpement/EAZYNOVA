FROM ubuntu:22.04

USER root

# Build date: 2025-11-22 - Force rebuild to include all security files
ENV DEBIAN_FRONTEND=noninteractive


# Installation des dépendances système (incl. dlib/face_recognition)
RUN apt-get update && \
    apt-get install -y python3-pip python3-dev build-essential libpq-dev curl git wget cmake libboost-python-dev libboost-system-dev libopenblas-dev liblapack-dev && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y python3-lxml python3-ldap postgresql postgresql-client && \
    pip3 install lxml-html-clean

# Installation de wheel

# Installation des dépendances Python du projet (reconnaissance faciale, etc.)
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install wheel && pip3 install -r /tmp/requirements.txt

# Clonage et installation d'Odoo 19
RUN git clone --depth 1 --branch 19.0 https://github.com/odoo/odoo.git /opt/odoo \
    && pip3 install -e /opt/odoo \
    && pip3 install gevent zope.interface zope.event

# Fix du script odoo
RUN sed -i "s/__import__('pkg_resources').require('odoo==19.0')/# __import__('pkg_resources').require('odoo==19.0')/" /usr/local/bin/odoo

# Patch Odoo pour accepter l'utilisateur postgres (nécessaire pour Railway)
COPY patch_odoo.py /patch_odoo.py
RUN python3 /patch_odoo.py

# Créer dossier config et copier fichier minimal
#RUN mkdir -p /etc/odoo
COPY odoo.conf /etc/odoo/odoo.conf

# Créer dossier pour les données Odoo
RUN mkdir -p /var/lib/odoo

# HEALTHCHECK Railway
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=5 \
    CMD curl -f http://localhost:${PORT:-8069}/web/health || exit 1

# Exposer le port (dynamique Railway)
EXPOSE ${PORT:-8069}

# Force rebuild - invalidate cache with build arg
ARG BUILD_DATE=2025-11-22T22:25:00
RUN echo "Build date: ${BUILD_DATE}"

# Copie et permission des scripts

# On copie les deux scripts et on normalise les fins de ligne pour start-odoo.sh, puis on rend les deux exécutables
COPY start-odoo.sh /start-odoo.sh
COPY init-railway.sh /init-railway.sh
RUN sed -i 's/\r$//' /start-odoo.sh && chmod +x /start-odoo.sh /init-railway.sh

# Point d'entrée
COPY addons/addons-perso /opt/odoo/custom_addons
COPY clean_assets.py /opt/clean_assets.py
CMD ["/start-odoo.sh"]
