# app/models/technicien.py

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.database import Base

# Table d'association many-to-many entre Technicien et Compétence
technicien_competence = Table(
    "technicien_competence",
    Base.metadata,
    Column("technicien_id", Integer, ForeignKey("techniciens.id", ondelete="CASCADE")),
    Column("competence_id", Integer, ForeignKey("competences.id", ondelete="CASCADE")),
)

class Competence(Base):
    __tablename__ = "competences"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False, unique=True)

    # relation vers les techniciens ayant cette compétence
    techniciens = relationship(
        "Technicien",
        secondary=technicien_competence,
        back_populates="competences",
        lazy="joined"
    )

class Technicien(Base):
    __tablename__ = "techniciens"

    id = Column(Integer, primary_key=True, index=True)
    equipe = Column(String, nullable=True)
    disponibilite = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="technicien", lazy="joined")

    competences = relationship(
        "Competence",
        secondary=technicien_competence,
        back_populates="techniciens",
        lazy="joined"
    )
    interventions = relationship("Intervention", back_populates="technicien")

