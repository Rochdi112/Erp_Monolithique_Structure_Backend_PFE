# app/api/v1/users.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import SessionLocal
from app.services.user_service import create_user, get_user_by_id, get_all_users
from app.schemas.user import UserCreate, UserOut
from app.core.rbac import admin_required

router = APIRouter(
    prefix="/users",
    tags=["utilisateurs"],
    responses={404: {"description": "Utilisateur non trouvé"}}
)

# Dépendance DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/",
    response_model=UserOut,
    summary="Créer un utilisateur",
    description="Création d’un nouvel utilisateur (réservé à l’administrateur uniquement).",
    dependencies=[Depends(admin_required)]
)
def create_new_user(data: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, data)

@router.get(
    "/{user_id}",
    response_model=UserOut,
    summary="Lire un utilisateur par ID",
    description="Retourne un utilisateur par son ID. Accès réservé à l’administrateur.",
    dependencies=[Depends(admin_required)]
)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_by_id(db, user_id)

@router.get(
    "/",
    response_model=List[UserOut],
    summary="Lister tous les utilisateurs",
    description="Retourne la liste complète des utilisateurs (réservé à l’administrateur).",
    dependencies=[Depends(admin_required)]
)
def list_users(db: Session = Depends(get_db)):
    return get_all_users(db)
