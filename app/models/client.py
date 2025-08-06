# app/models/client.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Client(Base):
    """
    Modèle Client pour la gestion des entreprises clientes.
    
    Représente une entreprise cliente avec :
    - Informations de contact et entreprise
    - Lien vers un utilisateur avec rôle 'client'
    - Relations avec interventions et contrats
    - Métadonnées de création et mise à jour
    """
    __tablename__ = "clients"

    # Clé primaire
    id = Column(Integer, primary_key=True, index=True)

    # Informations entreprise
    nom_entreprise = Column(String(255), nullable=False, index=True)
    secteur_activite = Column(String(100), nullable=True)
    numero_siret = Column(String(14), nullable=True, unique=True)
    
    # Contact principal
    contact_principal = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    telephone = Column(String(20), nullable=True)
    telephone_mobile = Column(String(20), nullable=True)
    
    # Adresse complète
    adresse = Column(Text, nullable=True)
    code_postal = Column(String(10), nullable=True)
    ville = Column(String(100), nullable=True)
    pays = Column(String(100), default="France")
    
    # Statut et métadonnées
    is_active = Column(Boolean, default=True, nullable=False)
    date_creation = Column(DateTime, default=datetime.utcnow, nullable=False)
    date_modification = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Clé étrangère vers User (obligatoire)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)

    # Relations ORM
    user = relationship("User", back_populates="client", lazy="joined")
    interventions = relationship(
        "Intervention", 
        back_populates="client", 
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    contrats = relationship(
        "Contrat", 
        back_populates="client", 
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    def __repr__(self):
        return f"<Client(id={self.id}, entreprise='{self.nom_entreprise}')>"

    @property
    def nb_interventions_total(self):
        """Retourne le nombre total d'interventions pour ce client"""
        return self.interventions.count()

    @property
    def interventions_ouvertes(self):
        """Retourne les interventions ouvertes pour ce client"""
        from app.models.intervention import StatutIntervention
        return self.interventions.filter_by(statut=StatutIntervention.ouverte)

    @property
    def derniere_intervention(self):
        """Retourne la dernière intervention créée pour ce client"""
        return self.interventions.order_by(
            self.interventions.property.mapper.class_.date_creation.desc()
        ).first()

    def to_dict(self):
        """Sérialisation simple en dictionnaire"""
        return {
            "id": self.id,
            "nom_entreprise": self.nom_entreprise,
            "secteur_activite": self.secteur_activite,
            "contact_principal": self.contact_principal,
            "email": self.email,
            "telephone": self.telephone,
            "ville": self.ville,
            "is_active": self.is_active
        }