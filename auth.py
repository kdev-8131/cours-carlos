"""Système d'authentification local avec stockage JSON.

Ce fichier est volontairement commenté comme un mini-cours. Il montre le
chemin complet : saisir un mot de passe, le hacher, enregistrer le résultat,
puis vérifier ce mot de passe lors d'une connexion.
"""

from __future__ import annotations

import argparse
import base64
import getpass
import hashlib
import hmac
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any


# MINI-LEÇON 1 — Les constantes
# Une constante centralise une valeur qui ne doit pas changer pendant
# l'exécution. Le fichier JSON sera créé à côté de ce script.
DEFAULT_STORAGE = Path(__file__).with_name("users.json")

# Une expression régulière définit ici les caractères autorisés dans un nom.
USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{3,30}$")

# Ces paramètres règlent le coût de scrypt. Un calcul volontairement coûteux
# ralentit les tentatives massives de découverte des mots de passe.
SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1


def load_users(storage: str | Path = DEFAULT_STORAGE) -> list[dict[str, Any]]:
    """Charge les comptes depuis le fichier JSON."""
    # MINI-LEÇON 2 — Lire du JSON
    # JSON transforme des données structurées en texte. json.load effectue
    # l'opération inverse et reconstruit les dictionnaires et les listes Python.
    path = Path(storage)
    if not path.exists():
        # Au premier lancement, aucun fichier n'existe encore : la liste des
        # utilisateurs est donc simplement vide.
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        raise RuntimeError(f"Impossible de lire {path} : {error}") from error

    # Ne jamais supposer qu'un fichier externe contient le bon format.
    if not isinstance(data, dict) or not isinstance(data.get("users"), list):
        raise RuntimeError(f"Le fichier {path} ne possède pas un format valide.")
    return data["users"]


def save_users(users: list[dict[str, Any]], storage: str | Path) -> None:
    """Enregistre les comptes avec un remplacement atomique du fichier."""
    # MINI-LEÇON 3 — Écrire sans abîmer le fichier
    # On écrit d'abord dans un fichier temporaire, puis os.replace le déplace.
    # Ainsi, une interruption pendant l'écriture ne laisse pas un JSON à moitié
    # rempli à la place du fichier principal.
    path = Path(storage)
    path.parent.mkdir(parents=True, exist_ok=True)

    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as file:
            json.dump({"users": users}, file, ensure_ascii=False, indent=2)
            file.write("\n")
            temporary_path = Path(file.name)
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def validate_username(username: str) -> None:
    # MINI-LEÇON 4 — Valider les entrées
    # Les données venant d'un utilisateur doivent toujours être contrôlées
    # avant d'être utilisées ou enregistrées.
    if not USERNAME_PATTERN.fullmatch(username):
        raise ValueError(
            "Le nom d'utilisateur doit contenir entre 3 et 30 caractères : "
            "lettres, chiffres, tiret ou tiret bas."
        )


def validate_password(password: str) -> None:
    # Plusieurs règles simples évitent les mots de passe trop faibles. Dans une
    # vraie application, une phrase de passe longue est souvent préférable.
    if len(password) < 8:
        raise ValueError("Le mot de passe doit contenir au moins 8 caractères.")
    if not any(character.isalpha() for character in password):
        raise ValueError("Le mot de passe doit contenir au moins une lettre.")
    if not any(character.isdigit() for character in password):
        raise ValueError("Le mot de passe doit contenir au moins un chiffre.")


def hash_password(password: str, salt: bytes) -> bytes:
    # MINI-LEÇON 5 — Hacher n'est pas chiffrer
    # Un chiffrement peut être inversé avec une clé. Un hachage de mot de passe
    # est conçu pour être à sens unique : on compare les empreintes sans
    # retrouver ni enregistrer le mot de passe original.
    return hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
    )


