# 📚 LITRevu 🎉

Bienvenue dans LITRevu, une application Django permettant aux utilisateurs de publier et consulter des critiques de livres ou d’articles. Avec LITRevu, vous pouvez non seulement demander une critique sur un livre ou un article, mais aussi partager votre avis et découvrir des recommandations basées sur les critiques d'autres utilisateurs.

## 📜 Table des Matières

- [Introduction](#-introduction)
- [Fonctionnalités](#-fonctionnalités)
- [Installation](#%EF%B8%8F-installation)
  - [Prérequis](#prérequis)
  - [Étapes](#étapes)
    - [Cloner le Répertoire](#cloner-le-répertoire)
    - [Créer un Environnement Virtuel](#créer-un-environnement-virtuel)
    - [Installer les Dépendances](#installer-les-dépendances)
    - [Appliquer les Migrations](#appliquer-les-migrations)
    - [Lancer le Serveur](#lancer-le-serveur)
- [Utilisation](#-utilisation)
  - [Créer un Billet](#créer-un-billet)
  - [Poster une Critique](#poster-une-critique)
  - [Suivre d'autres Utilisateurs](#suivre-dautres-utilisateurs)
  - [Consulter le Flux](#consulter-le-flux)
- [Structure des Fichiers](#-structure-des-fichiers)
- [Contribution](#-contribution)

## 🌟 Introduction

LITRevu est une application qui permet aux utilisateurs de publier et demander des critiques de livres ou d’articles. Conçu pour être convivial et intuitif, LITRevu offre une plateforme où chacun peut lire des critiques pertinentes, demander des avis et partager ses propres réflexions littéraires.

## 🚀 Fonctionnalités

- 📖 **Demande de Critiques** : Créez un billet pour demander une critique d'un livre ou article.

- 📝 **Publication de Critiques** : Publiez votre propre critique ou répondez aux demandes d'autres utilisateurs.

- 🔍 **Recherche et Suivi** : Suivez d'autres utilisateurs pour voir leurs dernières publications et critiques.

- 📰 **Flux Personnalisé** : Consultez votre flux pour voir les dernières publications des utilisateurs que vous suivez, classées par

     ordre antéchronologique.

## 🛠️ Installation

### Prérequis

- Python 3.x
- Git

### Étapes

1. **Cloner le Répertoire**
   
    git clone https://github.com/VincentDesmouceaux/LITRevu.git

    cd LITRevu

2. **Créer un Environnement Virtuel**
   
    python3 -m venv env
    
    source env/bin/activate  
    
    Sur Windows : env\Scripts\activate

3. **Installer les Dépendances**

    pip install -r requirements.txt

4. **Appliquer les Migrations**

    python manage.py migrate

5. **Lancer le Serveur**

    python manage.py runserver

## 📖 Utilisation

### Créer un Billet

1. **Connectez-vous à votre compte**

    Allez dans la section "Créer un Billet".
    
    Remplissez le titre, la description, et ajoutez une image (facultatif).

    Publiez pour demander une critique sur votre livre ou article préféré.

2. **Poster une Critique**

    Sélectionnez un billet dans votre flux ou allez dans la section "Poster une Critique".

    Remplissez le formulaire de critique, incluant le titre, la note (de 1 à 5 étoiles) et le contenu.

    Soumettez votre critique pour la publier.

3. **Suivre d'autres Utilisateurs**

    Recherchez le nom d'utilisateur dans la section "Suivre des Utilisateurs".

    Ajoutez l'utilisateur à votre liste pour voir ses futures publications et critiques.

4. **Consulter le Flux**

    Accédez à votre flux pour voir les billets et critiques des utilisateurs que vous suivez.
    Consultez les dernières publications classées de la plus récente à la plus ancienne.

## 📂 Structure des Fichiers

    
    ├── authentication
    │   ├── views.py
    │   └── templates/authentication/
    ├── feed
    │   ├── views.py
    │   └── templates/feed/
    ├── reviews
    │   ├── models.py
    │   └── templates/reviews/
    ├── subscriptions
    │   ├── views.py
    │   └── templates/subscriptions/
    ├── db.sqlite3
    ├── manage.py
    └── README.md

## 🤝 Contribution

    Les contributions sont les bienvenues ! Voici comment vous pouvez aider :

    Signaler des Bugs : Si vous rencontrez un problème, signalez-le dans le suivi des problèmes GitHub.

    Soumettre des Pull Requests : Ajoutez de nouvelles fonctionnalités ou corrigez des bugs.

    Suggérer des Améliorations : Nous sommes ouverts aux suggestions pour améliorer l'application.

    Merci d'utiliser LITRevu ! Si vous avez des questions, n'hésitez pas à nous contacter.    

