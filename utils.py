#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Format d'en-tête standard à respecter pour ce projet.
Voir HEADER_TEMPLATE_PYTHON.md pour les détails.

Module        : utils.py
Type          : Python module
Auteur        : Pierre Théberge
Compagnie     : Innovations, Performances, Technologies inc.
Créé le       : 2025-08-05
Modifié le    : 2026-01-19
Version       : 0.2.15
Copyright     : Pierre Théberge

Description
-----------
Fonctions utilitaires partagées (chemins, téléchargement, nettoyage des logs, helpers Selenium, validation URL).

Modifications
-------------
0.0.0  - 2025-08-05   [N/A]  : Version initiale.
0.0.1  - 2025-08-13   [N/A]  : Ajout du logging détaillé, robustesse sur le renommage,
                               récupération et logging des erreurs JS du navigateur.
0.0.2  - 2025-08-13   [N/A]  : Centralisation de capture_screenshot, ajout du délai avant capture,
                               préparation pour tests unitaires de toutes les fonctions utilitaires.
0.0.3  - 2025-08-18   [N/A]  : Centralisation de normalize_path, centralisation de capture_screenshot,
                               ajout du délai avant capture, préparation et couverture par tests unitaires.
0.1.6  - 2025-08-22   [N/A]  : Synchronisation des versions dans tous les modules, ajout de version.py, log de la version exécutée.
0.1.7  - 2025-08-25   [N/A]  : Création automatique de config.yaml à partir de config_example.yaml si absent.
                               Gestion interactive des credentials si .env absent (demande à l'utilisateur, non conservé).
0.1.8  - 2025-08-27   [N/A]  : Configuration interactive avancée pour config.yaml et .env.
                               Copie minimale du profil Chrome lors de la configuration.
                               Ajout du paramètre log_retention_days (0 = conservation illimitée).
                               Nettoyage automatique des logs selon la rétention.
                               Messages utilisateurs colorés et validation renforcée.
0.1.9  - 2025-08-28   [N/A]  : Vérification interactive de la clé chromedriver_log lors de la création de config.yaml.
                               Empêche la saisie d'un dossier pour le log, exige un chemin de fichier.
                               Correction de la robustesse de la configuration initiale.
0.1.10 - 2025-08-28   [N/A]  : Le ménage des logs s'effectue désormais uniquement après l'activation du logging.
                               Chaque suppression de log est loggée.
0.2.0  - 2025-08-28   [N/A]  : Prise en charge du chiffrement/déchiffrement du fichier .env via config.py.
                               Les identifiants Dexcom sont lus uniquement via get_dexcom_credentials (plus de saisie interactive ici).
                               Sécurisation de la gestion des identifiants et des logs.
0.2.1  - 2025-08-29   [N/A]  : Changement de nom du projet (anciennement Dexcom Clarity Reports Downloader).
0.2.2  - 2025-08-29   [N/A]  : Nettoyage des fonctions CLI, robustesse accrue du help, synchronisation des entêtes.
0.2.3  - 2025-10-14   [ES-12] : Ajout de la colonne Billet dans le bloc des modifications.
0.2.4  - 2025-10-16   [ES-12] : Suppression du paramètre obsolète chromedriver_path (non utilisé depuis v0.2.3).
                               Nettoyage du code : CHROMEDRIVER_PATH retiré de la configuration.
                               Simplification : le répertoire chromedriver-win64/ n'est plus nécessaire.
0.2.4  - 2025-10-16   [ES-12] : Synchronisation de version (aucun changement fonctionnel).
0.2.5  - 2025-10-16   [ES-10] : Ajout de la suppression des captures d'écran (.png) lors du nettoyage des logs.
0.2.6  - 2025-10-21   [ES-7]  : Synchronisation de version (aucun changement fonctionnel).
0.2.7  - 2025-10-27   [ES-16] : Ajout de check_for_502_errors pour détecter les erreurs 502 dans les logs du navigateur.
                               Ajout de wait_for_page_load_with_retry pour gérer les erreurs temporaires avec retry automatique.
                               NOTE: ces helpers ne sont pas présents dans cette version du fichier.
0.2.11 - 2025-12-22   [ES-18] : Exclusion des fichiers .crdownload lors de la recherche du dernier téléchargement.
0.2.12 - 2025-12-22   [ES-3]  : Synchronisation de version.
0.2.13 - 2026-01-19   [ES-19] : Synchronisation de version (aucun changement fonctionnel).
0.2.14 - 2026-01-19   [ES-19] : Ajout d'une attente "vérification humaine" Cloudflare (pause + reprise automatique) basée sur une ancre UI.
0.2.15 - 2026-01-19   [ES-19] : Sécurité : validation d'URL (allowlist host + parsing) et durcissement de la détection Cloudflare.

Paramètres
----------
N/A (helpers importés par le reste du projet).

Exemple
-------
>>> from utils import url_is_allowed
>>> url_is_allowed("https://clarity.dexcom.eu", ["clarity.dexcom.eu"], allow_subdomains=True)
True
"""

import os
import sys
import time
import urllib.request
import urllib.parse
from urllib.parse import urlparse
from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from colorama import Fore  # type: ignore

ONE_DAY_SECONDS = 86400


def _normalize_hostname(hostname: Optional[str]) -> Optional[str]:
    if hostname is None:
        return None
    host = hostname.strip().lower().rstrip(".")
    return host or None


def host_is_allowed(hostname: Optional[str], allowed_hosts: list[str], allow_subdomains: bool = False) -> bool:
    """Retourne True si hostname est autorisé.

    Évite les pièges des checks par sous-chaîne en travaillant sur la valeur
    normalisée du hostname.
    """
    host = _normalize_hostname(hostname)
    if host is None:
        return False

    normalized_allowed = [_normalize_hostname(h) for h in allowed_hosts]
    normalized_allowed = [h for h in normalized_allowed if h]

    if host in normalized_allowed:
        return True

    if allow_subdomains:
        return any(host.endswith("." + allowed) for allowed in normalized_allowed)

    return False


def url_is_allowed(
    url: str,
    allowed_hosts: list[str],
    *,
    allow_subdomains: bool = False,
    allowed_schemes: tuple[str, ...] = ("https",),
) -> bool:
    """Valide une URL en la parsant, puis en vérifiant le host et le schéma.

    Cette approche évite les bypass classiques des checks par sous-chaîne.
    """
    try:
        parsed = urlparse(url)
    except Exception:
        return False

    scheme = (parsed.scheme or "").lower()
    if scheme not in tuple(s.lower() for s in allowed_schemes):
        return False

    return host_is_allowed(parsed.hostname, allowed_hosts, allow_subdomains=allow_subdomains)

def check_internet(url: str = "https://clarity.dexcom.eu", timeout: int = 5) -> bool:
    """Vérifie la connexion internet en tentant d'ouvrir l'URL spécifiée."""
    try:
        parsed = urlparse(url)
        if (parsed.scheme or "").lower() not in {"http", "https"}:
            return False
        if not _normalize_hostname(parsed.hostname):
            return False
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
    """Retourne le dernier fichier téléchargé (hors .log et .crdownload) dans le dossier donné."""
    files = [os.path.join(download_dir, f) for f in os.listdir(download_dir)]
    # On exclut les fichiers .log et les fichiers temporaires de téléchargement .crdownload
    files = [f for f in files if os.path.isfile(f) and not f.lower().endswith('.log') and not f.lower().endswith('.crdownload')]
    if not files:
        return None
    last_file = max(files, key=os.path.getctime)
    if logger:
        logger.debug(f"[get_last_downloaded_nonlog_file] Dernier fichier valide trouvé : {last_file}")
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
        return os.path.join(getattr(sys, '_MEIPASS'), relative_path)
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


def cloudflare_challenge_detecte(driver: WebDriver) -> bool:
    """Détecte (au mieux) la présence d'un challenge Cloudflare dans l'onglet courant.

    Note: on ne tente PAS de contourner la vérification; ce helper sert uniquement à
    décider si l'automatisation doit se mettre en pause pour laisser l'utilisateur agir.
    """
    try:
        url = (driver.current_url or "").lower()
    except Exception:
        url = ""

    if "cdn-cgi" in url or "challenge" in url or "turnstile" in url:
        return True

    # Certains challenges sont rendus via iframe (Turnstile) ou scripts dédiés.
    try:
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
    except Exception:
        iframes = []

    for iframe in iframes:
        try:
            src = (iframe.get_attribute("src") or "").lower()
        except Exception:
            src = ""

        # Analyse l'URL pour vérifier le nom d'hôte plutôt qu'un simple sous-texte.
        try:
            parsed = urllib.parse.urlparse(src)
            host = (parsed.hostname or "").lower()
        except Exception:
            host = ""

        if (
            host
            and (host == "challenges.cloudflare.com" or host.endswith(".challenges.cloudflare.com"))
        ) or "turnstile" in src:
            return True

    try:
        # Fallback léger : recherche de marqueurs courants dans le HTML.
        # (On évite les regex lourdes; page_source peut être volumineux.)
        html = (driver.page_source or "").lower()
        markers = [
            "challenge-platform",
            "cf-chl",
            "checking your browser",
            "cloudflare ray id",
            "turnstile",
        ]
        return any(m in html for m in markers)
    except Exception:
        return False


def attendre_verification_humaine_cloudflare(
    driver: WebDriver,
    logger,
    ancre_locator: tuple,
    log_dir: str,
    now_str: str,
    timeout: int = 600,
    poll_seconds: float = 2.0,
    debug: bool = False,
) -> None:
    """Attend que l'utilisateur termine une éventuelle vérification Cloudflare.

    Fonction pensée pour les challenges multi-étapes: on boucle jusqu'à ce que
    l'"ancre" (un élément Selenium stable) soit disponible.

    Args:
        driver: WebDriver Selenium.
        logger: Logger applicatif.
        ancre_locator: tuple Selenium (By, value) indiquant que la page attendue est prête.
        log_dir: Répertoire de logs (pour screenshots en debug).
        now_str: Timestamp actuel (pour nommage screenshot).
        timeout: Durée max d'attente (secondes).
        poll_seconds: Intervalle entre deux vérifications.
        debug: Active logs/screenshot supplémentaires.
    """
    start = time.time()
    notified = False
    last_debug_shot = 0.0

    while True:
        # 1) Condition de succès: l'ancre est présente/visible.
        try:
            element = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located(ancre_locator)
            )
            try:
                if element.is_displayed():
                    if notified:
                        logger.info("Vérification Cloudflare terminée. Reprise du script.")
                    return
            except Exception:
                # Si on ne peut pas lire is_displayed, la présence suffit.
                if notified:
                    logger.info("Vérification Cloudflare terminée. Reprise du script.")
                return
        except Exception:
            # Les timeouts/interruptions de WebDriverWait sont attendus dans cette boucle de polling:
            # on ignore l'exception et on laisse la boucle continuer avec les contrôles suivants.
            pass

        # 2) Si un challenge est détecté, on laisse l'utilisateur agir.
        challenge = cloudflare_challenge_detecte(driver)
        if challenge and not notified:
            notified = True
            logger.warning(
                "Vérification Cloudflare détectée. Complétez-la manuellement dans Chrome; reprise automatique ensuite."
            )
            if debug:
                capture_screenshot(driver, logger, "cloudflare_detecte", log_dir, now_str)

        # 3) Timeout.
        elapsed = time.time() - start
        if elapsed > timeout:
            msg = (
                "Timeout en attendant la vérification Cloudflare (ou le chargement de la page attendue). "
                "Vous pouvez relancer avec --debug pour diagnostic (screenshots/logs)."
            )
            logger.error(msg)
            if debug:
                capture_screenshot(driver, logger, "cloudflare_timeout", log_dir, now_str)
            raise TimeoutError(msg)

        # 4) Debug périodique (évite de spammer).
        if debug and notified:
            if time.time() - last_debug_shot >= 30:
                last_debug_shot = time.time()
                logger.debug(f"En attente Cloudflare... url={getattr(driver, 'current_url', '')}")

        time.sleep(poll_seconds)