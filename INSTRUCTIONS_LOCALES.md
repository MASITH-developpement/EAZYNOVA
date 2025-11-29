# 🚀 Instructions pour Exécuter l'Auto-Provisioning Localement

## Étape 1 : Récupérer les Fichiers

Sur votre Mac, dans le dossier EAZYNOVA :

```bash
git pull origin claude/configure-railway-01BFMjoetfrJMFfTcSHVn5fv
```

Cela téléchargera :
- `create-instance.js`
- `api-server.js`
- `package.json`
- `AUTO_PROVISIONING.md`
- `QUICKSTART.md`

## Étape 2 : Obtenir le Token Railway

La commande correcte pour Railway CLI v3+ est :

```bash
railway login
```

Puis pour voir votre token :

```bash
railway whoami
```

Cela affichera votre email et projet, mais **PAS le token directement**.

### Option A : Via le Site Web Railway (Recommandé)

1. Allez sur : https://railway.app/account/tokens
2. Cliquez sur "Create New Token"
3. Copiez le token
4. Exportez-le :

```bash
export RAILWAY_API_TOKEN=votre-token-ici
```

### Option B : Via Fichier de Config Railway

```bash
cat ~/.railway/config.json
```

Cherchez le champ `token` dans le JSON.

## Étape 3 : Créer une Instance

Une fois le token exporté :

```bash
node create-instance.js masith-fr contact@masith.fr
```

**Note** : Utilisez `masith-fr` (avec tiret) au lieu de `masith.fr` car le nom du projet Railway ne peut pas contenir de points.

## Étape 4 : Alternative - Serveur API avec Interface Web

Si vous voulez une interface web pour tester :

```bash
node api-server.js
```

Puis ouvrez dans votre navigateur : http://localhost:3000

Vous verrez un formulaire pour créer des instances.

## ⚠️ Important : Commandes une par une

**NE PAS** copier-coller les lignes avec `#` (commentaires).

**Bon** ✅ :
```bash
git pull origin claude/configure-railway-01BFMjoetfrJMFfTcSHVn5fv
```

**Mauvais** ❌ :
```bash
# Récupérer les fichiers
git pull origin claude/configure-railway-01BFMjoetfrJMFfTcSHVn5fv
```

Le `#` fait crasher zsh.

## 🔍 Vérifier que les Fichiers sont Présents

```bash
ls -la create-instance.js api-server.js package.json
```

Vous devriez voir :
```
-rw-r--r--  create-instance.js
-rw-r--r--  api-server.js
-rw-r--r--  package.json
```

## 📊 Exemple Complet

```bash
cd ~/EAZYNOVA

git pull origin claude/configure-railway-01BFMjoetfrJMFfTcSHVn5fv

export RAILWAY_API_TOKEN=votre-token-depuis-railway-app

node create-instance.js test-client admin@test.com
```

## 🐛 Dépannage

### Erreur : "Cannot find module"

**Cause** : Les fichiers ne sont pas dans votre dossier local.

**Solution** :
```bash
git pull origin claude/configure-railway-01BFMjoetfrJMFfTcSHVn5fv
ls -la *.js
```

### Erreur : "RAILWAY_API_TOKEN non défini"

**Cause** : Token pas exporté.

**Solution** :
1. Allez sur https://railway.app/account/tokens
2. Créez un token
3. Exportez :
```bash
export RAILWAY_API_TOKEN=votre-token
```

### Erreur : "unexpected argument --token"

**Cause** : Ancienne syntaxe Railway CLI.

**Solution** : Obtenez le token via le site web (voir Étape 2 Option A).

## ✅ Succès

Si tout fonctionne, vous verrez :

```
🚀 Création d'une instance EAZYNOVA pour masith-fr...
📦 Création du projet Railway...
🔗 Connexion au repository GitHub...
🗄️ Création de PostgreSQL...
🐳 Création du service Odoo...
⚙️ Configuration des variables...
🚀 Déploiement en cours...
⏳ Attente du déploiement (5-8 min)...
✅ Instance créée avec succès !

=================================
URL: https://eazynova-masith-fr-xxxx.up.railway.app
Email: contact@masith.fr
Mot de passe: [généré automatiquement]
Base de données: masith-fr_prod
Temps de déploiement: 6 minutes
=================================
```

## 🎯 Prochaines Étapes

Une fois l'instance créée :

1. **Tester l'accès** : Ouvrez l'URL fournie
2. **Se connecter** : Utilisez l'email et mot de passe affichés
3. **Créer plus d'instances** : Répétez avec d'autres noms de clients
4. **Intégrer dans votre site** : Utilisez `api-server.js` pour créer des instances via API

## 📚 Documentation

- **AUTO_PROVISIONING.md** - Guide complet du système
- **QUICKSTART.md** - Comparaison des 3 méthodes de déploiement
- **DEPLOY.md** - Utilisation du script deploy.sh
