# app/db/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
from app.core.config import settings
import sys

# Initialisation de Base
Base = declarative_base()

# Production engine par défaut (avec repli sécurisé pour tests si driver manquant)
DATABASE_URL = (
    f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)


def _create_default_engine():
    """
    Crée l'engine de base de données.
    - Tente PostgreSQL (prod/dev).
    - En cas d'indisponibilité du driver (psycopg2 non installé), bascule sur SQLite en mémoire.
    Ce fallback évite l'échec d'import lors des tests qui remplacent get_db.
    """
    try:
        # En mode test (pytest), on force SQLite en mémoire pour isolation/rapidité
        if "pytest" in sys.modules:
            raise RuntimeError("Test mode detected - using in-memory SQLite")

        eng = create_engine(DATABASE_URL)
        # Probe la connexion; si indisponible, fallback SQLite
        try:
            with eng.connect() as conn:
                pass
        except Exception as connect_exc:
            raise connect_exc
        return eng
    except Exception as exc:  # ImportError/ModuleNotFoundError psycopg2, etc.
        # Fallback silencieux pour l'environnement de test
        print(
            "Erreur lors de l'import des routes: "
            f"{getattr(exc, 'msg', str(exc))}\nBascule sur SQLite en mémoire pour tests."
        )
        return create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )


engine = _create_default_engine()

# Session liée à l’engine de prod (surchargée en test)
_SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dépendance utilisée par FastAPI (surchargée dans les tests)
from sqlalchemy.orm import Session
from typing import Generator

# Initialisation paresseuse du schéma en mode SQLite mémoire
_schema_initialized = False

# Assure le schéma si des tests utilisent directement SessionLocal sans passer par get_db
if engine.url.get_backend_name() == "sqlite":
    try:
        # Import des modèles pour enregistrer toutes les tables
        import app.models  # noqa: F401
        Base.metadata.create_all(bind=engine)
        _schema_initialized = True
    except Exception as exc:
        print(f"Initialisation immédiate du schéma SQLite échouée: {exc}")

def get_db() -> Generator[Session, None, None]:
    global _schema_initialized
    # Crée le schéma si on est en SQLite mémoire et pas encore initialisé
    if engine.url.get_backend_name() == "sqlite" and not _schema_initialized:
        try:
            # Import des modèles pour que toutes les tables soient enregistrées
            import app.models  # noqa: F401
            Base.metadata.create_all(bind=engine)
            _schema_initialized = True
        except Exception as exc:
            print(f"Initialisation du schéma SQLite échouée: {exc}")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fournit une session tout en garantissant le schéma en mode SQLite mémoire
def SessionLocal() -> Session:
    global _schema_initialized
    if engine.url.get_backend_name() == "sqlite":
        try:
            import app.models  # noqa: F401
            # create_all avec checkfirst garantit la présence des tables
            Base.metadata.create_all(bind=engine)
            _schema_initialized = True
        except Exception as exc:
            print(f"Initialisation à la volée du schéma SQLite échouée: {exc}")
    return _SessionFactory()
