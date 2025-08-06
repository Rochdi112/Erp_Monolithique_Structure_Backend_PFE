#!/usr/bin/env python3
"""
Script de test direct du serveur
"""
import sys
import os

# Ajouter le répertoire racine au PYTHONPATH
sys.path.insert(0, os.path.abspath('.'))

print("🔍 Test de démarrage du serveur ERP\n")

try:
    print("1. Import de l'application FastAPI...")
    from app.main import app
    print("✅ Import réussi!")
    
    print("\n2. Routes disponibles:")
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            print(f"   {', '.join(route.methods):6} {route.path}")
    
    print("\n✅ L'application semble prête!")
    print("\nPour lancer le serveur, exécutez:")
    print("  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    
except Exception as e:
    print(f"\n❌ Erreur: {type(e).__name__}: {str(e)}")
    
    # Affichage de la trace complète pour debug
    import traceback
    print("\nTrace complète:")
    traceback.print_exc()
