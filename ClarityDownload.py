#'''////////////////////////////////////////////////////////////////////////////////////////////////////
#'''<summary>
#'''FileName: ClarityDownload.py
#'''FileType: py Source file
#'''
#'''Author : Pierre Théberge
#'''Created On : 2025-03-03
#'''Last Modified On : 2025-08-04
#'''CopyRights : Innovations Performances Technologies inc
#'''Description : Programme pour télécharger les différents rapports provenant de Clarity ainsi que les relevés bruts
#'''                Le dossier de téléchargement est : C:\Users\thebe\Downloads\Dexcom_download
#'''                Le dossier final est C:\Users\thebe\OneDrive\Documents\Santé\Suivie glycémie et pression\AAAA
#'''Version : 0.0.19
#'''Modifications :
#'''Version   Date          Description
#'''0.0.0	2025-03-03    Version initiale.
#'''0.0.1	2025-03-07    Connectoin à Clarity et authentification
#''                       Utilisation de Chrome au lieu de Edge
#'''0.0.2   2025-03-20    Cliquer sur le sélecteur de dates et choisir la période
#'''0.0.3   2025-03-28    Ajout du traitement des rapports
#'''0.0.4   2025-04-07    Conversion à Python 3.13 et une erreur de syntaxe dans le code de la fonction traitement_rapport_apercu
#'''0.0.5   2025-04-11    Ajout de la sélection du rapport Apercu
#'''0.0.6   2025-04-16    Ajout du code pour télécharger un rapport.
#'''                        Reste à cliquer sur les boutons télécharger le rapport et
#'''                        enregistrer sous.
#'''0.0.7   2025-04-24    Retour à Python 3.12. Besoin Tensorflow et il n'est pas supporté par Python 3.13
#'''                      Cliquer sur le bouton "Enregistrer le rapport"
#'''                      Enlever la sélection du mode couleur (problème à avoir le bon xpath)
#'''0.0.8   2025-05-23    Terminé la fonction téléchargement_rapport
#'''                      Ajout de la fonction deplace_et_renomme_rapport
#'''                      Reconversion à Python 3.13
#'''0.0.9   2025-07-01    Ajout de l'option debug et ajout d'un fichier de log
#'''0.0.10  2025-07-02    Modification pour tenir compte d'une connexion internet lente et instable (4mb/s)Ajout de la fonction traitement_rapport
#'''                      Ajout de la fonction check_internet pour vérifier la connexion internet
#'''                      Ajout du traitement pour les rapports Modèles
#'''                      Dans la fonction deplace_et_renomme_rapport, ne pas tenir compte des fichiers *.log
#'''0.0.11  2025-07-03    La vérification de la connexion internet ne fonctionne pas avec NordVPN
#'''                      Ajout du traitement pour le rapport Superposition
#'''                      Rendre plus robuste le traitement du rapport Aperçu
#'''                      Ajout du traitement pour le rapport Quotidien
#'''                      Ajout du traitement pour le rapport AGP
#'''0.0.12  2025-07-08    Ajout du traitement pour le rapport Statistiques
#'''0.0.13  2025-07-13    Ajout du traitement pour le rapport Comparer
#'''0.0.14  2025-07-18    Ajout de l'exportation des données en format csv
#'''0.0.15  2025-07-21    Terminer la fonction traitement_export_csv
#'''                        Ajout des sous-rapport pour le rapport Comparer
#'''                        Les sous-rapports Superposition et Quotidien de comparer ne fonctioone pas.
#'''                            Ils produisent le même PDF que Tendances.
#'''                        Ajouter la déconnexion du compte avant de fermer le navigateur
#'''0.0.16  2025-07-25    Correction pour la déconnexion du compte
#'''                        Correction pour le bouton Fermer de la fenêtre modale Exporter
#'''0.0.17  2025-07-25    Correction pour le déconnexion du compte. Éliminer la référence au nom d'utilisateur.
#'''                        Ajout de TODO pour la correction du code.
#'''0.0.18  2025-07-30    Gestion des exceptions plus précise. Évite les except: nus. Précise toujours le type d’exception
#'''                      Factorisation des attentes sur les overlays/loaders. Crée une fonction utilitaire
#'''                          pour attendre la disparition des overlays, et utilise-la partout où c’est pertinent.
#'''                      Centralisation des paramètres et chemins. Définis tous les chemins, URLs, et paramètres en haut du script ou dans un fichier de config.
#'''                      Ajout d’une fonction main()
#'''                      Fermeture du navigateur dans un finally
#'''0.0.19  2025-08-04    Ajout de docstrings pour toutes les fonctions
#'''                      Logging cohérent. Utilise le logger pour tous les messages (pas de print).
#  </summary>
#'''/////////////////////////////////////////////////////////////////////////////////////////////////////

