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
