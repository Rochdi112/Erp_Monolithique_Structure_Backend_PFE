from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.database import Base



class Document(Base):
    """
    Représente un document lié à une intervention :
    - Peut être une photo, un rapport PDF ou tout fichier joint
    - Stocké dans le dossier /static/uploads/
    - Chaque document est obligatoirement lié à une intervention
    """
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    nom_fichier = Column(String(255), nullable=False)  # ex: rapport.pdf
    chemin = Column(String(255), nullable=False)       # chemin complet vers le fichier sur le serveur
    date_upload = Column(DateTime, default=datetime.utcnow)  # auto-rempli à l'upload

    # Clé étrangère vers une intervention
    intervention_id = Column(Integer, ForeignKey("interventions.id", ondelete="CASCADE"), nullable=False)
    intervention = relationship("Intervention", back_populates="documents")
