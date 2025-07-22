# app/models/intervention.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.database import Base
import enum

class InterventionType(str, enum.Enum):
    corrective = "corrective"
    preventive = "preventive"

class StatutIntervention(str, enum.Enum):
    ouverte = "ouverte"
    affectee = "affectee"
    en_cours = "en_cours"
    en_attente = "en_attente"
    cloturee = "cloturee"
    archivee = "archivee"

class Intervention(Base):
    __tablename__ = "interventions"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    # En base la colonne s'appelle "type", mais l'attribut Python est type_intervention
    type_intervention = Column("type", Enum(InterventionType), nullable=False)
    statut = Column(Enum(StatutIntervention), default=StatutIntervention.ouverte, nullable=False)
    priorite = Column(Integer, nullable=True)
    urgence = Column(Boolean, default=False)
    date_creation = Column(DateTime, default=datetime.utcnow)
    date_limite = Column(DateTime, nullable=True)
    date_cloture = Column(DateTime, nullable=True)
    technicien_id = Column(Integer, ForeignKey("techniciens.id", ondelete="SET NULL"), nullable=True)
    equipement_id = Column(Integer, ForeignKey("equipements.id", ondelete="CASCADE"), nullable=False)

    # Relations ORM
    technicien = relationship("Technicien", back_populates="interventions")
    equipement = relationship("Equipement", back_populates="interventions")
    documents = relationship("Document", back_populates="intervention", cascade="all, delete-orphan")
    historiques = relationship("HistoriqueIntervention", back_populates="intervention", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="intervention", cascade="all, delete-orphan")
