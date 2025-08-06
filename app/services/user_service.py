from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

def create_user(db: Session, user_data: UserCreate) -> User:
    """
    Crée un nouvel utilisateur :
    - Vérifie l’unicité email/username
    - Hash le mot de passe
    - Ajoute à la DB

    Raises:
        HTTPException 409: email ou username déjà utilisé.
    """
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email déjà utilisé."
        )
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username déjà utilisé."
        )

    hashed_password = get_password_hash(user_data.password)
    user = User(
        username=user_data.username,
        full_name=user_data.full_name,
        email=user_data.email,
        role=user_data.role,
        hashed_password=hashed_password,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_id(db: Session, user_id: int) -> User:
    """
    Récupère un utilisateur par ID.
    Raises:
        HTTPException 404: si utilisateur inexistant.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé."
        )
    return user

def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Récupère un utilisateur par email.
    """
    return db.query(User).filter(User.email == email).first()

def get_all_users(db: Session) -> list[User]:
    """
    Liste tous les utilisateurs.
    """
    return db.query(User).all()

def update_user(db: Session, user_id: int, update_data: UserUpdate) -> User:
    """
    Met à jour les infos (nom, mot de passe) d’un utilisateur.
    Raises:
        HTTPException 404: si utilisateur inexistant.
    """
    user = get_user_by_id(db, user_id)
    if update_data.full_name is not None:
        user.full_name = update_data.full_name
    if update_data.password is not None:
        user.hashed_password = get_password_hash(update_data.password)
    db.commit()
    db.refresh(user)
    return user

def deactivate_user(db: Session, user_id: int) -> None:
    """
    Désactive un utilisateur (soft delete).
    """
    user = get_user_by_id(db, user_id)
    user.is_active = False
    db.commit()

def reactivate_user(db: Session, user_id: int) -> User:
    """
    Réactive un utilisateur désactivé.
    """
    user = get_user_by_id(db, user_id)
    user.is_active = True
    db.commit()
    db.refresh(user)
    return user
