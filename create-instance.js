#!/usr/bin/env node

/**
 * Script de Création Automatique d'Instance EAZYNOVA
 *
 * Utilisation depuis un site web :
 * - Recevoir une requête HTTP
 * - Créer une nouvelle instance Odoo
 * - Retourner l'URL et les identifiants
 *
 * API Railway utilisée pour créer des projets programmatiquement
 */

const https = require('https');
const { execSync } = require('child_process');

// Configuration
const RAILWAY_API_TOKEN = process.env.RAILWAY_API_TOKEN; // À obtenir depuis Railway
const GITHUB_REPO = 'MASITH-developpement/EAZYNOVA';
const GITHUB_BRANCH = 'main';

/**
 * Créer une nouvelle instance EAZYNOVA
 * @param {string} clientName - Nom du client (ex: "acme-corp")
 * @param {string} adminEmail - Email de l'admin (ex: "admin@acme.com")
 * @returns {Promise<Object>} - URL et identifiants de l'instance
 */
async function createEAZYNOVAInstance(clientName, adminEmail) {
    console.log(`🚀 Création d'une instance EAZYNOVA pour ${clientName}...`);

    const projectName = `eazynova-${clientName}`;

    // Étape 1 : Créer le projet Railway via CLI
    console.log('📦 Création du projet Railway...');
    const projectId = await createRailwayProject(projectName);

    // Étape 2 : Lier le repository GitHub
    console.log('🔗 Connexion au repository GitHub...');
    await linkGitHubRepo(projectId, GITHUB_REPO, GITHUB_BRANCH);

    // Étape 3 : Créer les services (PostgreSQL + Odoo)
    console.log('🗄️ Création de PostgreSQL...');
    const dbServiceId = await createPostgreSQLService(projectId);

    console.log('🐳 Création du service Odoo...');
    const odooServiceId = await createOdooService(projectId, dbServiceId);

    // Étape 4 : Configurer les variables d'environnement
    console.log('⚙️ Configuration des variables...');
    await configureEnvironmentVariables(projectId, odooServiceId, {
        INIT_ADMIN_EMAIL: adminEmail,
        INIT_COMPANY_NAME: clientName.toUpperCase(),
        INIT_DB_NAME: `${clientName}_prod`,
    });

    // Étape 5 : Déclencher le déploiement
    console.log('🚀 Déploiement en cours...');
    await triggerDeployment(projectId, odooServiceId);

    // Étape 6 : Attendre le déploiement
    console.log('⏳ Attente du déploiement (5-8 min)...');
    const deploymentStatus = await waitForDeployment(projectId, odooServiceId);

    // Étape 7 : Récupérer l'URL et les identifiants
    const instanceUrl = await getInstanceUrl(projectId, odooServiceId);
    const adminPassword = await getAdminPassword(projectId, odooServiceId);

    console.log('✅ Instance créée avec succès !');

    return {
        success: true,
        instanceUrl: instanceUrl,
        adminEmail: adminEmail,
        adminPassword: adminPassword,
        databaseName: `${clientName}_prod`,
        projectId: projectId,
        deploymentTime: deploymentStatus.duration,
    };
}

/**
 * Créer un projet Railway via API
 */
async function createRailwayProject(projectName) {
    const mutation = `
        mutation {
            projectCreate(input: {
                name: "${projectName}"
            }) {
                id
                name
            }
        }
    `;

    const response = await callRailwayAPI(mutation);
    return response.data.projectCreate.id;
}

/**
 * Lier le repository GitHub
 */
async function linkGitHubRepo(projectId, repo, branch) {
    const mutation = `
        mutation {
            serviceConnect(input: {
                projectId: "${projectId}"
                source: {
                    repo: "${repo}"
                    branch: "${branch}"
                }
            }) {
                id
            }
        }
    `;

    await callRailwayAPI(mutation);
}

/**
 * Créer le service PostgreSQL
 */
async function createPostgreSQLService(projectId) {
    const mutation = `
        mutation {
            serviceCreate(input: {
                projectId: "${projectId}"
                source: {
                    image: "postgres:15-alpine"
                }
            }) {
                id
            }
        }
    `;

    const response = await callRailwayAPI(mutation);
    return response.data.serviceCreate.id;
}

/**
 * Créer le service Odoo
 */
async function createOdooService(projectId, dbServiceId) {
    // Le service Odoo sera créé automatiquement via railway.json
    // lors du déploiement depuis GitHub
    return null; // Railway détectera railway.json
}

/**
 * Configurer les variables d'environnement
 */