# TODO 4 Centralisation des paramètres et chemins. Définis tous les chemins, URLs, et paramètres dans un fichier de config.
# TODO 10 Passer les dates et la liste de rapports en paramètres.
# TODO 11 Réparer le problème avec les rapports Comparer
# TODO 12 Exécuter l'application pour produire les rapports Comparer depuis 2024-08-19
# TODO 13 Appliquer la même solution pour obtenir des rapports séparés pour Modèle
# TODO 14 Rendre l'application indépendante de la langue de l'utilisateur.

import os
import sys
import logging
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import uuid
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import socket
import urllib.request

# Ajout du parser d'arguments
parser = argparse.ArgumentParser(description="Téléchargement des rapports Dexcom Clarity")
parser.add_argument('--debug', '-d', action='store_true', help='Activer le mode debug')
args = parser.parse_args()

# === PARAMÈTRES ET CHEMINS CENTRALISÉS ===

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
DATE_DEBUT = "2025-02-03"
DATE_FIN = "2025-02-16"

# ==========================================

# Configuration du logger pour fichier et console
logger = logging.getLogger('dexcom_clarity')
logger.setLevel(logging.DEBUG if args.debug else logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

# Handler fichier
file_handler = logging.FileHandler(os.path.join(DOWNLOAD_DIR, f"clarity_download_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Handler console (optionnel)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Configuration du service ChromeDriver
service = ChromeService(log_path=CHROMEDRIVER_LOG)

# Configuration des options Chrome
options = Options()
options.add_argument(f"--user-data-dir={CHROME_USER_DATA_DIR}")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-background-networking")
options.add_argument("--disable-client-side-phishing-detection")
options.add_argument("--disable-default-apps")
options.add_argument("--disable-hang-monitor")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-sync")
options.add_argument("--disable-translate")
options.add_argument("--disable-features=PaintHolding")

prefs = {
    "download.default_directory": DOWNLOAD_DIR,  # Dossier de téléchargement
    "download.prompt_for_download": False,       # Pas de popup de confirmation
    "directory_upgrade": True,                   # Mise à jour du dossier si déjà ouvert
    "safebrowsing.enabled": True                 # Désactive l'avertissement de sécurité
}
options.add_experimental_option("prefs", prefs)

# Initialisation du WebDriver
driver = webdriver.Chrome(service=service, options=options)

# URL de la page Dexcom Clarity
url = DEXCOM_URL

def check_internet(url="https://www.google.com", timeout=5):
    """
    Vérifie la connexion internet en tentant d'ouvrir l'URL spécifiée.

    Args:
        url (str): URL à tester (par défaut Google).
        timeout (int): Durée maximale en secondes pour la tentative.

    Returns:
        bool: True si la connexion fonctionne, False sinon.
    """
    try:
        urllib.request.urlopen(url, timeout=timeout)
        return True
    except Exception:
        return False

def get_last_downloaded_file(DOWNLOAD_DIR):
    """
    Retourne le chemin du fichier le plus récemment téléchargé dans le dossier donné.

    Args:
        DOWNLOAD_DIR (str): Chemin du dossier de téléchargement.

    Returns:
        str or None: Chemin du fichier le plus récent, ou None si aucun fichier.
    """
    files = [os.path.join(DOWNLOAD_DIR, f) for f in os.listdir(DOWNLOAD_DIR)]
    files = [f for f in files if os.path.isfile(f)]
    if not files:
        logger.warning("Aucun fichier téléchargé trouvé dans le dossier.")
        return None
    logger.debug(f"Fichiers trouvés : {files}")
    return max(files, key=os.path.getctime)

def renomme_prefix(prefix):
    """
    Renomme le préfixe du fichier téléchargé en ajoutant la date de fin.

    Args:
        prefix (str): Préfixe original du fichier.

    Returns:
        str: Nouveau préfixe formaté.
    """
    nom, date, numero = prefix.split("_")
    nouveau_prefix = nom + "_" + DATE_FIN + "_" + numero
    logger.debug(f"Nouveau préfix : {nouveau_prefix}")
    return nouveau_prefix

def attendre_disparition_overlay(driver, timeout=60):
    """
    Attend la disparition des overlays, loaders ou spinners courants.

    Args:
        driver (WebDriver): Instance du navigateur Selenium.
        timeout (int): Durée maximale d'attente en secondes.
    """
    try:
        WebDriverWait(driver, timeout).until_not(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".overlay, .loader, .spinner"))
        )
    except Exception as e:
        logger.debug(f"Aucun overlay/loader détecté ou disparition non confirmée : {e}", exc_info=args.debug)

def get_user_menu_button(driver, timeout=10):
    """
    Retourne le bouton du menu utilisateur pour la déconnexion.

    Args:
        driver (WebDriver): Instance du navigateur Selenium.
        timeout (int): Durée maximale d'attente en secondes.

    Returns:
        WebElement: Bouton du menu utilisateur.

    Raises:
        Exception: Si le bouton n'est pas trouvé ou cliquable.
    """
    try:
        xpath = "(//button[.//span[@class='clarity-menu__primarylabel'] and .//span[@class='clarity-menu__trigger-item-down-arrow']])[last()]"
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
    except Exception as e:
        logger.error(f"Bouton utilisateur introuvable : {e}", exc_info=args.debug)
        raise

def deplace_et_renomme_rapport(nom_rapport):
    """
    Déplace et renomme le rapport téléchargé dans le dossier final.

    Args:
        nom_rapport (str): Nom du rapport à traiter.
    """
    logger.info(f"Deplacement et renommage du rapport {nom_rapport}")
    annee = DATE_FIN[:4]
    dir_final = os.path.join(DIR_FINAL_BASE, annee)

    # Création du répertoire s'il n'existe pas
    if not os.path.exists(dir_final):
        os.makedirs(dir_final)
        logger.debug(f"Répertoire créé : {dir_final}")

    def get_last_downloaded_nonlog_file(DOWNLOAD_DIR):
        """
        Retourne le dernier fichier téléchargé (hors .log) dans le dossier donné.

        Args:
            DOWNLOAD_DIR (str): Chemin du dossier de téléchargement.

        Returns:
            str or None: Chemin du fichier le plus récent, ou None si aucun fichier.
        """
        files = [os.path.join(DOWNLOAD_DIR, f) for f in os.listdir(DOWNLOAD_DIR)]
        files = [f for f in files if os.path.isfile(f) and not f.lower().endswith('.log')]
        if not files:
            return None
        return max(files, key=os.path.getctime)

    chemin_fichier_telecharge = get_last_downloaded_nonlog_file(DOWNLOAD_DIR)
    if chemin_fichier_telecharge:
        nom_fichier_telecharge = os.path.basename(chemin_fichier_telecharge)
        prefix, suffix = os.path.splitext(nom_fichier_telecharge)
        suffix = suffix[1:] if suffix.startswith('.') else suffix

        if nom_rapport == "Export":
            # Renommer au format Clarity_Exporter_Théberge_Pierre_AAAA-MM-JJ.csv
            nouveau_nom_fichier = f"Clarity_Exporter_Théberge_Pierre_{DATE_FIN}.csv"
            destination = os.path.join(dir_final, nouveau_nom_fichier)
            logger.debug(f"Renommage Export : {chemin_fichier_telecharge} -> {destination}")
            try:
                os.replace(chemin_fichier_telecharge, destination)
                logger.info(f"Le fichier Export {chemin_fichier_telecharge} a été renommé en {destination}")
            except Exception as e:
                logger.error(f"Erreur lors du renommage du fichier Export : {e}")
        else:
            nouveau_prefix = renomme_prefix(prefix)
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

def telechargement_rapport(nom_rapport):
    """
    Télécharge le rapport spécifié et le déplace dans le dossier final.

    Args:
        nom_rapport (str): Nom du rapport à télécharger.
    """
    logger.info(f"Telechargement du rapport {nom_rapport}")
    # Ajoutez ici le code spécifique pour telecharger le rapport
    try:
        attendre_disparition_overlay(driver, 60)
        # Attendre que le bouton "Télécharger" (icône) soit cliquable
        xpath_bouton = "//button[.//img[@alt='Télécharger']]"
        bouton = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, xpath_bouton))
        )
        # Faire défiler jusqu'au bouton pour s'assurer qu'il est visible
        driver.execute_script("arguments[0].scrollIntoView(true);", bouton)
        time.sleep(2)
        # Essayer un clic classique
        try:
            bouton.click()
        except Exception:
            # Si le clic classique échoue, essayer un clic JS
            driver.execute_script("arguments[0].click();", bouton)
        time.sleep(5)
        logger.debug("Le bouton Télécharger a été cliqué avec succès!")
    except Exception as e:
        logger.error(f"Une erreur s'est produite lors du clic sur le bouton Télécharger : {e}", exc_info=args.debug)
        return
    # Choisir le rapport en couleur
    try:
        # Attendre que l'input radio pour le mode couleur soit présent (pas forcément cliquable)
        radio_mode_couleur = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//input[@data-test-color-mode-picker-color-input]"))
        )
        # Faire défiler jusqu'à l'élément pour s'assurer qu'il est visible
        driver.execute_script("arguments[0].scrollIntoView(true);", radio_mode_couleur)
        time.sleep(1)
        try:
            radio_mode_couleur.click()
        except Exception:
            # Si le clic classique échoue (élément masqué), utiliser JS
            driver.execute_script("arguments[0].click();", radio_mode_couleur)
        time.sleep(5)
        logger.debug("Le mode couleur a été sélectionné avec succès!")
    except Exception as e:
        logger.error(f"Une erreur s'est produite lors de la sélection du mode couleur : {e}")
        return
    # Cliquer sur le bouton Enregistrer le rapport
    try:
        # Attendre que le bouton "Enregistrer le rapport" soit cliquable
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
            # Attendre que l'élément soit recréé
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
    deplace_et_renomme_rapport(nom_rapport)

