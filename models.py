from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship

from database import Base
from enumClasses import SituationFamilialeEnum, SexeEnum


class Client(Base):
    """
    Modèle SQLAlchemy représentant un client dans la base de données.
    """
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    prenom = Column(String)
    date_creation_compte = Column(Date)
    contrats = relationship("Contrat", back_populates="client", cascade="all, delete-orphan")
    client_meta = relationship("ClientMeta", back_populates="client", uselist=False, cascade="all, delete-orphan")
    client_situation = relationship("ClientSituation", back_populates="client", uselist=False, cascade="all, delete-orphan")

class ClientMeta(Base):
    __tablename__ = "clients_meta"
    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    poids = Column(Float)
    taille = Column(Float)
    sexe = Column(Enum(SexeEnum))  # 'H' ou 'F'
    sport_licence = Column(Boolean)
    niveau_etude = Column(String)
    region = Column(String)
    smoker = Column(Boolean)
    nationalite_francaise = Column(Boolean)
    situation_familiale = Column(Enum(SituationFamilialeEnum))
    client_id = Column(Integer, ForeignKey("clients.id"), unique=True)
    client = relationship("Client", back_populates="client_meta")

class ClientSituation(Base):
    __tablename__ = "clients_situation"
    id = Column(Integer, primary_key=True, index=True)
    revenu_estime_mois = Column(Integer)
    historique_credits = Column(Float, nullable=True)
    risque_personnel = Column(Float)
    score_credit = Column(Float, nullable=True)
    loyer_mensuel = Column(Float, nullable=True)
    client_id = Column(Integer, ForeignKey("clients.id"), unique=True)
    client = relationship("Client", back_populates="client_situation")

class Contrat(Base):
    __tablename__ = "contrats"

    id = Column(Integer, primary_key=True, index=True)
    montant_pret = Column(Float)
    client_id = Column(Integer, ForeignKey("clients.id"))
    client = relationship("Client", back_populates="contrats")