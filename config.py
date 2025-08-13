#'''////////////////////////////////////////////////////////////////////////////////////////////////////
#'''<summary>
#'''FileName: config.py
#'''FileType: py Source file
#'''
#'''Author : Pierre Théberge
#'''Created On : 2025-08-05
#'''Last Modified On : 2025-08-13
#'''CopyRights : Innovations Performances Technologies inc
#'''Description : Centralisation de la configuration du projet Dexcom Clarity Reports Downloader.
#'''              Lecture de tous les paramètres depuis config.yaml, normalisation des chemins,
#'''              gestion des erreurs si un paramètre obligatoire est absent, génération interactive de config.yaml.
#'''Version : 0.1.1
#'''Modifications :
#'''Version   Date          Description
#'''0.0.0	2025-08-05    Version initiale.
#'''0.1.0	2025-08-06    Ajout de la gestion des paramètres de configuration via un fichier YAML.
#'''0.1.1   2025-08-13    Normalisation systématique des chemins, gestion d'erreur sur les paramètres,
#'''                      conservation de tous les paramètres importants (chemins, URL, rapports, etc.).
#''' </summary>
#'''/////////////////////////////////////////////////////////////////////////////////////////////////////

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
import yaml
import logging

# Prépare le logger minimal pour ce module
logger = logging.getLogger("config")
if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO)

# Charger les secrets
load_dotenv()

# Charger la config YAML utilisateur (gérer le cas où le fichier n'existe pas)
CONFIG_PATH = os.environ.get("CLARITY_CONFIG", "config.yaml")
EXAMPLE_CONFIG_PATH = "config_example.yaml"

# Création interactive si config.yaml absent
if not os.path.exists(CONFIG_PATH):
    if os.path.exists(EXAMPLE_CONFIG_PATH):
        with open(EXAMPLE_CONFIG_PATH, "r", encoding="utf-8") as f:
            example_config = yaml.safe_load(f) or {}

        # Demander à l'usager les valeurs pour output_dir et chromedriver_log
        annee = (datetime.today() - timedelta(days=1)).strftime("%Y")
        default_output_dir = f"{os.path.expanduser('~')}/Downloads/Dexcom_download/{annee}"
        default_chromedriver_log = f"{os.path.expanduser('~')}/Downloads/Dexcom_download/clarity_chromedriver.log"

        output_dir = input(f"Répertoire final pour les rapports ? (défaut: {default_output_dir})\n> ").strip() or default_output_dir
        chromedriver_log = input(f"Chemin du log ChromeDriver ? (défaut: {default_chromedriver_log})\n> ").strip() or default_chromedriver_log

        # Mettre à jour la config d'exemple
        example_config["output_dir"] = output_dir
        example_config["chromedriver_log"] = chromedriver_log

        # Sauvegarder le nouveau config.yaml
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            yaml.dump(example_config, f, allow_unicode=True, default_style='"')
        print(f"Fichier de configuration '{CONFIG_PATH}' créé avec vos paramètres.")
    else:
        logger.error(f"Impossible de trouver '{EXAMPLE_CONFIG_PATH}' pour créer '{CONFIG_PATH}'. Arrêt du script.")
        sys.exit(1)

# Charger la config YAML utilisateur
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}
else:
    logger.error(f"Impossible de charger le fichier de configuration '{CONFIG_PATH}'. Arrêt du script.")
    sys.exit(1)

def get_param(name, required=True):
    value = config.get(name)
    if value is None and required:
        logger.error(f"Le paramètre obligatoire '{name}' est manquant dans config.yaml. Arrêt du script.")
        sys.exit(1)
    return value

def normalize_path(path):
    return os.path.abspath(os.path.expanduser(path))

DOWNLOAD_DIR = normalize_path(get_param("download_dir"))
OUTPUT_DIR = normalize_path(get_param("output_dir"))
CHROME_USER_DATA_DIR = normalize_path(get_param("chrome_user_data_dir"))
DEXCOM_URL = get_param("dexcom_url")
CHROMEDRIVER_LOG = normalize_path(get_param("chromedriver_log"))
RAPPORTS = get_param("rapports")

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