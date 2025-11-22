# Guide de Contribution EAZYNOVA

Merci de votre intérêt pour contribuer à EAZYNOVA ! 🎉

## Code de Conduite

En participant à ce projet, vous acceptez de respecter notre [Code de Conduite](CODE_OF_CONDUCT.md).

## Comment Contribuer

### Signaler des Bugs 🐛

Les bugs sont suivis via [GitHub Issues](https://github.com/your-repo/eazynova/issues).

**Avant de créer un rapport de bug :**
- Vérifiez qu'il n'existe pas déjà
- Collectez les informations nécessaires

**Créer un bon rapport de bug :**
```markdown
**Description**
Description claire du problème

**Reproduction**
1. Aller à '...'
2. Cliquer sur '...'
3. Voir l'erreur

**Comportement attendu**
Description du comportement attendu

**Captures d'écran**
Si applicable, ajoutez des captures d'écran

**Environnement:**
 - OS: [ex. Ubuntu 22.04]
 - Odoo Version: [ex. 19.0]
 - Module Version: [ex. 19.0.1.0.0]
```

### Proposer des Améliorations 💡

Les améliorations sont suivies via [GitHub Issues](https://github.com/your-repo/eazynova/issues).

**Template pour proposer une amélioration :**
```markdown
**Problème actuel**
Description du problème ou limitation

**Solution proposée**
Description de la solution

**Alternatives considérées**
Autres solutions envisagées

**Contexte additionnel**
Tout autre contexte utile
```

### Pull Requests 🔀

1. **Fork le projet**
2. **Créer une branche** (`git checkout -b feature/AmazingFeature`)
3. **Faire vos modifications**
4. **Ajouter des tests** si applicable
5. **Commit** (`git commit -m 'Add: Amazing Feature'`)
6. **Push** (`git push origin feature/AmazingFeature`)
7. **Ouvrir une Pull Request**

## Standards de Code

### Python

- Suivre [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Utiliser les conventions Odoo
- Commenter en français
- Docstrings en français

**Exemple :**
```python
def ma_fonction(param1, param2):
    """
    Description courte de la fonction
    
    Args:
        param1 (str): Description du paramètre 1
        param2 (int): Description du paramètre 2
        
    Returns:
        bool: Description du retour
        
    Raises:
        ValueError: Si param2 < 0
    """
    # Vérification des paramètres
    if param2 < 0:
        raise ValueError("param2 doit être positif")
    
    # Traitement
    result = self._traitement_interne(param1, param2)
    
    return result
```

### JavaScript

- Utiliser ES6+
- Commentaires en français
- JSDoc pour les fonctions importantes

### XML

- Indentation: 4 espaces
- Ordre des attributs: id, name, autres
- Commentaires pour sections importantes

### Commits

Format des messages de commit :
```
Type: Description courte (max 50 caractères)

Description détaillée si nécessaire (max 72 caractères par ligne)

Refs: #123
```

**Types de commit :**
- `Add:` Nouvelle fonctionnalité
- `Fix:` Correction de bug
- `Update:` Mise à jour de fonctionnalité
- `Refactor:` Refactorisation sans changement fonctionnel
- `Docs:` Documentation uniquement
- `Test:` Ajout ou modification de tests
- `Style:` Formatage, point-virgule manquant, etc.
- `Perf:` Amélioration de performance
- `Chore:` Maintenance

## Tests

### Lancer les tests
```bash
# Tous les tests
python odoo-bin -c odoo.conf -d test_db --test-enable --stop-after-init -i eazynova

# Tests spécifiques
python odoo-bin -c odoo.conf -d test_db --test-enable --stop-after-init -i eazynova --test-tags test_facial_recognition
```

### Écrire des tests

- Un test par fonctionnalité
- Nom explicite: `test_<fonctionnalite>_<scenario>`
- Suivre le pattern AAA (Arrange, Act, Assert)

## Documentation

- Documenter toute nouvelle fonctionnalité
- Mettre à jour le README si nécessaire
- Ajouter des exemples d'utilisation

## Processus de Review

1. **Vérification automatique** (CI/CD)
   - Tests unitaires
   - Linting
   - Coverage

2. **Review humaine**
   - Code quality
   - Fonctionnalité
   - Documentation

3. **Approbation** par un mainteneur

4. **Merge** dans la branche principale

## Questions ?

N'hésitez pas à poser vos questions via :
- [GitHub Discussions](https://github.com/your-repo/eazynova/discussions)
- Email: dev@eazynova.com

Merci pour votre contribution ! 🙏