from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.db.database import Base


# ---------- BASE ----------

class PlanningBase(BaseModel):
    """
    Champs communs pour un planning préventif :
    - fréquence de maintenance
    - dates prévisionnelle et dernière exécution
    """
    frequence: str  # Exemple : "mensuel", "hebdomadaire"
    prochaine_date: Optional[datetime] = None
    derniere_date: Optional[datetime] = None


# ---------- CRÉATION ----------

class PlanningCreate(PlanningBase):
    """
    Schéma utilisé lors de la création d’un planning :
    - nécessite un `equipement_id`
    """
    equipement_id: int


# ---------- RÉPONSE ----------

class PlanningOut(PlanningBase):
    """
    Schéma renvoyé par l’API pour lecture d’un planning :
    - inclut ID, équipement et date de création
    """
    id: int
    equipement_id: int
    date_creation: datetime

    class Config:
        orm_mode = True
