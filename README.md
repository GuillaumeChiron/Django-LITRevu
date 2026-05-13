# booksApp

Application Django de partage de tickets et critiques de livres.

## Description du projet

`booksApp` est une application web developpée avec Django qui permet aux utilisateurs de demander des avis sur des livres ou articles, puis de publier des critiques.

Le principe est simple :
- un utilisateur peut creer un `ticket` pour demander une recommendation ou un retour sur une lecture ;
- les autres utilisateurs peuvent repondre avec une `review` (note + commentaire) ;
- chaque utilisateur dispose d'un flux personnalise base sur ses abonnements.

L'application propose egalement un systeme de suivi entre utilisateurs pour construire un fil de contenu pertinent.

## Fonctionnalités

- Authentification : inscription, connexion, deconnexion.
- Gestion des tickets :
  - creation d'un ticket (titre, description, image optionnelle) ;
  - modification d'un ticket ;
  - suppression d'un ticket.
- Gestion des critiques (reviews) :
  - creation d'une critique sur un ticket ;
  - creation combinee ticket + critique en une seule action ;
  - modification d'une critique ;
  - suppression d'une critique ;
  - notation de 0 a 5.
- Flux personnalise :
  - affichage des tickets et critiques de l'utilisateur ;
  - affichage des contenus des utilisateurs suivis ;
  - tri antichronologique.
- Page "Posts" :
  - vue centree sur les publications de l'utilisateur.
- Abonnements :
  - recherche d'utilisateurs ;
  - suivi et desabonnement ;
  - affichage des abonnements et abonnes.

## Prerequis

- Python 3.12+
- `venv` pour isoler les dependances

## Installation

1. Cloner le depot puis se placer dans le dossier du projet.
2. Creer un environnement virtuel :

```powershell
python -m venv env
```

3. Activer l'environnement virtuel :

```powershell
.\env\Scripts\Activate.ps1 (windows)
```
```powershell
source env/bin/activate (MacOS)
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
Administration accessible sur : `http://127.0.0.1:8000/admin`