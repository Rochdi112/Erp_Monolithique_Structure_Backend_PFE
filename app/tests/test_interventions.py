import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import SessionLocal
from app.models.user import User
from app.models.intervention import Intervention
from app.core.security import get_password_hash

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture(scope="module")
def admin_user_and_token(db):
    """Crée un utilisateur admin + token d’authentification"""
    user = User(
        username="intervadmin",
        email="intervadmin@example.com",
        hashed_password=get_password_hash("admin123"),
        role="admin",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    response = client.post(
        "/api/v1/auth/login",
        data={"username": "intervadmin", "password": "admin123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}, user

@pytest.fixture()
def created_intervention(db):
    """Créer une intervention temporaire pour les tests"""
    intervention = Intervention(
        titre="Intervention Temp",
        description="Pour test",
        type="corrective",
        statut="ouverte",
        urgence=True
    )
    db.add(intervention)
    db.commit()
    db.refresh(intervention)
    yield intervention
    db.delete(intervention)
    db.commit()

def test_create_intervention(admin_user_and_token):
    """Test création intervention"""
    headers, _ = admin_user_and_token
    response = client.post(
        "/api/v1/interventions/",
        json={
            "titre": "Test Intervention",
            "description": "Intervention de test",
            "type": "corrective",
            "statut": "ouverte",
            "urgence": True
        },
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["titre"] == "Test Intervention"
    assert data["type"] == "corrective"
    assert data["urgence"] is True

    # Nettoyage après test
    intervention_id = data["id"]
    client.delete(f"/api/v1/interventions/{intervention_id}", headers=headers)

def test_get_intervention_by_id(admin_user_and_token, created_intervention):
    """Récupération intervention par ID"""
    headers, _ = admin_user_and_token
    response = client.get(f"/api/v1/interventions/{created_intervention.id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == created_intervention.id

def test_get_all_interventions(admin_user_and_token):
    """Liste des interventions"""
    headers, _ = admin_user_and_token
    response = client.get("/api/v1/interventions/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_intervention_statut(admin_user_and_token, created_intervention):
    """Mise à jour statut"""
    headers, _ = admin_user_and_token
    response = client.put(
        f"/api/v1/interventions/{created_intervention.id}",
        json={"statut": "en_cours"},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["statut"] == "en_cours"

def test_delete_intervention(admin_user_and_token):
    """Suppression d'une intervention créée à la volée"""
    headers, _ = admin_user_and_token
    # Création d’une intervention à supprimer
    response = client.post(
        "/api/v1/interventions/",
        json={
            "titre": "To Delete",
            "description": "Temp",
            "type": "corrective",
            "statut": "ouverte",
            "urgence": False
        },
        headers=headers
    )
    assert response.status_code == 201
    intervention_id = response.json()["id"]

    # Suppression
    delete_resp = client.delete(f"/api/v1/interventions/{intervention_id}", headers=headers)
    assert delete_resp.status_code == 204
