from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from app.services.auth_service import authenticate_user
from app.db.database import SessionLocal
from app.schemas.user import TokenResponse

router = APIRouter(
    tags=["auth"],
    responses={404: {"description": "Not found"}}
)

# Dépendance DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/token", response_model=TokenResponse, summary="Connexion utilisateur", description="Authentifie un utilisateur avec email + mot de passe. Retourne un token JWT si valide.")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    ⚙️ Endpoint de login :
    - Vérifie l'email + mot de passe.
    - Retourne un token JWT avec rôle embarqué.
    - Utilisé dans le header `Authorization: Bearer <token>`
    """
    return authenticate_user(db, username, password)
