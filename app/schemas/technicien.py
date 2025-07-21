# app/schemas/technicien.py

from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.user import UserOut  # On suppose que UserOut existe déjà

# ---------- Schémas pour les compétences ----------

class CompetenceBase(BaseModel):
    """Champs communs pour une compétence."""
    nom: str

class CompetenceCreate(CompetenceBase):
    """Données nécessaires à la création d'une compétence."""
    pass

class CompetenceOut(CompetenceBase):
    """Schéma utilisé en sortie API (inclut l'id)."""
    id: int

    class Config:
        orm_mode = True

# ---------- Schémas pour les techniciens ----------

class TechnicienBase(BaseModel):
    """Champs communs à tous les techniciens."""
    equipe: Optional[str] = None
    disponibilite: Optional[str] = None

class TechnicienCreate(TechnicienBase):
    """Payload attendu pour créer un technicien."""
    user_id: int
    competences_ids: Optional[List[int]] = Field(default_factory=list)

class TechnicienOut(TechnicienBase):
    """Données retournées pour un technicien (lecture/detail)."""
    id: int
    user: UserOut
    competences: List[CompetenceOut] = []

    class Config:
        orm_mode = True
