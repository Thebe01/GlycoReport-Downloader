#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Format d'en-tête standard à respecter pour ce projet.
Voir .github/HEADER_TEMPLATE_PYTHON.md pour les détails.

Module        : config.py
Type          : Python module
Auteur        : Pierre Théberge
Compagnie     : Innovations, Performances, Technologies inc.
Créé le       : 2025-08-05
Modifié le    : 2026-04-17
Version       : 0.5.9
Copyright     : Pierre Théberge

Description
-----------
Centralisation et validation de la configuration (config.yaml) et des secrets (.env chiffré).

Modifications
-------------
0.0.0  - 2025-08-05   [N/A]   : Version initiale.
0.1.0  - 2025-08-06   [N/A]   : Ajout de la gestion des paramètres de configuration via un fichier YAML.
0.1.1  - 2025-08-13   [N/A]   : Normalisation systématique des chemins, gestion d'erreur sur les paramètres,
                               conservation de tous les paramètres importants (chemins, URL, rapports, etc.).
0.1.2  - 2025-08-13   [N/A]   : Ajout de la fonction normalize_path, harmonisation de l’utilisation des chemins.
0.1.3  - 2025-08-18   [N/A]   : Suppression de la duplication de normalize_path, import depuis utils.py,
                               harmonisation de l’utilisation des chemins dans tout le projet.
0.1.4  - 2025-08-18   [N/A]   : Sécurisation du chargement de la configuration : utilisation stricte de yaml.safe_load,
                               validation des types et de la présence des paramètres, vérification des droits d'accès,
                               protection contre l'exposition de secrets et contre l'injection de code.
