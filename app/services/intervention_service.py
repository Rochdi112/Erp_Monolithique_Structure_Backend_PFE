from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app.models.intervention import Intervention, StatutIntervention
from app.models.historique import HistoriqueIntervention
from app.models.technicien import Technicien
from app.models.equipement import Equipement
from app.models.user import User
from app.schemas.intervention import InterventionCreate

def create_intervention(db: Session, data: InterventionCreate, user_id: int) -> Intervention:
    # Vérification technicien si renseigné
    if data.technicien_id:
        if not db.query(Technicien).filter(Technicien.id == data.technicien_id).first():
            raise HTTPException(status_code=404, detail="Technicien assigné introuvable")
    equipement = db.query(Equipement).filter(Equipement.id == data.equipement_id).first()
    if not equipement:
        raise HTTPException(status_code=404, detail="Équipement cible introuvable")
    intervention = Intervention(
        titre=data.titre,
        description=data.description,
        type_intervention=data.type_intervention,
        statut=data.statut,
        priorite=data.priorite,
        urgence=data.urgence,
        date_limite=data.date_limite,
        technicien_id=data.technicien_id,
        equipement_id=data.equipement_id,
        date_creation=datetime.utcnow()
    )
    db.add(intervention)
    db.commit()
    db.refresh(intervention)
    # 👇 Historise avec l'utilisateur qui crée (user_id courant, pas technicien_id)
    add_historique(
        db,
        intervention_id=intervention.id,
        user_id=user_id,
        statut=data.statut,
        remarque="Création de l’intervention"
    )
    return intervention

def get_intervention_by_id(db: Session, intervention_id: int) -> Intervention:
    intervention = db.query(Intervention).filter(Intervention.id == intervention_id).first()
    if not intervention:
        raise HTTPException(status_code=404, detail="Intervention introuvable")
    return intervention

def get_all_interventions(db: Session) -> list[Intervention]:
    return db.query(Intervention).all()

def update_statut_intervention(
    db: Session,
    intervention_id: int,
    new_statut: StatutIntervention,
    user_id: int,
    remarque: str = ""
) -> Intervention:
    intervention = get_intervention_by_id(db, intervention_id)
    if intervention.statut == StatutIntervention.cloturee:
        raise HTTPException(status_code=400, detail="Intervention déjà clôturée")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    intervention.statut = new_statut
    if new_statut == StatutIntervention.cloturee:
        intervention.date_cloture = datetime.utcnow()
    db.commit()
    add_historique(db, intervention_id, user_id, new_statut, remarque)
    return intervention

def add_historique(
    db: Session,
    intervention_id: int,
    user_id: int,  # Doit être obligatoire/NOT NULL
    statut: StatutIntervention,
    remarque: str
):
    historique = HistoriqueIntervention(
        statut=statut,
        remarque=remarque,
        horodatage=datetime.utcnow(),
        user_id=user_id,
        intervention_id=intervention_id
    )
    db.add(historique)
    db.commit()
