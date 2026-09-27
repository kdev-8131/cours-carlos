"""Exemple très simple d'inscription et de connexion en Python."""

import getpass
import hashlib
import hmac
import json
import os


# Une variable permet de garder une information en mémoire.
FICHIER = "users.json"


# Une fonction est un petit bloc de code que l'on peut réutiliser.
def lire_utilisateurs(fichier=FICHIER):
    # Si le fichier n'existe pas, on retourne un dictionnaire vide.
    if not os.path.exists(fichier):
        return {}

    with open(fichier, "r", encoding="utf-8") as fichier_json:
        return json.load(fichier_json)


def enregistrer_utilisateurs(utilisateurs, fichier=FICHIER):
    # JSON permet d'enregistrer un dictionnaire dans un fichier.
    with open(fichier, "w", encoding="utf-8") as fichier_json:
        json.dump(utilisateurs, fichier_json, indent=2)


def hacher(mot_de_passe, sel):
    # Cette fonction transforme le mot de passe en empreinte sécurisée.
    # Il n'est pas nécessaire de comprendre cette ligne dès le premier cours.
    resultat = hashlib.pbkdf2_hmac(
        "sha256", mot_de_passe.encode(), bytes.fromhex(sel), 100_000
    )
    return resultat.hex()


def register_user(nom, mot_de_passe, fichier=FICHIER):
    utilisateurs = lire_utilisateurs(fichier)
    nom = nom.strip().lower()

    if len(nom) < 3:
        raise ValueError("Le nom doit contenir au moins 3 caractères.")

    if len(mot_de_passe) < 8:
        raise ValueError("Le mot de passe doit contenir au moins 8 caractères.")

    # Si le nom est déjà dans le dictionnaire, on refuse l'inscription.
    if nom in utilisateurs:
        return False

    # Le sel est une valeur aléatoire ajoutée avant le hachage.
    sel = os.urandom(16).hex()

    utilisateurs[nom] = {
        "mot_de_passe": hacher(mot_de_passe, sel),
        "sel": sel,
    }

    enregistrer_utilisateurs(utilisateurs, fichier)
    return True


def authenticate_user(nom, mot_de_passe, fichier=FICHIER):
    utilisateurs = lire_utilisateurs(fichier)
    nom = nom.strip().lower()

    if nom not in utilisateurs:
        return False

    utilisateur = utilisateurs[nom]
    empreinte = hacher(mot_de_passe, utilisateur["sel"])

    return hmac.compare_digest(empreinte, utilisateur["mot_de_passe"])


def main():
    print("1 - Créer un compte")
    print("2 - Se connecter")
    choix = input("Votre choix : ")

    nom = input("Nom d'utilisateur : ")
    mot_de_passe = getpass.getpass("Mot de passe : ")

    if choix == "1":
        try:
            if register_user(nom, mot_de_passe):
                print("Compte créé !")
            else:
                print("Ce compte existe déjà.")
        except ValueError as erreur:
            print("Erreur :", erreur)

    elif choix == "2":
        if authenticate_user(nom, mot_de_passe):
            print("Connexion réussie !")
        else:
            print("Identifiants incorrects.")

    else:
        print("Choix incorrect.")


# Python lance main seulement si on exécute ce fichier directement.
if __name__ == "__main__":
    main()
