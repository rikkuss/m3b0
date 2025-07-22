import pandas as pd
from sqlalchemy.orm import Session
from loguru import logger
from datetime import datetime

from database import SessionLocal, engine
from models import Client, Base

# Chemin vers votre fichier CSV
CSV_FILE_PATH = "dataset.csv"

def populate_database():
    """
    Lit les données d'un fichier CSV, les transforme et les insère dans la base de données SQLite.
    """
    # Crée la table si elle n'existe pas déjà
    Base.metadata.create_all(bind=engine)

    # Ouvre une session de base de données
    db: Session = SessionLocal()

    try:
        logger.info(f"Lecture du fichier CSV : {CSV_FILE_PATH}")
        df = pd.read_csv(CSV_FILE_PATH)

        # Remplace les valeurs NaN (Not a Number) de Pandas par None, qui est le NULL de Python/SQL
        df = df.where(pd.notna(df), None)

        clients_to_add = []
        logger.info(f"{len(df)} lignes trouvées. Début de la transformation et de l'insertion...")

        for _, row in df.iterrows():
            # Crée une instance du modèle Client pour chaque ligne du CSV
            client_data = Client(
                nom=row['nom'],
                prenom=row['prenom'],
                age=row['age'],
                taille=row['taille'],
                poids=row['poids'],
                sexe=row['sexe'],
                # Conversion des 'oui'/'non' en booléens (True/False)
                sport_licence=(row['sport_licence'] == 'oui'),
                niveau_etude=row['niveau_etude'],
                region=row['region'],
                smoker=(row['smoker'] == 'oui'),
                nationalite_francaise=(row['nationalité_francaise'] == 'oui'),
                situation_familiale=row['situation_familiale'],
                revenu_estime_mois=row['revenu_estime_mois'],
                historique_credits=row['historique_credits'],
                risque_personnel=row['risque_personnel'],
                score_credit=row['score_credit'],
                loyer_mensuel=row['loyer_mensuel'],
                montant_pret=row['montant_pret'],
                # Conversion de la chaîne de caractères en objet Date
                date_creation_compte=datetime.strptime(row['date_creation_compte'], '%Y-%m-%d').date()
            )
            clients_to_add.append(client_data)

        # Ajoute tous les nouveaux objets à la session en une seule fois (plus performant)
        db.bulk_save_objects(clients_to_add)

        # Valide la transaction pour enregistrer les données de manière permanente
        db.commit()

        logger.success(f"{len(clients_to_add)} clients ont été ajoutés avec succès à la base de données !")

    except FileNotFoundError:
        logger.error(f"Le fichier {CSV_FILE_PATH} n'a pas été trouvé. Vérifiez le chemin d'accès.")
    except Exception as e:
        logger.error(f"Une erreur est survenue : {e}")
        # En cas d'erreur, annule toutes les modifications pour garder la base de données propre
        db.rollback()
    finally:
        # Ferme la session de base de données
        db.close()

if __name__ == "__main__":
    populate_database()