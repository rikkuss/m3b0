# API CRUD Générique avec FastAPI

Ce projet est une API RESTful puissante et générique construite avec **FastAPI** et **SQLAlchemy**. Elle est conçue pour effectuer des opérations CRUD (Create, Read, Update, Delete) sur n'importe quelle table d'une base de données SQLite, en spécifiant simplement le nom de la table dans l'URL.

---

## ✨ Fonctionnalités

* **CRUD Générique** : Effectuez les quatre opérations de base sur n'importe quelle table sans écrire de code spécifique à cette table.
* **Base de Données** : Utilise **SQLite** pour la simplicité et la portabilité, géré par l'ORM **SQLAlchemy**.
* **Validation des Données** : La validation robuste des requêtes et la sérialisation des réponses sont assurées par **Pydantic**.
* **Journalisation Avancée** : Les requêtes, les erreurs et les événements importants sont journalisés via **Loguru** dans la console et dans des fichiers rotatifs.
* **Documentation Automatique** : Obtenez une documentation interactive et visuelle de l'API prête à l'emploi grâce à Swagger UI (`/docs`) et ReDoc (`/redoc`).

---

## 📂 Structure du Projet

```
/
|-- main.py              # Point d'entrée de l'application FastAPI et définition des routes
|-- crud.py              # Logique des opérations CRUD génériques
|-- database.py          # Configuration de la base de données (moteur et session)
|-- models.py            # Définition des modèles de table SQLAlchemy (ORM)
|-- schemas.py           # Définition des schémas Pydantic pour la validation des données
|-- populate_db.py       # Script pour remplir la base de données depuis un CSV
|-- requirements.txt     # Dépendances Python du projet
|-- dataset.csv          # Fichier de données CSV
|-- logs/                # Répertoire pour les fichiers de logs
|-- test.db              # Fichier de la base de données SQLite
|-- README.md            # Ce fichier
```

---

## 🚀 Installation et Démarrage

### 1. Prérequis

* Python 3.11+

### 2. Installation

Clonez ce projet (ou téléchargez les fichiers), ouvrez un terminal à la racine du projet et suivez ces étapes :

```bash
# 1. (Optionnel mais recommandé) Créez et activez un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# 2. Installez les dépendances nécessaires
pip install -r requirements.txt
```

### 3. Premier Lancement : Remplir la base de données

Avant de lancer l'API pour la première fois, remplissez la base de données en utilisant le fichier CSV fourni.

```bash
python populate_db.py
```

Cette commande va créer le fichier `test.db` et y insérer les données de la table `clients`.

### 4. Lancer le serveur de l'API

Une fois la base de données prête, lancez le serveur FastAPI avec Uvicorn :

```bash
uvicorn main:app --reload
```

Le serveur sera alors accessible à l'adresse **http://127.0.0.1:8000**.

---

## 📖 Utilisation de l'API

L'API est conçue pour être simple et intuitive. Une fois le serveur lancé, vous pouvez accéder à la documentation interactive pour tester tous les endpoints :

* **Swagger UI** : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc** : [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Endpoints Disponibles

Les endpoints fonctionnent en remplaçant `{table_name}` par le nom de la table que vous souhaitez interroger (ex: `clients`).

#### `POST /{table_name}/`

Crée un nouvel enregistrement dans la table spécifiée.

* **Exemple de corps de requête** pour `POST /clients/` :

```json
{
  "data": {
    "nom": "Durand",
    "prenom": "Alice",
    "age": 34,
    "taille": 165.5,
    "poids": 60.2,
    "sexe": "F",
    "sport_licence": true,
    "niveau_etude": "master",
    "region": "Nouvelle-Aquitaine",
    "smoker": false,
    "nationalite_francaise": true,
    "revenu_estime_mois": 3500,
    "risque_personnel": 0.3,
    "montant_pret": 15000,
    "date_creation_compte": "2025-07-22"
  }
}
```

#### `GET /{table_name}/`

Récupère une liste paginée de tous les enregistrements de la table.

* **Exemple** : `GET /clients/?skip=0&limit=10`

#### `GET /{table_name}/{item_id}`

Récupère un enregistrement unique par son `id`.

* **Exemple** : `GET /clients/1`

#### `PUT /{table_name}/{item_id}`

Met à jour un ou plusieurs champs d'un enregistrement existant.

* **Exemple de corps de requête** pour `PUT /clients/1` :

```json
{
  "data": {
    "revenu_estime_mois": 3800,
    "smoker": true
  }
}
```

#### `DELETE /{table_name}/{item_id}`

Supprime un enregistrement par son `id`.

* **Exemple** : `DELETE /clients/1`
