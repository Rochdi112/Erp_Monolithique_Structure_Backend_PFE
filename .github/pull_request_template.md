---
name: 🚀 ERP MIF Maroc - Pull Request Template
about: Template standardisé pour les PRs du backend FastAPI
---

## 🎯 **Description des changements**

### Résumé
<!-- Décrivez brièvement les changements apportés -->

### Type de changement
- [ ] 🐛 Correction de bug
- [ ] ✨ Nouvelle fonctionnalité  
- [ ] 🔧 Refactoring/amélioration
- [ ] 📚 Documentation
- [ ] 🧪 Tests
- [ ] 🔒 Sécurité
- [ ] 🗄️ Base de données/migration

---

## 📋 **Checklist avant merge**

### Tests & Qualité
- [ ] ✅ Tous les tests passent localement (`pytest app/tests/ --disable-warnings -v`)
- [ ] 📊 Code coverage > 80%
- [ ] 🔍 Aucune vulnérabilité de sécurité détectée
- [ ] 🎨 Code formaté avec Black/isort

### Fonctionnel  
- [ ] 🗄️ Migration de base de données testée (`alembic upgrade head`)
- [ ] 🔐 Endpoints protégés par RBAC
- [ ] 📧 Notifications fonctionnelles (si applicable)
- [ ] 📁 Upload de documents testé (si applicable)

### Documentation
- [ ] 📝 README mis à jour (si nécessaire)
- [ ] 📖 Docstrings ajoutées pour nouvelles fonctions
- [ ] 🏷️ Schémas Pydantic documentés

---

## 🧪 **Instructions de test**

### Prérequis
```bash
# 1. Installation des dépendances
pip install -r requirements.txt

# 2. Configuration de l'environnement
cp .env.example .env  # Puis éditer .env

# 3. Migration de la base de données
alembic upgrade head

# 4. (Optionnel) Charger des données de test
python app/seed/seed_data.py
```

### Tests à effectuer
<!-- Décrivez les tests manuels spécifiques à effectuer -->

1. **Test d'authentification**:
   ```bash
   # Tester login
   curl -X POST http://localhost:8000/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@test.com", "password": "password"}'
   ```

2. **Test des endpoints modifiés**:
   <!-- Listez les endpoints à tester manuellement -->

---

## 🔄 **Changements dans la base de données**

- [ ] Aucune migration nécessaire
- [ ] ✅ Migration Alembic créée et testée
- [ ] ⚠️ Migration destructive (perte de données possible)

### Détails migration
<!-- Si migration, décrivez les changements de schéma -->

---

## 📊 **Impact et risques**

### Impact utilisateur
- [ ] Aucun impact
- [ ] Amélioration UX
- [ ] Changement breaking (nécessite mise à jour client)

### Risques identifiés
<!-- Listez les risques potentiels et mesures de mitigation -->

---

## 🔗 **Liens utiles**

- **Issue liée**: #[numéro]
- **Documentation**: [lien vers docs]
- **Démo/Screenshots**: [si applicable]

---

## 🤖 **Résultats CI/CD**

<!-- Cette section sera automatiquement mise à jour par GitHub Actions -->

### Statut des tests
- **Build Status**: ⏳ En attente...
- **Code Coverage**: ⏳ En cours...
- **Security Scan**: ⏳ En cours...

Les résultats détaillés apparaîtront automatiquement une fois les tests lancés.

---

## 👥 **Reviewers**

<!-- @mentionnez les personnes qui doivent reviewer -->
- [ ] @[nom-reviewer-1] - Validation technique
- [ ] @[nom-reviewer-2] - Validation fonctionnelle  
- [ ] @[nom-reviewer-3] - Validation sécurité

---

**🚦 Cette PR peut être mergée une fois que tous les tests passent et que 2 reviewers ont approuvé.**