def traitement_rapport_standard(nom_rapport):
    """
    Traite le rapport standard en cliquant sur le bouton correspondant et en lançant le téléchargement.

    Args:
        nom_rapport (str): Nom du rapport à traiter.
    """
    logger.info(f"Traitement du rapport {nom_rapport}")
    try:
        # Exemple robuste : sélectionne le bouton par le texte visible (à adapter selon le rapport)
        xpath_rapport = f"//button[normalize-space()='{nom_rapport}']"
        selection_rapport_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, xpath_rapport))
        )
        # Faire défiler jusqu'au bouton pour s'assurer qu'il est visible
        driver.execute_script("arguments[0].scrollIntoView(true);", selection_rapport_button)
        time.sleep(1)
        try:
            selection_rapport_button.click()
        except Exception:
            # Si le clic classique échoue, utiliser JS
            driver.execute_script("arguments[0].click();", selection_rapport_button)
        time.sleep(2)
        telechargement_rapport(nom_rapport)
    except Exception as e:
        logger.error(f"Une erreur s'est produite lors de la page des rapports {nom_rapport} : {e}", exc_info=args.debug)
        return

def traitement_rapport_apercu(nom_rapport):
    """
    Traite le rapport Aperçu.

    Args:
        nom_rapport (str): Nom du rapport à traiter.
    """
    traitement_rapport_standard(nom_rapport)

