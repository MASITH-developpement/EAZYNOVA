# 🚀 Système de Provisioning Automatique EAZYNOVA

**Créez des instances SaaS Odoo automatiquement depuis votre site web**

---

## 📋 Vue d'Ensemble

Ce système permet de créer automatiquement des instances EAZYNOVA (Odoo 19 + PostgreSQL) à la demande, parfait pour un modèle SaaS multi-tenant.

### Cas d'Usage

- ✅ **Site web SaaS** : Client s'inscrit → Instance créée automatiquement
- ✅ **Plateforme de partenaires** : Créer des instances pour des revendeurs
- ✅ **Démonstrations** : Générer des instances de test à la volée
- ✅ **Multi-tenant** : Gérer des centaines de clients isolés

---

## 🏗️ Architecture

```
Site Web Client
    ↓ (HTTP POST)
API Server (api-server.js)
    ↓ (Appel fonction)
create-instance.js
    ↓ (Railway API GraphQL)
Railway Platform
    ↓ (Déploiement)
Instance EAZYNOVA (PostgreSQL + Odoo)
```

---

## 📦 Fichiers Inclus

| Fichier | Description |
|---------|-------------|
| `create-instance.js` | Script de création d'instance via Railway API |
| `api-server.js` | Serveur API REST avec interface web |
| `package.json` | Dépendances Node.js |
| `AUTO_PROVISIONING.md` | Cette documentation |

---

## ⚙️ Installation

### 1. Prérequis

```bash
# Node.js (v16 ou supérieur)
node --version

# Railway CLI
npm install -g @railway/cli

# Se connecter à Railway
railway login
```

### 2. Obtenir le Token Railway

```bash
# Obtenir votre token API
railway whoami --token
```

**Copiez le token affiché !**

### 3. Configuration

```bash
# Définir le token
export RAILWAY_API_TOKEN=your-token-here

# Installer les dépendances (si nécessaire)
npm install
```

---

## 🚀 Utilisation

### Option 1 : Ligne de Commande

```bash
# Créer une instance
node create-instance.js nom-client admin@client.com

# Exemple
node create-instance.js acme-corp admin@acme.com
```

**Sortie :**
```
🚀 Création d'une instance EAZYNOVA pour acme-corp...
📦 Création du projet Railway...
🔗 Connexion au repository GitHub...
🗄️ Création de PostgreSQL...
🐳 Création du service Odoo...
⚙️ Configuration des variables...
🚀 Déploiement en cours...
⏳ Attente du déploiement (5-8 min)...
✅ Instance créée avec succès !

=================================
URL: https://eazynova-acme-corp-production.up.railway.app
Email: admin@acme.com
Mot de passe: xyz123abc...
Base de données: acme-corp_prod
Temps de déploiement: 6 minutes
=================================
```

### Option 2 : Serveur API

```bash
# Démarrer le serveur
node api-server.js
```

**Le serveur démarre sur http://localhost:3000**

#### Interface Web

Ouvrez http://localhost:3000 dans votre navigateur :

1. Entrez le nom du client
2. Entrez l'email admin
3. Cliquez sur "Créer l'Instance"
4. Attendez 5-8 minutes
5. Récupérez l'URL et les identifiants

#### API REST

**Créer une instance :**

```bash
curl -X POST http://localhost:3000/api/instances \
  -H "Content-Type: application/json" \
  -d '{
    "clientName": "acme-corp",
    "adminEmail": "admin@acme.com",
    "companyName": "ACME Corporation"
  }'
```

**Réponse :**
```json
{
  "instanceId": "acme-corp-1701234567890",
  "status": "creating",
  "message": "Instance creation started..."
}
```

**Vérifier le statut :**

```bash
curl http://localhost:3000/api/instances/acme-corp-1701234567890
```

**Réponse (quand prêt) :**
```json
{
  "status": "ready",
  "progress": 100,
  "instanceUrl": "https://eazynova-acme-corp.up.railway.app",
  "adminEmail": "admin@acme.com",
  "adminPassword": "xyz123abc...",
  "databaseName": "acme_corp_prod",
  "projectId": "abc-123-def"
}
```

---

## 🌐 Intégration dans Votre Site Web

### Exemple HTML + JavaScript

```html
<!DOCTYPE html>
<html>
<head>
    <title>Créer Mon Instance EAZYNOVA</title>
</head>
<body>
    <h1>Essayez EAZYNOVA Gratuitement</h1>

    <form id="signupForm">
        <input type="text" id="companyName" placeholder="Nom de votre entreprise" required>
        <input type="email" id="email" placeholder="Votre email" required>
        <button type="submit">Créer Mon Instance</button>
    </form>

    <div id="result"></div>

    <script>
        document.getElementById('signupForm').addEventListener('submit', async (e) => {
            e.preventDefault();

            const companyName = document.getElementById('companyName').value;
            const email = document.getElementById('email').value;
            const clientName = companyName.toLowerCase().replace(/[^a-z0-9]/g, '-');

            // Appeler votre API
            const response = await fetch('https://votre-api.com/api/instances', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    clientName: clientName,
                    adminEmail: email,
                    companyName: companyName
                })
            });

            const data = await response.json();

            document.getElementById('result').innerHTML = `
                <h3>✅ Votre instance est en cours de création !</h3>
                <p>Vous recevrez un email avec vos identifiants dans 5-8 minutes.</p>
            `;

            // Optionnel : Envoyer un email au client avec les identifiants
            // via votre backend
        });
    </script>
</body>
</html>
```

