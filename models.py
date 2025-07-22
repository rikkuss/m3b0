from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from database import Base

class Client(Base):
    """
    Modèle SQLAlchemy représentant un client dans la base de données.
    Les colonnes sont mappées à partir du fichier CSV fourni.
    """
    __tablename__ = "clients"

    # Clé primaire auto-incrémentée
    id = Column(Integer, primary_key=True, index=True)

    # Informations personnelles
    nom = Column(String)
    prenom = Column(String)
    age = Column(Integer)
    taille = Column(Float)
    poids = Column(Float)
    sexe = Column(String(1))  # 'H' ou 'F'

    # Statut et informations complémentaires
    sport_licence = Column(Boolean)
    niveau_etude = Column(String)
    region = Column(String)
    smoker = Column(Boolean)
    nationalite_francaise = Column(Boolean)
    situation_familiale = Column(String, nullable=True)

    # Informations financières
    revenu_estime_mois = Column(Integer)
    historique_credits = Column(Float, nullable=True)
    risque_personnel = Column(Float)
    score_credit = Column(Float, nullable=True)
    loyer_mensuel = Column(Float, nullable=True)
    montant_pret = Column(Float)

    # Métadonnées du compte
    date_creation_compte = Column(Date)