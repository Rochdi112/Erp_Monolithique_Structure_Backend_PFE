from pydantic import BaseModel
from typing import Optional

class EquipementBase(BaseModel):
    nom: str
    type: str
    localisation: str
    frequence_entretien: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "validate_by_name": True
    }

class EquipementCreate(EquipementBase):
    pass

class EquipementOut(EquipementBase):
    id: int

    model_config = {
        "from_attributes": True,
        "validate_by_name": True
    }
