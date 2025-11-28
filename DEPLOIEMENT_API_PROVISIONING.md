# 🚀 Déploiement de l'API de Provisioning sur Railway

Guide pour héberger l'API de création d'instances EAZYNOVA publiquement, permettant à vos clients de créer des instances depuis votre site web sans rien télécharger.

## 📋 Architecture

```
Site Web Client → API Railway (Publique) → Création Instance EAZYNOVA
```

**Avantages :**
- ✅ Aucun téléchargement côté client
- ✅ API hébergée 24/7 sur Railway
- ✅ Accès via simple appel HTTP
- ✅ Intégration facile dans n'importe quel site web

---

## 🔧 Étape 1 : Déployer l'API sur Railway

### Option A : Via Interface Web Railway

1. **Allez sur Railway Dashboard** : https://railway.app/dashboard

2. **Créez un Nouveau Projet** :
   - Cliquez sur "New Project"
   - Sélectionnez "Deploy from GitHub repo"
   - Choisissez `MASITH-developpement/EAZYNOVA`
   - Branch : `claude/configure-railway-01BFMjoetfrJMFfTcSHVn5fv`

3. **Configurez le Service** :
   - Root Directory : `.` (racine)
   - Build Command : `npm install`
   - Start Command : `node api-server.js`

4. **Ajoutez les Variables d'Environnement** :
   ```
   RAILWAY_API_TOKEN=votre-token-railway
   PORT=3000
   NODE_ENV=production
   ```

5. **Générez un Domaine Public** :
   - Settings → Networking → Generate Domain
   - Vous obtiendrez : `https://eazynova-api-xxxx.up.railway.app`

### Option B : Via Railway CLI

```bash
# 1. Se connecter
railway login

# 2. Créer le projet
railway init --name "eazynova-provisioning-api"

# 3. Lier au repository
railway link

# 4. Configurer les variables
railway variables set RAILWAY_API_TOKEN=votre-token-railway
railway variables set NODE_ENV=production
railway variables set PORT=3000

# 5. Déployer
railway up --service api-server.js
```

---

## 🌐 Étape 2 : Intégrer dans Votre Site Web

Une fois l'API déployée, intégrez-la dans votre site web.

### Exemple HTML/JavaScript Simple

