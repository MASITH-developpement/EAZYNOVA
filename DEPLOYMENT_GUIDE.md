# 🚀 Guide de Déploiement EAZYNOVA avec Reconnaissance Faciale

## 📋 Pré-requis

- Odoo 19 Community Edition
- Accès administrateur
- Python 3.8+
- Accès SSH au serveur (pour installation dépendances)

## 🔧 Étape 1: Installation des dépendances

### Sur le serveur Odoo, exécutez:

```bash
# Aller dans le répertoire du projet
cd /home/user/EAZYNOVA

# Installer les dépendances
./install_dependencies.sh

# Ou manuellement:
pip install face_recognition pillow numpy ofxparse pandas PyPDF2 pytesseract pdf2image
```

### Vérification des dépendances:

```bash
python3 -c "import face_recognition; print('✅ face_recognition OK')"
python3 -c "import PIL; print('✅ PIL OK')"
python3 -c "import numpy; print('✅ numpy OK')"
```

## 📦 Étape 2: Récupérer les changements depuis GitHub

### Option A: Depuis la branche feature (recommandé pour test)

```bash
cd /home/user/EAZYNOVA
git fetch origin
git checkout claude/bank-statement-import-014c4eh7h2EjZQUpDc6HZoBP
git pull origin claude/bank-statement-import-014c4eh7h2EjZQUpDc6HZoBP
```

### Option B: Depuis main (après merge de la PR)

```bash
cd /home/user/EAZYNOVA
git checkout main
git pull origin main
```

## 🔄 Étape 3: Redémarrer Odoo

### Si Odoo est un service systemd:

```bash
sudo systemctl restart odoo
sudo systemctl status odoo
```

### Si Odoo est lancé manuellement:

```bash
# Trouver le processus
ps aux | grep odoo

# Tuer le processus (remplacer PID)
kill -9 PID

# Redémarrer
cd /path/to/odoo
./odoo-bin -c /path/to/odoo.conf
```

### Si Odoo est sur Railway/Docker:

```bash
# Redéployer l'application
# Ou utiliser l'interface Railway pour redémarrer
```

## 📱 Étape 4: Mettre à jour le module dans Odoo

### Via l'interface web:

1. **Connectez-vous** à Odoo en tant qu'administrateur

2. **Activer le mode développeur**:
   - Paramètres → Activer le mode développeur
   - Ou ajouter `?debug=1` à l'URL

3. **Mettre à jour la liste des applications**:
   - Applications → menu ⋮ → Mettre à jour la liste des applications
   - Confirmer

4. **Mettre à jour le module EAZYNOVA**:
   - Applications → Rechercher "EAZYNOVA"
   - Cliquer sur "Mettre à jour"

### Via la ligne de commande:

```bash
# Mettre à jour le module
odoo-bin -c /path/to/odoo.conf -u eazynova -d votre_database --stop-after-init

# Ou pour tous les modules EAZYNOVA
odoo-bin -c /path/to/odoo.conf -u eazynova,eazynova_bank_statement,eazynova_chantier,eazynova_facture_ocr -d votre_database --stop-after-init
```

## ✅ Étape 5: Vérification post-installation

### 1. Vérifier les modules installés:

- Applications → Rechercher "EAZYNOVA"
- Vérifier que les modules sont marqués "Installé"

### 2. Vérifier les menus:

Dans Odoo, vous devriez voir:
- **EAZYNOVA** (menu principal)
  - **Reconnaissance Faciale**
    - Enregistrements Faciaux
    - Nouvel Enregistrement
  - **Relevés Bancaires** (si module bank_statement installé)
  - **Configuration**

### 3. Tester la reconnaissance faciale:

1. Aller dans **EAZYNOVA → Reconnaissance Faciale → Nouvel Enregistrement**
2. Cliquer sur "📷 Capturer depuis la Webcam"
3. Autoriser l'accès à la webcam
4. Capturer votre visage
5. Enregistrer

### 4. Tester l'authentification faciale:

1. **Se déconnecter** d'Odoo
2. Sur la page de login, chercher le bouton:
   **"Se connecter par reconnaissance faciale"**
3. Cliquer dessus
4. Autoriser la webcam
5. Votre visage devrait être reconnu automatiquement
6. Connexion sans mot de passe! ✅

## 🐛 Résolution de problèmes

### Problème: "Opération invalide"

**Cause**: Module en cours de traitement

