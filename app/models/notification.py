from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.database import Base


class Notification(Base):
    """
    Notification liée à une intervention :
    - Peut être envoyée par email ou stockée comme log interne
    - Concerne un utilisateur et une intervention
    - Contient le type, le canal, le contenu, et la date d’envoi
    """
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    type_notification = Column("type", String(50), nullable=False)  # ex: "affectation", "cloture"
    canal = Column(String(50), nullable=False)                      # ex: "email", "log"
    contenu = Column(String(1000), nullable=True)                   # sujet/message
    date_envoi = Column(DateTime, default=datetime.utcnow)          # date de création/envoi

    # Foreign Keys
    intervention_id = Column(Integer, ForeignKey("interventions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # ORM relationships
    intervention = relationship("Intervention", back_populates="notifications")
    user = relationship("User", back_populates="notifications")
