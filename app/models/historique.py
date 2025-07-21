from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.database import Base
from .intervention import StatutIntervention



class HistoriqueIntervention(Base):
    """
    Historique des statuts d'une intervention :
    - Trace tous les changements de statut
    - Enregistre l'auteur du changement et une remarque facultative
    - Utile pour audit, suivi RGPD, analyse de délais
    """
    __tablename__ = "historiques_interventions"

    id = Column(Integer, primary_key=True, index=True)

    statut = Column(Enum(StatutIntervention), nullable=False)  # Statut enregistré
    remarque = Column(String, nullable=True)                   # Remarque libre
    horodatage = Column(DateTime, default=datetime.utcnow)     # Date de changement

    # Liens vers intervention et utilisateur
    intervention_id = Column(Integer, ForeignKey("interventions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    intervention = relationship("Intervention", back_populates="historiques")
    user = relationship("User", back_populates="historiques")
