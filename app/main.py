# app/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(f"🚀 {settings.PROJECT_NAME} démarré!")
    print(f"📚 Documentation disponible sur: http://localhost:8000/docs")
    try:
        yield
    finally:
        # Shutdown
        print("👋 Arrêt de l'application...")


# Création de l'application FastAPI avec gestionnaire de cycle de vie
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Backend ERP pour la gestion des interventions industrielles",
    lifespan=lifespan,
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import des routes v1
try:
    from app.api.v1 import (
        auth, users, techniciens, equipements,
        interventions, planning, notifications,
        documents, filters,
    )
    
    # Inclusions des routeurs avec préfixe API v1
    api_prefix = settings.API_V1_STR
    
    app.include_router(auth.router, prefix=api_prefix)
    # Compat tests: expose auth also at root (no /api/v1) for /auth/token calls
    app.include_router(auth.router)
    app.include_router(users.router, prefix=api_prefix)
    app.include_router(techniciens.router, prefix=api_prefix)
    # Compat tests: expose some routers also at root (tests call /users and /techniciens)
    app.include_router(users.router)
    app.include_router(techniciens.router)
    app.include_router(equipements.router, prefix=api_prefix)
    app.include_router(interventions.router, prefix=api_prefix)
    app.include_router(planning.router, prefix=api_prefix)
    app.include_router(notifications.router, prefix=api_prefix)
    app.include_router(documents.router, prefix=api_prefix)
    app.include_router(filters.router, prefix=api_prefix)
    
except ImportError as e:
    print(f"Erreur lors de l'import des routes: {e}")
    print("Certaines routes peuvent ne pas être disponibles.")

# Route de base pour vérifier que l'API fonctionne
@app.get("/")
def read_root():
    return {
        "message": "Bienvenue sur l'API ERP MIF Maroc",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Route de santé
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ERP Backend API"
    }

 # Les événements startup/shutdown sont maintenant gérés par lifespan ci-dessus
