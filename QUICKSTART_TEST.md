# 🚀 Démarrage rapide - Test EAZYNOVA

Guide ultra-rapide pour tester EAZYNOVA avec Docker en **5 minutes** ! ⚡

## ⚡ TL;DR - La commande magique

```bash
./test-docker.sh
```

C'est tout ! 🎉

## 📋 Ce que vous allez avoir

Après cette commande unique, vous aurez :

✅ **Odoo 19 CE** avec tous les modules EAZYNOVA
✅ **PostgreSQL 15** pour la base de données
✅ **PgAdmin 4** pour gérer la base
✅ **MailHog** pour capturer les emails de test
✅ **Tous les modules installés** et prêts à tester

## 🔗 Accès rapide

Une fois démarré (environ 2-3 minutes) :

| Service | URL | Login | Mot de passe |
|---------|-----|-------|--------------|
| **Odoo** | http://localhost:8069 | admin | admin |
| **PgAdmin** | http://localhost:5050 | admin@eazynova.local | admin |
| **MailHog** | http://localhost:8025 | - | - |

## 🧪 Tester le module SaaS (eazynova_website)

### 1. Installer le module

1. Ouvrir http://localhost:8069
2. Se connecter (admin / admin)
3. Aller dans **Apps**
4. Chercher **"EAZYNOVA - Site Web SaaS"**
5. Cliquer sur **Installer**

### 2. Tester le site web SaaS

| Page | URL | Description |
|------|-----|-------------|
| Accueil | http://localhost:8069/ | Page d'accueil marketing |
| Tarifs | http://localhost:8069/saas/pricing | Page de tarification |
| Inscription | http://localhost:8069/saas/signup | Formulaire d'inscription |
| Fonctionnalités | http://localhost:8069/saas/features | Liste des fonctionnalités |

### 3. Créer un abonnement de test

1. Aller sur http://localhost:8069/saas/signup
2. Remplir le formulaire :
   - **Entreprise** : Test Company
   - **Contact** : John Doe
   - **Email** : test@example.com
   - **Téléphone** : +33 1 23 45 67 89
   - **Nombre d'utilisateurs** : 5
3. Soumettre
4. ✅ Vérifier l'email dans **MailHog** : http://localhost:8025

### 4. Gérer les abonnements (Backend)

1. Dans Odoo, aller dans le menu **SaaS EAZYNOVA**
2. Voir :
   - **Abonnements** : Liste des abonnements clients
   - **Instances** : Instances provisionnées
   - **Plans** : Configuration des tarifs

## 🛠️ Commandes utiles

```bash
# Voir les logs en temps réel
docker-compose -f docker-compose.dev.yml logs -f

# Voir seulement les logs Odoo
docker-compose -f docker-compose.dev.yml logs -f odoo

# Redémarrer Odoo
docker-compose -f docker-compose.dev.yml restart odoo

# Arrêter tout
docker-compose -f docker-compose.dev.yml down

# Nettoyer et recommencer à zéro
./test-docker.sh --clean
```

## 📧 Tester les emails

Tous les emails envoyés par Odoo sont capturés dans **MailHog**.

Pour tester :
1. Créer un abonnement SaaS
2. Aller sur http://localhost:8025
3. Voir les emails :
   - ✉️ Bienvenue + Essai gratuit
   - ✉️ Credentials de connexion
   - ✉️ Notifications diverses

## 🐛 Problèmes courants

### Odoo ne démarre pas ?

```bash
# Vérifier les logs
docker-compose -f docker-compose.dev.yml logs odoo

# Redémarrer
docker-compose -f docker-compose.dev.yml restart odoo
```

### Port déjà utilisé ?

Si le port 8069 est déjà pris, éditez `.env` :
```env
ODOO_PORT=8070  # Ou un autre port libre
```

Puis redémarrez :
```bash
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml up -d
```

### Module non visible ?

```bash
# Mettre à jour la liste des modules
docker exec -it eazynova_test_odoo odoo -d eazynova_test -u all --stop-after-init
docker-compose -f docker-compose.dev.yml restart odoo
```

### Tout plante ? Reset complet !

```bash
./test-docker.sh --clean
```

⚠️ **Attention** : Cette commande supprime TOUTES les données !

## 📚 Documentation complète

Pour aller plus loin, consultez **[DOCKER_TEST.md](./DOCKER_TEST.md)** :
- Configuration avancée
- Développement de modules
- Debugging
- Cas d'usage détaillés
- Sauvegarde/restauration
- Et bien plus...

## 🎯 Workflow de test complet

Voici un scénario de test complet du SaaS :

1. ✅ **Inscription** : Créer un compte test via /saas/signup
2. ✅ **Email** : Vérifier la réception dans MailHog
3. ✅ **Provisioning** : Voir l'instance créée dans SaaS > Instances
4. ✅ **Portail** : Se connecter au portail client
5. ✅ **Upgrade** : Modifier le nombre d'utilisateurs
6. ✅ **Activation** : Activer l'abonnement payant
7. ✅ **Facture** : Vérifier la facture de configuration
8. ✅ **Crons** : Tester les tâches automatiques
9. ✅ **Annulation** : Annuler l'abonnement
10. ✅ **Suppression** : Vérifier la suppression après 30 jours

## 💡 Astuces

### Rechargement automatique

Le mode dev est activé avec **rechargement automatique**. Modifiez le code Python et il sera rechargé automatiquement !

### Shell Odoo

Pour tester du code Python directement :
```bash
docker exec -it eazynova_test_odoo odoo shell -d eazynova_test
```

Puis :
```python
# Lister les abonnements
env['saas.subscription'].search([])

# Créer un abonnement
sub = env['saas.subscription'].create({
    'partner_id': 1,
    'plan_id': 1,
    'nb_users': 5,
})

# Démarrer l'essai
sub.action_start_trial()
```

### Vérifier les crons

```python
# Dans le shell Odoo
env['saas.subscription']._cron_check_trial_expiration()
env['saas.subscription']._cron_generate_invoices()
```

## 🆘 Besoin d'aide ?

1. 📖 Lire **[DOCKER_TEST.md](./DOCKER_TEST.md)** (documentation complète)
2. 🔍 Vérifier les logs : `docker-compose -f docker-compose.dev.yml logs`
3. 🐛 Créer une issue : https://github.com/MASITH-developpement/EAZYNOVA/issues

## 🎉 C'est parti !

```bash
./test-docker.sh
```

Et rendez-vous sur **http://localhost:8069** ! 🚀

---

**Bon test !** 🧪✨
