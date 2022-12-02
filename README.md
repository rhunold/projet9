# LITReview


Cette application est développée avec le framework Django.

## Installation

1. Cloner ce dossier `$ git clone https://github.com/rhunold/projet9.git` 
2. Se placer à la racine du projet
3. Créer un environnement virtuel `python -m venv env`
4. Activer l'environnement virtuel `source env/bin/activate`
5. Installer les dépendances  `pip install -r requirements.txt`
6. Aller dans le dossier 'litreview'
7. Lancer le serveur `python manage.py runserver`

## Utiliser l'application

Ouvrir cette url dans un navigateur : `http://localhost:8000/`

Utiliser l'un des comptes existants ou en créer un nouveau.


| typeUser  | username | password    |
|-----------|----------|-------------|
| User      | toto     | tata        |
| User      | titi     | tata        |
| User      | tutu     | tata        |
| SuperUser | raf      | happycoding |

## Admin Django

1. Aller à l'url 'http://127.0.0.1:8000/admin/login/'
2. Utiliser les accès d'un SuperUser


## Pep8
Pour vérifier la pep8, `pep8 litreview  --max-line-length 120 --exclude=migrations`




