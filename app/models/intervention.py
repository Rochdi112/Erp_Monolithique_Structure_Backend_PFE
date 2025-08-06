# app/models/intervention.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
import enum


class InterventionType(str, enum.Enum):
    """Types d'intervention"""
    corrective = "corrective"
    preventive = "preventive"


class StatutIntervention(str, enum.Enum):
    """Statuts possibles d'une intervention"""
    ouverte = "ouverte"
    affectee = "affectee"
    en_cours = "en_cours"
    en_attente = "en_attente"
    cloturee = "cloturee"
    archivee = "archivee"


class Intervention(Base):
    """
    Modèle Intervention - Cœur métier de l'ERP.
    
    Représente une intervention de maintenance avec :
    - Informations de base (titre, description, type)
    - Cycle de vie avec statuts
    - Affectation technicien et équipement
    - Relations avec client, contrat, documents
    - Traçabilité complète et historique
    - Gestion des pièces détachées utilisées
    """
    __tablename__ = "interventions"

    # Clé primaire
    id = Column(Integer, primary_key=True, index=True)
    
    # Informations de base
    titre = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    type_intervention = Column("type", Enum(InterventionType), nullable=False, index=True)
    
    # Cycle de vie
    statut = Column(Enum(StatutIntervention), default=StatutIntervention.ouverte, nullable=False, index=True)
    priorite = Column(Integer, nullable=True)  # 1 = haute, 5 = basse
    urgence = Column(Boolean, default=False, nullable=False)
    
    # Dates importantes
    date_creation = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    date_limite = Column(DateTime, nullable=True)
    date_debut_travaux = Column(DateTime, nullable=True)
    date_cloture = Column(DateTime, nullable=True)
    
    # Durée et coûts
    duree_estimee = Column(Integer, nullable=True)  # en minutes
    duree_reelle = Column(Integer, nullable=True)   # en minutes
    cout_estime = Column(Integer, nullable=True)    # en centimes d'euro
    cout_reel = Column(Integer, nullable=True)      # en centimes d'euro
    
    # Relations obligatoires
    equipement_id = Column(Integer, ForeignKey("equipements.id", ondelete="CASCADE"), nullable=False)
    
    # Relations optionnelles
    technicien_id = Column(Integer, ForeignKey("techniciens.id", ondelete="SET NULL"), nullable=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=True)  # ✨ NOUVEAU
    contrat_id = Column(Integer, ForeignKey("contrats.id", ondelete="SET NULL"), nullable=True)  # ✨ NOUVEAU

    # 🔗 Relations ORM
    
    # Relations principales
    technicien = relationship("Technicien", back_populates="interventions", lazy="joined")
    equipement = relationship("Equipement", back_populates="interventions", lazy="joined")
    client = relationship("Client", back_populates="interventions", lazy="joined")  # ✨ NOUVEAU
    contrat = relationship("Contrat", back_populates="interventions", lazy="joined")  # ✨ NOUVEAU
    
    # Relations de traçabilité
    documents = relationship(
        "Document", 
        back_populates="intervention", 
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    historiques = relationship(
        "HistoriqueIntervention", 
        back_populates="intervention", 
        cascade="all, delete-orphan",
        order_by="HistoriqueIntervention.horodatage.desc()",
        lazy="dynamic"
    )
    
    notifications = relationship(
        "Notification", 
        back_populates="intervention", 
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    # Relations avec le stock ✨ NOUVEAU
    mouvements_stock = relationship(
        "MouvementStock", 
        back_populates="intervention", 
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    pieces_utilisees = relationship(
        "InterventionPiece", 
        back_populates="intervention", 
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    def __repr__(self):
        return f"<Intervention(id={self.id}, titre='{self.titre}', statut='{self.statut}')>"

    # Propriétés calculées
    
    @property
    def est_ouverte(self):
        """Vérifie si l'intervention est ouverte"""
        return self.statut == StatutIntervention.ouverte

    @property
    def est_en_cours(self):
        """Vérifie si l'intervention est en cours"""
        return self.statut == StatutIntervention.en_cours

    @property
    def est_terminee(self):
        """Vérifie si l'intervention est terminée"""
        return self.statut in [StatutIntervention.cloturee, StatutIntervention.archivee]

    @property
    def est_en_retard(self):
        """Vérifie si l'intervention est en retard"""
        if not self.date_limite or self.est_terminee:
            return False
        return datetime.utcnow() > self.date_limite

    @property
    def duree_reelle_calculee(self):
        """Calcule la durée réelle si dates disponibles"""
        if self.date_debut_travaux and self.date_cloture:
            delta = self.date_cloture - self.date_debut_travaux
            return int(delta.total_seconds() / 60)  # en minutes
        return self.duree_reelle

    @property
    def temps_ecoule(self):
        """Calcule le temps écoulé depuis la création"""
        if self.est_terminee and self.date_cloture:
            return self.date_cloture - self.date_creation
        return datetime.utcnow() - self.date_creation

    @property
    def niveau_priorite_label(self):
        """Retourne le label de priorité"""
        if not self.priorite:
            return "Non définie"
        labels = {1: "Très haute", 2: "Haute", 3: "Normale", 4: "Basse", 5: "Très basse"}
        return labels.get(self.priorite, "Inconnue")

    @property
    def cout_total_pieces(self):
        """Calcule le coût total des pièces utilisées"""
        total = 0
        for intervention_piece in self.pieces_utilisees:
            if intervention_piece.piece_detachee.prix_unitaire:
                total += float(intervention_piece.piece_detachee.prix_unitaire) * intervention_piece.quantite_utilisee
        return total

    @property
    def nb_documents(self):
        """Retourne le nombre de documents attachés"""
        return self.documents.count()

    @property
    def nb_pieces_utilisees(self):
        """Retourne le nombre de types de pièces différentes utilisées"""
        return self.pieces_utilisees.count()

    @property
    def derniere_modification(self):
        """Retourne la date de dernière modification (dernier historique)"""
        dernier_historique = self.historiques.first()
        return dernier_historique.horodatage if dernier_historique else self.date_creation

    # Méthodes métier
    
    def peut_etre_modifiee(self) -> bool:
        """Vérifie si l'intervention peut encore être modifiée"""
        return self.statut not in [StatutIntervention.cloturee, StatutIntervention.archivee]

    def peut_etre_affectee(self) -> bool:
        """Vérifie si l'intervention peut être affectée à un technicien"""
        return self.statut in [StatutIntervention.ouverte, StatutIntervention.affectee]

    def peut_etre_demarree(self) -> bool:
        """Vérifie si l'intervention peut être démarrée"""
        return self.statut == StatutIntervention.affectee and self.technicien_id is not None

    def peut_etre_cloturee(self) -> bool:
        """Vérifie si l'intervention peut être clôturée"""
        return self.statut == StatutIntervention.en_cours

    def demarrer_travaux(self):
        """Démarre les travaux de l'intervention"""
        if self.peut_etre_demarree():
            self.date_debut_travaux = datetime.utcnow()
            self.statut = StatutIntervention.en_cours

    def cloturer(self, duree_reelle: int = None, cout_reel: int = None):
        """Clôture l'intervention"""
        if self.peut_etre_cloturee():
            self.date_cloture = datetime.utcnow()
            self.statut = StatutIntervention.cloturee
            
            if duree_reelle:
                self.duree_reelle = duree_reelle
            if cout_reel:
                self.cout_reel = cout_reel

    def affecter_technicien(self, technicien_id: int):
        """Affecte un technicien à l'intervention"""
        if self.peut_etre_affectee():
            self.technicien_id = technicien_id
            if self.statut == StatutIntervention.ouverte:
                self.statut = StatutIntervention.affectee

    def ajouter_piece(self, piece_detachee_id: int, quantite: int):
        """Ajoute une pièce détachée utilisée dans l'intervention"""
        from app.models.stock import InterventionPiece
        
        # Vérifier si la pièce n'est pas déjà ajoutée
        existing = self.pieces_utilisees.filter_by(piece_detachee_id=piece_detachee_id).first()
        if existing:
            existing.quantite_utilisee += quantite
        else:
            nouvelle_piece = InterventionPiece(
                intervention_id=self.id,
                piece_detachee_id=piece_detachee_id,
                quantite_utilisee=quantite
            )
            # La création du mouvement de stock sera gérée par le service

    def to_dict(self, include_relations=False):
        """
        Sérialisation en dictionnaire.
        
        Args:
            include_relations: Si True, inclut les données des relations
        """
        data = {
            "id": self.id,
            "titre": self.titre,
            "description": self.description,
            "type_intervention": self.type_intervention,
            "statut": self.statut,
            "priorite": self.priorite,
            "urgence": self.urgence,
            "date_creation": self.date_creation.isoformat() if self.date_creation else None,
            "date_limite": self.date_limite.isoformat() if self.date_limite else None,
            "date_debut_travaux": self.date_debut_travaux.isoformat() if self.date_debut_travaux else None,
            "date_cloture": self.date_cloture.isoformat() if self.date_cloture else None,
            "duree_estimee": self.duree_estimee,
            "duree_reelle": self.duree_reelle_calculee,
            "equipement_id": self.equipement_id,
            "technicien_id": self.technicien_id,
            "client_id": self.client_id,
            "contrat_id": self.contrat_id,
            "est_en_retard": self.est_en_retard,
            "niveau_priorite_label": self.niveau_priorite_label,
            "nb_documents": self.nb_documents,
            "cout_total_pieces": self.cout_total_pieces
        }
        
        if include_relations:
            data.update({
                "equipement": self.equipement.to_dict() if self.equipement else None,
                "technicien": self.technicien.to_dict() if self.technicien else None,
                "client": self.client.to_dict() if self.client else None,
                "contrat": self.contrat.to_dict() if self.contrat else None
            })
            
        return data