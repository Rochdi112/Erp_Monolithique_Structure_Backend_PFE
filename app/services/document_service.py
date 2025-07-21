# app/services/document_service.py

import os
from uuid import uuid4
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.document import Document
from app.models.intervention import Intervention

UPLOAD_DIR = "app/static/uploads"


def save_uploaded_file(file: UploadFile) -> str:
    """
    Sauvegarde physique d’un fichier uploadé dans le dossier `uploads/`.

    Returns:
        str: chemin relatif à stocker en base (ex: uploads/abcd1234.png)
    """
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    extension = os.path.splitext(file.filename)[1]
    if not extension:
        raise HTTPException(status_code=400, detail="Le fichier doit avoir une extension valide")

    unique_name = f"{uuid4().hex}{extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)

    return f"uploads/{unique_name}"


def create_document(db: Session, file: UploadFile, intervention_id: int) -> Document:
    """
    Associe un fichier uploadé à une intervention existante.

    Raises:
        HTTPException 404: si l'intervention est introuvable
    """
    intervention = db.query(Intervention).filter(Intervention.id == intervention_id).first()
    if not intervention:
        raise HTTPException(status_code=404, detail="Intervention cible introuvable")

    chemin = save_uploaded_file(file)

    document = Document(
        nom_fichier=file.filename,
        chemin=chemin,
        intervention_id=intervention_id,
        date_upload=datetime.utcnow()
    )

    db.add(document)
    db.commit()
    db.refresh(document)
    return document
