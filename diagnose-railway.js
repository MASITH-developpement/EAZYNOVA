#!/usr/bin/env node

/**
 * Script de Diagnostic Railway API
 * Teste toutes les opérations nécessaires pour créer une instance
 */

const https = require('https');

const RAILWAY_API_TOKEN = process.env.RAILWAY_API_TOKEN;

console.log('🔍 Diagnostic de l\'API Railway\n');

if (!RAILWAY_API_TOKEN) {
    console.error('❌ RAILWAY_API_TOKEN non défini');
    process.exit(1);
}

console.log('✅ Token trouvé:', RAILWAY_API_TOKEN.substring(0, 15) + '...\n');

async function callRailwayAPI(query, operationName) {
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

        console.log(`📡 Test: ${operationName}...`);

        const req = https.request(options, (res) => {
            let body = '';

            res.on('data', (chunk) => {
                body += chunk;
            });

            res.on('end', () => {
                console.log(`   Status HTTP: ${res.statusCode}`);

                try {
                    const response = JSON.parse(body);

                    if (response.errors) {
                        console.error(`   ❌ Erreur:`, response.errors[0].message);
                        console.error(`   Détails:`, JSON.stringify(response.errors, null, 2));
                        resolve({ success: false, error: response.errors });
                    } else if (response.data) {
                        console.log(`   ✅ Succès`);
                        resolve({ success: true, data: response.data });
                    } else {
                        console.error(`   ❌ Réponse inattendue:`, body);
                        resolve({ success: false, error: 'Unexpected response' });
                    }
                } catch (error) {
                    console.error(`   ❌ Parsing error:`, error.message);
                    console.error(`   Body:`, body);
                    reject(error);
                }
            });
        });

        req.on('error', (error) => {
            console.error(`   ❌ Network error:`, error.message);
            reject(error);
        });

        req.write(data);
        req.end();
    });
}

async function runDiagnostics() {
    console.log('═══════════════════════════════════════════════════\n');

    // Test 1: Récupérer les projets existants
    const test1 = await callRailwayAPI(`
        query {
            projects {
                edges {
                    node {
                        id
                        name
                    }
                }
            }
        }
    `, 'Lister les projets existants');

    if (test1.success) {
        const projects = test1.data.projects.edges;
        console.log(`   📊 Projets trouvés: ${projects.length}`);
        projects.slice(0, 5).forEach(p => {
            console.log(`      - ${p.node.name} (${p.node.id})`);
        });
    }

    console.log('\n═══════════════════════════════════════════════════\n');

    // Test 2: Récupérer les informations utilisateur
    const test2 = await callRailwayAPI(`
        query {
            me {
                id
                email
                name
            }
        }
    `, 'Informations utilisateur');

    if (test2.success) {
        console.log(`   👤 Email: ${test2.data.me.email}`);
        console.log(`   👤 Nom: ${test2.data.me.name || 'N/A'}`);
    }

    console.log('\n═══════════════════════════════════════════════════\n');

    // Test 3: Tester la création d'un projet (sans vraiment le créer)
    console.log('📡 Test: Vérifier les permissions de création...');
    const test3 = await callRailwayAPI(`
        mutation {
            projectCreate(input: {
                name: "test-diagnostic-${Date.now()}"
            }) {
                id
                name
            }
        }
    `, 'Créer un projet de test');

    if (test3.success) {
        console.log(`   🎉 Projet créé: ${test3.data.projectCreate.name}`);
        console.log(`   🗑️  Vous devriez supprimer ce projet de test manuellement`);
    }

    console.log('\n═══════════════════════════════════════════════════\n');

    // Résumé
    console.log('📊 RÉSUMÉ DU DIAGNOSTIC\n');
    console.log(`Test 1 - Lister projets:     ${test1.success ? '✅ OK' : '❌ ÉCHEC'}`);
    console.log(`Test 2 - Info utilisateur:   ${test2.success ? '✅ OK' : '❌ ÉCHEC'}`);
    console.log(`Test 3 - Créer projet:       ${test3.success ? '✅ OK' : '❌ ÉCHEC'}`);

    console.log('\n═══════════════════════════════════════════════════\n');

    if (test1.success && test2.success && test3.success) {
        console.log('🎉 TOUS LES TESTS RÉUSSIS');
        console.log('✅ L\'API Railway fonctionne correctement');
        console.log('✅ Votre token a les bonnes permissions');
        console.log('\n💡 Le problème vient probablement d\'autre chose.');
        console.log('   Vérifiez les logs du serveur API (api-server.js)');
    } else {
        console.log('❌ CERTAINS TESTS ONT ÉCHOUÉ');
        console.log('\n💡 Solutions possibles:');
        console.log('   1. Vérifiez que le token est valide');
        console.log('   2. Créez un nouveau token sur https://railway.app/account/tokens');
        console.log('   3. Assurez-vous d\'avoir les permissions nécessaires');
    }

    console.log('\n═══════════════════════════════════════════════════\n');
}

runDiagnostics().catch(error => {
    console.error('💥 Erreur fatale:', error);
    process.exit(1);
});
