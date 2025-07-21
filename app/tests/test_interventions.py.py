import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import SessionLocal
from app.models.user import User
from app.models.intervention import Intervention
from app.models.equipement import Equipement
from app.core.security import get_password_hash

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture()
def equipement(db):
    equip = Equipement(
        nom="Machine Test",
        type="électrique",
        localisation="Atelier A",
        frequence_entretien="mensuel"
    )
    db.add(equip)
    db.commit()
    db.refresh(equip)
    return equip

@pytest.fixture()
def admin_user_and_token(db):
    email = "intervadmin@example.com"
    user = db.query(User).filter_by(email=email).first()
    if not user:
        user = User(
            username="intervadmin",
            full_name="Admin Interventions",
            email=email,
            hashed_password=get_password_hash("admin123"),
            role="admin",
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    response = client.post(
        "/api/v1/auth/token",
        data={"username": email, "password": "admin123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200, f"Erreur login : {response.status_code} - {response.text}"
    token = response.json()["access_token"]
    return user, f"Bearer {token}"

@pytest.fixture()
def created_intervention(db, equipement):
    intervention = Intervention(
        titre="Intervention Temp",
        description="Pour test",
        type_intervention="corrective",
        statut="ouverte",
        urgence=True,
        equipement_id=equipement.id
    )
    db.add(intervention)
    db.commit()
    db.refresh(intervention)
    yield intervention
    db.delete(intervention)
    db.commit()

def test_create_intervention(admin_user_and_token, equipement):
    _, headers = admin_user_and_token
    response = client.post(
        "/api/v1/interventions/",
        json={
            "titre": "Test Intervention",
            "description": "Intervention de test",
            "type": "corrective",
            "statut": "ouverte",
            "urgence": True,
            "equipement_id": equipement.id
        },
        headers={"Authorization": headers}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["titre"] == "Test Intervention"
    assert data["type"] == "corrective"
    assert data["urgence"] is True
    client.delete(f"/api/v1/interventions/{data['id']}", headers={"Authorization": headers})

def test_get_intervention_by_id(admin_user_and_token, created_intervention):
    _, headers = admin_user_and_token
    response = client.get(f"/api/v1/interventions/{created_intervention.id}", headers={"Authorization": headers})
    assert response.status_code == 200
    assert response.json()["id"] == created_intervention.id

def test_get_all_interventions(admin_user_and_token):
    _, headers = admin_user_and_token
    response = client.get("/api/v1/interventions/", headers={"Authorization": headers})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_intervention_statut(admin_user_and_token, created_intervention):
    _, headers = admin_user_and_token
    response = client.patch(
        f"/api/v1/interventions/{created_intervention.id}/statut",
        params={"statut": "en_cours", "remarque": "Test maj"},
        headers={"Authorization": headers}
    )
    assert response.status_code == 200
    assert response.json()["statut"] == "en_cours"

def test_delete_intervention(admin_user_and_token, equipement):
    _, headers = admin_user_and_token
    response = client.post(
        "/api/v1/interventions/",
        json={
            "titre": "To Delete",
            "description": "Temp",
            "type": "corrective",
            "statut": "ouverte",
            "urgence": False,
            "equipement_id": equipement.id
        },
        headers={"Authorization": headers}
    )
    assert response.status_code == 201
    intervention_id = response.json()["id"]
    delete_resp = client.delete(f"/api/v1/interventions/{intervention_id}", headers={"Authorization": headers})
    assert delete_resp.status_code == 204