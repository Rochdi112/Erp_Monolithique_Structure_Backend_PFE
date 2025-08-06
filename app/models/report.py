# app/models/report.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text, JSON, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
import enum


class ReportStatus(str, enum.Enum):
    """Statuts d'un rapport"""
    pending = "pending"
    generating = "generating"
    completed = "completed"
    failed = "failed"
    expired = "expired"


class ReportType(str, enum.Enum):
    """Types de rapports"""
    interventions = "interventions"
    equipements = "equipements"
    techniciens = "techniciens"
    clients = "clients"
    dashboard = "dashboard"
    planning = "planning"
    stock = "stock"
    financial = "financial"


class ReportFormat(str, enum.Enum):
    """Formats de rapport"""
    pdf = "pdf"
    excel = "excel"
    csv = "csv"
    json = "json"


class Report(Base):
    """
    Modèle Report pour la sauvegarde et traçabilité des rapports générés.
    
    Permet de :
    - Sauvegarder les rapports générés pour consultation ultérieure
    - Tracer qui a généré quoi et quand
    - Gérer les permissions d'accès aux rapports
    - Planifier des rapports automatiques
    - Optimiser les performances en évitant la régénération
    """
    __tablename__ = "reports"

    # Clé primaire
    id = Column(Integer, primary_key=True, index=True)

    # Informations de base
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    report_type = Column(String(50), nullable=False, index=True)  # Peut être un enum ou string libre
    report_format = Column(String(10), nullable=False, index=True)
    
    # Statut et cycle de vie
    status = Column(String(20), default="pending", nullable=False, index=True)
    
    # Fichier généré
    file_path = Column(String(500), nullable=True)
    file_name = Column(String(255), nullable=True)
    file_size = Column(BigInteger, nullable=True)  # Taille en bytes
    mime_type = Column(String(100), nullable=True)
    
    # Paramètres et filtres utilisés pour la génération
    filters_json = Column(JSON, nullable=True)  # Sauvegarde des filtres appliqués
    parameters = Column(JSON, nullable=True)    # Paramètres de génération
    
    # Métadonnées temporelles
    date_creation = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    date_generation_start = Column(DateTime, nullable=True)
    date_generation_end = Column(DateTime, nullable=True)
    date_expiration = Column(DateTime, nullable=True, index=True)
    
    # Accès et sécurité
    is_public = Column(Boolean, default=False, nullable=False)
    is_downloadable = Column(Boolean, default=True, nullable=False)
    access_token = Column(String(100), nullable=True, unique=True)  # Token pour accès anonyme
    
    # Statistiques d'utilisation
    download_count = Column(Integer, default=0, nullable=False)
    last_downloaded_at = Column(DateTime, nullable=True)
    
    # Erreurs et logs
    error_message = Column(Text, nullable=True)
    generation_log = Column(Text, nullable=True)
    
    # Relations
    created_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Relations ORM
    created_by = relationship("User", backref="reports_created", lazy="joined")

    def __repr__(self):
        return f"<Report(id={self.id}, title='{self.title}', type='{self.report_type}', status='{self.status}')>"

    # Propriétés calculées
    
    @property
    def is_ready(self):
        """Vérifie si le rapport est prêt à être téléchargé"""
        return self.status == "completed" and self.file_path is not None

    @property
    def is_expired(self):
        """Vérifie si le rapport a expiré"""
        if self.date_expiration is None:
            return False
        return datetime.utcnow() > self.date_expiration

    @property
    def is_generating(self):
        """Vérifie si le rapport est en cours de génération"""
        return self.status in ["pending", "generating"]

    @property
    def generation_duration(self):
        """Calcule la durée de génération en secondes"""
        if self.date_generation_start and self.date_generation_end:
            delta = self.date_generation_end - self.date_generation_start
            return delta.total_seconds()
        return None

    @property
    def file_size_mb(self):
        """Retourne la taille du fichier en MB"""
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return 0

    @property
    def can_download(self):
        """Vérifie si le rapport peut être téléchargé"""
        return (
            self.is_ready and 
            not self.is_expired and 
            self.is_downloadable
        )

    @property
    def download_url(self):
        """Génère l'URL de téléchargement"""
        if self.can_download:
            if self.access_token:
                return f"/api/reports/{self.id}/download?token={self.access_token}"
            else:
                return f"/api/reports/{self.id}/download"
        return None

    # Méthodes métier
    
    def start_generation(self):
        """Marque le début de la génération"""
        self.status = "generating"
        self.date_generation_start = datetime.utcnow()
        self.error_message = None

    def complete_generation(self, file_path: str, file_size: int = None):
        """Marque la fin de la génération avec succès"""
        self.status = "completed"
        self.date_generation_end = datetime.utcnow()
        self.file_path = file_path
        if file_size:
            self.file_size = file_size

    def fail_generation(self, error_message: str):
        """Marque l'échec de la génération"""
        self.status = "failed"
        self.date_generation_end = datetime.utcnow()
        self.error_message = error_message

    def increment_download(self):
        """Incrémente le compteur de téléchargement"""
        self.download_count += 1
        self.last_downloaded_at = datetime.utcnow()

    def extend_expiration(self, days: int = 7):
        """Prolonge la date d'expiration"""
        from datetime import timedelta
        if self.date_expiration:
            self.date_expiration += timedelta(days=days)
        else:
            self.date_expiration = datetime.utcnow() + timedelta(days=days)

    def can_be_accessed_by_user(self, user_id: int) -> bool:
        """Vérifie si un utilisateur peut accéder au rapport"""
        # Le créateur peut toujours accéder
        if self.created_by_id == user_id:
            return True
        
        # Les rapports publics sont accessibles à tous
        if self.is_public:
            return True
        
        # TODO: Ajouter logique de permissions par rôle
        return False

    def to_dict(self, include_sensitive=False):
        """
        Sérialisation en dictionnaire.
        
        Args:
            include_sensitive: Si True, inclut les données sensibles (tokens, etc.)
        """
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "report_type": self.report_type,
            "report_format": self.report_format,
            "status": self.status,
            "file_name": self.file_name,
            "file_size": self.file_size,
            "file_size_mb": self.file_size_mb,
            "date_creation": self.date_creation.isoformat() if self.date_creation else None,
            "date_expiration": self.date_expiration.isoformat() if self.date_expiration else None,
            "is_public": self.is_public,
            "is_ready": self.is_ready,
            "is_expired": self.is_expired,
            "can_download": self.can_download,
            "download_count": self.download_count,
            "last_downloaded_at": self.last_downloaded_at.isoformat() if self.last_downloaded_at else None,
            "generation_duration": self.generation_duration,
            "created_by_id": self.created_by_id
        }
        
        if include_sensitive:
            data.update({
                "file_path": self.file_path,
                "access_token": self.access_token,
                "filters_json": self.filters_json,
                "parameters": self.parameters,
                "error_message": self.error_message,
                "download_url": self.download_url
            })
            
        return data


