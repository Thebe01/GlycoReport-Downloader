#'''////////////////////////////////////////////////////////////////////////////////////////////////////
#'''<summary>
#'''FileName: utils.py
#'''FileType: py Source file
#'''
#'''Author : Pierre Théberge
#'''Created On : 2025-08-05
#'''Last Modified On : 2025-10-21
#'''CopyRights : Pierre Théberge
#'''Description : Fonctions utilitaires pour le projet GlycoReport-Downloader.
#'''              Connexion internet, overlay, renommage, détection du dernier fichier téléchargé,
#'''              logging détaillé, robustesse accrue pour le renommage, logs JS navigateur.
#'''Version : 0.2.6
#'''Modifications :
#'''Version   Date         Billet   Description
#'''0.0.0	2025-08-05              Version initiale.
#'''0.0.1   2025-08-13              Ajout du logging détaillé, robustesse sur le renommage,
#'''                                    récupération et logging des erreurs JS du navigateur.
#'''0.0.2   2025-08-13              Centralisation de capture_screenshot, ajout du délai avant capture,
#'''                                    préparation pour tests unitaires de toutes les fonctions utilitaires.
#'''0.0.3   2025-08-18              Centralisation de normalize_path, centralisation de capture_screenshot,
#'''                                    ajout du délai avant capture, préparation et couverture par tests unitaires.
#'''0.1.6   2025-08-22              Synchronisation des versions dans tous les modules, ajout de version.py, log de la version exécutée.
#'''0.1.7   2025-08-25              Création automatique de config.yaml à partir de config_example.yaml si absent.
#'''                                    Gestion interactive des credentials si .env absent (demande à l'utilisateur, non conservé).
#'''0.1.8   2025-08-27              Configuration interactive avancée pour config.yaml et .env.
#'''                                    Copie minimale du profil Chrome lors de la configuration.
#'''                                    Ajout du paramètre log_retention_days (0 = conservation illimitée).
#'''                                    Nettoyage automatique des logs selon la rétention.
#'''                                    Messages utilisateurs colorés et validation renforcée.
#'''0.1.9   2025-08-28              Vérification interactive de la clé chromedriver_log lors de la création de config.yaml.
#'''                                    Empêche la saisie d'un dossier pour le log, exige un chemin de fichier.
#'''                                    Correction de la robustesse de la configuration initiale.
#'''0.1.10  2025-08-28              Le ménage des logs s'effectue désormais uniquement après l'activation du logging.
#'''                                    Chaque suppression de log est loggée.
#'''0.2.0   2025-08-28              Prise en charge du chiffrement/déchiffrement du fichier .env via config.py.
#'''                                    Les identifiants Dexcom sont lus uniquement via get_dexcom_credentials (plus de saisie interactive ici).
#'''                                    Sécurisation de la gestion des identifiants et des logs.
#'''0.2.1   2025-08-29              Changement de nom du projet (anciennement Dexcom Clarity Reports Downloader).
#'''0.2.2   2025-08-29              Nettoyage des fonctions CLI, robustesse accrue du help, synchronisation des entêtes.
#'''0.2.3   2025-10-14    ES-12     Ajout de la colonne Billet dans le bloc des modifications.
#'''0.2.4   2025-10-16    ES-12     Suppression du paramètre obsolète chromedriver_path (non utilisé depuis v0.2.3).
#'''                      ES-12     Nettoyage du code : CHROMEDRIVER_PATH retiré de la configuration.
#'''                      ES-12     Simplification : le répertoire chromedriver-win64/ n'est plus nécessaire.
#'''0.2.4    2025-10-16    ES-12    Synchronisation de version (aucun changement fonctionnel).
#'''0.2.5    2025-10-16    ES-10    Ajout de la suppression des captures d'écran (.png) lors du nettoyage des logs.
#'''0.2.6    2025-10-21    ES-7     Synchronisation de version (aucun changement fonctionnel).
#'''0.2.7    2025-10-27    ES-16    Ajout de check_for_502_errors pour détecter les erreurs 502 dans les logs du navigateur.
#'''                       ES-16    Ajout de wait_for_page_load_with_retry pour gérer les erreurs temporaires avec retry automatique.
#'''</summary>
#'''/////////////////////////////////////////////////////////////////////////////////////////////////////

import os
import sys
import time
import urllib.request
from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from colorama import Fore

ONE_DAY_SECONDS = 86400

def check_internet(url: str = "https://clarity.dexcom.eu", timeout: int = 5) -> bool:
    """Vérifie la connexion internet en tentant d'ouvrir l'URL spécifiée."""
    try:
        urllib.request.urlopen(url, timeout=timeout)
        return True
    except Exception:
        return False

def attendre_disparition_overlay(driver: WebDriver, timeout: int = 60, logger=None, debug: bool = False) -> None:
    """Attend la disparition des overlays, loaders ou spinners courants."""
    try:
        WebDriverWait(driver, timeout).until_not(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".overlay, .loader, .spinner"))
        )
    except Exception as e:
        if logger:
            logger.debug(f"Aucun overlay/loader détecté ou disparition non confirmée : {e}", exc_info=debug)

