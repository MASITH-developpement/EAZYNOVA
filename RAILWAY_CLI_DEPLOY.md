# 🚀 Déploiement Railway 100% Automatique via CLI

**Solution scalable et reproductible** - Déployez EAZYNOVA automatiquement en quelques commandes.

---

## 📋 Pré-requis

- Node.js installé (pour Railway CLI)
- Compte Railway.app
- Repository GitHub avec le code dans `main`

---

## ⚡ Installation Railway CLI

```bash
npm install -g @railway/cli
```

Ou via Homebrew (macOS) :
```bash
brew install railway
```

---

## 🚀 Déploiement Automatique en 5 Commandes

### 1. Connexion à Railway

```bash
railway login
```

Cela ouvrira votre navigateur pour vous connecter avec GitHub.

### 2. Créer le Projet et Lier au Repo

```bash
# Aller dans le dossier du projet
cd /chemin/vers/EAZYNOVA

# Créer un nouveau projet Railway
railway init

# Railway détectera automatiquement le railway.json !
```

Railway va :
- ✅ Lire le fichier `railway.json`
- ✅ Créer PostgreSQL automatiquement
- ✅ Créer le service Odoo automatiquement
- ✅ Configurer toutes les variables automatiquement
- ✅ Générer les secrets automatiquement

### 3. Lier au Repository GitHub

```bash
railway link
```

Sélectionnez le repository `MASITH-developpement/EAZYNOVA`.

### 4. Déployer

```bash
railway up
```

Railway va :
1. ✅ Construire l'image Docker
2. ✅ Démarrer PostgreSQL
3. ✅ Démarrer Odoo
4. ✅ Initialiser la base de données
5. ✅ Générer l'URL HTTPS

### 5. Suivre les Logs

```bash
railway logs
```

Vous verrez les logs en temps réel :
```
==========================================
EAZYNOVA - Initialisation Railway
==========================================
✅ PostgreSQL est prêt !
📦 Création de la base de données Odoo...
✅ Base de données 'eazynova_prod' créée avec succès !
✅ INITIALISATION TERMINÉE AVEC SUCCÈS !
==========================================
```

---

## 🌐 Obtenir l'URL du Projet

```bash
railway open
```

Cela ouvrira votre projet dans le navigateur.

Pour voir l'URL directement :
```bash
railway status
```

---

## 🔑 Voir les Variables d'Environnement

```bash
railway variables
```

Pour voir le mot de passe admin :
```bash
railway run echo $ODOO_ADMIN_PASSWORD
```

---

## 📊 Commandes Utiles

| Commande | Description |
|----------|-------------|
| `railway login` | Se connecter à Railway |
| `railway init` | Créer un nouveau projet |
| `railway link` | Lier au repository GitHub |
| `railway up` | Déployer le projet |
| `railway logs` | Voir les logs en temps réel |
| `railway logs -f` | Suivre les logs (follow) |
| `railway status` | Voir le statut du projet |
| `railway open` | Ouvrir le projet dans le navigateur |
| `railway variables` | Voir les variables d'environnement |
| `railway variables set KEY=VALUE` | Définir une variable |
| `railway run COMMAND` | Exécuter une commande dans le container |
| `railway down` | Arrêter le projet |
| `railway delete` | Supprimer le projet |

---

## 🔧 Configuration Avancée

### Déployer depuis une Branche Spécifique

```bash
railway up --branch main
```

### Définir des Variables Personnalisées

```bash
railway variables set INIT_COMPANY_NAME="Ma Société"
railway variables set INIT_ADMIN_EMAIL="admin@monsociete.com"
```

### Voir les Détails du Build

```bash
railway logs --service odoo
railway logs --service postgresql
```

---

## 📦 Script de Déploiement Automatique

Créez un fichier `deploy-railway.sh` :

