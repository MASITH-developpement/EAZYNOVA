#!/usr/bin/env node

/**
 * Serveur API pour Créer des Instances EAZYNOVA à la Demande
 *
 * Ce serveur expose une API REST qui permet de créer des instances
 * EAZYNOVA automatiquement depuis votre site web.
 *
 * Endpoints:
 * - POST /api/instances - Créer une nouvelle instance
 * - GET /api/instances/:id - Vérifier le statut d'une instance
 */

const http = require('http');
const { createEAZYNOVAInstance } = require('./create-instance');

const PORT = process.env.PORT || 3000;

// Store des instances en cours de création (en production, utiliser une DB)
const instances = new Map();

/**
 * Créer le serveur HTTP
 */
const server = http.createServer(async (req, res) => {
    // CORS Headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }

    // Route: POST /api/instances - Créer une instance
    if (req.method === 'POST' && req.url === '/api/instances') {
        let body = '';

        req.on('data', chunk => {
            body += chunk.toString();
        });

        req.on('end', async () => {
            try {
                const data = JSON.parse(body);
                const { clientName, adminEmail, companyName } = data;

                // Validation
                if (!clientName || !adminEmail) {
                    res.writeHead(400, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({
                        error: 'clientName and adminEmail are required'
                    }));
                    return;
                }

                // Générer un ID unique pour cette instance
                const instanceId = `${clientName}-${Date.now()}`;

                // Répondre immédiatement (création asynchrone)
                res.writeHead(202, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({
                    instanceId: instanceId,
                    status: 'creating',
                    message: 'Instance creation started. Check status with GET /api/instances/' + instanceId
                }));

                // Créer l'instance en arrière-plan
                instances.set(instanceId, { status: 'creating', progress: 0 });

                createEAZYNOVAInstance(clientName, adminEmail)
                    .then(result => {
                        instances.set(instanceId, {
                            status: 'ready',
                            progress: 100,
                            ...result
                        });
                    })
                    .catch(error => {
                        instances.set(instanceId, {
                            status: 'failed',
                            error: error.message
                        });
                    });

            } catch (error) {
                res.writeHead(500, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: error.message }));
            }
        });

        return;
    }

    // Route: GET /api/instances/:id - Vérifier le statut
    if (req.method === 'GET' && req.url.startsWith('/api/instances/')) {
        const instanceId = req.url.split('/')[3];
        const instance = instances.get(instanceId);

        if (!instance) {
            res.writeHead(404, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Instance not found' }));
            return;
        }

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(instance));
        return;
    }

    // Route: GET / - Page d'accueil
    if (req.method === 'GET' && req.url === '/') {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(`
            <!DOCTYPE html>
            <html>
            <head>
                <title>EAZYNOVA Instance Creator</title>
                <style>
                    body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
                    input, button { display: block; width: 100%; margin: 10px 0; padding: 10px; }
                    button { background: #4CAF50; color: white; border: none; cursor: pointer; }
                    button:hover { background: #45a049; }
                    #result { margin-top: 20px; padding: 15px; background: #f0f0f0; border-radius: 5px; }
                </style>
            </head>
            <body>
                <h1>🚀 Créer une Instance EAZYNOVA</h1>
                <form id="instanceForm">
                    <input type="text" id="clientName" placeholder="Nom du client (ex: acme-corp)" required>
                    <input type="email" id="adminEmail" placeholder="Email admin (ex: admin@acme.com)" required>
                    <input type="text" id="companyName" placeholder="Nom de l'entreprise (ex: ACME Corp)">
                    <button type="submit">Créer l'Instance</button>
                </form>
                <div id="result" style="display:none"></div>

                <script>
                    document.getElementById('instanceForm').addEventListener('submit', async (e) => {
                        e.preventDefault();

                        const clientName = document.getElementById('clientName').value;
                        const adminEmail = document.getElementById('adminEmail').value;
                        const companyName = document.getElementById('companyName').value || clientName;

                        const resultDiv = document.getElementById('result');
                        resultDiv.style.display = 'block';
                        resultDiv.innerHTML = '⏳ Création en cours...';

                        try {
                            const response = await fetch('/api/instances', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ clientName, adminEmail, companyName })
                            });

                            const data = await response.json();

                            if (response.ok) {
                                resultDiv.innerHTML = \`
                                    <h3>✅ Création démarrée !</h3>
                                    <p><strong>ID:</strong> \${data.instanceId}</p>
                                    <p><strong>Statut:</strong> \${data.status}</p>
                                    <p>L'instance sera prête dans 5-8 minutes.</p>
                                    <button onclick="checkStatus('\${data.instanceId}')">Vérifier le Statut</button>
                                \`;
                            } else {
                                resultDiv.innerHTML = \`<p style="color:red">❌ Erreur: \${data.error}</p>\`;
                            }
                        } catch (error) {
                            resultDiv.innerHTML = \`<p style="color:red">❌ Erreur: \${error.message}</p>\`;
                        }
                    });

                    async function checkStatus(instanceId) {
                        const resultDiv = document.getElementById('result');

                        try {
                            const response = await fetch(\`/api/instances/\${instanceId}\`);
                            const data = await response.json();

                            if (data.status === 'ready') {
                                resultDiv.innerHTML = \`
                                    <h3>🎉 Instance Prête !</h3>
                                    <p><strong>URL:</strong> <a href="\${data.instanceUrl}" target="_blank">\${data.instanceUrl}</a></p>
                                    <p><strong>Email:</strong> \${data.adminEmail}</p>
                                    <p><strong>Mot de passe:</strong> \${data.adminPassword}</p>
                                    <p><strong>Base de données:</strong> \${data.databaseName}</p>
                                \`;
                            } else if (data.status === 'creating') {
                                resultDiv.innerHTML = \`
                                    <p>⏳ Création en cours... (\${data.progress}%)</p>
                                    <button onclick="checkStatus('\${instanceId}')">Actualiser</button>
                                \`;
                            } else if (data.status === 'failed') {
                                resultDiv.innerHTML = \`<p style="color:red">❌ Échec: \${data.error}</p>\`;
                            }
                        } catch (error) {
                            resultDiv.innerHTML = \`<p style="color:red">❌ Erreur: \${error.message}</p>\`;
                        }
                    }
                </script>
            </body>
            </html>
        `);
        return;
    }

    // Route non trouvée
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Route not found' }));
});

// Démarrer le serveur
server.listen(PORT, () => {
    console.log(`🚀 Serveur API EAZYNOVA démarré sur http://localhost:${PORT}`);
    console.log('');
    console.log('Endpoints disponibles :');
    console.log(`  - POST http://localhost:${PORT}/api/instances`);
    console.log(`  - GET  http://localhost:${PORT}/api/instances/:id`);
    console.log('');
    console.log(`Interface web : http://localhost:${PORT}`);
});

module.exports = server;