```html
<!DOCTYPE html>
<html>
<head>
    <title>Créer votre Instance EAZYNOVA</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
        }
        .form-group {
            margin: 15px 0;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            background: #4CAF50;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        }
        button:hover {
            background: #45a049;
        }
        #result {
            margin-top: 20px;
            padding: 15px;
            border-radius: 4px;
            display: none;
        }
        .success {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        .error {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        .loading {
            background: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
        }
    </style>
</head>
<body>
    <h1>🚀 Créer Votre Instance EAZYNOVA</h1>
    <p>Obtenez votre propre plateforme Odoo 19 en 5 minutes !</p>

    <form id="createInstanceForm">
        <div class="form-group">
            <label for="clientName">Nom de votre entreprise :</label>
            <input type="text" id="clientName" required placeholder="ex: ma-societe">
        </div>

        <div class="form-group">
            <label for="adminEmail">Email administrateur :</label>
            <input type="email" id="adminEmail" required placeholder="admin@votresociete.com">
        </div>

        <div class="form-group">
            <label for="companyName">Nom complet de l'entreprise :</label>
            <input type="text" id="companyName" placeholder="Ma Société SARL">
        </div>

        <button type="submit">Créer Mon Instance</button>
    </form>

    <div id="result"></div>

    <script>
        // URL de votre API déployée sur Railway
        const API_URL = 'https://eazynova-api-xxxx.up.railway.app';

        document.getElementById('createInstanceForm').addEventListener('submit', async (e) => {
            e.preventDefault();

            const resultDiv = document.getElementById('result');
            const clientName = document.getElementById('clientName').value;
            const adminEmail = document.getElementById('adminEmail').value;
            const companyName = document.getElementById('companyName').value || clientName;

            // Afficher le chargement
            resultDiv.className = 'loading';
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = '⏳ Création de votre instance en cours...';

            try {
                // Appel à l'API
                const response = await fetch(`${API_URL}/api/instances`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        clientName: clientName,
                        adminEmail: adminEmail,
                        companyName: companyName
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    const instanceId = data.instanceId;

                    // Succès - Commencer à vérifier le statut
                    resultDiv.className = 'success';
                    resultDiv.innerHTML = `
                        <h3>✅ Création Démarrée !</h3>
                        <p><strong>ID :</strong> ${instanceId}</p>
                        <p>Votre instance sera prête dans 5-8 minutes.</p>
                        <p>Vérification du statut...</p>
                    `;

                    // Vérifier le statut toutes les 30 secondes
                    checkStatus(instanceId);
                } else {
                    // Erreur
                    resultDiv.className = 'error';
                    resultDiv.innerHTML = `❌ Erreur : ${data.error || 'Une erreur est survenue'}`;
                }
            } catch (error) {
                resultDiv.className = 'error';
                resultDiv.innerHTML = `❌ Erreur de connexion : ${error.message}`;
            }
        });

        async function checkStatus(instanceId) {
            const resultDiv = document.getElementById('result');

            const interval = setInterval(async () => {
                try {
                    const response = await fetch(`${API_URL}/api/instances/${instanceId}`);
                    const data = await response.json();

                    if (data.status === 'ready') {
                        clearInterval(interval);
                        resultDiv.className = 'success';
                        resultDiv.innerHTML = `
                            <h3>🎉 Votre Instance est Prête !</h3>
                            <p><strong>URL :</strong> <a href="${data.instanceUrl}" target="_blank">${data.instanceUrl}</a></p>
                            <p><strong>Email :</strong> ${data.adminEmail}</p>
                            <p><strong>Mot de passe :</strong> ${data.adminPassword}</p>
                            <p><strong>Base de données :</strong> ${data.databaseName}</p>
                            <hr>
                            <p>Connectez-vous maintenant et profitez de votre plateforme EAZYNOVA ! 🚀</p>
                        `;
                    } else if (data.status === 'failed') {
                        clearInterval(interval);
                        resultDiv.className = 'error';
                        resultDiv.innerHTML = `❌ Échec de la création : ${data.error}`;
                    } else {
                        // Toujours en cours
                        resultDiv.innerHTML = `
                            <h3>⏳ Création en Cours...</h3>
                            <p>Progression : ${data.progress || 0}%</p>
                            <p>Veuillez patienter, cela prend 5-8 minutes...</p>
                        `;
                    }
                } catch (error) {
                    console.error('Erreur lors de la vérification du statut:', error);
                }
            }, 30000); // Vérifier toutes les 30 secondes
        }
    </script>
</body>
</html>
```

### Exemple React

```jsx
import React, { useState } from 'react';

const API_URL = 'https://eazynova-api-xxxx.up.railway.app';

function CreateInstanceForm() {
    const [formData, setFormData] = useState({
        clientName: '',
        adminEmail: '',
        companyName: ''
    });
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const response = await fetch(`${API_URL}/api/instances`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                setResult({ type: 'success', data });
                checkStatus(data.instanceId);
            } else {
                setResult({ type: 'error', message: data.error });
            }
        } catch (error) {
            setResult({ type: 'error', message: error.message });
        } finally {
            setLoading(false);
        }
    };

    const checkStatus = async (instanceId) => {
        const interval = setInterval(async () => {
            const response = await fetch(`${API_URL}/api/instances/${instanceId}`);
            const data = await response.json();

            if (data.status === 'ready') {
                clearInterval(interval);
                setResult({ type: 'ready', data });
            } else if (data.status === 'failed') {
                clearInterval(interval);
                setResult({ type: 'error', message: data.error });
            }
        }, 30000);
    };

    return (
        <div>
            <h1>Créer Votre Instance EAZYNOVA</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Nom de l'entreprise"
                    value={formData.clientName}
                    onChange={(e) => setFormData({...formData, clientName: e.target.value})}
                    required
                />
                <input
                    type="email"
                    placeholder="Email administrateur"
                    value={formData.adminEmail}
                    onChange={(e) => setFormData({...formData, adminEmail: e.target.value})}
                    required
                />
                <button type="submit" disabled={loading}>
                    {loading ? 'Création...' : 'Créer Mon Instance'}
                </button>
            </form>

            {result && result.type === 'ready' && (
                <div className="success">
                    <h2>🎉 Instance Prête !</h2>
                    <p>URL: <a href={result.data.instanceUrl}>{result.data.instanceUrl}</a></p>
                    <p>Email: {result.data.adminEmail}</p>
                    <p>Mot de passe: {result.data.adminPassword}</p>
                </div>
            )}
        </div>
    );
}

export default CreateInstanceForm;
```

