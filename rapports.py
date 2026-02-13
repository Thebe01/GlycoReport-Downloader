#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Format d'en-tête standard à respecter pour ce projet.
Voir HEADER_TEMPLATE_PYTHON.md pour les détails.

Module        : rapports.py
Type          : Python module
Auteur        : Pierre Théberge
Compagnie     : Innovations, Performances, Technologies inc.
Créé le       : 2025-08-05
Modifié le    : 2026-02-12
Version       : 0.3.13
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
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import (
    attendre_disparition_overlay,
    get_last_downloaded_report_file,
    renomme_prefix,
    check_internet,
    capture_screenshot,
)

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

def deplace_et_renomme_rapport(nom_rapport, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, driver=None, log_dir=None, now_str=None):
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

        if nom_rapport == "Export":
            nouveau_nom_fichier = f"Clarity_Exporter_Théberge_Pierre_{DATE_FIN}.csv"
            destination = os.path.join(dir_final, nouveau_nom_fichier)
            logger.debug(f"Renommage Export : {chemin_fichier_telecharge} -> {destination}")
            try:
                os.replace(chemin_fichier_telecharge, destination)
                logger.info(f"Le fichier Export {chemin_fichier_telecharge} a été renommé en {destination}")
            except Exception as e:
                logger.error(f"Erreur lors du renommage du fichier Export : {e}")
        else:
            nouveau_prefix = renomme_prefix(prefix, DATE_FIN, logger=logger)
            nouveau_nom_fichier = nouveau_prefix + "_" + nom_rapport + "." + suffix
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

def telechargement_rapport(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args):
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
    try:
        attendre_disparition_overlay(driver, 60, logger=logger, debug=args.debug)
        xpath_bouton = "//button[.//img[@alt='Télécharger']]"
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
        logger.error(f"Une erreur s'est produite lors de la sélection du mode couleur : {e}")
        return
    try:
        xpath_enregistrer = "//button[contains(@class, 'btn-primary') and contains(., 'Enregistrer le rapport')]"
        enregistrer_rapport_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, xpath_enregistrer))
        )
        if args.debug:
            logger.debug("Bouton 'Enregistrer le rapport' trouvé et cliqué")
        enregistrer_rapport_button.click()
        time.sleep(5)
        logger.debug("Le bouton Enregistrer le rapport a été cliqué avec succès!")
        try:
            # Augmentation du délai à 60s pour les rapports longs à générer (ex: Superposition)
            WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Fermer')]"))
            )
            fermer_fenetre_telechargement_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Fermer')]")
            fermer_fenetre_telechargement_button.click()
            # Pause pour laisser le temps au téléchargement de se finaliser complètement
            time.sleep(10)
            logger.debug("La fenêtre de téléchargement a été fermée.")
        except Exception as e:
            logger.error(f"Une erreur s'est produite lors de la fermeture de la fenêtre de téléchargement: {e}")
            # On tente quand même de continuer, le fichier est peut-être déjà là

    except Exception as e:
        logger.error(f"Une erreur s'est produite lors de l'enregistrement du rapport : {e}")
        return
    deplace_et_renomme_rapport(nom_rapport, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, driver)

def traitement_rapport_standard(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args):
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
    try:
        xpath_rapport = f"//button[normalize-space()='{nom_rapport}']"
        selection_rapport_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, xpath_rapport))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", selection_rapport_button)
        time.sleep(1)
        try:
            selection_rapport_button.click()
        except Exception:
            driver.execute_script("arguments[0].click();", selection_rapport_button)
        time.sleep(2)
        telechargement_rapport(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args)
    except Exception as e:
        logger.error(f"Une erreur s'est produite lors de la page des rapports {nom_rapport} : {e}", exc_info=args.debug)
        return

def traitement_rapport_apercu(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args):
    """
    Traite le rapport Aperçu.
    """
    traitement_rapport_standard(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args)

def traitement_rapports_modeles(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args):
    """
    Traite le rapport Modèles.
    """
    traitement_rapport_standard(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args)

def traitement_rapport_superposition(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args):
    """
    Traite le rapport Superposition.
    """
    traitement_rapport_standard(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args)

def traitement_rapport_quotidien(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args):
    """
    Traite le rapport Quotidien.
    """
    traitement_rapport_standard(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args)

def traitement_rapport_comparer(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args):
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
            xpath_rapport = f"//button[normalize-space()='{nom_rapport}']"
            click_element_with_retry(xpath_rapport, "bouton comparer")
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
        xpath_tendances = "//a[contains(@href, '/compare/trends') and contains(@class, 'data-page__report-choice-button--trends') and normalize-space(.//div)='Tendances']"
        click_compare_link(xpath_tendances, "/compare/trends", "Tendances")
        telechargement_rapport(rapport_comparer, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args)
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

    except Exception as e:
        logger.error(f"Une erreur s'est produite lors de la page des rapports {nom_rapport} : {e}")
        if args.debug:
            logger.error("Stack trace complète : ", exc_info=True)
        return