def register_user(
    username: str,
    password: str,
    storage: str | Path = DEFAULT_STORAGE,
) -> bool:
    """Crée un compte et retourne False si le nom existe déjà."""
    username = username.strip()
    validate_username(username)
    validate_password(password)

    # MINI-LEÇON 6 — Le sel
    # Chaque compte reçoit 16 octets aléatoires. Deux utilisateurs ayant le
    # même mot de passe auront ainsi des empreintes différentes.
    salt = os.urandom(16)
    password_hash = hash_password(password, salt)

    users = load_users(storage)
    # casefold permet une comparaison sans tenir compte des majuscules.
    if any(user["username"].casefold() == username.casefold() for user in users):
        return False

    # JSON ne sait pas stocker directement des octets. Base64 les représente
    # sous forme de texte. Attention : Base64 n'est pas un chiffrement.
    users.append(
        {
            "username": username,
            "password_hash": base64.b64encode(password_hash).decode("ascii"),
            "salt": base64.b64encode(salt).decode("ascii"),
        }
    )
    save_users(users, storage)
    return True


def authenticate_user(
    username: str,
    password: str,
    storage: str | Path = DEFAULT_STORAGE,
) -> bool:
    """Vérifie les identifiants sans révéler la cause d'un échec."""
    # MINI-LEÇON 7 — Authentifier
    # On retrouve le compte, on recalcule l'empreinte avec le sel enregistré,
    # puis on compare cette empreinte avec celle du fichier JSON.
    normalized_username = username.strip().casefold()
    user = next(
        (
            item
            for item in load_users(storage)
            if item["username"].casefold() == normalized_username
        ),
        None,
    )
    if user is None:
        return False

    try:
        stored_hash = base64.b64decode(user["password_hash"], validate=True)
        salt = base64.b64decode(user["salt"], validate=True)
    except (KeyError, TypeError, ValueError) as error:
        raise RuntimeError("Les données du compte sont invalides.") from error
    candidate_hash = hash_password(password, salt)

    # compare_digest limite les différences de durée entre deux comparaisons et
    # réduit les informations exploitables par une attaque temporelle.
    return hmac.compare_digest(stored_hash, candidate_hash)


def register_command(storage: Path) -> int:
    username = input("Nom d'utilisateur : ")
    # MINI-LEÇON 8 — Saisir un secret
    # getpass masque le mot de passe dans le terminal, contrairement à input.
    password = getpass.getpass("Mot de passe : ")
    confirmation = getpass.getpass("Confirmez le mot de passe : ")

    if password != confirmation:
        print("Les mots de passe ne correspondent pas.")
        return 1

    try:
        created = register_user(username, password, storage)
    except ValueError as error:
        print(f"Erreur : {error}")
        return 1

    if not created:
        print("Ce nom d'utilisateur existe déjà.")
        return 1

    print("Compte créé avec succès.")
    return 0


def login_command(storage: Path) -> int:
    username = input("Nom d'utilisateur : ")
    password = getpass.getpass("Mot de passe : ")

    if authenticate_user(username, password, storage):
        print(f"Bienvenue, {username.strip()} !")
        return 0

    print("Nom d'utilisateur ou mot de passe incorrect.")
    return 1


def build_parser() -> argparse.ArgumentParser:
    # MINI-LEÇON 9 — Une interface en ligne de commande
    # argparse lit les arguments, affiche l'aide et refuse les actions inconnues.
    parser = argparse.ArgumentParser(
        description="Inscription et connexion avec stockage local JSON."
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=DEFAULT_STORAGE,
        help="chemin du fichier JSON (users.json par défaut)",
    )
    parser.add_argument(
        "action",
        choices=("register", "login"),
        help="register pour créer un compte, login pour se connecter",
    )
    return parser


def main() -> int:
    # 0 signifie succès pour le système ; une autre valeur signale une erreur.
    arguments = build_parser().parse_args()
    if arguments.action == "register":
        return register_command(arguments.file)
    return login_command(arguments.file)


if __name__ == "__main__":
    # Cette condition lance main uniquement quand auth.py est exécuté directement.
    # Lors d'un import depuis les tests, les fonctions restent disponibles sans
    # démarrer l'interface interactive.
    raise SystemExit(main())