async function configureEnvironmentVariables(projectId, serviceId, variables) {
    for (const [key, value] of Object.entries(variables)) {
        const mutation = `
            mutation {
                variableUpsert(input: {
                    projectId: "${projectId}"
                    environmentId: "production"
                    name: "${key}"
                    value: "${value}"
                }) {
                    id
                }
            }
        `;

        await callRailwayAPI(mutation);
    }
}

/**
 * Déclencher le déploiement
 */
async function triggerDeployment(projectId, serviceId) {
    const mutation = `
        mutation {
            deploymentTrigger(input: {
                projectId: "${projectId}"
                environmentId: "production"
            }) {
                id
            }
        }
    `;

    await callRailwayAPI(mutation);
}

/**
 * Attendre que le déploiement soit terminé
 */
async function waitForDeployment(projectId, serviceId, maxWaitMinutes = 15) {
    const startTime = Date.now();
    const maxWaitMs = maxWaitMinutes * 60 * 1000;

    while (Date.now() - startTime < maxWaitMs) {
        const status = await getDeploymentStatus(projectId);

        if (status === 'SUCCESS') {
            return {
                status: 'success',
                duration: Math.round((Date.now() - startTime) / 1000 / 60), // en minutes
            };
        }

        if (status === 'FAILED') {
            throw new Error('Deployment failed');
        }

        // Attendre 30 secondes avant de revérifier
        await sleep(30000);
    }

    throw new Error('Deployment timeout');
}

/**
 * Récupérer l'URL de l'instance
 */
async function getInstanceUrl(projectId, serviceId) {
    const query = `
        query {
            service(id: "${serviceId}") {
                domains {
                    domain
                }
            }
        }
    `;

    const response = await callRailwayAPI(query);
    const domain = response.data.service.domains[0].domain;
    return `https://${domain}`;
}

/**
 * Récupérer le mot de passe admin
 */
async function getAdminPassword(projectId, serviceId) {
    const query = `
        query {
            variables(projectId: "${projectId}", environmentId: "production") {
                edges {
                    node {
                        name
                        value
                    }
                }
            }
        }
    `;

    const response = await callRailwayAPI(query);
    const variables = response.data.variables.edges;
    const adminPasswordVar = variables.find(v => v.node.name === 'ODOO_ADMIN_PASSWORD');

    return adminPasswordVar ? adminPasswordVar.node.value : null;
}

/**
 * Appeler l'API Railway
 */
async function callRailwayAPI(query) {
    return new Promise((resolve, reject) => {
        const data = JSON.stringify({ query });

        const options = {
            hostname: 'backboard.railway.app',
            path: '/graphql/v2',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${RAILWAY_API_TOKEN}`,
                'Content-Length': data.length,
            },
        };

        const req = https.request(options, (res) => {
            let body = '';

            res.on('data', (chunk) => {
                body += chunk;
            });

            res.on('end', () => {
                try {
                    const response = JSON.parse(body);
                    if (response.errors) {
                        reject(new Error(response.errors[0].message));
                    } else {
                        resolve(response);
                    }
                } catch (error) {
                    reject(error);
                }
            });
        });

        req.on('error', reject);
        req.write(data);
        req.end();
    });
}

/**
 * Récupérer le statut du déploiement
 */
async function getDeploymentStatus(projectId) {
    const query = `
        query {
            deployments(projectId: "${projectId}", first: 1) {
                edges {
                    node {
                        status
                    }
                }
            }
        }
    `;

    const response = await callRailwayAPI(query);
    return response.data.deployments.edges[0]?.node.status || 'PENDING';
}

/**
 * Fonction sleep
 */
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// ============================================
// EXEMPLE D'UTILISATION
// ============================================

if (require.main === module) {
    // Récupérer les paramètres depuis la ligne de commande
    const clientName = process.argv[2] || 'test-client';
    const adminEmail = process.argv[3] || 'admin@test.com';

    if (!RAILWAY_API_TOKEN) {
        console.error('❌ RAILWAY_API_TOKEN non défini !');
        console.log('Obtenez votre token : railway whoami --token');
        console.log('Puis : export RAILWAY_API_TOKEN=your-token');
        process.exit(1);
    }

    // Créer l'instance
    createEAZYNOVAInstance(clientName, adminEmail)
        .then(result => {
            console.log('\n✅ Instance créée avec succès !');
            console.log('=================================');
            console.log('URL:', result.instanceUrl);
            console.log('Email:', result.adminEmail);
            console.log('Mot de passe:', result.adminPassword);
            console.log('Base de données:', result.databaseName);
            console.log('Temps de déploiement:', result.deploymentTime, 'minutes');
            console.log('=================================');
        })
        .catch(error => {
            console.error('❌ Erreur:', error.message);
            process.exit(1);
        });
}

// Export pour utilisation en tant que module
module.exports = { createEAZYNOVAInstance };
