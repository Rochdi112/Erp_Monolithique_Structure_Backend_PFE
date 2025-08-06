# app/models/contrat.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric, Boolean, Text, Date, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, date
from app.db.database import Base
import enum


class TypeContrat(str, enum.Enum):
    """Types de contrats de maintenance"""
    maintenance_preventive = "maintenance_preventive"
    maintenance_corrective = "maintenance_corrective"
    maintenance_complete = "maintenance_complete"
    support_technique = "support_technique"
    contrat_cadre = "contrat_cadre"


class StatutContrat(str, enum.Enum):
    """Statuts d'un contrat"""
    brouillon = "brouillon"
    en_cours = "en_cours"
    expire = "expire"
    resilie = "resilie"
    suspendu = "suspendu"


class Contrat(Base):
    """
    Modèle Contrat de Maintenance.
    
    Représente un contrat entre l'entreprise et un client avec :
    - Informations contractuelles (numéro, dates, type)
    - Conditions financières (tarifs, facturation)
    - Équipements couverts
    - SLA (Service Level Agreement)
    - Relations avec interventions
    """
    __tablename__ = "contrats"

    # Clé primaire
    id = Column(Integer, primary_key=True, index=True)

    # Informations contractuelles
    numero_contrat = Column(String(50), nullable=False, unique=True, index=True)
    nom_contrat = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    type_contrat = Column(Enum(TypeContrat), nullable=False, index=True)
    statut = Column(Enum(StatutContrat), default=StatutContrat.brouillon, nullable=False, index=True)
    
    # Dates
    date_signature = Column(Date, nullable=True)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=False)
    date_renouvellement = Column(Date, nullable=True)
    
    # Conditions financières
    montant_annuel = Column(Numeric(12, 2), nullable=True)
    montant_mensuel = Column(Numeric(10, 2), nullable=True)
    devise = Column(String(3), default="EUR")
    mode_facturation = Column(String(50), default="mensuel")  # mensuel, trimestriel, annuel
    
    # SLA (Service Level Agreement)
    temps_reponse_urgence = Column(Integer, nullable=True)  # en heures
    temps_reponse_normal = Column(Integer, nullable=True)   # en heures
    taux_disponibilite = Column(Numeric(5, 2), nullable=True)  # pourcentage
    penalites_retard = Column(Numeric(10, 2), nullable=True)
    
    # Limites et conditions
    nb_interventions_incluses = Column(Integer, nullable=True)
    nb_interventions_utilisees = Column(Integer, default=0)
    heures_maintenance_incluses = Column(Integer, nullable=True)  # en heures
    heures_maintenance_utilisees = Column(Integer, default=0)
    
    # Équipements couverts (JSON ou relation séparée)
    equipements_couverts = Column(Text, nullable=True)  # JSON list d'IDs ou descriptions
    
    # Contacts
    contact_client = Column(String(255), nullable=True)
    contact_responsable = Column(String(255), nullable=True)
    
    # Métadonnées
    is_active = Column(Boolean, default=True, nullable=False)
    date_creation = Column(DateTime, default=datetime.utcnow, nullable=False)
    date_modification = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Clé étrangère vers Client
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)

    # Relations ORM
    client = relationship("Client", back_populates="contrats", lazy="joined")
    interventions = relationship(
        "Intervention", 
        back_populates="contrat", 
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    factures = relationship(
        "Facture", 
        back_populates="contrat", 
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    def __repr__(self):
        return f"<Contrat(id={self.id}, numero='{self.numero_contrat}', client='{self.client_id}')>"

    @property
    def est_actif(self):
        """Vérifie si le contrat est actuellement actif"""
        today = date.today()
        return (
            self.statut == StatutContrat.en_cours and
            self.date_debut <= today <= self.date_fin
        )

    @property
    def est_expire(self):
        """Vérifie si le contrat est expiré"""
        return date.today() > self.date_fin

    @property
    def jours_restants(self):
        """Calcule le nombre de jours restants du contrat"""
        if self.est_expire:
            return 0
        return (self.date_fin - date.today()).days

    @property
    def pourcentage_interventions_utilisees(self):
        """Calcule le pourcentage d'interventions utilisées"""
        if self.nb_interventions_incluses and self.nb_interventions_incluses > 0:
            return (self.nb_interventions_utilisees / self.nb_interventions_incluses) * 100
        return 0.0

    @property
    def pourcentage_heures_utilisees(self):
        """Calcule le pourcentage d'heures de maintenance utilisées"""
        if self.heures_maintenance_incluses and self.heures_maintenance_incluses > 0:
            return (self.heures_maintenance_utilisees / self.heures_maintenance_incluses) * 100
        return 0.0

    @property
    def interventions_restantes(self):
        """Calcule le nombre d'interventions restantes"""
        if self.nb_interventions_incluses:
            return max(0, self.nb_interventions_incluses - self.nb_interventions_utilisees)
        return None

    @property
    def heures_restantes(self):
        """Calcule le nombre d'heures de maintenance restantes"""
        if self.heures_maintenance_incluses:
            return max(0, self.heures_maintenance_incluses - self.heures_maintenance_utilisees)
        return None

    def peut_faire_intervention(self) -> bool:
        """Vérifie si une intervention peut être faite sous ce contrat"""
        if not self.est_actif:
            return False
        
        # Vérifier les limites d'interventions
        if self.nb_interventions_incluses and self.nb_interventions_utilisees >= self.nb_interventions_incluses:
            return False
            
        return True

    def consommer_intervention(self, heures_travaillees: int = 0):
        """Consomme une intervention du contrat"""
        if self.nb_interventions_incluses:
            self.nb_interventions_utilisees += 1
            
        if self.heures_maintenance_incluses and heures_travaillees > 0:
            self.heures_maintenance_utilisees += heures_travaillees

    def to_dict(self):
        """Sérialisation en dictionnaire"""
        return {
            "id": self.id,
            "numero_contrat": self.numero_contrat,
            "nom_contrat": self.nom_contrat,
            "type_contrat": self.type_contrat,
            "statut": self.statut,
            "date_debut": self.date_debut.isoformat() if self.date_debut else None,
            "date_fin": self.date_fin.isoformat() if self.date_fin else None,
            "montant_annuel": float(self.montant_annuel) if self.montant_annuel else None,
            "client_id": self.client_id,
            "est_actif": self.est_actif,
            "jours_restants": self.jours_restants,
            "interventions_restantes": self.interventions_restantes,
            "heures_restantes": self.heures_restantes
        }


class Facture(Base):
    """
    Modèle Facture liée à un contrat.
    
    Représente une facture émise dans le cadre d'un contrat de maintenance.
    """
    __tablename__ = "factures"

    # Clé primaire
    id = Column(Integer, primary_key=True, index=True)

    # Informations facture
    numero_facture = Column(String(50), nullable=False, unique=True, index=True)
    date_emission = Column(Date, nullable=False)
    date_echeance = Column(Date, nullable=False)
    
    # Montants
    montant_ht = Column(Numeric(10, 2), nullable=False)
    taux_tva = Column(Numeric(5, 2), default=20.0)
    montant_ttc = Column(Numeric(10, 2), nullable=False)
    
    # Statut
    statut_paiement = Column(String(20), default="en_attente")  # en_attente, payee, en_retard
    date_paiement = Column(Date, nullable=True)
    
    # Description
    description = Column(Text, nullable=True)
    periode_debut = Column(Date, nullable=True)
    periode_fin = Column(Date, nullable=True)
    
    # Métadonnées
    date_creation = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relations
    contrat_id = Column(Integer, ForeignKey("contrats.id", ondelete="CASCADE"), nullable=False)
    contrat = relationship("Contrat", back_populates="factures")

    def __repr__(self):
        return f"<Facture(id={self.id}, numero='{self.numero_facture}', montant={self.montant_ttc})>"

    @property
    def est_en_retard(self):
        """Vérifie si la facture est en retard de paiement"""
        return (
            self.statut_paiement != "payee" and 
            date.today() > self.date_echeance
        )

    @property
    def jours_retard(self):
        """Calcule le nombre de jours de retard"""
        if self.est_en_retard:
            return (date.today() - self.date_echeance).days
        return 0

    def to_dict(self):
        """Sérialisation en dictionnaire"""
        return {
            "id": self.id,
            "numero_facture": self.numero_facture,
            "date_emission": self.date_emission.isoformat() if self.date_emission else None,
            "date_echeance": self.date_echeance.isoformat() if self.date_echeance else None,
            "montant_ttc": float(self.montant_ttc),
            "statut_paiement": self.statut_paiement,
            "contrat_id": self.contrat_id,
            "est_en_retard": self.est_en_retard,
            "jours_retard": self.jours_retard
        }