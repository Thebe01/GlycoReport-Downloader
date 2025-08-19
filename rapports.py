#'''////////////////////////////////////////////////////////////////////////////////////////////////////
#'''<summary>
#'''FileName: rapports.py
#'''FileType: py Source file
#'''
#'''Author : Pierre Théberge
#'''Created On : 2025-08-05
#'''Last Modified On : 2025-08-13
#'''CopyRights : Innovations Performances Technologies inc
#'''Description : Traitement et gestion des rapports Dexcom Clarity.
#'''              Utilisation des chemins et paramètres centralisés, logging détaillé,
#'''              robustesse pour la détection et gestion des fichiers téléchargés,
#'''              logging des erreurs JS lors du déplacement/renommage.
#'''Version : 0.0.2
#'''Modifications :
#'''Version   Date          Description
#'''0.0.0	2025-08-05    Version initiale.
#'''0.0.1   2025-08-13    Logging JS navigateur, robustesse accrue sur la gestion des fichiers,
#'''                      utilisation systématique des chemins centralisés.
#'''0.0.2   2025-08-13    Utilisation de capture_screenshot centralisée (utils.py) avec délai,
#'''                      ajout de logs pour le diagnostic.
#  </summary>
#'''/////////////////////////////////////////////////////////////////////////////////////////////////////

import os
import time
import glob
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import attendre_disparition_overlay, get_last_downloaded_nonlog_file, renomme_prefix, check_internet, capture_screenshot

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

    chemin_fichier_telecharge = get_last_downloaded_nonlog_file(DOWNLOAD_DIR)
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
        logger.error("Aucun fichier téléchargé trouvé (hors fichiers .log).")
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
            WebDriverWait(driver,30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Fermer')]"))
            )
            fermer_fenetre_telechargement_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Fermer')]")
            fermer_fenetre_telechargement_button.click()
            time.sleep(30)
            logger.debug("La fenêtre de téléchargement a été fermée.")
        except Exception as e:
            logger.error(f"Une erreur s'est produite lors de la fermeture de la fenêtre de téléchargement: {e}")
            return
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

        # Tendances
        rapport_comparer = "Comparer-Tendances"
        logger.info(f"Traitement du rapport {rapport_comparer}")
        xpath_tendances = "//a[contains(@href, '/compare/trends') and contains(@class, 'data-page__report-choice-button--trends') and normalize-space(.//div)='Tendances']"
        tendances_link = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, xpath_tendances))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", tendances_link)
        time.sleep(1)
        try:
            tendances_link.click()
        except Exception:
            driver.execute_script("arguments[0].click();", tendances_link)
        time.sleep(2)
        telechargement_rapport(rapport_comparer, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args)

        # Superposition
        rapport_comparer = "Comparer-Superposition"
        logger.info(f"Traitement du rapport {rapport_comparer}")
        xpath_superposition = "//a[contains(@href, '/compare/overlay') and contains(@class, 'data-page__report-choice-button--overlay') and .//div[@title='Superposition' and normalize-space()='Superposition']]"
        superposition_link = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, xpath_superposition))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", superposition_link)
        time.sleep(1)
        try:
            superposition_link.click()
        except Exception:
            driver.execute_script("arguments[0].click();", superposition_link)
        time.sleep(2)
        telechargement_rapport(rapport_comparer, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args)

        # Quotidien
        rapport_comparer = "Comparer-Quotidien"
        logger.info(f"Traitement du rapport {rapport_comparer}")
        xpath_quotidien = (
            "//a[contains(@href, '/compare/daily') "
            "and contains(@class, 'data-page__report-choice-button--daily') "
            "and .//div[@title='Quotidien' and normalize-space()='Quotidien']]"
        )
        quotidien_link = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, xpath_quotidien))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", quotidien_link)
        time.sleep(2)
        driver.execute_script("arguments[0].click();", quotidien_link)
        WebDriverWait(driver, 60).until(lambda d: "/compare/daily" in d.current_url)
        time.sleep(10)
        telechargement_rapport(rapport_comparer, driver, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN, args)

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
        xpath_horaire = "//a[contains(@href, '/statistics/hourly') and normalize-space()='Par heure']"
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
        xpath_bouton_export_modal = "//button[contains(@class, 'btn-primary') and contains(@class, 'btn-3d') and normalize-space()='Exporter']"
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
        bouton_fermer = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-primary') and contains(@class, 'btn-3d') and normalize-space()='Fermer']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", bouton_fermer)
        time.sleep(1)
        bouton_fermer.click()
        logger.debug("Le bouton Fermer de la fenêtre modale a été cliqué avec succès!")
    except Exception as e:
        logger.warning(f"Bouton Fermer non trouvé ou non cliquable dans la fenêtre modale : {e}")

    if wait_for_csv_download(DOWNLOAD_DIR):
        logger.info("Fichier CSV exporté détecté et téléchargement terminé.")
        deplace_et_renomme_rapport(nom_rapport, logger, DOWNLOAD_DIR, DIR_FINAL_BASE, DATE_FIN)
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