def traitement_rapports_modeles(nom_rapport):
    """
    Code pour traiter les rapports "Modèles"
    Il y a une possibilité de 3 rapports qui sont téléchargés dans le même PDF

    Args:
        nom_rapport (str): Nom du rapport à traiter.
    """
    traitement_rapport_standard(nom_rapport)

def traitement_rapport_superposition(nom_rapport):
    """
    Traite le rapport Superposition.

    Args:
        nom_rapport (str): Nom du rapport à traiter.
    """
    traitement_rapport_standard(nom_rapport)

def traitement_rapport_quotidien(nom_rapport):
    """
    Traite le rapport Quotidien.

    Args:
        nom_rapport (str): Nom du rapport à traiter.
    """
    traitement_rapport_standard(nom_rapport)

def attendre_nouveau_bouton_telecharger(driver, bouton_avant, timeout=30):
    """
    Attend que le bouton Télécharger soit recréé dans le DOM (nouvelle instance).

    Args:
        driver (WebDriver): Instance du navigateur Selenium.
        bouton_avant (WebElement): Ancienne instance du bouton.
        timeout (int): Durée maximale d'attente en secondes.
    """
    def bouton_a_change(drv):
        try:
            nouveau_bouton = drv.find_element(By.XPATH, "//button[.//img[@alt='Télécharger']]")
            return nouveau_bouton and nouveau_bouton != bouton_avant
        except Exception:
            return False
    WebDriverWait(driver, timeout).until(bouton_a_change)

