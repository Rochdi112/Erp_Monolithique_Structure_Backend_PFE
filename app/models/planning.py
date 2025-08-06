from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Planning(Base):
    """
    Planning de maintenance préventive :
    - Fréquence prévue (ex: mensuel, trimestriel)
    - Dates importantes (dernière intervention réalisée, prochaine prévue)
    - Lié à un équipement industriel
    """
    __tablename__ = "plannings"

    id = Column(Integer, primary_key=True, index=True)

    frequence = Column(String(50), nullable=False)              # ex: "mensuel", "hebdomadaire"
    prochaine_date = Column(DateTime, nullable=True)            # Prochaine intervention programmée
    derniere_date = Column(DateTime, nullable=True)             # Dernière réalisée
    date_creation = Column(DateTime, default=datetime.utcnow)   # Auto-rempli

    equipement_id = Column(Integer, ForeignKey("equipements.id", ondelete="CASCADE"), nullable=False)
    equipement = relationship("Equipement", back_populates="plannings")
