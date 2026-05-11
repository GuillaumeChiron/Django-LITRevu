# booksApp

Application Django de partage de tickets et critiques de livres.

## Prerequis

- Python 3.12+
- `pip`
- `venv` pour isoler les dependances

## Installation

1. Cloner le depot puis se placer dans le dossier du projet.
2. Creer un environnement virtuel :

```powershell
python -m venv env
```

3. Activer l'environnement virtuel :

```powershell
(.\env\Scripts\Activate.ps1) ou (source env/bin/activate)
```

4. Installer les dependances :

```powershell
pip install -r requirements.txt
```

5. Appliquer les migrations :

```powershell
python manage.py migrate
```

6. Lancer le serveur de developpement :

```powershell
python manage.py runserver
```

L'application sera accessible sur : `http://127.0.0.1:8000/`

## Commandes utiles

- Creer un superutilisateur :

```powershell
python manage.py createsuperuser
```
