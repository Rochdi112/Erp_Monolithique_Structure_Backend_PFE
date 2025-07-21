from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
from app.db.database import Base


# ---------- ENUMS ----------

class InterventionType(str, Enum):
    """Type d’intervention : corrective ou préventive"""
    corrective = "corrective"
    preventive = "preventive"


class StatutIntervention(str, Enum):
    """Statuts possibles dans le cycle de vie d’une intervention"""
    ouverte = "ouverte"
    affectee = "affectee"
    en_cours = "en_cours"
    en_attente = "en_attente"
    cloturee = "cloturee"
    archivee = "archivee"


# ---------- BASE ----------

class InterventionBase(BaseModel):
    """
    Champs de base pour une intervention :
    - Titre, description, type
    - Statut, urgence, priorité, date limite
    """
    titre: str
    description: Optional[str] = None
    type_intervention: InterventionType = Field(..., alias="type")
    statut: Optional[StatutIntervention] = StatutIntervention.ouverte
    priorite: Optional[int] = None
    urgence: Optional[bool] = False
    date_limite: Optional[datetime] = None


# ---------- CRÉATION ----------

class InterventionCreate(InterventionBase):
    """
    Données nécessaires pour créer une intervention :
    - Équipement obligatoire
    - Technicien optionnel (affectation automatique ou manuelle)
    """
    technicien_id: Optional[int] = None
    equipement_id: int


# ---------- RÉPONSE API ----------

class InterventionOut(InterventionBase):
    """
    Données retournées par l’API :
    - Informations complètes sur l’intervention
    """
    id: int
    date_creation: datetime
    date_cloture: Optional[datetime] = None
    technicien_id: Optional[int]
    equipement_id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True  # Permet d'accepter le champ "type" en sortie
