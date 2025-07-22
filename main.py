import sys
from fastapi import FastAPI, Depends, Path, Request
from sqlalchemy.orm import Session
from typing import List, Any
from loguru import logger

import crud
import models
import schema
from database import engine, get_db

# --- Configuration de Loguru ---
# Supprime le handler par défaut pour éviter les doublons
logger.remove()
# Ajoute un handler pour la sortie console avec un format personnalisé
logger.add(sys.stderr, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
# Ajoute un handler pour écrire les logs dans un fichier, avec rotation et compression
logger.add("logs/file_{time}.log", rotation="5 MB", compression="zip", enqueue=True, serialize=False)

# Crée les tables dans la base de données si elles n'existent pas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Generic CRUD API with Logging",
    description="Une API pour effectuer des opérations CRUD sur n'importe quelle table, avec des logs via Loguru.",
    version="1.1.0",
)

# --- Middleware pour logger chaque requête ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware pour logger chaque requête HTTP reçue par l'API.
    """
    logger.info(f"Requête entrante: {request.method} {request.url.path} from {request.client.host}")
    response = await call_next(request)
    logger.info(f"Réponse: {response.status_code}")
    return response


# --- Routes de l'API avec logging ---

@app.post("/{table_name}/", response_model=schema.Client, status_code=201, summary="Créer un enregistrement")
def create_new_item(
        table_name: str,
        request: schema.GenericRequest,
        db: Session = Depends(get_db)
):
    """Crée un nouvel enregistrement dans la table spécifiée."""
    logger.info(f"Tentative de création d'un enregistrement dans la table '{table_name}'")
    return crud.create_item(db=db, tablename=table_name, data=request.data)

@app.get("/{table_name}/", response_model=List[schema.Client], summary="Lire plusieurs enregistrements")
def read_all_items(
        table_name: str,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    """Lit une liste d'enregistrements depuis la table spécifiée avec pagination."""
    logger.info(f"Lecture de la liste des enregistrements de la table '{table_name}' (skip={skip}, limit={limit})")
    return crud.get_items(db=db, tablename=table_name, skip=skip, limit=limit)

@app.get("/{table_name}/{item_id}", response_model=schema.Client, summary="Lire un enregistrement par ID")
def read_single_item(
        table_name: str,
        item_id: int,
        db: Session = Depends(get_db)
):
    """Lit un seul enregistrement par son ID dans la table spécifiée."""
    logger.info(f"Lecture de l'enregistrement ID {item_id} de la table '{table_name}'")
    return crud.get_item(db=db, tablename=table_name, item_id=item_id)

@app.put("/{table_name}/{item_id}", response_model=schema.Client, summary="Mettre à jour un enregistrement")
def update_existing_item(
        table_name: str,
        item_id: int,
        request: schema.GenericRequest,
        db: Session = Depends(get_db)
):
    """Met à jour un enregistrement existant par son ID."""
    logger.info(f"Tentative de mise à jour de l'enregistrement ID {item_id} dans la table '{table_name}'")
    return crud.update_item(db=db, tablename=table_name, item_id=item_id, data=request.data)

@app.delete("/{table_name}/{item_id}", summary="Supprimer un enregistrement")
def delete_existing_item(
        table_name: str,
        item_id: int,
        db: Session = Depends(get_db)
):
    """Supprime un enregistrement par son ID."""
    logger.info(f"Tentative de suppression de l'enregistrement ID {item_id} de la table '{table_name}'")
    return crud.delete_item(db=db, tablename=table_name, item_id=item_id)