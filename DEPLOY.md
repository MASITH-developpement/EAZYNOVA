# 🚀 Déploiement EAZYNOVA en UNE SEULE COMMANDE

**Solution scalable, automatique et universelle**

---

## ⚡ UNE SEULE COMMANDE

```bash
./deploy.sh
```

**C'est tout !** Le script fait TOUT automatiquement :
- ✅ Installe Railway CLI (si nécessaire)
- ✅ Se connecte à Railway
- ✅ Détecte `railway.json`
- ✅ Crée PostgreSQL + Odoo
- ✅ Configure les 18 variables
- ✅ Génère les secrets
- ✅ Déploie automatiquement

---

## 📋 Prérequis

**Seulement 1 prérequis :** Node.js

### Installer Node.js

| OS | Commande |
|---------|----------|
| **Windows** | Télécharger: https://nodejs.org/ |
| **macOS** | `brew install node` |
| **Linux** | `sudo apt install nodejs npm` |

---

## 🎯 Utilisation

### Option 1 : Depuis le Terminal

```bash
# Aller dans le dossier
cd /chemin/vers/EAZYNOVA

# Exécuter le script
./deploy.sh
```

### Option 2 : Double-Clic (Windows/macOS/Linux)

1. Ouvrez le dossier EAZYNOVA
2. Double-cliquez sur `deploy.sh`
3. Suivez les instructions

---

## 🔄 Pour Créer Plusieurs Instances

**Instance de Production :**
```bash
./deploy.sh
# Nommez le projet: eazynova-production
```

**Instance de Staging :**
```bash
./deploy.sh
# Nommez le projet: eazynova-staging
```

**Instance de Développement :**
```bash
./deploy.sh
# Nommez le projet: eazynova-dev
```

Chaque exécution crée une **nouvelle instance isolée** !

---

## 📊 Ce Qui Se Passe Automatiquement

1. ✅ Vérifie Railway CLI (installe si absent)
2. ✅ Se connecte à Railway (ouvre le navigateur)
3. ✅ Lit `railway.json`
4. ✅ Crée service PostgreSQL
5. ✅ Crée service Odoo
6. ✅ Configure 18 variables d'environnement
7. ✅ Génère ODOO_ADMIN_PASSWORD (secret)
8. ✅ Génère PGPASSWORD (secret)
9. ✅ Build de l'image Docker
10. ✅ Déploiement
11. ✅ Initialisation de la DB Odoo
12. ✅ Configuration entreprise + admin
13. ✅ Génération URL HTTPS

**Temps : ~10 minutes**

---

## 🔑 Après le Déploiement

### Obtenir l'URL

```bash
railway open
```

Ou dans l'interface : **Service Odoo** → **Settings** → **Networking**

### Obtenir le Mot de Passe

```bash
railway variables | grep ODOO_ADMIN_PASSWORD
```

### Se Connecter

```
URL: https://eazynova-production-xxxx.up.railway.app
Email: admin@eazynova.com
Mot de passe: [Voir ci-dessus]
```

---

## 📱 Partage avec Clients

Envoyez simplement le fichier `deploy.sh` à vos clients :

```
Bonjour,

Pour déployer votre instance EAZYNOVA :

1. Installez Node.js : https://nodejs.org/
2. Téléchargez le projet EAZYNOVA
3. Exécutez : ./deploy.sh

Tout sera configuré automatiquement en ~10 minutes.

Cordialement,
L'équipe EAZYNOVA
```

---

## 🌐 Fonctionne Sur

- ✅ Windows 10/11
- ✅ macOS (Intel & Apple Silicon)
- ✅ Linux (Ubuntu, Debian, Fedora, etc.)
- ✅ WSL (Windows Subsystem for Linux)
- ✅ ChromeOS (Linux mode)

---

## 🔧 Dépannage

### "npm: command not found"

**Solution :** Installez Node.js
- Windows/macOS : https://nodejs.org/
- Linux : `sudo apt install nodejs npm`

### "Permission denied"

**Solution :**
```bash
chmod +x deploy.sh
./deploy.sh
```

### Le script s'arrête

**Solution :** Vérifiez les logs :
```bash
railway logs
```

---

## 📦 Contenu du Script

Le script `deploy.sh` :
- 200 lignes de bash
- Détection automatique de l'OS
- Installation automatique de Railway CLI
- Gestion d'erreurs complète
- Messages clairs à chaque étape
- Détection du fichier `railway.json`
- Configuration 100% automatique

---

## ✅ Avantages

| Caractéristique | Status |
|----------------|--------|
| **Une seule commande** | ✅ `./deploy.sh` |
| **Multiplateforme** | ✅ Windows, Mac, Linux |
| **100% Automatique** | ✅ Zéro configuration manuelle |
| **Scalable** | ✅ Créez autant d'instances que vous voulez |
| **Partageable** | ✅ Envoyez le script à vos clients |
| **Reproductible** | ✅ Même résultat à chaque fois |
| **Détecte railway.json** | ✅ Configuration automatique |

---

## 🎓 Exemple Complet

```bash
# Télécharger le projet
git clone https://github.com/MASITH-developpement/EAZYNOVA.git

# Aller dans le dossier
cd EAZYNOVA

# Exécuter le script
./deploy.sh

# C'est tout ! ✅
```

---

## 📞 Support

Si vous avez un problème, le script affichera un message d'erreur clair avec la solution.

---

**Version** : 1.0.0
**Date** : 2025-11-27
**Commande** : `./deploy.sh`
**Temps** : ~10 minutes
**Configuration manuelle** : 0
