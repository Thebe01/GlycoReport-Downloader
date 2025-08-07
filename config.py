#'''////////////////////////////////////////////////////////////////////////////////////////////////////
#'''<summary>
#'''FileName: config.py
#'''FileType: py Source file
#'''
#'''Author : Pierre Théberge
#'''Created On : 2025-08-05
#'''Last Modified On : 2025-08-06
#'''CopyRights : Innovations Performances Technologies inc
#'''Description : Sous-module contenant toutes les variables.
#'''Version : 0.1.0
#'''Modifications :
#'''Version   Date          Description
#'''0.0.0	2025-08-05    Version initiale.
#'''0.1.0	2025-08-06    Ajout de la gestion des paramètres de configuration via un fichier YAML.
#''' </summary>
#'''/////////////////////////////////////////////////////////////////////////////////////////////////////

import os
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
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}
else:
    logger.warning(f"Fichier de configuration '{CONFIG_PATH}' non trouvé. Les valeurs par défaut seront utilisées.")
    config = {}

# Fonctions d'accès aux paramètres (avec fallback)
def get_param(name, default=None):
    return config.get(name, default)

DOWNLOAD_DIR = get_param("download_dir", "./downloads")
DIR_FINAL_BASE = get_param("output_dir", "./output")
CHROME_USER_DATA_DIR = get_param("chrome_user_data_dir", "./chrome_profile")
DEXCOM_URL = get_param("dexcom_url", "https://clarity.dexcom.eu/?&locale=fr-CA")
CHROMEDRIVER_LOG = get_param("chromedriver_log", "./chromedriver.log")
RAPPORTS = get_param("rapports", ["Aperçu", "Modèles", "Superposition", "Quotidien", "Statistiques", "AGP", "Export"])

# Gestion des dates par défaut : si non spécifiées, la date de fin est hier, la date de début est 14 jours avant
DATE_FIN = get_param("date_fin")
DATE_DEBUT = get_param("date_debut")

if not DATE_FIN:
    DATE_FIN = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
if not DATE_DEBUT:
    date_fin_obj = datetime.strptime(DATE_FIN, "%Y-%m-%d")
    DATE_DEBUT = (date_fin_obj - timedelta(days=14 - 1)).strftime("%Y-%m-%d")

NOW_STR = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')