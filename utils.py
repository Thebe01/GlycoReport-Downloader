#'''////////////////////////////////////////////////////////////////////////////////////////////////////
#'''<summary>
#'''FileName: utils.py
#'''FileType: py Source file
#'''
#'''Author : Pierre Théberge
#'''Created On : 2025-08-05
#'''Last Modified On : 2025-08-05
#'''CopyRights : Innovations Performances Technologies inc
#'''Description : Sous-module contenant des fonctions utilitaires pour la gestion des téléchargements, 
#                   des overlays et des fichiers.
#'''Version : 0.0.0
#'''Modifications :
#'''Version   Date          Description
#'''0.0.0	2025-08-05    Version initiale.
#  </summary>
#'''/////////////////////////////////////////////////////////////////////////////////////////////////////

import os
import urllib.request
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def check_internet(url="https://www.google.com", timeout=5):
    """
    Vérifie la connexion internet en tentant d'ouvrir l'URL spécifiée.

    Args:
        url (str): URL à tester.
        timeout (int): Durée maximale d'attente en secondes.

    Returns:
        bool: True si la connexion fonctionne, False sinon.
    """
    try:
        urllib.request.urlopen(url, timeout=timeout)
        return True
    except Exception:
        return False


def attendre_disparition_overlay(driver, timeout=60, logger=None, debug=False):
    """
    Attend la disparition des overlays, loaders ou spinners courants.

    Args:
        driver (WebDriver): Instance Selenium.
        timeout (int): Durée maximale d'attente en secondes.
        logger (Logger, optionnel): Logger pour les messages.
        debug (bool): Mode debug.

    Returns:
        None
    """
    try:
        WebDriverWait(driver, timeout).until_not(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".overlay, .loader, .spinner"))
        )
    except Exception as e:
        if logger:
            logger.debug(f"Aucun overlay/loader détecté ou disparition non confirmée : {e}", exc_info=debug)


def get_last_downloaded_file(download_dir, logger=None):
    """
    Retourne le chemin du fichier le plus récemment téléchargé dans le dossier donné.

    Args:
        download_dir (str): Dossier à analyser.
        logger (Logger, optionnel): Logger pour les messages.

    Returns:
        str or None: Chemin du fichier le plus récent, ou None si aucun fichier.
    """
    files = [os.path.join(download_dir, f) for f in os.listdir(download_dir)]
    files = [f for f in files if os.path.isfile(f)]
    if not files:
        if logger:
            logger.warning("Aucun fichier téléchargé trouvé dans le dossier.")
        return None
    if logger:
        logger.debug(f"Fichiers trouvés : {files}")
    return max(files, key=os.path.getctime)


def get_last_downloaded_nonlog_file(download_dir):
    """
    Retourne le dernier fichier téléchargé (hors .log) dans le dossier donné.

    Args:
        download_dir (str): Dossier à analyser.

    Returns:
        str or None: Chemin du fichier le plus récent hors .log, ou None si aucun fichier.
    """
    files = [os.path.join(download_dir, f) for f in os.listdir(download_dir)]
    files = [f for f in files if os.path.isfile(f) and not f.lower().endswith('.log')]
    if not files:
        return None
    return max(files, key=os.path.getctime)


def renomme_prefix(prefix, date_fin, logger=None):
    """
    Renomme le préfixe du fichier téléchargé en ajoutant la date de fin.

    Args:
        prefix (str): Préfixe original du fichier.
        date_fin (str): Date à ajouter.
        logger (Logger, optionnel): Logger pour les messages.

    Returns:
        str: Nouveau préfixe.
    """
    nom, date, numero = prefix.split("_")
    nouveau_prefix = nom + "_" + date_fin + "_" + numero
    if logger:
        logger.debug(f"Nouveau préfix : {nouveau_prefix}")
    return nouveau_prefix


def attendre_nouveau_bouton_telecharger(driver, bouton_avant, timeout=30):
    """
    Attend que le bouton Télécharger soit recréé dans le DOM (nouvelle instance).

    Args:
        driver (WebDriver): Instance du navigateur Selenium.
        bouton_avant (WebElement): L'ancien bouton à comparer.
        timeout (int): Durée maximale d'attente en secondes.

    Returns:
        None

    Raises:
        TimeoutException: Si le nouveau bouton n'apparaît pas dans le délai imparti.
    """
    def bouton_a_change(drv):
        try:
            nouveau_bouton = drv.find_element(By.XPATH, "//button[.//img[@alt='Télécharger']]")
            return nouveau_bouton and nouveau_bouton != bouton_avant
        except Exception:
            return False

    WebDriverWait(driver, timeout).until(bouton_a_change)