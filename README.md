# ERP Interventions — Backend FastAPI (MVP1)

[![CI/CD Pipeline](https://github.com/Rochdi112/Erp_Monolithique_Structure_Backend_PFE/actions/workflows/backend-ci.yml/badge.svg)](https://gi## 🧪 Tests unitaires

L'ensemble du projet est testé avec **pytest** et **fixtures**.

**Lancer tous les tests :**

```bash
pytest app/tests/ --disable-warnings -v
```

**Exemple de couverture validé à jour:**

* `test_auth.py` (login, tokens, erreurs)
* `test_users.py` (création, unicité, droits)
* `test_equipements.py` (CRUD, droits)
* `test_techniciens.py` (association compétence, droits)
* etc.

---

## 🚦 CI/CD & Automatisation

### GitHub Actions Pipeline

Le projet dispose d'un pipeline CI/CD automatisé qui se lance à chaque push/PR :

- ✅ **Tests automatisés** avec couverture de code
- 🔍 **Analyse de sécurité** (pip-audit)
- 🎨 **Vérification de la qualité** (Black, isort, Flake8)
- 📊 **Rapports automatiques** en commentaire de PR
- 🏷️ **Badges de statut** sur le README

### Commandes locales (Makefile)

```bash
# 🔧 Valider l'environnement
make validate

# 🧪 Lancer les tests avec couverture
make test-cov

# 📊 Générer un rapport complet
make report

# 🎨 Formatter le code
make format

# 🔄 Pipeline complet (comme en CI)
make ci
```

### Scripts utiles

- `validate_env.py` - Vérifie que l'environnement est prêt
- `generate_report.py` - Génère un rapport HTML de qualité
- `.github/workflows/backend-ci.yml` - Pipeline GitHub Actions

### Templates

- **Pull Request** : Template standardisé avec checklist automatique
- **Issues** : Templates pour bugs et nouvelles fonctionnalités
- **Badges** : Statut CI, couverture, version Python...

---Erp_Monolithique_Structure_Backend_PFE/actions/workflows/backend-ci.yml)
[![codecov](https://codecov.io/gh/Rochdi112/Erp_Monolithique_Structure_Backend_PFE/branch/main/graph/badge.svg)](https://codecov.io/gh/Rochdi112/Erp_Monolithique_Structure_Backend_PFE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)

## 📑 Sommaire

- [Contexte & Objectifs](#contexte--objectifs)
- [Fonctionnalités](#fonctionnalités)
- [Architecture du projet](#architecture-du-projet)
- [Installation](#installation)
- [Lancement du serveur](#lancement-du-serveur)
- [Structure du code](#structure-du-code)
- [Sécurité & RBAC](#sécurité--rbac)
- [Endpoints principaux](#endpoints-principaux)
- [Jeux de données de démarrage (seed)](#jeux-de-données-de-démarrage-seed)
- [Tests unitaires](#tests-unitaires)
- [CI/CD & Automatisation](#cicd--automatisation)
- [Déploiement (Docker)](#déploiement-docker)
- [Crédits](#crédits)

---

## 🏭 Contexte & Objectifs

Ce projet est le backend du **Mini ERP Interventions** développé avec [FastAPI](https://fastapi.tiangolo.com/) pour la gestion intelligente des interventions industrielles (correctives & préventives).

**Objectifs du MVP1 :**
- Fournir une API REST complète et sécurisée pour la gestion :
    - des utilisateurs (RBAC)
    - des techniciens (compétences, équipes)
    - des équipements (inventaire)
    - des interventions (cycle de vie complet)
    - du planning préventif, notifications, documents
- Préparer la solution à l’automatisation, au reporting avancé, à l’intégration SI et à l’audit.

---

## 🚀 Fonctionnalités

- Authentification JWT sécurisée
- Gestion multi-rôles (admin, responsable, technicien, client)
- CRUD complet sur : utilisateurs, techniciens, équipements, interventions
- Association de compétences technicien
- Gestion planning préventif
- Notifications par email/log
- Upload de documents lié aux interventions
- Recherche/filtres avancés
- RBAC fort et logs d’audit
- Seed/fixtures réalistes pour tests

---

## 🏗️ Architecture du projet

```

ERP\_BACKEND/
├── app/
│   ├── main.py
│   ├── api/v1/           # Endpoints versionnés (REST)
│   ├── core/             # Sécurité, config, RBAC, exceptions
│   ├── db/               # Connexion, Base SQLAlchemy
│   ├── models/           # Modèles ORM
│   ├── schemas/          # Schémas Pydantic (validation)
│   ├── services/         # Logique métier
│   ├── tasks/            # Tâches background/notifications
│   ├── seed/             # Génération de jeux de données (Faker)
│   ├── tests/            # Tests unitaires/fixtures
│   ├── static/           # Uploads de documents
│   ├── templates/        # Templates emails HTML
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
├── README.md

````

---

## ⚙️ Installation

**Prérequis :**
- Python 3.11+
- PostgreSQL 14+
- [Git](https://git-scm.com/)
- (Optionnel) [Docker](https://www.docker.com/)

**1. Clonez le repo :**
```bash
git clone https://github.com/<your-org>/erp-interventions-backend.git
cd erp-interventions-backend
````

**2. Installez les dépendances :**

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate          # Windows

pip install --upgrade pip
pip install -r requirements.txt
```

**3. Paramétrez votre `.env`** (copiez `.env.example` si présent).

**4. Initialisez la base de données :**

```bash
alembic upgrade head
```

**5. (Optionnel) Seed de données :**

```bash
python app/seed/seed_data.py
```

---

## ▶️ Lancement du serveur

```bash
uvicorn app.main:app --reload
```

L’API sera disponible sur [http://127.0.0.1:8000](http://127.0.0.1:8000)
Documentation Swagger : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📁 Structure du code

* `api/v1/` — Endpoints versionnés (REST)
* `models/` — Modèles SQLAlchemy
* `schemas/` — Schémas Pydantic v2 (`model_config`)
* `services/` — Logique métier
* `core/` — Sécurité (JWT, RBAC), exceptions, config
* `db/` — Connexion BDD, Base SQLAlchemy
* `tests/` — Tests unitaires, fixtures
* `seed/` — Jeux de données de démarrage (Faker)
* `static/uploads/` — Pièces jointes interventions

---

## 🔒 Sécurité & RBAC

* Authentification par JWT (OAuth2)
* Hash de mots de passe (bcrypt)
* **RBAC fort** : chaque endpoint protégé par rôle (`admin`, `responsable`, `technicien`, `client`)
* Données sensibles non exposées
* Logs d’accès et d’actions critiques

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
| Documents     | `/api/v1/documents/`     | Tous/Tech   |
| Filtres       | `/api/v1/filters/`       | Tous        |

Voir la doc OpenAPI pour la liste complète et les permissions détaillées.

---

## 🧑‍💻 Jeux de données de démarrage (seed)

Le dossier `seed/` fournit un script générant :

* Admin, responsables, techniciens, clients
* Équipements réalistes
* Interventions variées (corrective/préventive)
* Notifications et planning
  Lancez : `python app/seed/seed_data.py`

---

## 🧪 Tests unitaires

L’ensemble du projet est testé avec **pytest** et **fixtures**.

**Lancer tous les tests :**

```bash
pytest app/tests/ --disable-warnings -v
```

**Exemple de couverture validé à jour:**

* `test_auth.py` (login, tokens, erreurs)
* `test_users.py` (création, unicité, droits)
* `test_equipements.py` (CRUD, droits)
* `test_techniciens.py` (association compétence, droits)
* etc.

---

## 🐳 Déploiement (Docker)

Le projet est **dockerisé** (prod/dev).

```bash
docker-compose up --build
```

* `db` = PostgreSQL
* `web` = FastAPI backend
* (Ajoutez un front ou un reverse proxy si besoin)

---

## 📚 Crédits

* Projet encadré par : \[Votre école/entreprise]
* Réalisé par : \[Votre nom]
* Stack : FastAPI, SQLAlchemy, Alembic, PostgreSQL, Pydantic v2, Docker, Pytest, Faker

---

> **ERP Interventions** — Projet PFE 2025, open source pour MIF Maroc
> Documentation générée le : 22/07/2025