class ReportSchedule(Base):
    """
    Modèle ReportSchedule pour la planification automatique de rapports.
    
    Permet de :
    - Programmer des rapports récurrents (quotidiens, hebdomadaires, mensuels)
    - Envoyer automatiquement par email
    - Garder un historique des exécutions
    """
    __tablename__ = "report_schedules"

    # Clé primaire
    id = Column(Integer, primary_key=True, index=True)

    # Configuration
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Configuration du rapport à générer
    report_type = Column(String(50), nullable=False)
    report_format = Column(String(10), nullable=False)
    report_title_template = Column(String(255), nullable=True)  # Template avec variables
    
    # Planification (expression cron)
    cron_expression = Column(String(100), nullable=False)  # Ex: "0 9 * * 1" pour tous les lundis à 9h
    timezone = Column(String(50), default="UTC")
    
    # Configuration des filtres et paramètres
    default_filters = Column(JSON, nullable=True)
    default_parameters = Column(JSON, nullable=True)
    
    # Notification par email
    email_enabled = Column(Boolean, default=False)
    email_recipients = Column(JSON, nullable=True)  # Liste d'emails
    email_subject_template = Column(String(255), nullable=True)
    email_body_template = Column(Text, nullable=True)
    
    # Gestion de la rétention
    keep_reports_days = Column(Integer, default=30)  # Conserver les rapports X jours
    max_reports_to_keep = Column(Integer, default=10)  # Nombre max de rapports à conserver
    
    # Statut et métadonnées
    is_active = Column(Boolean, default=True, nullable=False)
    last_run_at = Column(DateTime, nullable=True)
    next_run_at = Column(DateTime, nullable=True, index=True)
    last_success_at = Column(DateTime, nullable=True)
    last_error_message = Column(Text, nullable=True)
    run_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    
    # Audit
    date_creation = Column(DateTime, default=datetime.utcnow, nullable=False)
    date_modification = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Relations ORM
    created_by = relationship("User", backref="report_schedules_created", lazy="joined")

    def __repr__(self):
        return f"<ReportSchedule(id={self.id}, name='{self.name}', active={self.is_active})>"

    @property
    def success_rate(self):
        """Calcule le taux de succès des exécutions"""
        if self.run_count == 0:
            return 0.0
        return (self.success_count / self.run_count) * 100

    @property
    def is_overdue(self):
        """Vérifie si une exécution est en retard"""
        if not self.next_run_at:
            return False
        return datetime.utcnow() > self.next_run_at

    def record_run_start(self):
        """Enregistre le début d'une exécution"""
        self.run_count += 1
        self.last_run_at = datetime.utcnow()

    def record_run_success(self):
        """Enregistre le succès d'une exécution"""
        self.success_count += 1
        self.last_success_at = datetime.utcnow()
        self.last_error_message = None

    def record_run_error(self, error_message: str):
        """Enregistre l'échec d'une exécution"""
        self.last_error_message = error_message

    def to_dict(self):
        """Sérialisation en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "report_type": self.report_type,
            "report_format": self.report_format,
            "cron_expression": self.cron_expression,
            "is_active": self.is_active,
            "last_run_at": self.last_run_at.isoformat() if self.last_run_at else None,
            "next_run_at": self.next_run_at.isoformat() if self.next_run_at else None,
            "success_rate": self.success_rate,
            "run_count": self.run_count,
            "email_enabled": self.email_enabled,
            "created_by_id": self.created_by_id
        }
