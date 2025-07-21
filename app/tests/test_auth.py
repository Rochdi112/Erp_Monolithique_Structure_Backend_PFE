import pytest
from fastapi.testclient import TestClient
from app.db.database import get_db
from app.models.user import User, UserRole
from app.core.security import get_password_hash


# ---------- Fixtures ----------

@pytest.fixture
def create_test_user():
    """
    Crée un utilisateur actif admin dans la base de test
    """
    db = next(get_db())
    existing = db.query(User).filter(User.email == "admin@test.com").first()
    if existing:
        db.delete(existing)
        db.commit()

    user = User(
        username="admin",
        full_name="Admin Test",
        email="admin@test.com",
        hashed_password=get_password_hash("secret123"),
        role=UserRole.admin,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def create_inactive_user():
    """
    Crée un utilisateur inactif
    """
    db = next(get_db())
    existing = db.query(User).filter(User.email == "inactive@test.com").first()
    if existing:
        db.delete(existing)
        db.commit()

    user = User(
        username="inactive",
        full_name="Inactive User",
        email="inactive@test.com",
        hashed_password=get_password_hash("secret123"),
        role=UserRole.technicien,
        is_active=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ---------- Tests ----------

def test_login_success(client: TestClient, create_test_user):
    """
    Connexion réussie avec email + mot de passe correct
    """
    response = client.post("/auth/token", data={
        "username": "admin@test.com",
        "password": "secret123"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient, create_test_user):
    """
    Connexion échoue si mauvais mot de passe
    """
    response = client.post("/auth/token", data={
        "username": "admin@test.com",
        "password": "wrongpass"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401


def test_login_unknown_email(client: TestClient):
    """
    Connexion échoue si email inconnu
    """
    response = client.post("/auth/token", data={
        "username": "notfound@test.com",
        "password": "secret123"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401


def test_login_inactive_user(client: TestClient, create_inactive_user):
    """
    Connexion échoue si user inactif
    """
    response = client.post("/auth/token", data={
        "username": "inactive@test.com",
        "password": "secret123"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 403