### Exemple avec React

```jsx
import React, { useState } from 'react';

function CreateInstance() {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        const formData = new FormData(e.target);
        const clientName = formData.get('company').toLowerCase().replace(/[^a-z0-9]/g, '-');

        try {
            const response = await fetch('https://votre-api.com/api/instances', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    clientName: clientName,
                    adminEmail: formData.get('email'),
                    companyName: formData.get('company')
                })
            });

            const data = await response.json();
            setResult(data);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h2>Créer Votre Instance EAZYNOVA</h2>
            <form onSubmit={handleSubmit}>
                <input name="company" placeholder="Nom de l'entreprise" required />
                <input name="email" type="email" placeholder="Email" required />
                <button type="submit" disabled={loading}>
                    {loading ? 'Création en cours...' : 'Créer Mon Instance'}
                </button>
            </form>

            {result && (
                <div>
                    <h3>✅ Instance créée !</h3>
                    <p>ID: {result.instanceId}</p>
                </div>
            )}
        </div>
    );
}

export default CreateInstance;
```

---

## 📊 Scalabilité

### Capacité

- **Instances simultanées** : Illimitées (limité par votre compte Railway)
- **Temps de création** : 5-8 minutes par instance
- **Coût par instance** : ~$5-20/mois selon l'utilisation

### Optimisations

**1. Queue de Création**

Utilisez un système de queue pour gérer de nombreuses demandes :

```bash
npm install bull redis
```

**2. Base de Données pour le Suivi**

Stockez les instances dans une DB au lieu de la mémoire :

```bash
npm install pg
# Ou MongoDB, MySQL, etc.
```

**3. Webhooks**

Configurez des webhooks Railway pour notifier vos clients quand leur instance est prête.

---

## 🔐 Sécurité

### Token Railway

**IMPORTANT** : Ne jamais exposer votre token Railway côté client !

✅ **Bon** :
```
Client → Votre Backend (avec token) → Railway API
```

❌ **Mauvais** :
```
Client (avec token exposé) → Railway API
```

### Rate Limiting

Limitez le nombre d'instances créées par IP/utilisateur :

```javascript
// Exemple avec express-rate-limit
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
    windowMs: 60 * 60 * 1000, // 1 heure
    max: 5 // max 5 instances par heure
});

app.use('/api/instances', limiter);
```

### Validation

Validez toujours les données :

```javascript
function validateClientName(name) {
    return /^[a-z0-9-]+$/.test(name) && name.length >= 3 && name.length <= 50;
}

function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
```

---

## 💰 Coûts

### Railway Pricing

| Plan | Prix | Instances |
|------|------|-----------|
| **Hobby** | $5/mois de crédit | ~1-2 petites instances |
| **Pro** | $20/mois + usage | ~5-10 instances moyennes |
| **Team** | Sur mesure | Illimité |

**Estimation par instance :**
- PostgreSQL : ~$3-5/mois
- Odoo (small) : ~$5-10/mois
- **Total : ~$8-15/mois par client**

### Modèle SaaS Recommandé

- Client paie : **$49/mois**
- Coût instance : **$10/mois**
- **Marge : $39/mois par client**

---

## 🎓 Exemple Complet de Workflow

### 1. Client S'inscrit

```javascript
// Sur votre site web
POST /signup
{
  "company": "ACME Corp",
  "email": "john@acme.com",
  "plan": "starter"
}
```

### 2. Votre Backend Crée l'Instance

```javascript
const instance = await createEAZYNOVAInstance('acme-corp', 'john@acme.com');
```

### 3. Envoyer l'Email de Bienvenue

```javascript
sendEmail({
  to: 'john@acme.com',
  subject: 'Votre Instance EAZYNOVA est Prête !',
  body: `
    Bonjour,

    Votre instance EAZYNOVA est prête !

    URL: ${instance.instanceUrl}
    Email: ${instance.adminEmail}
    Mot de passe: ${instance.adminPassword}

    Connectez-vous maintenant et commencez à utiliser Odoo !
  `
});
```

### 4. Client Se Connecte

Le client accède à son instance privée d'Odoo avec ses identifiants.

---

## 📞 Support

### Logs

```bash
# Logs d'une instance spécifique
railway logs -p <project-id>
```

### Debug

```bash
# Mode debug
DEBUG=* node api-server.js
```

---

## ✅ Checklist de Production

Avant de mettre en production :

- [ ] Token Railway sécurisé (variable d'environnement)
- [ ] Rate limiting configuré
- [ ] Base de données pour le suivi des instances
- [ ] Système de queue pour les créations
- [ ] Webhooks Railway configurés
- [ ] Emails de notification configurés
- [ ] Monitoring et alertes
- [ ] Backup et récupération
- [ ] Documentation client
- [ ] Support technique

---

**Votre système de provisioning automatique est prêt !** 🚀

**Temps de création par instance : 5-8 minutes**
**Configuration manuelle : 0**
**Scalable : ♾️**
