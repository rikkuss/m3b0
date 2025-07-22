from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de la base de données SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Moteur SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # Requis pour SQLite pour autoriser les connexions multithread
    connect_args={"check_same_thread": False}
)

# Créateur de session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base déclarative pour les modèles ORM
Base = declarative_base()

# Fonction pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()