def traitement_rapport_comparer(nom_rapport):
    """
    Traite le rapport Comparer et ses sous-rapports.

    Args:
        nom_rapport (str): Nom du rapport à traiter.
    """
    # TODO Réparer le problème avec les rapports Comparer
    # Code pour traiter le rapport "Comparer"
    logger.info(f"Traitement des rapports {nom_rapport}")
    # Ajoutez ici le code spécifique pour traiter le rapport "Comparer"
    try:
        # Sélectionner le bouton desrapports Comparer
        xpath_rapport = f"//button[normalize-space()='{nom_rapport}']"
        selection_rapport_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, xpath_rapport))
        )
        # Faire défiler jusqu'au bouton pour s'assurer qu'il est visible
        driver.execute_script("arguments[0].scrollIntoView(true);", selection_rapport_button)
        time.sleep(1)
        try:
            selection_rapport_button.click()
        except Exception:
            # Si le clic classique échoue, utiliser JS
            driver.execute_script("arguments[0].click();", selection_rapport_button)
        time.sleep(2)

        # Sélectionner l'onglet/lien "Tendances"
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

        # Télécharger le rapport Tendances
        telechargement_rapport(rapport_comparer)

        # Sélectionner l'onglet/lien "Superposition"
        rapport_comparer = "Comparer-Superposition"
        logger.info(f"Traitement du rapport {rapport_comparer}")
        xpath_superposition = "//a[contains(@href, '/compare/overlay') and contains(@class, 'data-page__report-choice-button--overlay') and .//div[@title='Superposition' and normalize-space()='Superposition']]"
        superposition_link = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, xpath_superposition))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", superposition_link)
        time.sleep(1)

        # Avant le clic, récupérer le texte actuel de l'élément semaine (si présent)
        try:
            semaine_elem = driver.find_element(By.XPATH, "//strong[contains(@class, 'overlay_report__week-number')]")
            semaine_avant = semaine_elem.text.strip()
        except Exception:
            semaine_avant = None

        # Clic sur Superposition
        try:
            superposition_link.click()
        except Exception:
            driver.execute_script("arguments[0].click();", superposition_link)
        time.sleep(2)
        telechargement_rapport(rapport_comparer)


        # --- QUOTIDIEN ---
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

        # Attendre le chargement complet de Quotidien
        WebDriverWait(driver, 60).until(lambda d: "/compare/daily" in d.current_url)
        time.sleep(10)  # Attente pour s'assurer que le PDF est mis à jour
        telechargement_rapport(rapport_comparer)

    except Exception as e:
        logger.error(f"Une erreur s'est produite lors de la page des rapports {nom_rapport} : {e}")
        if args.debug:
            logger.error("Stack trace complète : ", exc_info=True)
        return


