from datetime import date

from pydantic import BaseModel
from typing import Dict, Any, Optional, List

from enumClasses import SexeEnum, SituationFamilialeEnum


class GenericRequest(BaseModel):
    data: Dict[str, Any]

class ClientMeta(BaseModel):
    age: int
    taille: float
    poids: float
    sexe: SexeEnum
    sport_licence: bool
    niveau_etude: str
    region: str
    smoker: bool
    nationalite_francaise: bool
    situation_familiale: Optional[SituationFamilialeEnum] = None

    class Config:
        from_attributes = True


class ClientSituation(BaseModel):
    revenu_estime_mois: int
    historique_credits: Optional[float] = None
    risque_personnel: float
    score_credit: Optional[float] = None
    loyer_mensuel: Optional[float] = None

    class Config:
        from_attributes = True

class Contrat(BaseModel):
    montant_pret: float

    class Config:
        from_attributes = True

class Client(BaseModel):
    nom: str
    prenom: str
    date_creation_compte: date
    client_meta: ClientMeta
    client_situation: ClientSituation
    contrats: List[Contrat]

    class Config:
        from_attributes = True


class ClientMetaRead(ClientMeta):
    id: int

class ClientSituationRead(ClientSituation):
    id: int

class ContratRead(Contrat):
    id: int

class ClientRead(Client):
    id: int
    client_meta: Optional[ClientMetaRead]
    client_situation: Optional[ClientSituationRead]
    contrats: List[ContratRead]