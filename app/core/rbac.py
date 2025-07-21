# app/core/rbac.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")

def decode_token(token: str) -> dict:
    """Décode le token JWT et retourne le payload"""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token invalide ou expiré"
        )

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Récupère les infos de l'utilisateur courant depuis le token"""
    payload = decode_token(token)
    if "sub" not in payload or "role" not in payload:
        raise HTTPException(status_code=403, detail="Informations utilisateur manquantes")
    return {
        "user_id": payload.get("sub"),
        "role": payload.get("role")
    }

def require_roles(*roles: str):
    """Dépendance pour autoriser l'accès uniquement à certains rôles"""
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Accès réservé aux rôles : {roles}"
            )
        return current_user
    return role_checker

# Dépendances prêtes à l’emploi pour chaque rôle
admin_required = require_roles("admin")
responsable_required = require_roles("responsable")
technicien_required = require_roles("technicien")
client_required = require_roles("client")
