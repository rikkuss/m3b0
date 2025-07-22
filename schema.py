from datetime import date

from pydantic import BaseModel
from typing import Dict, Any, Optional


class GenericRequest(BaseModel):
    data: Dict[str, Any]

# Ce schéma définit la structure JSON de sortie pour un client
class Client(BaseModel):
    id: int
    nom: str
    prenom: str
    age: int
    taille: float
    poids: float
    sexe: str
    sport_licence: bool
    niveau_etude: str
    region: str
    smoker: bool
    nationalite_francaise: bool
    situation_familiale: Optional[str] = None
    revenu_estime_mois: int
    historique_credits: Optional[float] = None
    risque_personnel: float
    score_credit: Optional[float] = None
    loyer_mensuel: Optional[float] = None
    montant_pret: float
    date_creation_compte: date

    # Cette configuration permet à Pydantic de lire les données
    # directement depuis un modèle ORM (comme votre modèle Client SQLAlchemy)
    class Config:
        from_attributes = True
