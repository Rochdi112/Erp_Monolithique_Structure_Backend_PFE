# app/services/auth_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import TokenResponse
from app.core.security import verify_password, create_access_token

def authenticate_user(db: Session, email: str, password: str) -> TokenResponse:
    """
    Authentifie un utilisateur avec son email et mot de passe.
    Retourne un Token JWT en cas de succès.

    Raises:
        HTTPException: 401 si utilisateur introuvable ou mot de passe invalide.
        HTTPException: 403 si utilisateur désactivé.
    """
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Compte désactivé"
        )

    access_token = create_access_token(
        data={"sub": user.email, "role": user.role, "user_id": user.id}
    )

    return TokenResponse(access_token=access_token)
