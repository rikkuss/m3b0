from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException
from loguru import logger
from models import Client


def _preprocess_data_for_client(data: dict):
    """
    Prétraite le dictionnaire de données pour la table 'clients'.
    Convertit les types si nécessaire (ex: string -> date).
    """
    if 'date_creation_compte' in data and isinstance(data['date_creation_compte'], str):
        try:
            data['date_creation_compte'] = datetime.strptime(data['date_creation_compte'], '%Y-%m-%d').date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Format de date invalide pour date_creation_compte. Utilisez AAAA-MM-JJ.")
    return data

def create_client(db: Session, data: dict):
    """Crée un enregistrement dans une table donnée."""
    data = _preprocess_data_for_client(data)

    try:
        db_client = Client(**data)
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        logger.success(f"Enregistrement créé avec succès dans 'clients' avec l'ID {db_client.id}")
        return db_client
    except Exception as e:
        logger.error(f"Erreur lors de la création dans 'clients': {e}")
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating client: {e}")


def get_client(db: Session, client_id: int):
    """Récupère un enregistrement par son ID."""
    stmt = select(Client).where(Client.id == client_id)
    client = db.scalar(stmt)
    if client is None:
        logger.warning(f"Enregistrement ID {client_id} non trouvé dans la table 'clients'")
        raise HTTPException(status_code=404, detail="client not found")
    logger.info(f"Enregistrement ID {client_id} trouvé dans la table 'clients'")
    return client

def get_clients(db: Session, skip: int = 0, limit: int = 100):
    """Récupère une liste d'enregistrements."""
    stmt = select(Client).offset(skip).limit(limit)
    clients = db.scalars(stmt).all()
    logger.info(f"{len(clients)} enregistrements récupérés de la table 'clients'")
    return clients

def update_client(db: Session, client_id: int, data: dict):
    """Met à jour un enregistrement."""
    db_client = get_client(db, client_id) # Utilise la fonction get_client pour la vérification et le log

    data = _preprocess_data_for_client(data)

    try:
        for key, value in data.items():
            setattr(db_client, key, value)

        db.commit()
        db.refresh(db_client)
        logger.success(f"Enregistrement ID {client_id} mis à jour avec succès dans 'clients'")
        return db_client
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour de l'ID {client_id} dans 'clients': {e}")
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating client: {e}")

def delete_client(db: Session, client_id: int):
    """Supprime un enregistrement."""
    db_client = get_client(db, client_id) # Utilise la fonction get_client pour la vérification et le log

    try:
        db.delete(db_client)
        db.commit()
        logger.success(f"Enregistrement ID {client_id} supprimé avec succès de la table 'clients'")
        return {"detail": "client deleted successfully"}
    except Exception as e:
        logger.error(f"Erreur lors de la suppression de l'ID {client_id} dans 'clients': {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting client: {e}")