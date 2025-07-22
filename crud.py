from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import HTTPException
from loguru import logger
import models


def get_model_by_tablename(tablename: str):
    """Retourne la classe du modèle SQLAlchemy basée sur le nom de la table."""
    logger.debug(f"Recherche du modèle pour la table: {tablename}")
    for mapper in models.Base.registry.mappers:
        if mapper.class_.__tablename__ == tablename:
            logger.debug(f"Modèle '{mapper.class_.__name__}' trouvé pour la table '{tablename}'")
            return mapper.class_
    logger.error(f"Aucun modèle trouvé pour la table '{tablename}'")
    raise HTTPException(status_code=404, detail=f"Table '{tablename}' not found.")

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

def create_item(db: Session, tablename: str, data: dict):
    """Crée un enregistrement dans une table donnée."""
    model = get_model_by_tablename(tablename)

    # Prétraitement des données si la table est 'clients'
    if tablename == 'clients':
        data = _preprocess_data_for_client(data)

    try:
        db_item = model(**data)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        logger.success(f"Enregistrement créé avec succès dans '{tablename}' avec l'ID {db_item.id}")
        return db_item
    except Exception as e:
        logger.error(f"Erreur lors de la création dans '{tablename}': {e}")
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating item: {e}")


def get_item(db: Session, tablename: str, item_id: int):
    """Récupère un enregistrement par son ID."""
    model = get_model_by_tablename(tablename)
    item = db.query(model).filter(model.id == item_id).first()
    if item is None:
        logger.warning(f"Enregistrement ID {item_id} non trouvé dans la table '{tablename}'")
        raise HTTPException(status_code=404, detail="Item not found")
    logger.info(f"Enregistrement ID {item_id} trouvé dans la table '{tablename}'")
    return item

def get_items(db: Session, tablename: str, skip: int = 0, limit: int = 100):
    """Récupère une liste d'enregistrements."""
    model = get_model_by_tablename(tablename)
    items = db.query(model).offset(skip).limit(limit).all()
    logger.info(f"{len(items)} enregistrements récupérés de la table '{tablename}'")
    return items

def update_item(db: Session, tablename: str, item_id: int, data: dict):
    """Met à jour un enregistrement."""
    model = get_model_by_tablename(tablename)
    db_item = get_item(db, tablename, item_id) # Utilise la fonction get_item pour la vérification et le log

    # Prétraitement des données si la table est 'clients'
    if tablename == 'clients':
        data = _preprocess_data_for_client(data)

    try:
        for key, value in data.items():
            setattr(db_item, key, value)

        db.commit()
        db.refresh(db_item)
        logger.success(f"Enregistrement ID {item_id} mis à jour avec succès dans '{tablename}'")
        return db_item
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour de l'ID {item_id} dans '{tablename}': {e}")
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating item: {e}")

def delete_item(db: Session, tablename: str, item_id: int):
    """Supprime un enregistrement."""
    model = get_model_by_tablename(tablename)
    db_item = get_item(db, tablename, item_id) # Utilise la fonction get_item pour la vérification et le log

    try:
        db.delete(db_item)
        db.commit()
        logger.success(f"Enregistrement ID {item_id} supprimé avec succès de la table '{tablename}'")
        return {"detail": "Item deleted successfully"}
    except Exception as e:
        logger.error(f"Erreur lors de la suppression de l'ID {item_id} dans '{tablename}': {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting item: {e}")