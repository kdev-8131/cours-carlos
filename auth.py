"""Petit système d'inscription et de connexion pour débuter en Python."""

import getpass
import hashlib
import hmac
import json
import os


FICHIER_UTILISATEURS = "users.json"


# MINI-LEÇON 1 : une fonction regroupe des instructions réutilisables.
def charger_utilisateurs(fichier=FICHIER_UTILISATEURS):
    """Retourne la liste des utilisateurs enregistrés."""
    if not os.path.exists(fichier):
        return []

    with open(fichier, "r", encoding="utf-8") as fichier_json:
        donnees = json.load(fichier_json)
        return donnees["utilisateurs"]


# MINI-LEÇON 2 : JSON permet d'enregistrer des listes et dictionnaires.
def sauvegarder_utilisateurs(utilisateurs, fichier=FICHIER_UTILISATEURS):
    """Enregistre la liste des utilisateurs dans le fichier JSON."""
    donnees = {"utilisateurs": utilisateurs}

    with open(fichier, "w", encoding="utf-8") as fichier_json:
        json.dump(donnees, fichier_json, indent=2, ensure_ascii=False)


# MINI-LEÇON 3 : on stocke une empreinte, jamais le mot de passe en clair.
def hacher_mot_de_passe(mot_de_passe, sel):
    """Crée une empreinte sécurisée du mot de passe."""
    empreinte = hashlib.pbkdf2_hmac(
        "sha256",
        mot_de_passe.encode("utf-8"),
        sel.encode("utf-8"),
        100_000,
    )
    return empreinte.hex()


def register_user(nom, mot_de_passe, fichier=FICHIER_UTILISATEURS):
    """Crée un compte. Retourne True si l'inscription réussit."""
    nom = nom.strip()

    # MINI-LEÇON 4 : il faut vérifier les données saisies par l'utilisateur.
    if len(nom) < 3:
        raise ValueError("Le nom doit contenir au moins 3 caractères.")

    if len(mot_de_passe) < 8:
        raise ValueError("Le mot de passe doit contenir au moins 8 caractères.")

    utilisateurs = charger_utilisateurs(fichier)

    for utilisateur in utilisateurs:
        if utilisateur["nom"].lower() == nom.lower():
            return False

    # MINI-LEÇON 5 : le sel rend l'empreinte unique pour chaque compte.
    sel = os.urandom(16).hex()
    empreinte = hacher_mot_de_passe(mot_de_passe, sel)

    nouvel_utilisateur = {
        "nom": nom,
        "empreinte": empreinte,
        "sel": sel,
    }

    utilisateurs.append(nouvel_utilisateur)
    sauvegarder_utilisateurs(utilisateurs, fichier)
    return True


def authenticate_user(nom, mot_de_passe, fichier=FICHIER_UTILISATEURS):
    """Retourne True si le nom et le mot de passe sont corrects."""
    utilisateurs = charger_utilisateurs(fichier)

    for utilisateur in utilisateurs:
        if utilisateur["nom"].lower() == nom.strip().lower():
            nouvelle_empreinte = hacher_mot_de_passe(
                mot_de_passe,
                utilisateur["sel"],
            )

            # MINI-LEÇON 6 : on compare les empreintes, pas les mots de passe.
            return hmac.compare_digest(
                nouvelle_empreinte,
                utilisateur["empreinte"],
            )

    return False


def creer_un_compte():
    """Demande les informations nécessaires pour créer un compte."""
    nom = input("Nom d'utilisateur : ")

    # getpass masque le mot de passe pendant la saisie.
    mot_de_passe = getpass.getpass("Mot de passe : ")

    try:
        compte_cree = register_user(nom, mot_de_passe)
    except ValueError as erreur:
        print("Erreur :", erreur)
        return

    if compte_cree:
        print("Compte créé avec succès !")
    else:
        print("Ce nom d'utilisateur existe déjà.")


def se_connecter():
    """Demande les informations nécessaires pour se connecter."""
    nom = input("Nom d'utilisateur : ")
    mot_de_passe = getpass.getpass("Mot de passe : ")

    if authenticate_user(nom, mot_de_passe):
        print("Connexion réussie. Bienvenue", nom, "!")
    else:
        print("Nom d'utilisateur ou mot de passe incorrect.")


def afficher_menu():
    """Affiche le menu principal."""
    print("\n--- Système d'authentification ---")
    print("1 - Créer un compte")
    print("2 - Se connecter")
    print("3 - Quitter")


def main():
    # MINI-LEÇON 7 : la boucle garde le menu ouvert jusqu'au choix Quitter.
    while True:
        afficher_menu()
        choix = input("Votre choix : ")

        if choix == "1":
            creer_un_compte()
        elif choix == "2":
            se_connecter()
        elif choix == "3":
            print("Au revoir !")
            break
        else:
            print("Choix invalide.")


# Ce bloc est exécuté uniquement si on lance directement : python auth.py
if __name__ == "__main__":
    main()
