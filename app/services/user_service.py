# app/services/user_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


def create_user(db: Session, user_data: UserCreate) -> User:
    """
    Crée un nouvel utilisateur dans la base de données.
    Vérifie l’unicité de l’email et hash le mot de passe.

    Raises:
        HTTPException 400: si l’email est déjà utilisé.
    """
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email déjà utilisé"
        )

    hashed_password = get_password_hash(user_data.password)

    user = User(
        username=user_data.username,  # ✅ À ajouter
        full_name=user_data.full_name,
        email=user_data.email,
        role=user_data.role,
        hashed_password=hashed_password,
        is_active=True
)


    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: int) -> User:
    """
    Récupère un utilisateur par son ID.

    Raises:
        HTTPException 404: si l'utilisateur n'existe pas.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    return user


def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Récupère un utilisateur par email. Retourne None si inexistant.
    """
    return db.query(User).filter(User.email == email).first()


def get_all_users(db: Session) -> list[User]:
    """
    Retourne tous les utilisateurs de la base de données.
    """
    return db.query(User).all()
