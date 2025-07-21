# app/tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import Base, get_db
from app.core.security import create_access_token
from app.models.user import UserRole

# ⚠️ SQLite mémoire persistante via StaticPool
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # <--- Critique
)

# Création des tables à l'initialisation
Base.metadata.create_all(bind=engine)

# Nouvelle session isolée
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

@pytest.fixture(scope="function")
def db_session():
    """
    Fournit une session avec rollback après chaque test.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    """
    Fournit un client avec dépendance DB override vers db_session
    """
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()

# ------------------ TOKENS ------------------

@pytest.fixture
def admin_token():
    return create_access_token(data={"sub": "admin@test.com", "role": UserRole.admin})

@pytest.fixture
def responsable_token():
    return create_access_token(data={"sub": "resp@test.com", "role": UserRole.responsable})

@pytest.fixture
def technicien_token():
    return create_access_token(data={"sub": "tech@test.com", "role": UserRole.technicien})

@pytest.fixture
def client_token():
    return create_access_token(data={"sub": "client@test.com", "role": UserRole.client})
