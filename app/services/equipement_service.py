# app/services/equipement_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.equipement import Equipement
from app.schemas.equipement import EquipementCreate

def create_equipement(db: Session, data: EquipementCreate) -> Equipement:
    existing = db.query(Equipement).filter(Equipement.nom == data.nom).first()
    if existing:
        raise HTTPException(status_code=400, detail="Équipement déjà existant")
    equipement = Equipement(
        nom=data.nom,
        type=data.type_equipement,
        localisation=data.localisation,
        frequence_entretien=data.frequence_entretien
    )
    db.add(equipement)
    db.commit()
    db.refresh(equipement)
    return equipement

def get_equipement_by_id(db: Session, equipement_id: int) -> Equipement:
    equipement = db.query(Equipement).filter(Equipement.id == equipement_id).first()
    if not equipement:
        raise HTTPException(status_code=404, detail="Équipement introuvable")
    return equipement

def get_all_equipements(db: Session) -> list[Equipement]:
    return db.query(Equipement).all()

def delete_equipement(db: Session, equipement_id: int) -> None:
    equipement = get_equipement_by_id(db, equipement_id)
    db.delete(equipement)
    db.commit()
