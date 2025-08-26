#'''////////////////////////////////////////////////////////////////////////////////////////////////////
#'''<summary>
#'''FileName: utils.py
#'''FileType: py Source file
#'''
#'''Author : Pierre Théberge
#'''Created On : 2025-08-05
#'''Last Modified On : 2025-08-25
#'''CopyRights : Innovations Performances Technologies inc
#'''Description : Fonctions utilitaires pour le projet Dexcom Clarity Reports Downloader.
#'''              Connexion internet, overlay, renommage, détection du dernier fichier téléchargé,
#'''              logging détaillé, robustesse accrue pour le renommage, logs JS navigateur.
#'''Version : 0.1.7
#'''Modifications :
#'''Version   Date          Description
#'''0.0.0	2025-08-05    Version initiale.
#'''0.0.1   2025-08-13    Ajout du logging détaillé, robustesse sur le renommage,
#'''                      récupération et logging des erreurs JS du navigateur.
#'''0.0.2   2025-08-13    Centralisation de capture_screenshot, ajout du délai avant capture,
#'''                      préparation pour tests unitaires de toutes les fonctions utilitaires.
#'''0.0.3   2025-08-18    Centralisation de normalize_path, centralisation de capture_screenshot,
#'''                      ajout du délai avant capture, préparation et couverture par tests unitaires.
#'''0.1.6   2025-08-22    Synchronisation des versions dans tous les modules, ajout de version.py, log de la version exécutée.
#'''0.1.7   2025-08-25    Création automatique de config.yaml à partir de config_example.yaml si absent.
#'''                      Gestion interactive des credentials si .env absent (demande à l'utilisateur, non conservé).
#'''</summary>
#'''/////////////////////////////////////////////////////////////////////////////////////////////////////

import os
import urllib.request
import time
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def check_internet(url="https://clarity.dexcom.eu", timeout=5):
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


def get_last_downloaded_nonlog_file(download_dir, logger=None):
    """
    Retourne le dernier fichier téléchargé (hors .log) dans le dossier donné.

    Args:
        download_dir (str): Dossier à analyser.
        logger (Logger, optionnel): Logger pour les messages.

    Returns:
        str or None: Chemin du fichier le plus récent hors .log, ou None si aucun fichier.
    """
    files = [os.path.join(download_dir, f) for f in os.listdir(download_dir)]
    files = [f for f in files if os.path.isfile(f) and not f.lower().endswith('.log')]
    if not files:
        return None
    last_file = max(files, key=os.path.getctime)
    if logger:
        logger.debug(f"[get_last_downloaded_nonlog_file] Dernier fichier non-log trouvé : {last_file}")
    return last_file


def renomme_prefix(prefix, date_fin, logger=None):
    """
    Renomme le préfixe du fichier téléchargé en ajoutant la date de fin.
    Gère les cas où le préfixe ne contient pas 3 parties.
    """
    if logger:
        logger.debug(f"[renomme_prefix] Préfixe reçu : {prefix}")
    parts = prefix.split("_")
    if len(parts) == 3:
        nom, date, numero = parts
        nouveau_prefix = f"{nom}_{date_fin}_{numero}"
    else:
        # Cas inattendu : on ajoute la date à la fin du préfixe
        nouveau_prefix = f"{prefix}_{date_fin}"
        if logger:
            logger.warning(f"Format de préfixe inattendu pour '{prefix}'. Utilisation d'un format alternatif : '{nouveau_prefix}'")
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


def capture_screenshot(driver, logger, step, log_dir, now_str):
    """
    Capture une capture d'écran du navigateur pour le diagnostic.
    """
    try:
        screenshot_path = os.path.join(log_dir, f"screenshot_{step}_{now_str}.png")
        driver.save_screenshot(screenshot_path)
        logger.info(f"Capture d'écran enregistrée : {screenshot_path}")
    except Exception as e:
        logger.warning(f"Impossible de prendre une capture d'écran : {e}")


def normalize_path(path):
    """
    Normalise un chemin en développant ~ et en le rendant absolu.
    """
    return os.path.abspath(os.path.expanduser(path))


def resource_path(relative_path):
    """
    Retourne le chemin absolu vers un fichier de ressource, compatible PyInstaller et exécution normale.
    """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller : les fichiers sont extraits dans _MEIPASS
        return os.path.join(sys._MEIPASS, relative_path)
    # Exécution normale : chemin relatif depuis le dossier courant
    return os.path.join(os.path.abspath("."), relative_path)


def pause_on_error():
    """
    Affiche un message et attend que l'utilisateur appuie sur Entrée avant de fermer la fenêtre du terminal.
    Utile pour garder la console ouverte en cas d'erreur lors d'une exécution en double-cliquant sur l'exécutable.
    """
    try:
        if sys.stdin.isatty():
            input("\nAppuyez sur Entrée pour fermer...")
    except Exception:
        pass