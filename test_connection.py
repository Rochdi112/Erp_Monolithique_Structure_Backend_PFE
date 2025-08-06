import os
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine

# Charger les variables d'environnement
load_dotenv()

# Test connexion PostgreSQL directe
try:
    print("1. Test connexion PostgreSQL directe...")
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_SERVER", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        database=os.getenv("POSTGRES_DB", "erp_db"),
        user=os.getenv("POSTGRES_USER", "erp_user"),
        password=os.getenv("POSTGRES_PASSWORD", "erp_pass")
    )
    conn.close()
    print("✅ Connexion PostgreSQL réussie!")
except Exception as e:
    print(f"❌ Erreur PostgreSQL: {e}")

# Test SQLAlchemy
try:
    print("\n2. Test connexion SQLAlchemy...")
    DATABASE_URL = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@{os.getenv('POSTGRES_SERVER')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    )
    print(f"URL: {DATABASE_URL}")
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    conn.close()
    print("✅ Connexion SQLAlchemy réussie!")
except Exception as e:
    print(f"❌ Erreur SQLAlchemy: {e}")

# Test import FastAPI
try:
    print("\n3. Test import FastAPI...")
    from app.main import app
    print("✅ Import FastAPI réussi!")
except Exception as e:
    print(f"❌ Erreur import: {e}")
