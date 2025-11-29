#!/usr/bin/env node

/**
 * Script de Test du Token Railway
 * Vérifie si le token Railway API fonctionne
 */

const https = require('https');

const RAILWAY_API_TOKEN = process.env.RAILWAY_API_TOKEN;

if (!RAILWAY_API_TOKEN) {
    console.error('❌ RAILWAY_API_TOKEN non défini !');
    console.log('');
    console.log('Pour obtenir votre token :');
    console.log('1. Allez sur https://railway.app/account/tokens');
    console.log('2. Cliquez sur "Create New Token"');
    console.log('3. Copiez le token');
    console.log('4. Exportez : export RAILWAY_API_TOKEN=votre-token');
    process.exit(1);
}

console.log('🔍 Test du token Railway API...');
console.log('Token:', RAILWAY_API_TOKEN.substring(0, 10) + '...');
console.log('');

// Test simple : récupérer les projets existants
const query = `
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
`;

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
        console.log('Status HTTP:', res.statusCode);
        console.log('');

        try {
            const response = JSON.parse(body);

            if (res.statusCode === 200 && response.data) {
                console.log('✅ Token valide !');
                console.log('');
                console.log('Vos projets Railway :');
                const projects = response.data.projects.edges;

                if (projects.length === 0) {
                    console.log('  (Aucun projet existant)');
                } else {
                    projects.forEach((p, i) => {
                        console.log(`  ${i + 1}. ${p.node.name} (${p.node.id})`);
                    });
                }
                console.log('');
                console.log('🎉 Le token fonctionne correctement !');
            } else if (response.errors) {
                console.error('❌ Erreur API Railway :');
                response.errors.forEach(err => {
                    console.error('  -', err.message);
                });
                console.log('');
                console.log('💡 Solutions :');
                console.log('  1. Vérifiez que le token est correct');
                console.log('  2. Créez un nouveau token sur https://railway.app/account/tokens');
                console.log('  3. Assurez-vous que le token a les permissions nécessaires');
            } else {
                console.error('❌ Réponse inattendue :');
                console.error(body);
            }
        } catch (error) {
            console.error('❌ Erreur de parsing JSON :');
            console.error(error.message);
            console.log('');
            console.log('Réponse brute :');
            console.log(body);
        }
    });
});

req.on('error', (error) => {
    console.error('❌ Erreur réseau :');
    console.error(error.message);
});

req.write(data);
req.end();