0.1.5  - 2025-08-22   [N/A]   : Ajout du paramètre chromedriver_path configurable via config.yaml,
                               valeur par défaut : "./chromedriver.exe" (même dossier que l'exécutable).
0.1.6  - 2025-08-22   [N/A]   : Synchronisation des versions dans tous les modules, ajout de version.py, log de la version exécutée.
0.1.7  - 2025-08-25   [N/A]   : Création automatique de config.yaml à partir de config_example.yaml si absent.
                               Gestion interactive des credentials si .env absent (demande à l'utilisateur, non conservé).
0.1.8  - 2025-08-27   [N/A]   : Configuration interactive avancée pour config.yaml et .env.
                               Copie minimale du profil Chrome lors de la configuration.
                               Ajout du paramètre log_retention_days (0 = conservation illimitée).
                               Nettoyage automatique des logs selon la rétention.
                               Messages utilisateurs colorés et validation renforcée.
0.1.9  - 2025-08-28   [N/A]   : Vérification interactive de la clé chromedriver_log lors de la création de config.yaml.
                               Empêche la saisie d'un dossier pour le log, exige un chemin de fichier.
                               Correction de la robustesse de la configuration initiale.
0.1.10 - 2025-08-28   [N/A]   : Le ménage des logs s'effectue désormais uniquement après l'activation du logging.
                               Chaque suppression de log est loggée.
0.2.0  - 2025-08-28   [N/A]   : Le fichier .env est désormais chiffré à l'écriture et déchiffré à la volée lors de la lecture.
                               La fonction get_dexcom_credentials ne propose plus de saisie interactive si les identifiants sont absents.
                               Correction de la suppression du fichier temporaire .env.tmp même en cas d'erreur.
                               Sécurisation de l'affichage des identifiants (plus d'affichage du mot de passe en clair).
0.2.1  - 2025-08-29   [N/A]   : Changement de nom du projet (anciennement Dexcom Clarity Reports Downloader).
0.2.2  - 2025-08-29   [N/A]   : Séparation stricte de la gestion des arguments CLI (retirée de ce module).
                               Désactivation de tout accès à la config lors de l'affichage du help.
                               Nettoyage des doublons de fonctions utilitaires CLI.
0.2.3  - 2025-10-14   [ES-11] : Remplacement d'une version spécifique de chromedriver par ChromeDriverManager qui charge toujours la version courante.
                               Modification du xpath pour le rapport statistiques horaires pour corriger l'erreur d'accès (indépendant de la langue de l'utilisateur).
                               Ajout de la colonne Billet dans le bloc des modifications.
0.2.4  - 2025-10-16   [ES-12] : Suppression du paramètre obsolète chromedriver_path (non utilisé depuis v0.2.3).
                               Nettoyage du code : CHROMEDRIVER_PATH retiré de la configuration.
                               Simplification : le répertoire chromedriver-win64/ n'est plus nécessaire.
0.2.5  - 2025-10-16   [ES-10] : Synchronisation de version (aucun changement fonctionnel).
0.2.6  - 2025-10-21   [ES-7]  : Synchronisation de version (aucun changement fonctionnel).
0.2.7  - 2025-10-27   [ES-16] : Synchronisation de version (aucun changement fonctionnel).
0.2.11 - 2025-12-22   [ES-18] : Synchronisation de version.
0.2.12 - 2025-12-22   [ES-3]  : Synchronisation de version.
0.2.13 - 2026-01-19   [ES-19] : Synchronisation de version (aucun changement fonctionnel).
0.2.14 - 2026-01-19   [ES-19] : Synchronisation de version (aucun changement fonctionnel).
0.2.15 - 2026-01-19   [ES-19] : Sécurité : validation stricte de dexcom_url (parsing + allowlist, HTTPS, sous-domaines).
0.2.16 - 2026-01-20   [ES-19] : Synchronisation de version (aucun changement fonctionnel).
0.2.17 - 2026-01-20   [ES-19] : Prise en compte de debug + durcissement typage (aucun changement fonctionnel majeur).
0.2.18 - 2026-01-20   [ES-19] : Synchronisation de version (aucun changement fonctionnel).
0.3.2  - 2026-02-02   [ES-19] : Synchronisation de version (aucun changement fonctionnel).
0.3.3  - 2026-02-02   [ES-19] : Synchronisation de version (aucun changement fonctionnel).
0.3.4  - 2026-02-12   [ES-3]  : Synchronisation de version (aucun changement fonctionnel).
0.3.5  - 2026-02-12   [ES-3]  : Synchronisation de version (aucun changement fonctionnel).
0.3.6  - 2026-02-12   [ES-3]  : Synchronisation de version (aucun changement fonctionnel).
0.3.15 - 2026-02-26   [ES-6]  : Synchronisation de version (aucun changement fonctionnel dans ce module).
0.3.16 - 2026-03-19   [ES-15] : Configuration des logs : valeur par defaut de log_retention_days portee a 30 jours.
                               Alignement de la retention par defaut lors de la saisie interactive et du chargement de la configuration.
                               Synchronisation de version et mise a jour de la documentation release.
0.3.17 - 2026-03-23   [ES-14] : Synchronisation de version (aucun changement fonctionnel dans ce module).
0.3.18 - 2026-03-25   [ES-14] : Synchronisation de version (aucun changement fonctionnel dans ce module).
0.3.19 - 2026-03-25   [ES-14] : Synchronisation de version (aucun changement fonctionnel dans ce module).
0.4.0  - 2026-04-14   [ES-20] : Synchronisation de version (aucun changement fonctionnel dans ce module).
0.5.0  - 2026-04-14   [ES-21] : Ajout de l'export DAYS (parametre days depuis config.yaml).
0.5.1  - 2026-04-15   [ES-22] : Synchronisation de version (aucun changement fonctionnel).
0.5.2  - 2026-04-15   [ES-25] : Synchronisation de version (aucun changement fonctionnel).
0.5.3  - 2026-04-15   [ES-25] : Synchronisation de version (aucun changement fonctionnel).
0.5.4  - 2026-04-15   [CR]    : Validation explicite de 'days' dans validate_config : type (int ou
                               chaine entiere), valeurs autorisees (7/14/30/90), message d'erreur
                               utilisateur. Avertissement si 'days' et 'date_debut'/'date_fin' sont
                               tous deux definis. Conversion DAYS securisee avec try/except.
0.5.5  - 2026-04-15   [CR]    : Synchronisation de version (aucun changement fonctionnel).
0.5.6  - 2026-04-16   [ES-25] : Synchronisation de version (aucun changement fonctionnel).
0.5.7  - 2026-04-17   [ES-25] : Synchronisation de version (aucun changement fonctionnel).
0.5.8  - 2026-04-17   [ES-25] : Synchronisation de version (aucun changement fonctionnel).
0.5.9  - 2026-04-17   [ES-25] : Synchronisation de version (aucun changement fonctionnel).

Paramètres
----------
N/A (module importé par l'application; la configuration provient de config.yaml et de l'environnement).

Exemple
-------
>>> python GlycoDownload.py --dry-run
"""

import os
import sys
import logging
from datetime import datetime, timedelta
import yaml
from dotenv import load_dotenv
from colorama import init, Fore, Style
from utils import normalize_path, pause_on_error, url_is_allowed
import getpass
import shutil
import re
from cryptography.fernet import Fernet
import subprocess
import ast  # à mettre en haut du fichier si pas déjà importé
import argparse
from typing import Any, cast

# Initialisation colorama pour la coloration des messages console
init(autoreset=True)

# --- Constantes ---
CONFIG_FILE = "config.yaml"
CONFIG_EXAMPLE_FILE = "config_example.yaml"
ENV_FILE = ".env"
ENV_EXAMPLE_FILE = ".env.example"

# --- Logger minimal pour ce module ---
logger = logging.getLogger("config")
if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO)

# --- Fonctions utilitaires pour l'affichage coloré ---
def print_info(msg):
    print(Fore.CYAN + msg)

def print_success(msg):
    print(Fore.GREEN + msg)

def print_error(msg):
    print(Fore.RED + msg)

def parse_args():
    """
    Parse les arguments de la ligne de commande pour GlycoReport-Downloader.
    Retourne l'objet Namespace argparse.
    """


def is_help_requested():
    """
    Détecte si l'utilisateur a demandé l'aide via -h, --help ou --h.
    """

# --- Fonction de validation de la configuration ---
def validate_config(config):
    """Valide la présence et le type des paramètres essentiels."""
    required_keys = [
        ("download_dir", str),
        ("output_dir", str),
        ("dexcom_url", str),
        ("chromedriver_log", str),
        ("chrome_user_data_dir", str),
        ("rapports", list),
        ("log_retention_days", int),
    ]
    for key, typ in required_keys:
        if key not in config:
            print_error(f"Le paramètre obligatoire '{key}' est manquant dans la configuration.")
            pause_on_error()
            sys.exit(1)
        if not isinstance(config[key], typ):
            print_error(f"Le paramètre '{key}' doit être de type {typ.__name__}.")
            pause_on_error()
            sys.exit(1)

    # Validation sécurité : dexcom_url doit être une URL HTTPS vers un host attendu (pas de check par sous-chaîne).
    dexcom_url = config.get("dexcom_url")
    allowed_hosts = [
        "clarity.dexcom.eu",
        "clarity.dexcom.com",
    ]
    if not url_is_allowed(str(dexcom_url), allowed_hosts, allow_subdomains=True, allowed_schemes=("https",)):
        print_error(
            "La valeur de 'dexcom_url' est invalide ou non autorisée. "
            "Utilisez une URL HTTPS Dexcom Clarity (ex: https://clarity.dexcom.eu)."
        )
        pause_on_error()
        sys.exit(1)

    # Validation de 'days' (optionnel : entier parmi 7/14/30/90, ou null/absent)
    _DAYS_ALLOWED = {7, 14, 30, 90}
    _days_raw = config.get("days")
    if _days_raw is not None:
        if isinstance(_days_raw, str):
            _days_stripped = _days_raw.strip()
            if not _days_stripped.lstrip("-").isdigit():
                print_error(
                    f"Le paramètre 'days' doit être un entier parmi "
                    f"{sorted(_DAYS_ALLOWED)} (ou null/absent). "
                    f"Valeur reçue : {_days_raw!r}."
                )
                pause_on_error()
                sys.exit(1)
            _days_val = int(_days_stripped)
        elif isinstance(_days_raw, int):
            _days_val = _days_raw
        else:
            print_error(
                f"Le paramètre 'days' doit être un entier parmi "
                f"{sorted(_DAYS_ALLOWED)} (ou null/absent). "
                f"Valeur reçue : {_days_raw!r} (type {type(_days_raw).__name__})."
            )
            pause_on_error()
            sys.exit(1)

        if _days_val not in _DAYS_ALLOWED:
            print_error(
                f"Valeur invalide pour 'days' : {_days_val}. "
                f"Valeurs autorisées : {sorted(_DAYS_ALLOWED)}."
            )
            pause_on_error()
            sys.exit(1)

        # Avertissement si date_debut ou date_fin sont aussi définis dans config.yaml.
        # Ce n'est pas une erreur (la chaîne de priorité gère le conflit), mais c'est ambigu.
        if config.get("date_debut") or config.get("date_fin"):
            logger.warning(
                "config.yaml : 'days' et 'date_debut'/'date_fin' sont tous deux définis. "
                "'days' sera prioritaire sur 'date_debut'/'date_fin' dans config.yaml "
                "(chaîne : CLI dates > CLI --days > config days > config dates)."
            )

# --- Fonction de copie minimale du profil Chrome ---
def copy_minimal_chrome_profile(src_base, dst_base):
    """
    Copie uniquement les fichiers et dossiers essentiels du profil Chrome 'Default'
    pour un environnement Selenium minimal.
    """
    INCLUDE = [
        "Preferences",
        "Extensions",
        "Secure Preferences",
        "Local Storage",
        "Extension State"
    ]

    if not os.path.exists(src_base):
        raise FileNotFoundError(f"Profil source introuvable : {src_base}")
    os.makedirs(dst_base, exist_ok=True)

    for item in INCLUDE:
        src_path = os.path.join(src_base, item)
        dst_path = os.path.join(dst_base, item)

        if os.path.exists(src_path):
            try:
                if os.path.isdir(src_path):
                    shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                else:
                    shutil.copy2(src_path, dst_path)
                print(f"✅ Copié : {item}")
            except Exception as e:
                print(f"⚠️ Erreur lors de la copie de {item} : {e}")
        else:
            print(f"❌ Introuvable : {item}")

    print("\n🧪 Environnement de test Chrome minimal créé avec succès.")

# --- Fonction de configuration interactive de config.yaml ---
def interactive_config():
    """Crée config.yaml de façon interactive à partir de config_example.yaml et logge chaque choix."""
    print_info("Configuration initiale : création interactive de 'config.yaml'.")
    logger.info("Début de la configuration interactive : création de config.yaml.")
    with open(CONFIG_EXAMPLE_FILE, "r", encoding="utf-8") as f:
        example_config = yaml.safe_load(f)

    # Forcer l'ordre : chromedriver_log en premier
    keys = list(example_config.keys())
    if "chromedriver_log" in keys:
        keys.insert(0, keys.pop(keys.index("chromedriver_log")))

    chrome_profile_default = os.path.expanduser(
        "~/AppData/Local/Google/Chrome/User Data/Default"
    )
    chrome_user_data_dir_value = None

    user_config = {}
    for key in keys:
        value = example_config[key]
        # Valeur par défaut pour la rétention des logs
        if key == "log_retention_days":
            value = 30
            prompt = (
                f"{Fore.CYAN}Entrez la valeur pour '{key}' [{value}] (0 = conservation illimitée) : {Style.RESET_ALL}"
            )
        elif key == "chromedriver_log":
            prompt = (
                f"{Fore.CYAN}Entrez le chemin complet du fichier log pour ChromeDriver "
                f"[{value}] : {Style.RESET_ALL}"
            )
        else:
            prompt = f"{Fore.CYAN}Entrez la valeur pour '{key}' [{value}] : {Style.RESET_ALL}"
        user_input = input(prompt).strip()

        if key == "rapports":
            if user_input == "":
                final_value = value
            else:
                try:
                    final_value = ast.literal_eval(user_input)
                    if not isinstance(final_value, list):
                        raise ValueError
                except Exception:
                    print_error("Veuillez entrer une liste Python valide, par exemple : [\"Aperçu\", \"AGP\"]")
                    logger.error("Saisie invalide pour 'rapports'.")
                    continue
        else:
            final_value = value if user_input == "" else type(value)(user_input)

        # Vérification spécifique pour chromedriver_log
        if key == "chromedriver_log":
            # On vérifie que ce n'est pas un dossier
            expanded = os.path.expanduser(cast(str, final_value))
            if os.path.isdir(expanded) or expanded.endswith(("/", "\\")):
                print_error("Le chemin du log doit être un fichier, pas un dossier. Exemple : C:/.../clarity_chromedriver.log")
                logger.error("L'utilisateur a saisi un dossier au lieu d'un fichier pour chromedriver_log.")
                # Redemande la saisie
                while True:
                    user_input = input(
                        f"{Fore.CYAN}Veuillez entrer un chemin de fichier log valide pour ChromeDriver : {Style.RESET_ALL}"
                    ).strip()
                    expanded = os.path.expanduser(user_input)
                    if not os.path.isdir(expanded) and not expanded.endswith(("/", "\\")):
                        final_value = user_input
                        break

        user_config[key] = final_value
        logger.info(f"Clé '{key}' définie sur : {final_value!r}")

        # Après saisie de chrome_user_data_dir, vérifier et copier si besoin
        if key == "chrome_user_data_dir":
            chrome_user_data_dir_value = os.path.expanduser(cast(str, final_value))
            if os.path.normpath(chrome_user_data_dir_value) != os.path.normpath(chrome_profile_default):
                try:
                    print_info(f"Copie du profil Chrome par défaut vers {chrome_user_data_dir_value} ...")
                    if not os.path.exists(chrome_user_data_dir_value):
                        copy_minimal_chrome_profile(chrome_profile_default, chrome_user_data_dir_value)
                        print_success("Copie minimale du profil Chrome terminée.")
                        logger.info(f"Profil Chrome minimal copié vers {chrome_user_data_dir_value}")
                    else:
                        print_info("Le dossier cible existe déjà, aucune copie effectuée.")
                        logger.info(f"Le dossier cible {chrome_user_data_dir_value} existe déjà, copie non effectuée.")
                except Exception as e:
                    print_error(f"Erreur lors de la copie du profil Chrome : {e}")
                    logger.error(f"Erreur lors de la copie du profil Chrome : {e}")
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        yaml.dump(user_config, f, allow_unicode=True)
    print_success(f"Le fichier '{CONFIG_FILE}' a été créé avec succès.")
    logger.info("Fichier config.yaml créé avec succès.")

# --- Fonction de configuration interactive pour .env (avec chiffrement) ---
def interactive_env():
    """
    Crée le fichier .env de façon interactive à partir de .env.example.
    Chiffre le contenu avec la clé Fernet stockée dans ENV_DEXCOM_KEY.
    Ne logge jamais les valeurs, seulement les clés renseignées.
    """
    print_info("Configuration initiale : création interactive de '.env'.")
    logger.info("Début de la configuration interactive : création de .env.")

    if not os.path.exists(ENV_EXAMPLE_FILE):
        print_error(f"Impossible de trouver '{ENV_EXAMPLE_FILE}' pour créer '{ENV_FILE}'. Arrêt du script.")
        logger.error(f"Impossible de trouver '{ENV_EXAMPLE_FILE}' pour créer '{ENV_FILE}'.")
        pause_on_error()
        sys.exit(1)

    # Charger les clés de l'exemple
    env_vars = {}
    with open(ENV_EXAMPLE_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.strip().split("=", 1)
                env_vars[k] = v

    # Demander à l'utilisateur le mode de connexion
    print_info("Souhaitez-vous vous connecter avec un numéro de téléphone ? (o/n)")
    use_phone = input("[o/n] : ").strip().lower() == "o"

    keys_to_ask = []
    if use_phone:
        env_vars["DEXCOM_USERNAME"] = ""
        keys_to_ask = ["DEXCOM_COUNTRY_CODE", "DEXCOM_PHONE_NUMBER", "DEXCOM_PASSWORD"]
    else:
        env_vars["DEXCOM_COUNTRY_CODE"] = ""
        env_vars["DEXCOM_PHONE_NUMBER"] = ""
        keys_to_ask = ["DEXCOM_USERNAME", "DEXCOM_PASSWORD"]

    # Demander les valeurs à l'utilisateur
    for key in keys_to_ask:
        prompt = f"{Fore.CYAN}Entrez la valeur pour '{key}' : {Style.RESET_ALL}"
        value = input(prompt).strip()
        env_vars[key] = value
        logger.info(f"L'utilisateur a fourni une valeur pour la clé '{key}'.")

    # Préparer le contenu à chiffrer
    env_content = ""
    for k, v in env_vars.items():
        env_content += f"{k}={v}\n"

    # Récupérer la clé Fernet depuis la variable d'environnement
    env_key = os.environ.get("ENV_DEXCOM_KEY")
    if not env_key:
        print_error("La clé d'encryption ENV_DEXCOM_KEY est absente de l'environnement.")
        logger.error("Impossible de chiffrer le fichier .env : clé absente.")
        pause_on_error()
        sys.exit(1)
    try:
        fernet = Fernet(env_key.encode())
        encrypted_content = fernet.encrypt(env_content.encode())
    except Exception as e:
        print_error(f"Erreur lors du chiffrement du fichier .env : {e}")
        logger.error(f"Erreur lors du chiffrement du fichier .env : {e}")
        pause_on_error()
        sys.exit(1)

    # Écrire le contenu chiffré dans le fichier .env
    with open(ENV_FILE, "wb") as f:
        f.write(encrypted_content)
    print_success(f"Le fichier '{ENV_FILE}' a été créé et chiffré avec succès.")
    logger.info("Fichier .env créé et chiffré avec succès.")

# --- Vérification/création de la clé d'encryption avant la création du .env ---
def ensure_encryption_key():
    """
    Vérifie si la variable d'environnement ENV_DEXCOM_KEY existe et est une clé Fernet valide.
    Logge la présence, l'absence, la validité ou la création de la variable.
    Si la variable est absente ou invalide, génère une nouvelle clé Fernet, propose la commande PowerShell
    pour la créer, puis ferme le script.
    """
    env_var_name = "ENV_DEXCOM_KEY"
    key = os.environ.get(env_var_name)
    if key:
        try:
            Fernet(key.encode())
            logger.info("La variable d'environnement ENV_DEXCOM_KEY existe et est valide.")
            return
        except Exception:
            print_error("La variable d'encryption ENV_DEXCOM_KEY existe mais n'est pas valide.")
            logger.warning("La variable d'encryption ENV_DEXCOM_KEY existe mais n'est pas valide.")
    else:
        logger.info("La variable d'encryption ENV_DEXCOM_KEY est absente.")

    # Génère une nouvelle clé si absente ou invalide
    encryption_key = Fernet.generate_key().decode()
    powershell_cmd = f'[Environment]::SetEnvironmentVariable("{env_var_name}", "{encryption_key}", "User")'
    print_info("\nUne clé d'encryption a été générée pour protéger le fichier .env.")
    print_info("Une fenêtre PowerShell va s'ouvrir.")
    print_info("Collez la commande suivante dans la fenêtre PowerShell, puis appuyez sur Entrée :\n")
    print(Fore.YELLOW + powershell_cmd)
    print_info("\nEnsuite, tapez : Exit puis appuyez sur Entrée pour fermer la fenêtre PowerShell.")
    print_info("L'application va se fermer. Veuillez la relancer pour continuer la configuration.\n")
    logger.info("Création d'une nouvelle clé Fernet et demande à l'utilisateur de créer la variable d'environnement ENV_DEXCOM_KEY.")
    subprocess.Popen("start powershell", shell=True)
    sys.exit(0)

# --- Gestion des credentials Dexcom ---
def get_dexcom_credentials():
    """
    Déchiffre le fichier .env avec la clé Fernet, charge les identifiants Dexcom.
    Retourne None, None, None, None si les informations sont absentes ou incomplètes.
    """
    env_key = os.environ.get("ENV_DEXCOM_KEY")
    if not env_key:
        print_error("La clé d'encryption ENV_DEXCOM_KEY est absente de l'environnement.")
        logger.error("Impossible de déchiffrer le fichier .env : clé absente.")
        pause_on_error()
        sys.exit(1)
    temp_env_path = ENV_FILE + ".tmp"
    try:
        with open(ENV_FILE, "rb") as f:
            encrypted_content = f.read()
        fernet = Fernet(env_key.encode())
        decrypted_content = fernet.decrypt(encrypted_content).decode()
        with open(temp_env_path, "w", encoding="utf-8") as f:
            f.write(decrypted_content)
        load_dotenv(temp_env_path)
    except Exception as e:
        print_error(f"Erreur lors du déchiffrement du fichier .env : {e}")
        logger.error(f"Erreur lors du déchiffrement du fichier .env : {e}")
        pause_on_error()
        sys.exit(1)
    finally:
        if os.path.exists(temp_env_path):
            try:
                os.remove(temp_env_path)
            except Exception:
                pass

    username = os.getenv("DEXCOM_USERNAME")
    password = os.getenv("DEXCOM_PASSWORD")
    country_code = os.getenv("DEXCOM_COUNTRY_CODE")
    phone_number = os.getenv("DEXCOM_PHONE_NUMBER")
    if username and password:
        return username, password, country_code, phone_number
    else:
        logger.warning("Identifiants Dexcom absents ou incomplets dans le fichier .env.")
        return None, None, None, None

# --- Création interactive des fichiers de configuration si absents ---
# Si l'utilisateur demande l'aide, ne rien faire (pour éviter toute interaction ou création de fichier)
HELP_ARGS = {'-h', '--help', '--h'}
if not any(arg in sys.argv for arg in HELP_ARGS):
    if not os.path.exists(ENV_FILE):
        ensure_encryption_key()  # Vérifie ou crée la clé AVANT la config interactive
        print_info("Le fichier '.env' est absent.")
        interactive_env()

    if not os.path.exists(CONFIG_FILE):
        print_info("Le fichier 'config.yaml' est absent.")
        logger.info("Le fichier 'config.yaml' est absent. Lancement de la configuration initiale.")
        if not os.path.exists(CONFIG_EXAMPLE_FILE):
            print_error(f"Impossible de trouver '{CONFIG_EXAMPLE_FILE}' pour créer '{CONFIG_FILE}'. Arrêt du script.")
            logger.error(f"Impossible de trouver '{CONFIG_EXAMPLE_FILE}' pour créer '{CONFIG_FILE}'.")
            pause_on_error()
            sys.exit(1)
        interactive_config()

# --- Chargement de la configuration ---
with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f) or {}
validate_config(config)

def get_param(name, required=True) -> Any:
    """Récupère un paramètre de la configuration, ou arrête le script si absent."""
    value = config.get(name)
    if value is None and required:
        print_error(f"Le paramètre obligatoire '{name}' est manquant dans config.yaml. Arrêt du script.")
        pause_on_error()
        sys.exit(1)
    return value


def _coerce_bool(value: Any, default: bool = False) -> bool:
    """Convertit une valeur arbitraire en booléen (robuste aux chaînes)."""
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "y", "on"}:
            return True
        if normalized in {"0", "false", "no", "n", "off"}:
            return False
    return default

# --- Extraction des paramètres principaux (exportés) ---
if not is_help_requested():
    DOWNLOAD_DIR = normalize_path(cast(str, get_param("download_dir")))
    OUTPUT_DIR = normalize_path(cast(str, get_param("output_dir")))
    CHROME_USER_DATA_DIR = normalize_path(cast(str, get_param("chrome_user_data_dir")))
    CHROMEDRIVER_LOG = normalize_path(cast(str, get_param("chromedriver_log")))
    DEXCOM_URL = cast(str, get_param("dexcom_url"))
    RAPPORTS = cast(list, get_param("rapports"))
    LOG_RETENTION_DAYS = int(config.get("log_retention_days", 30))
    DEBUG = _coerce_bool(config.get("debug"), default=False)
    _days_raw = config.get("days")
    try:
        DAYS = int(_days_raw) if _days_raw is not None else None
    except (ValueError, TypeError):
        DAYS = None  # validate_config a déjà rejeté les valeurs invalides

    DATE_FIN = config.get("date_fin")
    if not DATE_FIN:
        DATE_FIN = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    annee = DATE_FIN[:4]
    DIR_FINAL_BASE = OUTPUT_DIR.replace("AAAA", annee)

    DATE_DEBUT = config.get("date_debut")
    if not DATE_DEBUT:
        date_fin_obj = datetime.strptime(DATE_FIN, "%Y-%m-%d")
        DATE_DEBUT = (date_fin_obj - timedelta(days=14 - 1)).strftime("%Y-%m-%d")

    NOW_STR = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')