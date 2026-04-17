#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Format d'en-tête standard à respecter pour ce projet.
Voir .github/HEADER_TEMPLATE_PYTHON.md pour les détails.

Module        : rapports.py
Type          : Python module
Auteur        : Pierre Théberge
Compagnie     : Innovations, Performances, Technologies inc.
Créé le       : 2025-08-05
Modifié le    : 2026-04-17
Version       : 0.5.7
Copyright     : Pierre Théberge

Description
-----------
Traitement et gestion des rapports Dexcom Clarity (sélection, sous-rapports, téléchargement, renommage/déplacement).

Modifications
-------------
0.0.0  - 2025-08-05   [N/A]  : Version initiale.
0.0.1  - 2025-08-13   [N/A]  : Logging JS navigateur, robustesse accrue sur la gestion des fichiers,
                               utilisation systématique des chemins centralisés.
0.0.2  - 2025-08-13   [N/A]  : Utilisation de capture_screenshot centralisée (utils.py) avec délai,
                               ajout de logs pour le diagnostic.
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
0.2.3  - 2025-10-14   [ES-11] : Remplacement d'une version spécifique de chromedriver par ChromeDriverManager qui charge toujours la version courante.
                               Modification du xpath pour le rapport statistiques horaires pour corriger l'erreur d'accès (indépendant de la langue de l'utilisateur).
                               Ajout de la colonne Billet dans le bloc des modifications.
0.2.4  - 2025-10-16   [ES-12] : Suppression du paramètre obsolète chromedriver_path (non utilisé depuis v0.2.3).
                               Nettoyage du code : CHROMEDRIVER_PATH retiré de la configuration.
                               Simplification : le répertoire chromedriver-win64/ n'est plus nécessaire.
0.2.4  - 2025-10-16   [ES-12] : Synchronisation de version (aucun changement fonctionnel).
0.2.5  - 2025-10-16   [ES-10] : Synchronisation de version (aucun changement fonctionnel).
0.2.6  - 2025-10-21   [ES-7]  : Synchronisation de version (aucun changement fonctionnel).
0.2.7  - 2025-10-27   [ES-16] : Refactorisation de selection_rapport avec gestion des erreurs 502 et retry.
                               Ajout de select_rapport_with_retry pour gérer les erreurs temporaires.
                               Ajout de traiter_rapport pour dispatcher vers les fonctions de traitement.
                               Suivi global des rapports échoués avec résumé final.
                               NOTE: les helpers *with_retry ne sont pas présents dans cette version du fichier.
0.2.8  - 2025-11-28   [ES-16] : Correction du sélecteur pour le bouton 'Exporter' de la fenêtre modale.
                               Utilisation de l'attribut 'data-test-export-dialog-export-button' pour plus de robustesse.
0.2.9  - 2025-11-28   [ES-16] : Correction du sélecteur pour le bouton 'Fermer' de la fenêtre d'export CSV.
                               Suppression de la classe 'btn-3d' obsolète dans le sélecteur XPath.
0.2.11 - 2025-12-22   [ES-18] : Augmentation du timeout de fermeture de fenêtre (30s -> 60s) et gestion d'erreur non bloquante.
0.2.12 - 2025-12-22   [ES-3]  : Synchronisation de version.
0.2.13 - 2026-01-19   [ES-19] : Synchronisation de version (aucun changement fonctionnel).
0.2.14 - 2026-01-19   [ES-19] : Synchronisation de version (aucun changement fonctionnel).
0.2.15 - 2026-01-19   [ES-19] : Nettoyage mineur : suppression d'un pass redondant (aucun changement fonctionnel).
0.2.16 - 2026-01-20   [ES-19] : Synchronisation de version (aucun changement fonctionnel).
0.2.17 - 2026-01-20   [ES-19] : Synchronisation de version (aucun changement fonctionnel).
0.2.18 - 2026-01-20   [ES-19] : Synchronisation de version (aucun changement fonctionnel).
0.3.2  - 2026-02-02   [ES-19] : Filtrage des fichiers téléchargés par extension.
0.3.3  - 2026-02-02   [ES-19] : Normalisation des extensions attendues (téléchargements).
0.3.4  - 2026-02-12   [ES-3]  : Correction du téléchargement des sous-rapports Comparer.
0.3.5  - 2026-02-12   [ES-3]  : Stabilisation des sous-rapports Comparer.
0.3.6  - 2026-02-12   [ES-3]  : Stabilisation renforcée des sous-rapports Comparer.
0.3.7  - 2026-02-12   [ES-3]  : Attente contenu graphique + délai génération PDF Comparer.
0.3.8  - 2026-02-12   [ES-3]  : Fermeture/réouverture modale Comparer entre sous-rapports.
0.3.9  - 2026-02-12   [ES-3]  : Navigation /overview et /reports avec dates pour Comparer.
0.3.10 - 2026-02-12   [ES-3]  : Retry clics Comparer et navigation overview->reports.
0.3.11 - 2026-02-12   [ES-3]  : Navigation URL base /i pour Comparer.
0.3.12 - 2026-02-12   [ES-3]  : Acces direct /compare/overlay et /compare/daily.
0.3.13 - 2026-02-12   [ES-3]  : Comparer: telecharger Tendances seulement (bug Dexcom).
0.3.14 - 2026-02-13   [ES-11] : Ajout suffixe de periode dans les noms de fichiers.
0.3.15 - 2026-02-26   [ES-6]  : Harmonisation des XPath pour reduire la dependance a la langue du navigateur.
0.3.16 - 2026-03-19   [ES-15] : Synchronisation de version et robustesse fallback URL pour Statistiques.
0.3.17 - 2026-03-23   [ES-14] : Detection de perte reseau pendant le traitement des rapports,
                               tentative de reconnexion et arret du traitement en cas d'echec.
                               Dispatch explicite des rapports conserve avec retry reseau par rapport.
0.3.18 - 2026-03-25   [ES-14] : Gestion reseau harmonisee dans traitement_export_csv
                               (clic Export modal + fermeture modale).
0.3.19 - 2026-03-25   [ES-14] : Harmonisation de la gestion reseau dans selection_rapport et propagation explicite des erreurs reseau.
0.5.1  - 2026-04-15   [ES-22] : Documentation de get_period_suffix (docstring complet : Args, Returns, Description).
0.5.2  - 2026-04-15   [ES-25] : Synchronisation de version (aucun changement fonctionnel).
0.5.3  - 2026-04-15   [ES-25] : Synchronisation de version (aucun changement fonctionnel).
0.5.4  - 2026-04-15   [CR]    : Synchronisation de version (aucun changement fonctionnel).
0.5.5  - 2026-04-15   [CR]    : Synchronisation de version (aucun changement fonctionnel).
0.5.6  - 2026-04-16   [ES-25] : Synchronisation de version (aucun changement fonctionnel).
0.5.7  - 2026-04-17   [ES-25] : Correctif xpath_fermer dans traitement_export_csv : ancrage dans
                               le composant <export-dialog> (suppression des conditions data-test
                               obsoletes). Attente explicite de disparition du composant
                               <export-dialog> apres le clic Fermer.

Paramètres
----------
N/A (module importé par l'application).

Exemple
-------
>>> python GlycoDownload.py --rapports "AGP" "Export"
"""

import os
import time
import glob
import locale
import logging
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import (
    attendre_disparition_overlay,
    get_last_downloaded_report_file,
    renomme_prefix,
    check_internet,
    capture_screenshot,
)


class NetworkRecoveryRetry(Exception):
    """Signale qu'une reconnexion réseau a réussi et qu'un retry du rapport est requis."""


class NetworkRecoveryFailedError(RuntimeError):
    """Signale qu'une perte réseau persistante impose l'arrêt du traitement."""


def _recover_network_or_fail(logger, contexte: str, attempts: int = 3, delay_seconds: int = 10) -> None:
    """Tente de rétablir la connexion internet, sinon lève une erreur fatale."""
    if check_internet():
        return

    logger.warning(
        "Perte de connexion internet détectée (%s). Tentative de reconnexion (%d essais).",
        contexte,
        attempts,
    )
    for attempt in range(1, attempts + 1):
        logger.warning("Vérification réseau %d/%d dans %ds...", attempt, attempts, delay_seconds)
        time.sleep(delay_seconds)
        if check_internet():
            logger.info("Connexion internet rétablie (%s).", contexte)
            return

    raise NetworkRecoveryFailedError(
        f"Perte de connexion internet persistante ({contexte}) après {attempts} essais de reconnexion."
    )


def _handle_network_loss(logger, contexte: str, original_exception: Exception) -> None:
    """Détecte une perte réseau, tente la reconnexion et force un retry du rapport courant."""
    if not check_internet():
        _recover_network_or_fail(logger, contexte)
        raise NetworkRecoveryRetry(
            f"Connexion internet rétablie après incident durant {contexte}. Retry du rapport en cours."
        ) from original_exception


def _get_log_dir_from_logger(logger) -> str:
    """Retourne le dossier de logs à partir d'un handler fichier du logger."""
    try:
        for handler in getattr(logger, "handlers", []):
            base_filename = getattr(handler, "baseFilename", None)
            if base_filename:
                return os.path.dirname(base_filename) or "."
    except Exception:
        pass
    return "."


def _get_report_xpath_candidates(nom_rapport: str) -> list[str]:
    """Retourne des XPath candidats (du plus stable au fallback texte) pour un rapport."""
    candidates_by_report = {
        "Aperçu": [
            "//a[contains(@href, '/overview') and not(contains(@href, '/compare/'))]",
            "//button[.//a[contains(@href, '/overview') and not(contains(@href, '/compare/'))]]",
        ],
        "Modèles": [
            "//a[contains(@href, '/patterns')]",
            "//button[.//a[contains(@href, '/patterns')]]",
        ],
        "Superposition": [
            "//a[contains(@href, '/overlay') and not(contains(@href, '/compare/'))]",
            "//button[.//a[contains(@href, '/overlay') and not(contains(@href, '/compare/'))]]",
        ],
        "Quotidien": [
            "//a[contains(@href, '/daily') and not(contains(@href, '/statistics/')) and not(contains(@href, '/compare/'))]",
            "//button[.//a[contains(@href, '/daily') and not(contains(@href, '/statistics/')) and not(contains(@href, '/compare/'))]]",
        ],
        "Comparer": [
            "//a[contains(@href, '/compare')]",
            "//button[.//a[contains(@href, '/compare')]]",
        ],
        "Statistiques": [
            "//a[contains(@href, '/statistics')]",
            "//button[.//a[contains(@href, '/statistics')]]",
        ],
        "AGP": [
            "//a[contains(@href, '/agp')]",
            "//button[.//a[contains(@href, '/agp')]]",
        ],
    }
    candidates: list[str] = list(candidates_by_report.get(nom_rapport, []))

    # Fallback historique (texte) pour conserver la compatibilité si la structure DOM diffère.
    candidates.append(f"//button[normalize-space()='{nom_rapport}']")
    return candidates


def _find_clickable_with_xpath_candidates(driver, xpath_candidates: list[str], timeout: int = 30):
    """Cherche un élément cliquable via plusieurs XPath candidats."""
    last_error = None
    nb_candidates = max(1, len(xpath_candidates))
    if nb_candidates == 1:
        # Un seul XPath: on utilise tout le budget timeout.
        per_try_timeout = max(3, timeout)
    else:
        # Plusieurs XPath: on répartit le budget et on borne chaque essai.
        per_try_timeout = max(3, min(10, timeout // nb_candidates))
    for xpath in xpath_candidates:
        try:
            return WebDriverWait(driver, per_try_timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
        except Exception as exc:
            last_error = exc
            continue
    if last_error:
        raise last_error
    raise RuntimeError("Aucun XPath candidat fourni.")


def _is_report_active(driver, nom_rapport: str, timeout: int = 8) -> bool:
    """Vérifie que l'onglet du rapport ciblé est actif dans la barre des rapports."""
    active_xpath = (
        "//button[@data-testid='mdc-list-button' and @tabindex='0' "
        f"and .//span[normalize-space()='{nom_rapport}']]"
    )
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, active_xpath))
        )
        return True
    except Exception:
        return False

def wait_for_csv_download(DOWNLOAD_DIR, timeout=120):
    """
    Attend qu'un fichier .csv apparaisse dans le dossier et qu'il n'y ait plus de .crdownload.

    Args:
        DOWNLOAD_DIR (str): Chemin du dossier de téléchargement.
        timeout (int): Durée maximale d'attente en secondes.

    Returns:
        bool: True si le fichier est téléchargé, False sinon.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        files = [f for f in os.listdir(DOWNLOAD_DIR) if f.lower().endswith('.csv')]
        if files:
            crdownloads = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith('.crdownload')]
            if not crdownloads:
                return True
        time.sleep(1)
    return False

def get_period_suffix(date_debut, date_fin, args, logger=None):
    """
    Calcule un suffixe de période à ajouter au nom de fichier (par exemple "14j" ou "14d").

    Args:
        date_debut (str): Date de début au format ``YYYY-MM-DD``.
        date_fin (str): Date de fin au format ``YYYY-MM-DD``.
        args (argparse.Namespace, optional): Arguments de la ligne de commande. Si
            ``args.days`` est défini et strictement positif, cette valeur est utilisée en
            priorité pour le nombre de jours de la période.
        logger (logging.Logger, optional): Logger utilisé pour émettre des messages de
            debug en cas d'erreur de calcul (par exemple, format de date invalide).

    Returns:
        str or None: Le suffixe de période, composé du nombre de jours suivi de l'unité
        (``"j"`` pour les locales françaises, ``"d"`` sinon), par exemple ``"14j"`` ou
        ``"14d"``. Retourne ``None`` si la période ne peut pas être déterminée (dates
        manquantes ou invalides, nombre de jours nul ou négatif, ou erreur de parsing).

    Description:
        Si ``args.days`` est défini et valide, il est utilisé pour déterminer le nombre
        de jours. Sinon, la fonction calcule la période à partir de ``date_debut`` et
        ``date_fin`` (différence en jours + 1 pour inclure les deux bornes). L'unité
        renvoyée dépend de la locale système : ``"j"`` pour une locale commençant par
        ``"fr"`` (français), ou ``"d"`` pour les autres locales.
    """
    if not date_debut or not date_fin:
        return None

    if args is not None and getattr(args, "days", None):
        jours = args.days
    else:
        try:
            debut = datetime.strptime(date_debut, "%Y-%m-%d")
            fin = datetime.strptime(date_fin, "%Y-%m-%d")
            jours = (fin - debut).days + 1
        except Exception as exc:
            if logger:
                logger.debug("Impossible de calculer la periode: %s", exc)
            return None

    if jours is None or jours <= 0:
        return None

    langue = locale.getdefaultlocale()[0] if locale.getdefaultlocale() else None
    unite = "j" if langue and langue.lower().startswith("fr") else "d"
    return f"{jours}{unite}"


def deplace_et_renomme_rapport(nom_rapport, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT=None, args=None, driver=None, log_dir=None, now_str=None):
    """
    Déplace et renomme le rapport téléchargé dans le dossier final.

    Args:
        nom_rapport (str): Nom du rapport.
        logger (Logger): Logger pour les messages.
        DOWNLOAD_DIR (str): Dossier de téléchargement.
        DIR_FINAL_BASE (str): Dossier final de destination.
        DATE_FIN (str): Date de fin pour le nommage.
    """
    logger.info(f"Deplacement et renommage du rapport {nom_rapport}")
    annee = DATE_FIN[:4]
    dir_final = os.path.join(DIR_FINAL_BASE, annee)
    if not os.path.exists(dir_final):
        os.makedirs(dir_final)
        logger.debug(f"Répertoire créé : {dir_final}")

    allowed_exts = {".csv"} if nom_rapport == "Export" else {".pdf"}
    chemin_fichier_telecharge = get_last_downloaded_report_file(
        DOWNLOAD_DIR,
        allowed_extensions=allowed_exts,
        logger=logger,
    )
    if chemin_fichier_telecharge:
        nom_fichier_telecharge = os.path.basename(chemin_fichier_telecharge)
        prefix, suffix = os.path.splitext(nom_fichier_telecharge)
        suffix = suffix[1:] if suffix.startswith('.') else suffix
        period_suffix = get_period_suffix(DATE_DEBUT, DATE_FIN, args, logger=logger)
        suffix_periode = f"-{period_suffix}" if period_suffix else ""

        if nom_rapport == "Export":
            nouveau_nom_fichier = f"Clarity_Exporter_Théberge_Pierre_{DATE_FIN}{suffix_periode}.csv"
            destination = os.path.join(dir_final, nouveau_nom_fichier)
            logger.debug(f"Renommage Export : {chemin_fichier_telecharge} -> {destination}")
            try:
                os.replace(chemin_fichier_telecharge, destination)
                logger.info(f"Le fichier Export {chemin_fichier_telecharge} a été renommé en {destination}")
            except Exception as e:
                logger.error(f"Erreur lors du renommage du fichier Export : {e}")
        else:
            nouveau_prefix = renomme_prefix(prefix, DATE_FIN, logger=logger)
            nouveau_nom_fichier = nouveau_prefix + "_" + nom_rapport + suffix_periode + "." + suffix
            destination = os.path.join(dir_final, nouveau_nom_fichier)
            logger.debug(f"Renommage du fichier : {chemin_fichier_telecharge} -> {destination}")
            try:
                os.replace(chemin_fichier_telecharge, destination)
                logger.info(f"Le fichier {chemin_fichier_telecharge} a été renommé en {destination}")
            except Exception as e:
                logger.error(f"Erreur lors du renommage du fichier : {e}")
    else:
        logger.error("Aucun fichier téléchargé trouvé (pdf/csv).")
        if driver is not None and log_dir is not None and now_str is not None:
            time.sleep(2)
            capture_screenshot(driver, logger, "deplace_et_renomme_rapport_error", log_dir, now_str)

    # Log des erreurs JS du navigateur si driver est fourni
    if driver is not None:
        try:
            for entry in driver.get_log('browser'):
                if entry.get('level') == 'SEVERE':
                    logger.error(f"JS Browser Error: {entry}")
                else:
                    logger.debug(f"JS Browser Log: {entry}")
        except Exception as e:
            logger.warning(f"Impossible de récupérer les logs du navigateur : {e}")

def telechargement_rapport(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args):
    """
    Télécharge le rapport spécifié et le déplace dans le dossier final.

    Args:
        nom_rapport (str): Nom du rapport.
        driver (WebDriver): Instance Selenium.
        logger (Logger): Logger pour les messages.
        DOWNLOAD_DIR (str): Dossier de téléchargement.
        DIR_FINAL_BASE (str): Dossier final de destination.
        DATE_FIN (str): Date de fin pour le nommage.
        args (Namespace): Arguments de la ligne de commande.
    """
    logger.info(f"Telechargement du rapport {nom_rapport}")
    debug_enabled = bool(getattr(args, "debug", False) or logger.isEnabledFor(logging.DEBUG))
    _recover_network_or_fail(logger, f"telechargement du rapport {nom_rapport}")
    try:
        attendre_disparition_overlay(driver, 60, logger=logger, debug=args.debug)
        try:
            current_url = driver.current_url
        except Exception:
            current_url = "(url indisponible)"
        try:
            current_title = driver.title
        except Exception:
            current_title = "(titre indisponible)"
        logger.debug(
            "Contexte avant telechargement | rapport=%s | url=%s | titre=%s",
            nom_rapport,
            current_url,
            current_title,
        )
        xpath_bouton = "//button[.//img[contains(@src, 'download')]]"
        bouton = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, xpath_bouton))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", bouton)
        time.sleep(2)
        try:
            bouton.click()
        except Exception:
            driver.execute_script("arguments[0].click();", bouton)
        time.sleep(5)
        logger.debug("Le bouton Télécharger a été cliqué avec succès!")
    except Exception as e:
        _handle_network_loss(logger, f"clic du bouton Télécharger ({nom_rapport})", e)
        logger.error(f"Une erreur s'est produite lors du clic sur le bouton Télécharger : {e}", exc_info=args.debug)
        return
    try:
        radio_mode_couleur = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//input[@data-test-color-mode-picker-color-input]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", radio_mode_couleur)
        time.sleep(1)
        try:
            radio_mode_couleur.click()
        except Exception:
            driver.execute_script("arguments[0].click();", radio_mode_couleur)
        time.sleep(5)
        logger.debug("Le mode couleur a été sélectionné avec succès!")
    except Exception as e:
        _handle_network_loss(logger, f"sélection du mode couleur ({nom_rapport})", e)
        logger.error(f"Une erreur s'est produite lors de la sélection du mode couleur : {e}")
        return
    try:
        xpath_enregistrer = (
            "//button[@data-test-download-dialog-save-button "
            "or @data-testid='download-dialog-save-button' "
            "or (contains(@class, 'btn-primary') and "
            "(contains(normalize-space(), 'Enregistrer le rapport') "
            "or contains(normalize-space(), 'Save Report')))]"
        )
        enregistrer_rapport_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, xpath_enregistrer))
        )
        if debug_enabled:
            log_dir = _get_log_dir_from_logger(logger)
            now_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            logger.debug("Capture debug avant 'Enregistrer le rapport' (step=avant_enregistrer_rapport)")
            capture_screenshot(driver, logger, "avant_enregistrer_rapport", log_dir, now_str)
            logger.debug("Capture debug avant 'Enregistrer le rapport' terminée")
            logger.debug("Bouton 'Enregistrer le rapport' trouvé et cliqué")
        enregistrer_rapport_button.click()
        time.sleep(5)
        logger.debug("Le bouton Enregistrer le rapport a été cliqué avec succès!")
        try:
            close_xpath = "//button[@data-test-download-dialog-close-button or @data-testid='download-dialog-close-button' or contains(normalize-space(), 'Fermer') or contains(normalize-space(), 'Close')]"

            # Ce bouton peut ne pas apparaître selon le rapport / timing UI: traitement non bloquant.
            close_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, close_xpath))
            )
            try:
                close_button.click()
            except Exception:
                driver.execute_script("arguments[0].click();", close_button)

            # Pause pour laisser le temps au téléchargement de se finaliser complètement
            time.sleep(10)
            logger.debug("La fenêtre de téléchargement a été fermée.")
        except TimeoutException:
            logger.warning(
                "Bouton de fermeture de la fenêtre de téléchargement non détecté dans le délai (poursuite)."
            )
        except Exception as e:
            if debug_enabled:
                log_dir = _get_log_dir_from_logger(logger)
                now_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                capture_screenshot(driver, logger, "fermeture_fenetre_telechargement_error", log_dir, now_str)
            logger.warning(
                f"Impossible de fermer la fenêtre de téléchargement (poursuite) : {e}"
            )
            # On tente quand même de continuer, le fichier est peut-être déjà là

    except Exception as e:
        _handle_network_loss(logger, f"enregistrement du rapport ({nom_rapport})", e)
        logger.error(f"Une erreur s'est produite lors de l'enregistrement du rapport : {e}")
        return
    deplace_et_renomme_rapport(nom_rapport, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args, driver)

def traitement_rapport_standard(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args):
    """
    Traite un rapport standard en le sélectionnant puis en le téléchargeant.

    Args:
        nom_rapport (str): Nom du rapport.
        driver (WebDriver): Instance Selenium.
        logger (Logger): Logger pour les messages.
        DOWNLOAD_DIR (str): Dossier de téléchargement.
        DIR_FINAL_BASE (str): Dossier final de destination.
        DATE_FIN (str): Date de fin pour le nommage.
        args (Namespace): Arguments de la ligne de commande.
    """
    logger.info(f"Traitement du rapport {nom_rapport}")
    _recover_network_or_fail(logger, f"traitement du rapport {nom_rapport}")
    try:
        xpath_candidates = _get_report_xpath_candidates(nom_rapport)
        selection_rapport_button = _find_clickable_with_xpath_candidates(driver, xpath_candidates, timeout=30)
        driver.execute_script("arguments[0].scrollIntoView(true);", selection_rapport_button)
        time.sleep(1)
        try:
            selection_rapport_button.click()
        except Exception:
            driver.execute_script("arguments[0].click();", selection_rapport_button)
        time.sleep(2)

        if not _is_report_active(driver, nom_rapport, timeout=8):
            logger.warning(
                "Le rapport '%s' ne semble pas actif après le premier clic. Tentative fallback par texte.",
                nom_rapport,
            )
            fallback_xpath = f"//button[@data-testid='mdc-list-button' and .//span[normalize-space()='{nom_rapport}']]"
            fallback_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, fallback_xpath))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", fallback_btn)
            try:
                fallback_btn.click()
            except Exception:
                driver.execute_script("arguments[0].click();", fallback_btn)
            time.sleep(2)

        if not _is_report_active(driver, nom_rapport, timeout=8):
            raise RuntimeError(
                f"Le rapport '{nom_rapport}' n'a pas pu être activé avant téléchargement."
            )

        telechargement_rapport(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args)
    except NetworkRecoveryRetry:
        raise
    except NetworkRecoveryFailedError:
        raise
    except Exception as e:
        _handle_network_loss(logger, f"traitement du rapport {nom_rapport}", e)
        logger.error(f"Une erreur s'est produite lors de la page des rapports {nom_rapport} : {e}", exc_info=args.debug)
        return

def traitement_rapport_apercu(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args):
    """
    Traite le rapport Aperçu.
    """
    traitement_rapport_standard(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args)

def traitement_rapports_modeles(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args):
    """
    Traite le rapport Modèles.
    """
    traitement_rapport_standard(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args)

def traitement_rapport_superposition(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args):
    """
    Traite le rapport Superposition.
    """
    traitement_rapport_standard(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args)

def traitement_rapport_quotidien(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args):
    """
    Traite le rapport Quotidien.
    """
    traitement_rapport_standard(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args)

def traitement_rapport_comparer(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args):
    """
    Traite le rapport Comparer et ses sous-rapports (Tendances, Superposition, Quotidien).

    Args:
        nom_rapport (str): Nom du rapport.
        driver (WebDriver): Instance Selenium.
        logger (Logger): Logger pour les messages.
        DOWNLOAD_DIR (str): Dossier de téléchargement.
        DIR_FINAL_BASE (str): Dossier final de destination.
        DATE_FIN (str): Date de fin pour le nommage.
        args (Namespace): Arguments de la ligne de commande.
    """
    logger.info(f"Traitement des rapports {nom_rapport}")
    _recover_network_or_fail(logger, f"traitement du rapport {nom_rapport}")
    try:
        def get_base_url():
            return driver.current_url.split("#")[0]

        def click_element_with_retry(xpath, label, attempts=3):
            last_exc = None
            for _ in range(attempts):
                try:
                    element = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    time.sleep(1)
                    try:
                        element.click()
                    except Exception:
                        driver.execute_script("arguments[0].click();", element)
                    return
                except (StaleElementReferenceException, WebDriverException) as exc:
                    last_exc = exc
                    time.sleep(1)
            if last_exc is not None:
                raise last_exc

        def ouvrir_modale_comparer():
            """Ouvre la modale du rapport Comparer."""
            try:
                base_url = get_base_url()
                driver.get(base_url)
                WebDriverWait(driver, 60).until(lambda d: base_url in d.current_url)
            except Exception:
                logger.debug("Navigation vers l'URL base non confirmee; poursuite.")
            attendre_disparition_overlay(driver, 30, logger=logger, debug=args.debug)
            xpath_candidates = _get_report_xpath_candidates(nom_rapport)
            element = _find_clickable_with_xpath_candidates(driver, xpath_candidates, timeout=30)
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)
            try:
                element.click()
            except Exception:
                driver.execute_script("arguments[0].click();", element)
            time.sleep(2)
            logger.debug("Modale Comparer ouverte.")

        def fermer_modale_rapport():
            """Ferme la modale en naviguant vers l'URL base."""
            try:
                base_url = get_base_url()
                driver.get(base_url)
                WebDriverWait(driver, 60).until(lambda d: base_url in d.current_url)
                time.sleep(2)
                attendre_disparition_overlay(driver, 30, logger=logger, debug=args.debug)
                logger.debug("Modale de rapport fermee (navigation vers URL base).")
            except Exception as e:
                logger.debug(f"Erreur lors de la fermeture de modale: {e}")

        def click_compare_link(link_xpath, url_fragment, label):
            """Sélectionne un sous-rapport dans la modale Comparer."""
            click_element_with_retry(link_xpath, label)
            WebDriverWait(driver, 60).until(lambda d: url_fragment in d.current_url)
            attendre_contenu_graphique(label)

        def attendre_contenu_graphique(label):
            # Attendre que le contenu graphique soit charge
            try:
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//canvas|//svg[@class='chart']|//div[contains(@class,'chart')]|//table[contains(@class,'table')]")
                    )
                )
                logger.debug("Contenu graphique charge pour %s.", label)
            except Exception:
                logger.debug("Contenu graphique non confirme pour %s; poursuite.", label)
            attendre_disparition_overlay(driver, 30, logger=logger, debug=args.debug)
            time.sleep(3)

        # NOTE: Cette fonction est conservee pour une utilisation future.
        # Actuellement non utilisee en raison d'un bug Dexcom (voir ligne 432).
        # Sera reactivee une fois que Dexcom aura corrige le probleme de PDF dupliques.
        def ouvrir_page_comparer(route, label):
            """Ouvre directement un sous-rapport Comparer via l'URL."""
            base_url = get_base_url()
            target_url = f"{base_url}#/compare/{route}"
            driver.get(target_url)
            WebDriverWait(driver, 60).until(lambda d: f"/compare/{route}" in d.current_url)
            attendre_contenu_graphique(label)

        # Tendances: ouvrir modale -> selectionner -> telecharger -> fermer
        rapport_comparer = "Comparer-Tendances"
        logger.info(f"Traitement du rapport {rapport_comparer}")
        ouvrir_modale_comparer()
        xpath_tendances = "//a[contains(@href, '/compare/trends') and contains(@class, 'data-page__report-choice-button--trends')]"
        click_compare_link(xpath_tendances, "/compare/trends", "Tendances")
        telechargement_rapport(rapport_comparer, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args)
        fermer_modale_rapport()

        logger.warning(
            "Comparer: probleme connu cote Dexcom, Superposition et Quotidien non telecharges."
        )

        # NOTE: Bug Dexcom - les sous-rapports Comparer suivants generent le meme PDF.
        # TODO: Re-activer quand le site Dexcom sera corrige.
        #
        # # Superposition: ouvrir directement la page /compare/overlay
        # rapport_comparer = "Comparer-Superposition"
        # logger.info(f"Traitement du rapport {rapport_comparer}")
        # ouvrir_page_comparer("overlay", "Superposition")
        # telechargement_rapport(rapport_comparer, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args)
        #
        # # Quotidien: ouvrir directement la page /compare/daily
        # rapport_comparer = "Comparer-Quotidien"
        # logger.info(f"Traitement du rapport {rapport_comparer}")
        # ouvrir_page_comparer("daily", "Quotidien")
        # telechargement_rapport(rapport_comparer, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args)

    except NetworkRecoveryRetry:
        raise
    except NetworkRecoveryFailedError:
        raise
    except Exception as e:
        _handle_network_loss(logger, f"traitement du rapport {nom_rapport}", e)
        logger.error(f"Une erreur s'est produite lors de la page des rapports {nom_rapport} : {e}")
        if args.debug:
            logger.error("Stack trace complète : ", exc_info=True)
        return

