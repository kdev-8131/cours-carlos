# Cours : la gestion de versions avec Git

## Qu'est-ce que la gestion de versions ?

La gestion de versions consiste à enregistrer l'évolution d'un projet au fil du temps. Chaque version importante est conservée avec une description des changements réalisés.

Git est un logiciel de gestion de versions. GitHub est une plateforme en ligne qui permet d'héberger des dépôts Git, de partager du code et de collaborer avec d'autres personnes.

## Pourquoi gérer les versions d'un projet ?

La gestion de versions permet de :

- conserver l'historique des modifications ;
- savoir qui a effectué chaque changement et pourquoi ;
- revenir à une version précédente en cas d'erreur ;
- travailler à plusieurs sans écraser le travail des autres ;
- tester de nouvelles idées dans une branche séparée ;
- sauvegarder et partager le projet sur une plateforme comme GitHub ;
- comparer différentes versions d'un même fichier.

Sans gestion de versions, on finit souvent avec des fichiers difficiles à suivre, par exemple :

```text
projet-final.zip
projet-final-2.zip
projet-final-vraiment-final.zip
projet-final-corrige.zip
```

Avec Git, toutes ces étapes sont enregistrées proprement dans un seul projet.

## Vocabulaire essentiel

- **Dépôt (repository)** : dossier de projet suivi par Git.
- **Commit** : enregistrement d'un ensemble de modifications à un instant précis.
- **Branche (branch)** : ligne de développement indépendante. La branche principale s'appelle généralement `main`.
- **Dépôt distant (remote)** : copie du dépôt hébergée en ligne, par exemple sur GitHub.
- **Clone** : copie locale d'un dépôt distant.
- **Push** : envoi des commits locaux vers le dépôt distant.
- **Pull** : récupération des nouveaux commits du dépôt distant.
- **Merge** : fusion des changements d'une branche dans une autre.

## Le fonctionnement de Git

Un fichier peut passer par plusieurs états :

1. **Modifié** : le fichier a changé dans le dossier de travail.
2. **Ajouté à l'index** : le fichier est sélectionné pour le prochain commit avec `git add`.
3. **Enregistré** : les changements sont sauvegardés dans l'historique avec `git commit`.
4. **Publié** : le commit est envoyé sur GitHub avec `git push`.

Le chemin habituel est donc :

```text
Modification → git add → git commit → git push
```

## Commandes principales

### Créer un dépôt Git

```bash
git init
```

Cette commande initialise Git dans le dossier courant.

### Vérifier l'état du projet

```bash
git status
```

Elle indique les fichiers modifiés, ajoutés ou non suivis.

### Ajouter des changements

Pour ajouter un fichier précis :

```bash
git add README.md
```

Pour ajouter tous les changements :

```bash
git add .
```

### Créer un commit

```bash
git commit -m "Ajoute un cours sur la gestion de versions"
```

Un bon message de commit doit être court et expliquer clairement le changement.

### Consulter l'historique

```bash
git log --oneline
```

### Relier le projet à GitHub

```bash
git remote add origin https://github.com/utilisateur/depot.git
```

### Envoyer les commits sur GitHub

```bash
git push origin main
```

### Récupérer les changements depuis GitHub

```bash
git pull origin main
```

## Travailler avec des branches

Une branche permet de développer une fonctionnalité sans modifier immédiatement la version principale.

Créer une branche et s'y déplacer :

```bash
git switch -c nouvelle-fonctionnalite
```

Revenir sur la branche principale :

```bash
git switch main
```

Fusionner la branche :

```bash
git merge nouvelle-fonctionnalite
```

## Exemple de workflow quotidien

```bash
# Récupérer les changements récents
git pull origin main

# Modifier les fichiers, puis vérifier leur état
git status

# Préparer les changements
git add .

# Enregistrer une nouvelle version
git commit -m "Décris clairement la modification"

# Publier les commits
git push origin main
```

## Bonnes pratiques

- créer des commits petits et cohérents ;
- écrire des messages de commit explicites ;
- exécuter `git status` avant un commit ;
- récupérer les changements distants avant de commencer à travailler ;
- utiliser une branche pour une modification importante ;
- ne jamais enregistrer de mots de passe, de clés secrètes ou de jetons dans Git ;
- ajouter les fichiers inutiles ou sensibles dans un fichier `.gitignore`.

## À retenir

Git sert à conserver et organiser l'histoire d'un projet. GitHub facilite son stockage en ligne et le travail en équipe. Les quatre commandes essentielles à retenir sont :

```bash
git status
git add .
git commit -m "Message clair"
git push
```

## Projet pratique : système d'authentification Python

Le fichier `auth.py` contient un exemple très simple, adapté à une première heure de Python. Il utilise uniquement la bibliothèque standard :

- les utilisateurs sont enregistrés dans un fichier JSON local ;
- les comptes, mots de passe et scores sont enregistrés dans un fichier JSON ;
- les noms d'utilisateur ne sont pas sensibles aux majuscules.

### Prérequis

- Python 3.10 ou une version plus récente.

### Lancer le programme

```bash
python auth.py
```

Un menu permet ensuite de créer un compte ou de se connecter. Le code montre des variables, des fonctions, des conditions et un dictionnaire.

Les mots de passe saisis ne sont pas affichés dans le terminal. Le fichier `users.json` est créé automatiquement et ignoré par Git afin de ne pas publier les comptes.

> **Attention :** ce projet stocke les mots de passe en clair pour simplifier le premier exercice. Il sert uniquement à apprendre. Il ne faut jamais utiliser de vrais mots de passe ni employer cette méthode dans une véritable application.

### Lancer les tests

```bash
python -m unittest -v
```

Ce projet est un exemple pédagogique d'authentification locale. Pour un site en production, il faut utiliser le système d'authentification éprouvé d'un framework web, protéger les sessions, activer HTTPS et prévoir une limitation des tentatives de connexion.

## Petit jeu avec progression

Le fichier `jeu.py` contient un jeu du nombre mystère :

- le joueur doit d'abord se connecter avec son compte ;
- il doit trouver un nombre entre 1 et 10 en trois essais ;
- une victoire rapporte entre 10 et 20 points ;
- le joueur gagne un niveau tous les 30 points ;
- le score et le niveau sont enregistrés dans `users.json`.

Lancez le programme principal :

```bash
python auth.py
```

Choisissez `1` pour créer un compte. Relancez ensuite le programme, choisissez `2` et connectez-vous : le jeu démarre automatiquement après une connexion réussie. Sans identifiants valides, il est impossible de jouer ou d'enregistrer une progression.
