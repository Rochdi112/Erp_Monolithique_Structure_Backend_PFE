# app/core/rbac.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import settings
from sqlalchemy.orm import Session
from app.db.database import SessionLocal

# OAuth2 JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")

def decode_token(token: str) -> dict:
    """
    Décode le JWT et retourne le payload, ou lève une erreur si invalide.
    """
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token invalide ou expiré"
        )

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(lambda: SessionLocal())
):
    """
    Récupère l'utilisateur courant à partir du JWT et vérifie son existence/état en BDD.
    """
    from app.services.user_service import get_user_by_id  # Import local ici = ANTI-CERCLE
    payload = decode_token(token)
    user_id = payload.get("user_id")
    role = payload.get("role")
    if not user_id or not role:
        raise HTTPException(status_code=403, detail="Informations utilisateur manquantes dans le token")
    user = get_user_by_id(db, user_id)
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Utilisateur désactivé")
    return user

def require_roles(*roles: str):
    """
    Fabrique une dépendance FastAPI pour n'autoriser que certains rôles.
    """
    def role_checker(current_user=Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Accès réservé aux rôles : {roles}"
            )
        return current_user
    return role_checker

# Prêts à l'emploi pour tes routes
admin_required = require_roles("admin")
responsable_required = require_roles("responsable")
technicien_required = require_roles("technicien")
client_required = require_roles("client")
auth_required = require_roles("admin", "responsable", "technicien", "client")
