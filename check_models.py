#!/usr/bin/env python3
"""
Script de vérification des imports et modèles
"""
import sys
import os

# Ajouter le répertoire racine au PYTHONPATH
sys.path.insert(0, os.path.abspath('.'))

def test_imports():
    """Test l'import de tous les modèles"""
    print("=== Test des imports des modèles ===\n")
    
    models_to_test = [
        ("Base de données", "app.db.database", ["Base", "get_db"]),
        ("Configuration", "app.core.config", ["settings"]),
        ("User", "app.models.user", ["User", "UserRole"]),
        ("Client", "app.models.client", ["Client"]),
        ("Contrat", "app.models.contrat", ["Contrat", "Facture", "TypeContrat", "StatutContrat"]),
        ("Technicien", "app.models.technicien", ["Technicien", "Competence"]),
        ("Equipement", "app.models.equipement", ["Equipement"]),
        ("Intervention", "app.models.intervention", ["Intervention", "InterventionType", "StatutIntervention"]),
        ("Stock", "app.models.stock", ["PieceDetachee", "MouvementStock", "InterventionPiece"]),
        ("Planning", "app.models.planning", ["Planning"]),
        ("Document", "app.models.document", ["Document"]),
        ("Notification", "app.models.notification", ["Notification"]),
        ("Historique", "app.models.historique", ["HistoriqueIntervention"]),
        ("Tous les modèles", "app.models", [])
    ]
    
    errors = []
    
    for name, module_path, classes in models_to_test:
        try:
            print(f"Test {name}... ", end="")
            module = __import__(module_path, fromlist=classes)
            
            # Vérifier que les classes existent
            for class_name in classes:
                if not hasattr(module, class_name):
                    errors.append(f"  ❌ {module_path}.{class_name} n'existe pas")
                    print(f"\n  ❌ {class_name} manquant!")
            
            print("✅ OK")
            
        except ImportError as e:
            print(f"❌ ERREUR")
            errors.append(f"  ❌ {name}: {str(e)}")
        except Exception as e:
            print(f"❌ ERREUR")
            errors.append(f"  ❌ {name}: {type(e).__name__}: {str(e)}")
    
    print("\n=== Test de l'application principale ===")
    try:
        print("Test FastAPI app... ", end="")
        from app.main import app
        print("✅ OK")
    except Exception as e:
        print(f"❌ ERREUR")
        errors.append(f"  ❌ FastAPI: {type(e).__name__}: {str(e)}")
    
    # Résumé
    print("\n" + "="*50)
    if errors:
        print(f"❌ {len(errors)} erreur(s) trouvée(s):\n")
        for error in errors:
            print(error)
    else:
        print("✅ Tous les tests d'import ont réussi!")
    
    return len(errors) == 0

def check_database_tables():
    """Vérifie que les tables peuvent être créées"""
    print("\n\n=== Test de création des tables ===\n")
    
    try:
        from app.db.database import Base, engine
        from app.models import (
            User, Client, Contrat, Technicien, Equipement,
            Intervention, Planning, Document, Notification,
            HistoriqueIntervention, PieceDetachee, MouvementStock
        )
        
        print("Création des tables... ", end="")
        Base.metadata.create_all(bind=engine)
        print("✅ OK")
        
        # Lister les tables créées
        print("\nTables créées:")
        for table in Base.metadata.sorted_tables:
            print(f"  - {table.name}")
            
        return True
        
    except Exception as e:
        print(f"❌ ERREUR: {type(e).__name__}: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 Vérification du backend ERP MIF Maroc\n")
    
    # Test des imports
    imports_ok = test_imports()
    
    # Test de la base de données seulement si les imports sont OK
    if imports_ok:
        db_ok = check_database_tables()
        
        if db_ok:
            print("\n✅ Tous les tests ont réussi! Le backend devrait fonctionner.")
        else:
            print("\n❌ Problème avec la base de données. Vérifiez PostgreSQL.")
    else:
        print("\n❌ Corrigez d'abord les erreurs d'import.")