def traitement_rapport_statistiques(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args):
    """
    Traite le rapport Statistiques et ses sous-rapports (Quotidien, Par heure).

    Args:
        nom_rapport (str): Nom du rapport.
        driver (WebDriver): Instance Selenium.
        logger (Logger): Logger pour les messages.
        DOWNLOAD_DIR (str): Dossier de téléchargement.
        DIR_FINAL_BASE (str): Dossier final de destination.
        DATE_FIN (str): Date de fin pour le nommage.
        args (Namespace): Arguments de la ligne de commande.
    """
    logger.info(f"Traitement des rapports {nom_rapport}")
    _recover_network_or_fail(logger, f"traitement du rapport {nom_rapport}")
    try:
        xpath_candidates = _get_report_xpath_candidates(nom_rapport)
        selection_rapport_button = _find_clickable_with_xpath_candidates(driver, xpath_candidates, timeout=30)
        driver.execute_script("arguments[0].scrollIntoView(true);", selection_rapport_button)
        time.sleep(1)
        # Capturer l'URL de base avant la navigation, pour le fallback URL dans ouvrir_stats_route.
        try:
            base_url_stats = driver.current_url.split("#")[0]
        except Exception:
            base_url_stats = ""
        try:
            selection_rapport_button.click()
        except Exception:
            driver.execute_script("arguments[0].click();", selection_rapport_button)
        time.sleep(2)

        # Helper local: navigation robuste vers une sous-page Statistiques.
        def ouvrir_stats_route(route: str, label: str):
            xpath_route = f"//a[contains(@href, '/statistics/{route}')]"
            try:
                link = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, xpath_route))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", link)
                time.sleep(1)
                try:
                    link.click()
                except Exception:
                    driver.execute_script("arguments[0].click();", link)
            except Exception:
                # Fallback: navigation directe si le lien n'est pas disponible/cliquable.
                # Utiliser l'URL capturée avant la navigation (indépendante de la région).
                try:
                    base_url = driver.current_url.split("#")[0] or base_url_stats
                except Exception:
                    base_url = base_url_stats
                if not base_url:
                    raise RuntimeError(
                        "Impossible de déterminer l'URL de base pour le fallback Statistiques."
                    )
                target_url = f"{base_url}#/statistics/{route}"
                logger.debug("Navigation directe fallback vers %s (%s)", target_url, label)
                driver.get(target_url)
            WebDriverWait(driver, 30).until(lambda d: f"/statistics/{route}" in (d.current_url or ""))
            attendre_disparition_overlay(driver, 30, logger=logger, debug=args.debug)
            time.sleep(2)

        # Case à cocher "Avancé"
        checkbox = None
        checkbox_xpaths = [
            "//input[@id='advanced-stats' and @type='checkbox']",
            "//input[@type='checkbox' and (contains(@name, 'advanced') or contains(@id, 'advanced'))]",
            "//*[@data-test='advanced-stats' or @data-testid='advanced-stats']//input[@type='checkbox']",
        ]
        for xpath_checkbox in checkbox_xpaths:
            try:
                checkbox = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, xpath_checkbox))
                )
                break
            except Exception:
                continue

        if checkbox is None:
            log_dir = _get_log_dir_from_logger(logger)
            now_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            capture_screenshot(driver, logger, "statistiques_case_avancee_introuvable", log_dir, now_str)
            raise RuntimeError("Case 'Avancé' introuvable dans le rapport Statistiques.")

        try:
            if not checkbox.is_selected():
                driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                time.sleep(1)
                try:
                    checkbox.click()
                except Exception:
                    driver.execute_script("arguments[0].click();", checkbox)
                time.sleep(1)

            if not checkbox.is_selected():
                raise RuntimeError("La case 'Avancé' n'a pas pu être activée.")

            logger.info("La case à cocher 'Avancé' est activée.")
        except Exception as exc:
            log_dir = _get_log_dir_from_logger(logger)
            now_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            capture_screenshot(driver, logger, "statistiques_case_avancee_echec", log_dir, now_str)
            raise RuntimeError(f"Impossible d'activer la case 'Avancé' : {exc}") from exc

        # Quotidien
        rapport_statistiques = "Statistiques-Quotidiennes"
        logger.info(f"Traitement du rapport {rapport_statistiques}")
        ouvrir_stats_route("daily", "Quotidien")
        telechargement_rapport(rapport_statistiques, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args)

        # Par heure
        rapport_statistiques = "Statistiques-Horaires"
        logger.info(f"Traitement du rapport {rapport_statistiques}")
        ouvrir_stats_route("hourly", "Par heure")
        telechargement_rapport(rapport_statistiques, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args)

    except NetworkRecoveryRetry:
        raise
    except NetworkRecoveryFailedError:
        raise
    except Exception as e:
        _handle_network_loss(logger, f"traitement du rapport {nom_rapport}", e)
        logger.error(f"Une erreur s'est produite lors de la page des rapports {nom_rapport} : {e}")
        return

