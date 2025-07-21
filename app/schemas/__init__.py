# app/schemas/__init__.py

from .user import UserBase, UserCreate, UserOut, UserRole, TokenRequest, TokenResponse
from .technicien import TechnicienBase, TechnicienCreate, TechnicienOut, CompetenceBase, CompetenceCreate, CompetenceOut
from .equipement import EquipementBase, EquipementCreate, EquipementOut
from .intervention import (
    InterventionBase,
    InterventionCreate,
    InterventionOut,
    InterventionType,
    StatutIntervention
)
from .planning import PlanningBase, PlanningCreate, PlanningOut
from .document import DocumentBase, DocumentCreate, DocumentOut
from .notification import NotificationBase, NotificationCreate, NotificationOut
from .historique import HistoriqueBase, HistoriqueCreate, HistoriqueOut
