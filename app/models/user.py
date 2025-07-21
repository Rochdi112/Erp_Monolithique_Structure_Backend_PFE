from sqlalchemy import Column, Integer, String, Enum, Boolean
from sqlalchemy.orm import relationship
from ..db.database import Base
import enum


# 🎯 Rôles disponibles dans le système
class UserRole(str, enum.Enum):
    admin = "admin"
    responsable = "responsable"
    technicien = "technicien"
    client = "client"


class User(Base):
    """
    Utilisateur du système :
    - Peut avoir différents rôles (admin, technicien, client...)
    - Lié aux entités : technicien (si technicien), historiques, notifications
    - Utilisé pour l’authentification
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    role = Column(Enum(UserRole), nullable=False, index=True)
    is_active = Column(Boolean, default=True)

    # 🔗 Relations
    technicien = relationship("Technicien", uselist=False, back_populates="user")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    historiques = relationship("HistoriqueIntervention", back_populates="user", cascade="all, delete-orphan")
