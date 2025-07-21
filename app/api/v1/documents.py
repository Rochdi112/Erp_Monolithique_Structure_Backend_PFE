# app/api/v1/documents.py

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.db.database import SessionLocal
from app.models.document import Document
from app.schemas.document import DocumentOut
from app.services.document_service import create_document
from app.core.rbac import technicien_required, responsable_required, admin_required

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
    responses={404: {"description": "Document non trouvé"}}
)

# Dépendance DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/", 
    response_model=DocumentOut,
    summary="Uploader un document",
    description="Upload d’un fichier lié à une intervention (photo, rapport, preuve, etc.).",
    dependencies=[Depends(technicien_required)]
)
def upload_document(
    intervention_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return create_document(db, file, intervention_id)

@router.get(
    "/", 
    response_model=List[DocumentOut],
    summary="Lister tous les documents",
    description="Accès à la liste de tous les documents liés aux interventions (admin/responsable uniquement).",
    dependencies=[Depends(responsable_required)]
)
def list_documents(db: Session = Depends(get_db)):
    return db.query(Document).all()