def traitement_rapport_statistiques(nom_rapport):
    """
    Traite le rapport Statistiques et ses sous-rapports.

    Args:
        nom_rapport (str): Nom du rapport à traiter.
    """
    logger.info(f"Traitement des rapports {nom_rapport}")
    try:
        # Sélectionner le bouton du rapport Statistiques
        xpath_rapport = f"//button[normalize-space()='{nom_rapport}']"
        selection_rapport_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, xpath_rapport))
        )
        # Faire défiler jusqu'au bouton pour s'assurer qu'il est visible
        driver.execute_script("arguments[0].scrollIntoView(true);", selection_rapport_button)
        time.sleep(1)
        try:
            selection_rapport_button.click()
        except Exception:
            # Si le clic classique échoue, utiliser JS
            driver.execute_script("arguments[0].click();", selection_rapport_button)
        time.sleep(2)

        # Cliquer sur la case à cocher "Avancé"
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

        # Sélectionner l'onglet/lien "Quotidien"

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

        # Télécharger le rapport Quotidien
        telechargement_rapport(rapport_statistiques)

        # Sélectionner l'onglet/lien "Par heure"
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

        # Télécharger le rapport Horaire
        telechargement_rapport(rapport_statistiques)

    except Exception as e:
        logger.error(f"Une erreur s'est produite lors de la page des rapports {nom_rapport} : {e}")
        return

def traitement_rapport_agp(nom_rapport):
    """
    Traite le rapport AGP.

    Args:
        nom_rapport (str): Nom du rapport à traiter.
    """
    traitement_rapport_standard(nom_rapport)