---

## 🔒 Sécurité

### 1. Protéger l'API

Ajoutez une authentification pour éviter les abus :

```javascript
// Dans api-server.js
const API_KEY = process.env.API_KEY;

app.use((req, res, next) => {
    const apiKey = req.headers['x-api-key'];

    if (apiKey !== API_KEY) {
        return res.status(401).json({ error: 'Unauthorized' });
    }

    next();
});
```

Puis dans votre site web :

```javascript
fetch(`${API_URL}/api/instances`, {
    headers: {
        'X-API-Key': 'votre-cle-secrete',
        'Content-Type': 'application/json'
    },
    // ...
});
```

### 2. Rate Limiting

Limitez le nombre de créations par IP :

```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
    windowMs: 60 * 60 * 1000, // 1 heure
    max: 5, // Max 5 instances par heure
    message: 'Trop de créations. Réessayez dans 1 heure.'
});

app.post('/api/instances', limiter, async (req, res) => {
    // ...
});
```

---

## 📊 Suivi et Monitoring

### Base de Données des Instances

Ajoutez une base de données pour tracker toutes les instances créées :

```javascript
// Ajoutez PostgreSQL au projet API
// Variables : DATABASE_URL

const { Pool } = require('pg');
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

// Créer la table
await pool.query(`
    CREATE TABLE IF NOT EXISTS instances (
        id SERIAL PRIMARY KEY,
        client_name VARCHAR(255),
        admin_email VARCHAR(255),
        instance_url VARCHAR(500),
        railway_project_id VARCHAR(255),
        status VARCHAR(50),
        created_at TIMESTAMP DEFAULT NOW()
    )
`);

// Enregistrer chaque instance
await pool.query(
    'INSERT INTO instances (client_name, admin_email, instance_url, status) VALUES ($1, $2, $3, $4)',
    [clientName, adminEmail, instanceUrl, 'creating']
);
```

---

## 💰 Modèle Commercial

### Tarification Recommandée

- **Coût par instance** : ~$10/mois (Railway)
- **Prix de vente** : $49-99/mois
- **Marge** : $39-89/mois par client

### Facturation Automatique

Intégrez Stripe pour la facturation :

```javascript
// Vérifier le paiement avant de créer l'instance
const payment = await stripe.paymentIntents.create({
    amount: 4900, // $49
    currency: 'usd',
    // ...
});

if (payment.status === 'succeeded') {
    // Créer l'instance
    createEAZYNOVAInstance(clientName, adminEmail);
}
```

---

## ✅ Checklist de Déploiement

- [ ] API déployée sur Railway
- [ ] Domaine public généré
- [ ] Variable RAILWAY_API_TOKEN configurée
- [ ] Tests de création d'instance réussis
- [ ] Intégration dans le site web
- [ ] Authentification API ajoutée
- [ ] Rate limiting configuré
- [ ] Base de données de tracking
- [ ] Monitoring et alertes
- [ ] Documentation client

---

## 🎯 Résultat Final

**Client sur votre site web** :
1. Remplit le formulaire (30 secondes)
2. Clique sur "Créer"
3. Attend 5-8 minutes
4. Reçoit l'URL + identifiants
5. Se connecte à sa propre instance Odoo

**Tout est automatique. Zéro intervention manuelle.** 🚀

---

## 📞 Support

Pour toute question sur le déploiement de l'API :
- Documentation complète : [AUTO_PROVISIONING.md](./AUTO_PROVISIONING.md)
- Railway Docs : https://docs.railway.app
