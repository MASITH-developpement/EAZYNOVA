# 🌐 Site Web de Démonstration EAZYNOVA

Site web complet pour tester le système d'auto-provisioning EAZYNOVA.

## 🚀 Démarrage Rapide

### Prérequis

- Node.js installé
- Repository EAZYNOVA cloné
- Token Railway API

### Étape 1 : Démarrer l'API Server

Dans un terminal :

```bash
cd ~/EAZYNOVA

# Configurer le token Railway
export RAILWAY_API_TOKEN=votre-token-railway

# Démarrer l'API
node api-server.js
```

Vous verrez :
```
🚀 Serveur API EAZYNOVA démarré sur http://localhost:3000
```

### Étape 2 : Ouvrir le Site Web

Dans un autre terminal ou simplement :

```bash
# Ouvrir le fichier HTML dans votre navigateur
open demo-website/index.html

# Ou sur macOS
open demo-website/index.html

# Ou manuellement
# Double-cliquez sur demo-website/index.html
```

### Étape 3 : Créer une Instance de Test

1. **Remplissez le formulaire** :
   - Nom de l'entreprise : `test-client` (lettres minuscules et tirets)
   - Email admin : `admin@test.com`
   - Nom complet : `Test Company` (optionnel)

2. **Cliquez sur "Créer Mon Instance Maintenant"**

3. **Suivez la progression** :
   - La barre de progression s'affiche
   - Les étapes de création s'affichent
   - Temps estimé : 5-8 minutes

4. **Récupérez vos identifiants** :
   - URL de l'instance
   - Email administrateur
   - Mot de passe généré
   - Nom de la base de données

## 📋 Fonctionnalités du Site

### Interface Utilisateur

- ✅ Design moderne et responsive
- ✅ Formulaire de création d'instance
- ✅ Validation des entrées
- ✅ Indicateur de statut de l'API
- ✅ Barre de progression en temps réel
- ✅ Affichage des identifiants de connexion
- ✅ Lien direct vers l'instance créée

### Fonctionnalités Techniques

- ✅ Vérification automatique de la connexion API
- ✅ Suivi en temps réel du déploiement
- ✅ Gestion d'erreurs complète
- ✅ Interface responsive (mobile-friendly)
- ✅ Aucune dépendance externe

## 🔧 Architecture

```
┌─────────────────┐
│   Site Web      │
│  (index.html)   │
└────────┬────────┘
         │ HTTP POST
         ↓
┌─────────────────┐
│   API Server    │
│ (localhost:3000)│
└────────┬────────┘
         │ Railway API
         ↓
┌─────────────────┐
│  Railway Cloud  │
│  Nouvelle       │
│  Instance       │
└─────────────────┘
```

## 📊 Flux de Création

1. **Client remplit le formulaire** (30 secondes)
2. **Site envoie POST /api/instances** (instantané)
3. **API crée le projet Railway** (1-2 minutes)
4. **Railway déploie PostgreSQL + Odoo** (3-6 minutes)
5. **Site récupère les identifiants** (instantané)
6. **Client accède à son instance** ✅

## 🎨 Personnalisation

### Modifier l'URL de l'API

Dans `index.html`, ligne 317 :

```javascript
const API_URL = 'http://localhost:3000';
// Remplacez par votre API en production :
// const API_URL = 'https://votre-api.railway.app';
```

### Modifier le Design

Les styles CSS sont dans la balise `<style>` :

```css
/* Couleurs principales */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Modifier les couleurs */
#667eea → Votre couleur primaire
#764ba2 → Votre couleur secondaire
```

### Ajouter des Champs

Dans la section `<form>` :

```html
<div class="form-group">
    <label for="nouveauChamp">Nouveau Champ</label>
    <input type="text" id="nouveauChamp" placeholder="...">
</div>
```

Puis dans le JavaScript :

```javascript
const nouveauChamp = document.getElementById('nouveauChamp').value;
// Ajouter au body de la requête
```

## 🐛 Dépannage

### Problème : "🔴 API Non Connectée"

**Solution** :
```bash
# Vérifiez que l'API tourne
node api-server.js

# Vérifiez l'URL dans le code
# Doit être : http://localhost:3000
```

### Problème : Erreur CORS

**Solution** : L'API `api-server.js` inclut déjà les headers CORS :

```javascript
res.setHeader('Access-Control-Allow-Origin', '*');
```

### Problème : "Cannot find module"

**Solution** :
```bash
# Installez les dépendances
npm install

# Ou vérifiez que vous êtes dans le bon dossier
cd ~/EAZYNOVA
```

### Problème : La création prend plus de 8 minutes

**Solution** : C'est normal lors du premier déploiement. Railway doit :
- Cloner le repository
- Installer toutes les dépendances
- Builder l'image Docker
- Démarrer PostgreSQL et Odoo

## 🚀 Déploiement en Production

### Option 1 : Héberger le Site sur Netlify/Vercel

```bash
# Installer Netlify CLI
npm install -g netlify-cli

# Déployer
cd demo-website
netlify deploy --prod
```

### Option 2 : Héberger avec l'API sur Railway

Créez un `package.json` dans `demo-website/` :

```json
{
  "scripts": {
    "start": "npx http-server -p 8080"
  }
}
```

Puis déployez sur Railway.

### Option 3 : Intégrer dans Votre Site Existant

Copiez le code HTML/CSS/JS dans votre site :

1. **HTML** : Copiez la section `<div class="container">`
2. **CSS** : Copiez les styles
3. **JS** : Copiez le script et adaptez l'URL de l'API

## 📚 Documentation

- [AUTO_PROVISIONING.md](../AUTO_PROVISIONING.md) - Guide complet
- [DEPLOIEMENT_API_PROVISIONING.md](../DEPLOIEMENT_API_PROVISIONING.md) - Déploiement API
- [QUICKSTART.md](../QUICKSTART.md) - Démarrage rapide

## ✅ Checklist de Test

- [ ] API server démarrée (`node api-server.js`)
- [ ] Token Railway configuré
- [ ] Site web ouvert dans le navigateur
- [ ] Indicateur "🟢 API Connectée" affiché
- [ ] Formulaire rempli avec des données de test
- [ ] Instance créée avec succès
- [ ] Identifiants affichés
- [ ] Connexion à l'instance réussie

## 🎯 Résultat

Un site web professionnel prêt à l'emploi pour créer des instances EAZYNOVA automatiquement, sans aucune configuration manuelle côté client.

**Temps total de A à Z : ~6-8 minutes** ⚡