```bash
#!/bin/bash
set -e

echo "🚀 Déploiement EAZYNOVA sur Railway"
echo "===================================="

# Vérifier que Railway CLI est installé
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI n'est pas installé"
    echo "Installation : npm install -g @railway/cli"
    exit 1
fi

# Connexion Railway
echo "📝 Connexion à Railway..."
railway login

# Initialisation du projet
echo "🔧 Initialisation du projet..."
railway init

# Lien avec GitHub
echo "🔗 Lien avec le repository GitHub..."
railway link

# Déploiement
echo "🚀 Déploiement en cours..."
railway up

# Attendre le déploiement
echo "⏳ Attente du déploiement..."
sleep 10

# Afficher les informations
echo ""
echo "✅ Déploiement terminé !"
echo "===================================="
echo "📊 Statut du projet :"
railway status

echo ""
echo "🌐 Ouvrir le projet dans le navigateur..."
railway open

echo ""
echo "📋 Variables d'environnement :"
railway variables | grep -E "(ODOO_ADMIN_PASSWORD|INIT_|ENVIRONMENT)"

echo ""
echo "✅ Déploiement réussi !"
```

Rendez-le exécutable :
```bash
chmod +x deploy-railway.sh
```

Exécutez-le :
```bash
./deploy-railway.sh
```

---

## 🔄 CI/CD Automatique

### Configuration GitHub Actions

Créez `.github/workflows/railway-deploy.yml` :

```yaml
name: Deploy to Railway

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Install Railway CLI
        run: npm install -g @railway/cli

      - name: Deploy to Railway
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: |
          railway link ${{ secrets.RAILWAY_PROJECT_ID }}
          railway up
```

### Obtenir le Token Railway

```bash
railway whoami --token
```

Ajoutez ce token dans GitHub :
1. Repository → Settings → Secrets → New repository secret
2. Nom : `RAILWAY_TOKEN`
3. Valeur : Le token obtenu

Chaque push sur `main` déclenchera un déploiement automatique !

---

## 📈 Scalabilité

### Augmenter les Ressources

```bash
# Via l'interface Railway Dashboard
# Ou via des variables d'environnement
railway variables set WORKERS=4
railway variables set MAX_CRON_THREADS=4
```

### Activer le Mode Production

```bash
railway variables set ENVIRONMENT=production
```

Le script `start-odoo.sh` ajustera automatiquement :
- Workers : 2 (au lieu de 0)
- Cron threads : 2 (au lieu de 1)
- Dev mode : désactivé
- Log level : info (au lieu de debug)

---

## 🐛 Troubleshooting

### Problème : "No project found"

```bash
railway unlink
railway link
```

### Problème : "Build failed"

```bash
railway logs --service odoo
```

Vérifiez les erreurs dans les logs.

### Problème : "Database connection failed"

```bash
# Vérifier que PostgreSQL est démarré
railway logs --service postgresql

# Vérifier les variables
railway variables | grep PG
```

---

## ✅ Checklist de Déploiement

- [ ] Railway CLI installé
- [ ] Connecté à Railway (`railway login`)
- [ ] Code dans la branche `main`
- [ ] Fichier `railway.json` présent
- [ ] Projet initialisé (`railway init`)
- [ ] Lié au repo GitHub (`railway link`)
- [ ] Déployé (`railway up`)
- [ ] Logs vérifiés (`railway logs`)
- [ ] URL obtenue (`railway open`)
- [ ] Connexion Odoo testée

---

## 🎯 Avantages de Cette Méthode

| Avantage | Description |
|----------|-------------|
| ✅ **100% Automatique** | Aucune configuration manuelle |
| ✅ **Reproductible** | Scriptable et versionnable |
| ✅ **Scalable** | Facile à dupliquer pour plusieurs environnements |
| ✅ **CI/CD Ready** | Intégration GitHub Actions native |
| ✅ **Logs en Temps Réel** | Suivi complet du déploiement |
| ✅ **Rollback Facile** | `railway rollback` en cas de problème |

---

## 🚀 Déploiement Multi-Environnements

### Production

```bash
railway init --name eazynova-production
railway variables set ENVIRONMENT=production
railway up
```

### Staging

```bash
railway init --name eazynova-staging
railway variables set ENVIRONMENT=development
railway up
```

### Development

```bash
railway init --name eazynova-dev
railway variables set ENVIRONMENT=development
railway variables set AUTO_INIT_DB=false
railway up
```

---

## 📞 Support

- Railway CLI Docs : https://docs.railway.app/develop/cli
- Railway API : https://docs.railway.app/reference/api
- Discord Railway : https://discord.gg/railway

---

**Version** : 1.0.0
**Date** : 2025-11-27
**Méthode** : Railway CLI - 100% Automatique et Scalable
