from pydantic import BaseModel, EmailStr
from enum import Enum
from app.db.database import Base


# ---------- ENUM ROLES ----------

class UserRole(str, Enum):
    """
    Rôles disponibles dans l’ERP :
    - admin : contrôle total
    - responsable : supervise interventions
    - technicien : effectue interventions
    - client : consultation uniquement
    """
    admin = "admin"
    responsable = "responsable"
    technicien = "technicien"
    client = "client"


# ---------- BASE UTILISATEUR ----------

class UserBase(BaseModel):
    """
    Champs partagés pour lecture / écriture utilisateurs
    """
    username: str
    full_name: str
    email: EmailStr
    role: UserRole


# ---------- CRÉATION (POST) ----------

class UserCreate(UserBase):
    """
    Payload requis pour créer un utilisateur
    """
    password: str


# ---------- RÉPONSE (GET) ----------

class UserOut(UserBase):
    """
    Schéma utilisé pour retourner un utilisateur
    """
    id: int
    is_active: bool

    class Config:
        orm_mode = True


# ---------- AUTHENTIFICATION ----------

class TokenRequest(BaseModel):
    """
    Données pour se connecter (login form)
    """
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """
    Réponse JWT renvoyée après authentification
    """
    access_token: str
    token_type: str = "bearer"
