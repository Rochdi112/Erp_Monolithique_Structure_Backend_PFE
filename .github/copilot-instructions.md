# Copilot Instructions for ERP Interventions Backend (FastAPI)

## Project Overview
- **Monolithic FastAPI backend** for industrial interventions management (users, technicians, equipment, interventions, planning, notifications, documents).
- **Domain-driven structure**: API endpoints, business logic, data models, and schemas are separated by concern.
- **RBAC enforced**: All endpoints are protected by role-based access control (admin, responsable, technicien, client).

## Key Directories & Patterns
- `app/main.py`: FastAPI app entrypoint.
- `app/api/v1/`: Versioned REST endpoints, one file per resource (e.g., `users.py`, `equipements.py`).
- `app/models/`: SQLAlchemy ORM models, one file per entity.
- `app/schemas/`: Pydantic v2 schemas for request/response validation, mirrors models.
- `app/services/`: Business logic, called from API routes, keeps endpoints thin.
- `app/core/`: Security (JWT, RBAC), config, and custom exceptions.
- `app/db/`: Database connection, Alembic migrations, and base class.
- `app/seed/`: Data seeding scripts using Faker for dev/testing.
- `app/tests/`: Pytest-based unit tests, one file per resource, uses fixtures.

## Developer Workflows
- **Install**: `pip install -r requirements.txt` (use Python 3.11+)
- **DB Migrations**: `alembic upgrade head` (see `app/db/`)
- **Seed Data**: `python app/seed/seed_data.py`
- **Run Server**: `uvicorn app.main:app --reload`
- **Run Tests**: `pytest app/tests/ --disable-warnings -v`
- **Docker**: `docker-compose up --build` (runs both FastAPI and PostgreSQL)

## Project Conventions
- **Endpoints**: All under `/api/v1/`, grouped by resource, follow RESTful naming.
- **RBAC**: Use `Depends(get_current_user)` and role checks in endpoints. See `app/core/rbac.py`.
- **Schemas**: Use Pydantic v2, keep request/response schemas in `schemas/`, not in models.
- **Services**: Place business logic in `services/`, not in API or models.
- **Testing**: Use fixtures for setup, test files mirror API resource files.
- **Seeding**: Use `seed/seed_data.py` for realistic test data.

## Integration & External Dependencies
- **PostgreSQL**: Main DB, configured in `.env` and `app/db/database.py`.
- **JWT Auth**: Implemented in `core/security.py`, used in all protected endpoints.
- **Email/Notifications**: Handled in `tasks/` and `services/notification_service.py`.
- **Docker**: For local/prod deployment, see `docker-compose.yml`.

## Examples
- To add a new resource: create model, schema, service, and API file in respective folders.
- To add a protected endpoint: use FastAPI `Depends` with RBAC check.
- To test a new feature: add a test in `app/tests/` with fixtures.

## References
- See `README.md` for full setup, architecture, and workflow details.
- See `app/core/rbac.py` and `app/core/security.py` for security patterns.
- See `app/services/` for business logic structure.

---

> Update this file if project structure or conventions change. For questions, see `README.md` or ask maintainers.
