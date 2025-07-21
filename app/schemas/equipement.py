# app/schemas/equipement.py

from pydantic import BaseModel, Field
from typing import Optional

class EquipementBase(BaseModel):
    nom: str
    type_equipement: str = Field(..., alias="type")
    localisation: str
    frequence_entretien: Optional[str] = None

class EquipementCreate(EquipementBase):
    pass

class EquipementOut(EquipementBase):
    id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
