# app/schemas/intervention.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class InterventionType(str, Enum):
    corrective = "corrective"
    preventive = "preventive"

class StatutIntervention(str, Enum):
    ouverte = "ouverte"
    affectee = "affectee"
    en_cours = "en_cours"
    en_attente = "en_attente"
    cloturee = "cloturee"
    archivee = "archivee"

class InterventionBase(BaseModel):
    titre: str
    description: Optional[str] = None
    # Mapping JSON "type" <-> Python "type_intervention"
    type_intervention: InterventionType = Field(..., alias="type")
    statut: Optional[StatutIntervention] = StatutIntervention.ouverte
    priorite: Optional[int] = None
    urgence: Optional[bool] = False
    date_limite: Optional[datetime] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        populate_by_name = True  # <- important pour une compatibilité parfaite

class InterventionCreate(InterventionBase):
    technicien_id: Optional[int] = None
    equipement_id: int

class InterventionOut(InterventionBase):
    id: int
    date_creation: datetime
    date_cloture: Optional[datetime] = None
    technicien_id: Optional[int]
    equipement_id: int