def traitement_rapport_agp(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args):
    """
    Traite le rapport AGP.
    """
    traitement_rapport_standard(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args)

def traitement_export_csv(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args):
    """
    Traite l'export CSV Dexcom Clarity.

    Args:
        nom_rapport (str): Nom du rapport.
        driver (WebDriver): Instance Selenium.
        logger (Logger): Logger pour les messages.
        DOWNLOAD_DIR (str): Dossier de téléchargement.
        DIR_FINAL_BASE (str): Dossier final de destination.
        DATE_FIN (str): Date de fin pour le nommage.
        args (Namespace): Arguments de la ligne de commande.
    """
    logger.info(f"Traitement de l'export csv ")
    _recover_network_or_fail(logger, "traitement de l'export CSV")
    try:
        attendre_disparition_overlay(driver, 60, logger=logger, debug=args.debug)
        xpath_export = "//button[.//img[@src='/i/assets/cui_export.svg']]"
        bouton_export = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, xpath_export))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", bouton_export)
        time.sleep(2)
        try:
            bouton_export.click()
        except Exception:
            driver.execute_script("arguments[0].click();", bouton_export)
        time.sleep(5)
        logger.debug("Le bouton Exporter a été cliqué avec succès!")
    except Exception as e:
        _handle_network_loss(logger, "clic du bouton Exporter", e)
        logger.error(f"Une erreur s'est produite lors du clic sur le bouton Exporter : {e}", exc_info=args.debug)
        return
    try:
        # Utilisation de l'attribut data-test spécifique (plus robuste que le texte)
        xpath_bouton_export_modal = "//button[@data-test-export-dialog-export-button]"
        bouton_export_modal = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, xpath_bouton_export_modal))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", bouton_export_modal)
        time.sleep(1)
        bouton_export_modal.click()
        logger.debug("Le bouton Exporter de la fenêtre modale a été cliqué avec succès!")
    except Exception as e:
        _handle_network_loss(logger, "clic du bouton Exporter de la modale", e)
        logger.error(f"Impossible de cliquer sur le bouton Exporter de la fenêtre modale : {e}")
        return

    try:
        # Ancrage dans le composant <export-dialog> pour éviter toute ambiguïté avec
        # d'autres boutons primaires sur la page.
        xpath_fermer = "//export-dialog//button[normalize-space()='Fermer' or normalize-space()='Close']"
        bouton_fermer = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_fermer))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", bouton_fermer)
        time.sleep(1)
        bouton_fermer.click()
        logger.debug("Le bouton Fermer de la fenêtre modale a été cliqué avec succès!")
        # Attendre que le composant export-dialog disparaisse du DOM avant de poursuivre.
        try:
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.TAG_NAME, "export-dialog"))
            )
            logger.debug("Composant export-dialog disparu du DOM.")
        except Exception:
            logger.debug("Attente de disparition export-dialog expirée (poursuite).")
    except Exception as e:
        _handle_network_loss(logger, "fermeture de la fenêtre modale d'export", e)
        logger.warning(f"Bouton Fermer non trouvé ou non cliquable dans la fenêtre modale : {e}")

    if wait_for_csv_download(DOWNLOAD_DIR):
        logger.info("Fichier CSV exporté détecté et téléchargement terminé.")
        deplace_et_renomme_rapport(nom_rapport, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args, driver)
    else:
        logger.error("Le téléchargement du fichier CSV n'a pas été détecté ou n'est pas terminé après 2 minutes.")

