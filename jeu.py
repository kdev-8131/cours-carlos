"""Petit jeu du nombre mystère avec progression enregistrée."""

import getpass
import random

from auth import authenticate_user, enregistrer_utilisateurs, lire_utilisateurs


def ajouter_points(nom, points, fichier="users.json"):
    """Ajoute des points à un utilisateur et calcule son niveau."""
    utilisateurs = lire_utilisateurs(fichier)
    nom = nom.strip().lower()

    # get donne 0 si un ancien compte ne possède pas encore de score.
    ancien_score = utilisateurs[nom].get("score", 0)
    nouveau_score = ancien_score + points

    # Le joueur gagne un niveau tous les 30 points.
    niveau = 1 + nouveau_score // 30

    utilisateurs[nom]["score"] = nouveau_score
    utilisateurs[nom]["niveau"] = niveau
    enregistrer_utilisateurs(utilisateurs, fichier)

    return nouveau_score, niveau


def jouer(nom):
    """Lance une partie de nombre mystère."""
    nombre_secret = random.randint(1, 10)
    essais_restants = 3

    print("\nJe pense à un nombre entre 1 et 10.")
    print("Tu as 3 essais pour le trouver.")

    # La boucle continue tant qu'il reste des essais.
    while essais_restants > 0:
        reponse = input("Ton nombre : ")

        # isdigit vérifie que la réponse contient uniquement des chiffres.
        if not reponse.isdigit():
            print("Entre un nombre entier.")
            continue

        nombre = int(reponse)
        essais_restants = essais_restants - 1

        if nombre == nombre_secret:
            points = 10 + essais_restants * 5
            score, niveau = ajouter_points(nom, points)
            print("Bravo, tu as trouvé !")
            print("Points gagnés :", points)
            print("Score total :", score)
            print("Niveau :", niveau)
            return

        if nombre < nombre_secret:
            print("Le nombre mystère est plus grand.")
        else:
            print("Le nombre mystère est plus petit.")

    print("Perdu ! Le nombre était", nombre_secret)


def main():
    print("--- Connexion au jeu ---")
    nom = input("Nom d'utilisateur : ")
    mot_de_passe = getpass.getpass("Mot de passe : ")

    if authenticate_user(nom, mot_de_passe):
        utilisateurs = lire_utilisateurs()
        utilisateur = utilisateurs[nom.strip().lower()]

        print("\nBienvenue", nom, "!")
        print("Score :", utilisateur.get("score", 0))
        print("Niveau :", utilisateur.get("niveau", 1))
        jouer(nom)
    else:
        print("Identifiants incorrects.")


if __name__ == "__main__":
    main()
