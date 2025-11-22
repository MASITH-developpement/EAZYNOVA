#!/bin/bash

# Installation des dépendances pour EAZYNOVA avec reconnaissance faciale

echo "🔧 Installation des dépendances Python pour EAZYNOVA..."

# Reconnaissance faciale
pip install face_recognition
pip install pillow
pip install numpy

# Import bancaire
pip install ofxparse
pip install pandas
pip install PyPDF2
pip install pytesseract
pip install pdf2image

echo "✅ Toutes les dépendances sont installées!"
echo ""
echo "📝 Prochaines étapes:"
echo "1. Redémarrez votre serveur Odoo"
echo "2. Mettez à jour la liste des applications"
echo "3. Mettez à jour le module EAZYNOVA"
echo ""
echo "🔐 Nouvelles fonctionnalités disponibles:"
echo "  - Reconnaissance faciale complète"
echo "  - Authentification par webcam (/web/facial_login)"
echo "  - Import relevés bancaires CSV/OFX/PDF"
