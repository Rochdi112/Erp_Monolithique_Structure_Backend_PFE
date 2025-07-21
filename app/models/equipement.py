# app/models/equipement.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class Equipement(Base):
    """
    Représente un équipement industriel.
    """
    __tablename__ = "equipements"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False, unique=True)
    type = Column(String(255), nullable=False)
    localisation = Column(String(255), nullable=False)
    frequence_entretien = Column(String(50), nullable=True)

    # Relations (cascade pour interventions/planning)
    interventions = relationship(
        "Intervention", back_populates="equipement", cascade="all, delete-orphan"
    )
    plannings = relationship(
        "Planning", back_populates="equipement", cascade="all, delete-orphan"
    )
