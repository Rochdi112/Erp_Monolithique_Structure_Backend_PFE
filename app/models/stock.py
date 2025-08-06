# app/models/stock.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric, Boolean, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
import enum


class TypeMouvement(str, enum.Enum):
    """Types de mouvements de stock"""
    entree = "entree"
    sortie = "sortie"
    ajustement = "ajustement"
    retour = "retour"


class PieceDetachee(Base):
    """
    Modèle Pièce Détachée pour la gestion de l'inventaire.
    
    Représente une pièce détachée avec :
    - Informations produit (nom, référence, description)
    - Gestion du stock (actuel, minimum, maximum)
    - Prix et coûts
    - Relations avec mouvements et interventions
    """
    __tablename__ = "pieces_detachees"

    # Clé primaire
    id = Column(Integer, primary_key=True, index=True)

    # Informations produit
    nom = Column(String(255), nullable=False, index=True)
    reference = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    marque = Column(String(100), nullable=True)
    modele = Column(String(100), nullable=True)
    
    # Gestion stock
    stock_actuel = Column(Integer, default=0, nullable=False)
    stock_minimum = Column(Integer, default=0, nullable=False)
    stock_maximum = Column(Integer, nullable=True)
    
    # Prix et coûts
    prix_unitaire = Column(Numeric(10, 2), nullable=True)
    cout_achat = Column(Numeric(10, 2), nullable=True)
    devise = Column(String(3), default="EUR")
    
    # Fournisseur
    fournisseur = Column(String(255), nullable=True)
    reference_fournisseur = Column(String(100), nullable=True)
    
    # Localisation
    emplacement = Column(String(100), nullable=True)
    rangee = Column(String(50), nullable=True)
    etagere = Column(String(50), nullable=True)
    
    # Statut et métadonnées
    is_active = Column(Boolean, default=True, nullable=False)
    date_creation = Column(DateTime, default=datetime.utcnow, nullable=False)
    date_modification = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    derniere_entree = Column(DateTime, nullable=True)
    derniere_sortie = Column(DateTime, nullable=True)

    # Relations ORM
    mouvements = relationship(
        "MouvementStock", 
        back_populates="piece_detachee", 
        cascade="all, delete-orphan",
        order_by="MouvementStock.date_mouvement.desc()"
    )
    interventions_pieces = relationship(
        "InterventionPiece", 
        back_populates="piece_detachee", 
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<PieceDetachee(id={self.id}, ref='{self.reference}', stock={self.stock_actuel})>"

    @property
    def est_en_rupture(self):
        """Vérifie si la pièce est en rupture de stock"""
        return self.stock_actuel <= 0

    @property
    def est_stock_bas(self):
        """Vérifie si le stock est en dessous du minimum"""
        return self.stock_actuel <= self.stock_minimum

    @property
    def valeur_stock(self):
        """Calcule la valeur totale du stock"""
        if self.prix_unitaire:
            return float(self.prix_unitaire) * self.stock_actuel
        return 0.0

    @property
    def pourcentage_stock(self):
        """Calcule le pourcentage de stock par rapport au maximum"""
        if self.stock_maximum and self.stock_maximum > 0:
            return (self.stock_actuel / self.stock_maximum) * 100
        return 0.0

    def peut_prelever(self, quantite: int) -> bool:
        """Vérifie si on peut prélever une quantité donnée"""
        return self.stock_actuel >= quantite

    def to_dict(self):
        """Sérialisation en dictionnaire"""
        return {
            "id": self.id,
            "nom": self.nom,
            "reference": self.reference,
            "stock_actuel": self.stock_actuel,
            "stock_minimum": self.stock_minimum,
            "prix_unitaire": float(self.prix_unitaire) if self.prix_unitaire else None,
            "est_en_rupture": self.est_en_rupture,
            "est_stock_bas": self.est_stock_bas,
            "valeur_stock": self.valeur_stock
        }


class MouvementStock(Base):
    """
    Modèle Mouvement de Stock pour tracer les entrées/sorties.
    
    Enregistre tous les mouvements de stock avec :
    - Type de mouvement (entrée, sortie, ajustement)
    - Quantité et stock avant/après
    - Motif et intervention liée si applicable
    - Traçabilité complète
    """
    __tablename__ = "mouvements_stock"

    # Clé primaire
    id = Column(Integer, primary_key=True, index=True)

    # Type et quantité
    type_mouvement = Column(Enum(TypeMouvement), nullable=False, index=True)
    quantite = Column(Integer, nullable=False)
    
    # Stock avant/après pour traçabilité
    stock_avant = Column(Integer, nullable=False)
    stock_apres = Column(Integer, nullable=False)
    
    # Motif et commentaires
    motif = Column(String(255), nullable=True)
    commentaire = Column(Text, nullable=True)
    
    # Dates
    date_mouvement = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relations
    piece_detachee_id = Column(Integer, ForeignKey("pieces_detachees.id", ondelete="CASCADE"), nullable=False)
    intervention_id = Column(Integer, ForeignKey("interventions.id", ondelete="SET NULL"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Relations ORM
    piece_detachee = relationship("PieceDetachee", back_populates="mouvements")
    intervention = relationship("Intervention", back_populates="mouvements_stock")
    user = relationship("User", back_populates="mouvements_stock")

    def __repr__(self):
        return f"<MouvementStock(id={self.id}, type='{self.type_mouvement}', qty={self.quantite})>"

    def to_dict(self):
        """Sérialisation en dictionnaire"""
        return {
            "id": self.id,
            "type_mouvement": self.type_mouvement,
            "quantite": self.quantite,
            "stock_avant": self.stock_avant,
            "stock_apres": self.stock_apres,
            "motif": self.motif,
            "date_mouvement": self.date_mouvement.isoformat() if self.date_mouvement else None,
            "piece_detachee_id": self.piece_detachee_id,
            "intervention_id": self.intervention_id
        }


class InterventionPiece(Base):
    """
    Table d'association entre Interventions et Pièces Détachées.
    
    Permet de tracer quelles pièces ont été utilisées dans quelles interventions
    avec les quantités consommées.
    """
    __tablename__ = "interventions_pieces"

    # Clé primaire composite
    intervention_id = Column(Integer, ForeignKey("interventions.id", ondelete="CASCADE"), primary_key=True)
    piece_detachee_id = Column(Integer, ForeignKey("pieces_detachees.id", ondelete="CASCADE"), primary_key=True)
    
    # Quantité utilisée
    quantite_utilisee = Column(Integer, nullable=False, default=1)
    
    # Métadonnées
    date_utilisation = Column(DateTime, default=datetime.utcnow, nullable=False)
    commentaire = Column(Text, nullable=True)

    # Relations ORM
    intervention = relationship("Intervention", back_populates="pieces_utilisees")
    piece_detachee = relationship("PieceDetachee", back_populates="interventions_pieces")

    def __repr__(self):
        return f"<InterventionPiece(intervention={self.intervention_id}, piece={self.piece_detachee_id}, qty={self.quantite_utilisee})>"