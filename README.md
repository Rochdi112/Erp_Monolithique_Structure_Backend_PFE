# ERP Interventions — Backend FastAPI

[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-blue.svg)](https://www.postgresql.org/)
[![Tests](https://img.shields.io/badge/tests-38%20passed-brightgreen.svg)](#tests)

## 📑 Sommaire

- [Contexte & Objectifs](#contexte--objectifs)
- [Fonctionnalités](#fonctionnalités)
- [Services / Domaines](#services--domaines)
- [Architecture du projet](#architecture-du-projet)
- [Installation](#installation)
- [Lancement du serveur](#lancement-du-serveur)
- [Structure du code](#structure-du-code)
- [Sécurité & RBAC](#sécurité--rbac)
- [Endpoints principaux](#endpoints-principaux)
- [Tests](#tests)
- [Comment tester par dossier](#comment-tester-par-dossier)
- [Docs OpenAPI (Swagger/Redoc)](#docs-openapi-swaggerredoc)
- [Jeux de données (seed)](#jeux-de-données-seed)
- [Déploiement (Docker)](#déploiement-docker)
- [Crédits](#crédits)

---

## 🏭 Contexte & Objectifs

Backend du Mini ERP Interventions (MIF Maroc) pour la gestion des interventions industrielles (correctives & préventives) avec FastAPI.

Objectifs:
- API REST sécurisée (JWT, RBAC) couvrant utilisateurs, techniciens, équipements, interventions, planning, notifications et documents.
- Qualité: tests automatisés, structure claire, observabilité et maintenabilité.

---

## 🚀 Fonctionnalités

- Authentification JWT
- RBAC multi-rôles (admin, responsable, technicien, client)
- CRUD: utilisateurs, techniciens, équipements, interventions
- Workflow interventions (planifié → en_cours → terminé / annulé, attente_pieces)
- Planning préventif (APScheduler)
- Notifications email/log
- Upload de documents
- Recherche/filtres, pagination, tri
- Audit minimal et validations

---

## 🧩 Services / Domaines

- Authentification: login JWT, profils
- Utilisateurs: CRUD, rôles, activation
- Techniciens: compétences, disponibilité
- Équipements: inventaire, sites
- Interventions: cycle de vie, affectation, pièces
- Planning: préventif, non-chevauchement
- Documents: upload/download sécurisé
- Notifications: envoi mail/log
- Filtres/Recherche: pagination et tri

---

## 🏗️ Architecture du projet

```
ERP_BACKEND/
├── app/
│   ├── main.py
│   ├── api/v1/           # Endpoints versionnés (REST)
│   ├── core/             # Sécurité, config, RBAC, exceptions
│   ├── db/               # Connexion, Base SQLAlchemy
│   ├── models/           # Modèles ORM
│   ├── schemas/          # Schémas Pydantic v2
│   ├── services/         # Logique métier
│   ├── tasks/            # Tâches & scheduler
│   ├── seed/             # Données de démo (Faker)
│   ├── tests/            # Pytest
│   ├── static/           # Uploads
│   └── templates/        # Emails HTML
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
└── README.md
```

---

## ⚙️ Installation

1) Cloner le dépôt

```powershell
git clone https://github.com/Rochdi112/FastApi_ERP_BackEnd_MIF_Maroc.git
cd FastApi_ERP_BackEnd_MIF_Maroc
```

2) Créer un venv et installer les dépendances

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Linux/Mac:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

3) Paramétrer `.env` (POSTGRES_*, SECRET_KEY, etc.)

4) Initialiser la base de données

```bash
alembic upgrade head
```

5) (Optionnel) Seed de données

```bash
python app/seed/seed_data.py
```

---

## ▶️ Lancement du serveur

Windows (PowerShell):

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Linux/Mac:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API: http://127.0.0.1:8000

---

## 📁 Structure du code

- `api/v1/` — Endpoints REST v1
- `models/` — SQLAlchemy 2.0
- `schemas/` — Pydantic v2
- `services/` — Règles métier et transactions
- `core/` — JWT, RBAC, exceptions, config
- `db/` — Connexion BDD
- `tests/` — Tests unitaires, fixtures
- `seed/` — Données de démo (Faker)
- `static/uploads/` — Pièces jointes

---

## 🔒 Sécurité & RBAC

- JWT (OAuth2), bcrypt pour mots de passe
- Rôles: `admin`, `responsable`, `technicien`, `client`
- Dépendances de rôle sur chaque endpoint
- Données sensibles masquées dans les DTOs

---

## 🔗 Endpoints principaux

| Ressource     | Endpoints                | Accès       |
| ------------- | ------------------------ | ----------- |
| Auth          | `/api/v1/auth/token`     | Public      |
| Utilisateurs  | `/api/v1/users/`         | Admin       |
| Techniciens   | `/api/v1/techniciens/`   | Responsable |
| Équipements   | `/api/v1/equipements/`   | Responsable |
| Interventions | `/api/v1/interventions/` | Selon rôle  |
| Planning      | `/api/v1/planning/`      | Responsable |
| Notifications | `/api/v1/notifications/` | Resp/Admin  |
| Documents     | `/api/v1/documents/`     | Authentifié |
| Filtres       | `/api/v1/filters/`       | Authentifié |

Consultez la doc OpenAPI pour le détail et les permissions spécifiques.

---

## � Tests

Exécution locale (SQLite en mémoire pendant les tests):

```powershell
pytest -q
```

Résultat actuel (11/08/2025): 38 passed in ~13s.

Couverture/rapports (optionnels):

```powershell
pytest app/tests/ --cov=app --cov-report=term --cov-report=html:htmlcov -v
```

Les rapports HTML sont générés dans `htmlcov/` (ignoré par git).

---

## Comment tester par dossier

- Auth: `app/tests/test_auth.py`
- Utilisateurs: `app/tests/test_users.py`
- Techniciens: `app/tests/test_techniciens.py`
- Équipements: `app/tests/test_equipements.py`
- Interventions: `app/tests/test_interventions.py`
- Planning: `app/tests/test_planning.py`
- Documents: `app/tests/test_documents.py`
- Notifications: `app/tests/test_notifications.py`
- Filtres: `app/tests/test_filters.py`

Exécuter un seul module:

```powershell
pytest app/tests/test_users.py -q
```

---

## Docs OpenAPI (Swagger/Redoc)

- Swagger UI: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc

Le schéma OpenAPI est exposé par FastAPI (tous les endpoints sous `/api/v1`).

---

## 🧑‍💻 Jeux de données (seed)

```powershell
python app/seed/seed_data.py
```

---

## 🐳 Déploiement (Docker)

```bash
docker-compose up --build
```

Services:
- `db` PostgreSQL
- `web` FastAPI backend

---

## 📚 Crédits

- Projet: MIF Maroc
- Réalisé par: Équipe PFE
- Stack: FastAPI, SQLAlchemy 2.0, Alembic, PostgreSQL, Pydantic v2, Docker, Pytest, Faker
