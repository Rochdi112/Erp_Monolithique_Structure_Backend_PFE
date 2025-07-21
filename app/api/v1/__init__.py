from fastapi import APIRouter

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