def get_last_downloaded_file(download_dir: str, logger=None) -> Optional[str]:
    """Retourne le chemin du fichier le plus récemment téléchargé dans le dossier donné."""
    files = [os.path.join(download_dir, f) for f in os.listdir(download_dir)]
    files = [f for f in files if os.path.isfile(f)]
    if not files:
        if logger:
            logger.warning("Aucun fichier téléchargé trouvé dans le dossier.")
        return None
    if logger:
        logger.debug(f"Fichiers trouvés : {files}")
    return max(files, key=os.path.getctime)

def get_last_downloaded_nonlog_file(download_dir: str, logger=None) -> Optional[str]:
    """Retourne le dernier fichier téléchargé (hors .log) dans le dossier donné."""
    files = [os.path.join(download_dir, f) for f in os.listdir(download_dir)]
    files = [f for f in files if os.path.isfile(f) and not f.lower().endswith('.log')]
    if not files:
        return None
    last_file = max(files, key=os.path.getctime)
    if logger:
        logger.debug(f"[get_last_downloaded_nonlog_file] Dernier fichier non-log trouvé : {last_file}")
    return last_file

def renomme_prefix(prefix: str, date_fin: str, logger=None) -> str:
    """Renomme le préfixe du fichier téléchargé en ajoutant la date de fin."""
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

def attendre_nouveau_bouton_telecharger(driver: WebDriver, bouton_avant: WebElement, timeout: int = 30) -> None:
    """Attend que le bouton Télécharger soit recréé dans le DOM (nouvelle instance)."""
    def bouton_a_change(drv):
        try:
            nouveau_bouton = drv.find_element(By.XPATH, "//button[.//img[@alt='Télécharger']]")
            return nouveau_bouton and nouveau_bouton != bouton_avant
        except Exception:
            return False
    WebDriverWait(driver, timeout).until(bouton_a_change)

def capture_screenshot(driver: WebDriver, logger, step: str, log_dir: str, now_str: str) -> None:
    """Capture une capture d'écran du navigateur pour le diagnostic."""
    try:
        screenshot_path = os.path.join(log_dir, f"screenshot_{step}_{now_str}.png")
        driver.save_screenshot(screenshot_path)
        logger.info(f"Capture d'écran enregistrée : {screenshot_path}")
    except Exception as e:
        logger.warning(f"Impossible de prendre une capture d'écran : {e}")

def normalize_path(path: str) -> str:
    """Normalise un chemin en développant ~ et en le rendant absolu."""
    return os.path.abspath(os.path.expanduser(path))

def resource_path(relative_path: str) -> str:
    """Retourne le chemin absolu vers un fichier de ressource, compatible PyInstaller et exécution normale."""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller : les fichiers sont extraits dans _MEIPASS
        return os.path.join(sys._MEIPASS, relative_path)
    # Exécution normale : chemin relatif depuis le dossier courant
    return os.path.join(os.path.abspath("."), relative_path)

def pause_on_error() -> None:
    """Affiche un message et attend que l'utilisateur appuie sur Entrée avant de fermer la fenêtre du terminal."""
    try:
        if sys.stdin.isatty():
            input("\nAppuyez sur Entrée pour fermer...")
    except Exception:
        pass

def cleanup_logs(log_dir, retention_days, logger=None):
    """
    Supprime les fichiers logs (.log) et captures d'écran (.png) plus vieux que retention_days dans le dossier log_dir.
    Si retention_days vaut 0, aucun ménage n'est effectué (conservation illimitée).
    Logge les suppressions si un logger est fourni.
    """
 
    if retention_days == 0:
        msg = "Aucun ménage des logs et captures d'écran n'est effectué (conservation illimitée)."
        print(Fore.CYAN + msg)
        if logger:
            logger.info(msg)
        return
    now = time.time()
    retention_seconds = retention_days * 86400
    if not os.path.isdir(log_dir):
        msg = f"Le dossier de logs '{log_dir}' n'existe pas."
        print(Fore.YELLOW + msg)
        if logger:
            logger.warning(msg)
        return
    for filename in os.listdir(log_dir):
        if filename.endswith(".log") or filename.endswith(".png"):
            filepath = os.path.join(log_dir, filename)
            try:
                if os.stat(filepath).st_mtime < now - retention_seconds:
                    os.remove(filepath)
                    file_type = "Log" if filename.endswith(".log") else "Capture d'écran"
                    msg = f"{file_type} supprimé(e) : {filepath}"
                    print(Fore.GREEN + msg)
                    if logger:
                        logger.info(msg)
            except Exception as e:
                msg = f"Erreur lors de la suppression de {filepath} : {e}"
                print(Fore.RED + msg)
                if logger:
                    logger.error(msg)