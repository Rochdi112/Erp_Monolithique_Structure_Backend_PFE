# app/main.py

from fastapi import FastAPI
from app.api.v1 import (
    auth, users, techniciens, equipements,
    interventions, planning, notifications,
    documents, filters,
)

app = FastAPI()

# Inclusions explicites des routeurs
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(techniciens.router)
app.include_router(equipements.router)
app.include_router(interventions.router)
app.include_router(planning.router)
app.include_router(notifications.router)
app.include_router(documents.router)
app.include_router(filters.router)
# Point d'entrée pour la documentation