**Solutions**:
1. Attendre 30 secondes et réessayer
2. Redémarrer Odoo
3. Vider le cache: Paramètres → Base de données → Nettoyer
4. Via SQL:
   ```sql
   UPDATE ir_module_module
   SET state = 'installed'
   WHERE name LIKE 'eazynova%' AND state = 'to upgrade';
   ```

### Problème: "Module face_recognition non trouvé"

**Solution**:
```bash
# Installer avec pip
pip install face_recognition

# Si erreur de compilation, installer les dépendances système:
# Ubuntu/Debian
sudo apt-get install build-essential cmake
sudo apt-get install libopenblas-dev liblapack-dev
sudo apt-get install libx11-dev libgtk-3-dev

# Puis réinstaller
pip install face_recognition
```

### Problème: Webcam ne se lance pas

**Vérifications**:
1. HTTPS est requis pour accès webcam (sauf localhost)
2. Permissions navigateur accordées
3. Pas d'autre application utilisant la webcam
4. Console du navigateur pour voir les erreurs

### Problème: Template facial_recognition.xml non trouvé

**Solution**:
```bash
# Vérifier que le fichier existe
ls -la /path/to/odoo/addons/eazynova/static/src/xml/facial_recognition.xml

# Redémarrer Odoo avec assets update
odoo-bin -c /path/to/odoo.conf --update=web
```

### Problème: Page /web/facial_login retourne 404

**Solutions**:
1. Vérifier que le controller est chargé
2. Redémarrer Odoo
3. Vérifier les logs:
   ```bash
   tail -f /var/log/odoo/odoo.log | grep facial
   ```

## 📊 Logs et Monitoring

### Consulter les logs:

```bash
# Logs généraux
tail -f /var/log/odoo/odoo.log

# Filtrer reconnaissance faciale
tail -f /var/log/odoo/odoo.log | grep -i facial

# Filtrer authentification
tail -f /var/log/odoo/odoo.log | grep -i "facial.*auth"
```

### Statistiques d'utilisation:

Dans Odoo:
- **EAZYNOVA → Reconnaissance Faciale → Enregistrements Faciaux**
- Voir les stats: nombre de vérifications, dernière connexion, etc.

## 🔐 Sécurité

### Configuration recommandée:

1. **HTTPS obligatoire** en production
2. **Score de confiance**: Par défaut 70% (modifiable dans le code)
3. **Logging**: Tous les événements sont tracés
4. **Fallback**: Connexion classique toujours disponible

### Permissions:

- **Utilisateurs** (`group_eazynova_user`):
  - Créer leur propre enregistrement facial
  - Se connecter par reconnaissance faciale

- **Managers** (`group_eazynova_manager`):
  - Gérer tous les enregistrements faciaux
  - Voir les statistiques
  - Désactiver/activer les enregistrements

## 📝 Configuration post-installation

### 1. Configurer les groupes de sécurité:

- Paramètres → Utilisateurs & Sociétés → Groupes
- Rechercher "EAZYNOVA"
- Assigner les utilisateurs aux groupes appropriés

### 2. Enregistrer les utilisateurs:

**Option A**: Chaque utilisateur s'enregistre lui-même
- Se connecter avec mot de passe
- EAZYNOVA → Reconnaissance Faciale → Nouvel Enregistrement

**Option B**: Un admin enregistre tous les utilisateurs
- EAZYNOVA → Reconnaissance Faciale → Nouvel Enregistrement
- Sélectionner l'utilisateur à enregistrer
- Capturer la photo

### 3. Tester avant de déployer en production:

1. ✅ Test enregistrement facial
2. ✅ Test identification
3. ✅ Test authentification sans mot de passe
4. ✅ Test fallback (connexion classique)
5. ✅ Test sur différents navigateurs
6. ✅ Test sur mobile (si applicable)

## 🎉 Fonctionnalités activées

Après déploiement réussi, les utilisateurs peuvent:

✅ **S'enregistrer** via webcam (une fois)
✅ **Se connecter** par reconnaissance faciale (à chaque fois)
✅ **Importer** des relevés bancaires (CSV/OFX/PDF)
✅ **Rapprocher** automatiquement les transactions
✅ **Recevoir des alertes** sur les rapprochements incertains

## 📞 Support

En cas de problème:
1. Consulter les logs Odoo
2. Vérifier la console du navigateur (F12)
3. Tester avec un autre navigateur
4. Vérifier que toutes les dépendances sont installées

---

**Version**: 19.0.1.0.0
**Date**: 2024-11-22
**Modules**: eazynova, eazynova_bank_statement, eazynova_chantier, eazynova_facture_ocr