def traitement_export_csv(nom_rapport):
    """
    Traite l'export CSV du rapport.

    Args:
        nom_rapport (str): Nom du rapport à traiter.
    """
    logger.info(f"Traitement de l'export csv ")
    try:
        attendre_disparition_overlay(driver, 60)
        # Attendre que le bouton Exporter (icône) soit cliquable
        xpath_export = "//button[.//img[@src='/i/assets/cui_export.svg' and @alt='Exporter']]"
        bouton_export = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, xpath_export))
        )
        # Faire défiler jusqu'au bouton pour s'assurer qu'il est visible
        driver.execute_script("arguments[0].scrollIntoView(true);", bouton_export)
        time.sleep(2)
        # Essayer un clic classique
        try:
            bouton_export.click()
        except Exception:
            # Si le clic classique échoue, essayer un clic JS
            driver.execute_script("arguments[0].click();", bouton_export)
        time.sleep(5)
        logger.debug("Le bouton Exporter a été cliqué avec succès!")
    except Exception as e:
        logger.error(f"Une erreur s'est produite lors du clic sur le bouton Exporter : {e}", exc_info=args.debug)
        return
    # Cliquer sur le bouton Exporter dans la fenêtre modale
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

    # Cliquer sur le bouton Fermer de la fenêtre modale si présent
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

    # --- Attendre la fin réelle du téléchargement du fichier CSV ---
    def wait_for_csv_download(DOWNLOAD_DIR, timeout=120):
        """Attend qu'un fichier .csv apparaisse dans le dossier et qu'il n'y ait plus de .crdownload."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            files = [f for f in os.listdir(DOWNLOAD_DIR) if f.lower().endswith('.csv')]
            if files:
                # Vérifier qu'il n'y a pas de .crdownload
                crdownloads = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith('.crdownload')]
                if not crdownloads:
                    return True
            time.sleep(1)
        return False

    if wait_for_csv_download(DOWNLOAD_DIR):
        logger.info("Fichier CSV exporté détecté et téléchargement terminé.")
        deplace_et_renomme_rapport(nom_rapport)
    else:
        logger.error("Le téléchargement du fichier CSV n'a pas été détecté ou n'est pas terminé après 2 minutes.")

def selection_rapport(RAPPORTS):
    """
    Sélectionne et traite chaque rapport de la liste.

    Args:
        RAPPORTS (list): Liste des rapports à traiter.
    """
    # Code pour traiter les rapports
    for rapport in RAPPORTS:
        if rapport == "Aperçu":
            # Code pour traiter le rapport "Aperçu"
            traitement_rapport_apercu(rapport)
        elif rapport == "Modèles":
            # Code pour traiter le rapport "Modèles"
            traitement_rapports_modeles(rapport)
        elif rapport == "Superposition":
            # Code pour traiter le rapport "Superposition"
            traitement_rapport_superposition(rapport)
        elif rapport == "Quotidien":
            # Code pour traiter le rapport "Quotidien"
            traitement_rapport_quotidien(rapport)
        elif rapport == "Comparer":
            # Code pour traiter le rapport "Comparer"
            traitement_rapport_comparer(rapport)
        elif rapport == "Statistiques":
            # Code pour traiter le rapport "Statistiques"
            traitement_rapport_statistiques(rapport)
        elif rapport == "AGP":
            # Code pour traiter le rapport "AGP"
            traitement_rapport_agp(rapport)
        elif rapport == "Export":
            # Code pour traiter le rapport "Export"
            traitement_export_csv(rapport)
        else:
            logger.error(f"Rapport inconnu : {rapport}. Veuillez vérifier la liste des rapports.")


def main():
    """
    Fonction principale du script Dexcom Clarity Reports Downloader.
    Gère la connexion, la sélection des dates, le téléchargement des rapports et la déconnexion.
    """
    try:
        # Affichage de la version de Python si le mode debug est activé
        if args.debug:
            logger.debug(f"Version de Python : {sys.version}")

        logger.info(f"Rapports à traiter : {RAPPORTS}")
        logger.info(f"Dossier de téléchargement : {DOWNLOAD_DIR}")

        # Vérification de la connexion internet avant d'ouvrir la page
        if not check_internet():
            logger.error("Perte de connexion internet détectée avant l'ouverture de la page Dexcom Clarity.")
            logger.info("Arrêt du script suite à une perte de connexion internet.")
            sys.exit(0)

        # Ouvrir la page de connexion
        driver.get(DEXCOM_URL)

        # Attendez que la page soit entièrement chargée
        wait = WebDriverWait(driver=driver, timeout=60)  # Augmenté à 60s

        # Vérification de la connexion internet avant de cliquer sur le bouton d'accueil
        if not check_internet():
            logger.error("Perte de connexion internet détectée avant de cliquer sur le bouton d'accueil.")
            logger.info("Arrêt du script suite à une perte de connexion internet.")
            sys.exit(1)

        # Recherchez et cliquez sur le bouton "Dexcom Clarity pour les utilisateurs à domicile"
        try:
            bouton = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@value='Dexcom Clarity pour les utilisateurs à domicile']")))
            bouton.click()
            time.sleep(5)  # Augmenté à 5s
            logger.debug("Le bouton pour utilisateurs à domicile a été cliqué avec succès!")
        except Exception as e:
            if not check_internet():
                logger.error("Perte de connexion internet détectée lors du clic sur le bouton pour utilisateurs à domicile.")
            logger.error(f"Une erreur s'est produite au moment de cliquer sur le bouton pour utilisateurs à domicile : {e}")

        # Recherchez les champs de saisie pour le courriel/nom d'utilisateur et le mot de passe
        try:
            if not check_internet():
                logger.error("Perte de connexion internet détectée avant la saisie des identifiants.")
                raise RuntimeError("Connexion internet requise pour poursuivre.")

            username_input = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_input = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            dexcom_username = os.getenv("DEXCOM_USERNAME")
            dexcom_password = os.getenv("DEXCOM_PASSWORD")
            if dexcom_username is None or dexcom_password is None:
                raise ValueError("Les variables d'environnement DEXCOM_USERNAME et DEXCOM_PASSWORD doivent être définies.")

            username_input.send_keys(dexcom_username)
            password_input.send_keys(dexcom_password)

            login_button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Se connecter']"))
            )
            login_button.click()
            time.sleep(5)  # Augmenté à 5s

            logger.info("Connexion réussie !")
        except Exception as e:
            if not check_internet():
                logger.error("Perte de connexion internet détectée lors de la connexion.")
            logger.error(f"Une erreur s'est produite lors de la connexion : {e}")

        # Attendez que la page soit entièrement chargée
        time.sleep(10)  # Augmenté à 10s

        # Recherchez les champs de saisie des dates et entrez les nouvelles dates
        try:
            if not check_internet():
                logger.error("Perte de connexion internet détectée avant la sélection des dates.")
                raise RuntimeError("Connexion internet requise pour poursuivre.")

            date_picker_button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@data-test-date-range-picker-toggle]"))
            )
            date_picker_button.click()
            logger.debug("Bouton du sélecteur de dates trouvé et cliqué.")
            time.sleep(5)  # Augmenté à 5s

            if DATE_DEBUT is None or DATE_FIN is None:
                raise ValueError("Les variables DATE_DEBUT et DATE_FIN ne peuvent pas être None. Elles doivent être définies.")

            date_debut_input = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.NAME, "start_date"))
            )
            date_fin_input = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.NAME, "end_date"))
            )
            date_debut_input.clear()
            date_fin_input.clear()
            date_debut_input.send_keys(DATE_DEBUT)
            date_fin_input.send_keys(DATE_FIN)

            ok_button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-test-date-range-picker__ok-button]"))
            )
            ok_button.click()
            logger.debug("Bouton OK du sélecteur de dates cliqué.")
            time.sleep(5)  # Augmenté à 5s

            logger.info(f"Date de début: {DATE_DEBUT}")
            logger.info(f"Date de fin: {DATE_FIN}")
            logger.info("Les dates ont été saisies avec succès !")

        except Exception as e:
            if not check_internet():
                logger.error("Perte de connexion internet détectée lors de la saisie des dates.")
            logger.error(f"Une erreur s'est produite lors de la saisie des dates : {e}")

        # Téléchargez les rapports
        selection_rapport(RAPPORTS)

        # Attendez un peu pour vous assurer que le téléchargement est terminé
        time.sleep(60)

        # (optionnel) Derniers diagnostics AVANT de quitter
        if args.debug:
            boutons = driver.find_elements(By.XPATH, "//button")
            logger.info(f"{len(boutons)} boutons trouvés sur la page")
            for b in boutons:
                logger.debug(b.get_attribute("outerHTML"))

        # Déconnexion avant de fermer le navigateur
        try:
            user_menu_button = get_user_menu_button(driver)
            user_menu_button.click()
            time.sleep(2)
            # Cliquer sur le lien Déconnexion (structure <a> fournie)
            logout_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'cui-link__logout') and contains(., 'Déconnexion')]"))
            )
            logout_link.click()
            logger.info("Déconnexion effectuée avec succès.")
            time.sleep(3)
        except Exception as e:
            logger.warning(f"Impossible de se déconnecter proprement : {e}", exc_info=args.debug)

    finally:
        # Fermez le navigateur dans tous les cas
        try:
            driver.quit()
        except Exception as e:
            logger.warning(f"Erreur lors de la fermeture du navigateur : {e}", exc_info=args.debug)

if __name__ == "__main__":
    main()
