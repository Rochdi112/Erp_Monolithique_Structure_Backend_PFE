# app/models/user.py

from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
import enum


class UserRole(str, enum.Enum):
    """
    Rôles disponibles dans le système ERP :
    - admin : contrôle total du système
    - responsable : supervise les interventions et équipes
    - technicien : effectue les interventions
    - client : consultation de ses interventions uniquement
    """
    admin = "admin"
    responsable = "responsable"
    technicien = "technicien"
    client = "client"


class User(Base):
    """
    Modèle Utilisateur du système ERP.
    
    Représente un utilisateur avec :
    - Informations personnelles et de connexion
    - Rôle et permissions
    - Relations avec entités métier (technicien, client)
    - Historique des actions
    - Gestion des notifications
    """
    __tablename__ = "users"

    # Clé primaire
    id = Column(Integer, primary_key=True, index=True)

    # Informations d'identification
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # Rôle et statut
    role = Column(Enum(UserRole), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # Métadonnées temporelles
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    # 🔗 Relations ORM
    
    # Relation one-to-one avec Technicien (si role = technicien)
    technicien = relationship(
        "Technicien", 
        uselist=False, 
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    # Relation one-to-one avec Client (si role = client) ✨ NOUVEAU
    client = relationship(
        "Client", 
        uselist=False, 
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    # Relations avec les actions et notifications
    notifications = relationship(
        "Notification", 
        back_populates="user", 
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    # Historique des actions sur interventions
    historiques = relationship(
        "HistoriqueIntervention", 
        back_populates="user", 
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    # Mouvements de stock effectués ✨ NOUVEAU
    mouvements_stock = relationship(
        "MouvementStock", 
        back_populates="user", 
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"

    @property
    def is_admin(self):
        """Vérifie si l'utilisateur est administrateur"""
        return self.role == UserRole.admin

    @property
    def is_responsable(self):
        """Vérifie si l'utilisateur est responsable"""
        return self.role == UserRole.responsable

    @property
    def is_technicien(self):
        """Vérifie si l'utilisateur est technicien"""
        return self.role == UserRole.technicien

    @property
    def is_client(self):
        """Vérifie si l'utilisateur est client"""
        return self.role == UserRole.client

    @property
    def can_manage_users(self):
        """Vérifie si l'utilisateur peut gérer d'autres utilisateurs"""
        return self.role in [UserRole.admin]

    @property
    def can_manage_interventions(self):
        """Vérifie si l'utilisateur peut gérer les interventions"""
        return self.role in [UserRole.admin, UserRole.responsable]

    @property
    def can_execute_interventions(self):
        """Vérifie si l'utilisateur peut exécuter des interventions"""
        return self.role in [UserRole.admin, UserRole.responsable, UserRole.technicien]

    @property
    def display_name(self):
        """Nom d'affichage préféré"""
        return self.full_name or self.username

    def update_last_login(self):
        """Met à jour la date de dernière connexion"""
        self.last_login = datetime.utcnow()

    def to_dict(self, include_sensitive=False):
        """
        Sérialisation en dictionnaire.
        
        Args:
            include_sensitive: Si True, inclut des données sensibles (pour admin)
        """
        data = {
            "id": self.id,
            "username": self.username,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None
        }
        
        if include_sensitive:
            data.update({
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                "nb_notifications": self.notifications.count(),
                "nb_historiques": self.historiques.count()
            })
            
        return data