from fastapi import APIRouter
from .auth import router as auth_router
...
from .users import router as users_router
from .techniciens import router as techniciens_router
from .equipements import router as equipements_router
from .interventions import router as interventions_router
from .planning import router as planning_router
from .notifications import router as notifications_router
from .documents import router as documents_router
from .filters import router as filters_router
from app.api.v1 import (
    auth,
    users,
    techniciens,
    equipements,
    interventions,
    planning,
    notifications,
    documents,
    filters
)

api_v1_router = APIRouter()
api_v1_router.include_router(auth.router)
api_v1_router.include_router(users.router)
api_v1_router.include_router(techniciens.router)
api_v1_router.include_router(equipements.router)
api_v1_router.include_router(interventions.router)
api_v1_router.include_router(planning.router)
api_v1_router.include_router(notifications.router)
api_v1_router.include_router(documents.router)
api_v1_router.include_router(filters.router)