def selection_rapport(RAPPORTS, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args):
    """
    Sélectionne et traite chaque rapport de la liste RAPPORTS.

    Args:
        RAPPORTS (list): Liste des rapports à traiter.
        driver (WebDriver): Instance Selenium.
        logger (Logger): Logger pour les messages.
        DOWNLOAD_DIR (str): Dossier de téléchargement.
        DIR_FINAL_BASE (str): Dossier final de destination.
        DATE_FIN (str): Date de fin pour le nommage.
        args (Namespace): Arguments de la ligne de commande.
    """
    for rapport in RAPPORTS:
        _recover_network_or_fail(logger, f"avant le traitement du rapport {rapport}")

        def _execute_rapport_once() -> None:
            if rapport == "Aperçu":
                traitement_rapport_apercu(rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args)
            elif rapport == "Modèles":
                traitement_rapports_modeles(rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args)
            elif rapport == "Superposition":
                traitement_rapport_superposition(rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args)
            elif rapport == "Quotidien":
                traitement_rapport_quotidien(rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args)
            elif rapport == "Comparer":
                traitement_rapport_comparer(rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args)
            elif rapport == "Statistiques":
                traitement_rapport_statistiques(rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args)
            elif rapport == "AGP":
                traitement_rapport_agp(rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args)
            elif rapport == "Export":
                traitement_export_csv(rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, DATE_DEBUT, args)
            else:
                logger.error(f"Rapport inconnu : {rapport}. Veuillez vérifier la liste des rapports.")

        max_network_retries = 2
        retry_count = 0

        while True:
            try:
                _execute_rapport_once()
                break
            except NetworkRecoveryRetry as retry_error:
                if retry_count >= max_network_retries:
                    logger.error(
                        "Abandon du rapport '%s' après %d retries réseau.",
                        rapport,
                        max_network_retries,
                    )
                    raise NetworkRecoveryFailedError(
                        f"Retries réseau dépassés pendant le traitement du rapport {rapport}."
                    ) from retry_error

                retry_count += 1
                logger.warning(
                    "Reconnexion détectée. Nouvel essai du rapport '%s' (%d/%d).",
                    rapport,
                    retry_count,
                    max_network_retries,
                )
                _recover_network_or_fail(logger, f"retry {retry_count} du rapport {rapport}")
