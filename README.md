# ERP Backend MVP1

Projet FastAPI pour la gestion intelligente des interventions industrielles (correctives & préventives).

---

## 🧩 **Domaines & Services Métier du Backend**

Le backend est découpé en **8 services métier principaux** :

1. Authentification (`auth_service.py`)
2. Utilisateurs (`user_service.py`)
3. Techniciens & Compétences (`technicien_service.py`)
4. Équipements (`equipement_service.py`)
5. Interventions (`intervention_service.py`)
6. Planning (`planning_service.py`)
7. Notifications (`notification_service.py`)
8. Documents (`document_service.py`)

---

## ✅ **Services validés et testés à ce jour**

- [x] **Auth** : Authentification JWT, sécurité, RBAC
- [x] **Utilisateurs** : Gestion CRUD, sécurité, unicité, RBAC
- [x] **Techniciens & Compétences** : Création, association compétences, RBAC, tests complets

### 🟡 **Services en cours de validation**

- [ ] Équipements
- [ ] Interventions
- [ ] Planning
- [ ] Notifications
- [ ] Documents

---

## 🚦 **Tests & Qualité**

- **100% des tests passent sur les 3 premiers services validés**
- Voir `/app/tests/` et le badge pytest (à ajouter après CI/CD si besoin)
- Rapports techniques détaillés disponibles dans `/docs/`

---

## 🛠️ **Stack technique**

- FastAPI, SQLAlchemy, Alembic, PostgreSQL
- Authentification JWT, RBAC, passlib
- Tests : pytest, Faker, DB isolée
- Background tasks : APScheduler, FastAPI-Mail
- Docker-ready (`Dockerfile` & `docker-compose.yml`)

---

## 📦 **Installation rapide**

```bash
git clone https://github.com/Rochdi112/Erp_Monolithique_Structure_Backend_PFE.git
cd Erp_Monolithique_Structure_Backend_PFE
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
pip install -r requirements.txt
````

## 🚀 **Lancer le projet**

```bash
uvicorn app.main:app --reload
```

## 🧪 **Lancer les tests**

```bash
pytest app/tests/ --disable-warnings -v
```

---

## 📂 **Structure principale**

* `app/models/` : ORM SQLAlchemy
* `app/schemas/` : Schémas Pydantic (validation)
* `app/services/` : Logique métier par domaine
* `app/api/v1/` : Endpoints REST versionnés
* `app/tests/` : Tests unitaires, fixtures
* `app/core/` : Sécurité, RBAC, config
* `app/seed/` : Génération de données réalistes

---

## 📄 **Rapports techniques**

Les rapports techniques PDF de validation de chaque service sont disponibles dans le dossier `/docs/`.

---

## 👨‍💻 **Auteur**

Rochdi112 / PFE MIF Maroc 2025

---

```

---