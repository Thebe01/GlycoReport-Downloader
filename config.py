#'''////////////////////////////////////////////////////////////////////////////////////////////////////
#'''<summary>
#'''FileName: config.py
#'''FileType: py Source file
#'''
#'''Author : Pierre Théberge
#'''Created On : 2025-08-05
#'''Last Modified On : 2025-08-05
#'''CopyRights : Innovations Performances Technologies inc
#'''Description : Sous-module contenant toutes es variables.
#'''Version : 0.0.0
#'''Modifications :
#'''Version   Date          Description
#'''0.0.0	2025-08-05    Version initiale.
#  </summary>
#'''/////////////////////////////////////////////////////////////////////////////////////////////////////

import os
from datetime import datetime

# Dossier de téléchargement temporaire
DOWNLOAD_DIR = r"C:\Users\thebe\Downloads\Dexcom_download"

# Dossier final pour les rapports
DIR_FINAL_BASE = r"C:\Users\thebe\OneDrive\Documents\Santé\Suivie glycémie et pression"

# Profil Chrome dédié
CHROME_USER_DATA_DIR = r"C:/Users/thebe/AppData/Local/Google/Chrome/User Data/ClarityDownloadProfile"

# URL Dexcom Clarity
DEXCOM_URL = "https://clarity.dexcom.eu/?&locale=fr-CA"

# Fichier log ChromeDriver
CHROMEDRIVER_LOG = os.path.join(os.getcwd(), "chromedriver.log")

# Liste des rapports à traiter
RAPPORTS = ["Aperçu", "Modèles", "Superposition", "Quotidien", "Statistiques", "AGP", "Export"]

# Dates par défaut (à passer en paramètre idéalement)
DATE_DEBUT = "2025-04-28"
DATE_FIN = "2025-05-11"

# Date/heure pour le nommage des logs (optionnel)
NOW_STR = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')