def traitement_rapport_statistiques(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args):
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
    try:
        xpath_rapport = f"//button[normalize-space()='{nom_rapport}']"
        selection_rapport_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, xpath_rapport))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", selection_rapport_button)
        time.sleep(1)
        try:
            selection_rapport_button.click()
        except Exception:
            driver.execute_script("arguments[0].click();", selection_rapport_button)
        time.sleep(2)

        # Case à cocher "Avancé"
        xpath_checkbox = "//input[@id='advanced-stats' and @type='checkbox']"
        checkbox = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, xpath_checkbox))
        )
        if not checkbox.is_selected():
            driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
            time.sleep(1)
            try:
                checkbox.click()
            except Exception:
                driver.execute_script("arguments[0].click();", checkbox)
            time.sleep(1)
            logger.info("La case à cocher 'Avancé' a été activée.")
        else:
            logger.info("La case à cocher 'Avancé' était déjà activée.")

        # Quotidien
        rapport_statistiques = "Statistiques-Quotidiennes"
        logger.info(f"Traitement du rapport {rapport_statistiques}")
        xpath_quotidien = "//a[contains(@href, '/statistics/daily') and normalize-space()='Quotidien']"
        quotidien_link = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, xpath_quotidien))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", quotidien_link)
        time.sleep(1)
        try:
            quotidien_link.click()
        except Exception:
            driver.execute_script("arguments[0].click();", quotidien_link)
        time.sleep(2)
        telechargement_rapport(rapport_statistiques, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args)

        # Par heure
        rapport_statistiques = "Statistiques-Horaires"
        logger.info(f"Traitement du rapport {rapport_statistiques}")
        xpath_horaire = "//a[contains(@class, 'ember-view') and contains(@href, '/statistics/hourly')]"
        horaire_link = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, xpath_horaire))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", horaire_link)
        time.sleep(1)
        try:
            horaire_link.click()
        except Exception:
            driver.execute_script("arguments[0].click();", horaire_link)
        time.sleep(2)
        telechargement_rapport(rapport_statistiques, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args)

    except Exception as e:
        logger.error(f"Une erreur s'est produite lors de la page des rapports {nom_rapport} : {e}")
        return

def traitement_rapport_agp(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args):
    """
    Traite le rapport AGP.
    """
    traitement_rapport_standard(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args)

def traitement_export_csv(nom_rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args):
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
    try:
        attendre_disparition_overlay(driver, 60, logger=logger, debug=args.debug)
        xpath_export = "//button[.//img[@src='/i/assets/cui_export.svg' and @alt='Exporter']]"
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
        logger.error(f"Impossible de cliquer sur le bouton Exporter de la fenêtre modale : {e}")
        return

    try:
        # Correction du sélecteur pour le bouton Fermer (suppression de btn-3d qui n'est plus présent)
        xpath_fermer = "//button[contains(@class, 'btn-primary') and normalize-space()='Fermer']"
        bouton_fermer = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_fermer))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", bouton_fermer)
        time.sleep(1)
        bouton_fermer.click()
        logger.debug("Le bouton Fermer de la fenêtre modale a été cliqué avec succès!")
    except Exception as e:
        logger.warning(f"Bouton Fermer non trouvé ou non cliquable dans la fenêtre modale : {e}")

    if wait_for_csv_download(DOWNLOAD_DIR):
        logger.info("Fichier CSV exporté détecté et téléchargement terminé.")
        deplace_et_renomme_rapport(nom_rapport, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, driver)
    else:
        logger.error("Le téléchargement du fichier CSV n'a pas été détecté ou n'est pas terminé après 2 minutes.")

def selection_rapport(RAPPORTS, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args):
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
        if rapport == "Aperçu":
            traitement_rapport_apercu(rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args)
        elif rapport == "Modèles":
            traitement_rapports_modeles(rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args)
        elif rapport == "Superposition":
            traitement_rapport_superposition(rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args)
        elif rapport == "Quotidien":
            traitement_rapport_quotidien(rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args)
        elif rapport == "Comparer":
            traitement_rapport_comparer(rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args)
        elif rapport == "Statistiques":
            traitement_rapport_statistiques(rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args)
        elif rapport == "AGP":
            traitement_rapport_agp(rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args)
        elif rapport == "Export":
            traitement_export_csv(rapport, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args)
        else:
            logger.error(f"Rapport inconnu : {rapport}. Veuillez vérifier la liste des rapports.")
