#'''////////////////////////////////////////////////////////////////////////////////////////////////////
#'''<summary>
#'''FileName: ClarityDownload.py
#'''FileType: py Source file
#'''
#'''Author : Pierre Théberge
#'''Created On : 2025-03-03
#'''Last Modified On : 2025-08-28
#'''CopyRights : Innovations Performances Technologies inc
#'''Description : Script principal pour l'automatisation du téléchargement des rapports Dexcom Clarity.
#'''              Centralisation de la configuration, gestion CLI avancée, robustesse accrue,
#'''              logs détaillés (console, fichier, JS), gestion des exceptions et de la déconnexion.
#'''Version : 0.1.10
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
#'''0.0.20  2025-08-05    Ajout d'une validation pour la présende des variables d'environnement nécessaires
#'''                      Crée un fichier config.py pour centraliser tous les paramètres, chemins, URLs, etc.
#'''                      Crée un fichier utils.py pour toutes les fonctions utilitaires (connexion internet, overlay, renommage, etc.).
#'''                      Crée un fichier rapports.py pour le traitement des rapports
#'''0.0.21  2025-08-06    Ajout d'un exemple de fichier de configuration "config_example.yaml"
#'''0.0.22  2025-08-13    Centralisation et normalisation des chemins, gestion CLI améliorée,
#'''                      logs JS navigateur, robustesse accrue sur la gestion des erreurs,
#'''                      factorisation des utilitaires, gestion propre des exceptions et de la déconnexion.
#'''0.0.23  2025-08-13    Capture d’écran centralisée via utils.py, délai avant capture,
#'''                      suppression des duplications de code, ajout de logs pour le diagnostic.
#'''0.1.0   2025-08-18    Robustesse saisie identifiant : sélection usernameLogin, vérification visibilité/interactivité,
#'''                      captures d’écran uniquement en mode debug, gestion du bouton 'Pas maintenant' après connexion,
#'''                      adaptation aux changements d’interface Dexcom, logs détaillés pour le diagnostic.
#'''0.1.6   2025-08-22    Synchronisation des versions dans tous les modules, ajout de version.py, log de la version exécutée.
#'''0.1.7   2025-08-25    Création automatique de config.yaml à partir de config_example.yaml si absent.
#'''                      Gestion interactive des credentials si .env absent (demande à l'utilisateur, non conservé).
#'''                      Utilisation centralisée de get_dexcom_credentials depuis config.py.
#'''                      Plus d'accès direct à os.getenv dans ce module.
#'''0.1.8   2025-08-27    Configuration interactive avancée pour config.yaml et .env.
#'''                      Copie minimale du profil Chrome lors de la configuration.
#'''                      Ajout du paramètre log_retention_days (0 = conservation illimitée).
#'''                      Nettoyage automatique des logs selon la rétention.
#'''                      Messages utilisateurs colorés et validation renforcée.
#'''0.1.9   2025-08-28    Vérification interactive de la clé chromedriver_log lors de la création de config.yaml.
#'''                      Empêche la saisie d'un dossier pour le log, exige un chemin de fichier.
#'''                      Correction de la robustesse de la configuration initiale.
#'''0.1.10  2025-08-28    Le ménage des logs s'effectue désormais uniquement après l'activation du logging.
#'''                      Chaque suppression de log est loggée.
# #'''</summary>
#'''/////////////////////////////////////////////////////////////////////////////////////////////////////

# TODO 11 Réparer le problème avec les rapports Comparer
# TODO 12 Exécuter l'application pour produire les rapports Comparer depuis 2024-08-19
# TODO 13 Appliquer la même solution pour obtenir des rapports séparés pour Modèle
# TODO 14 Rendre l'application indépendante de la langue de l'utilisateur.
# TODO 15 Améliorer le help

import os
import sys
import logging
import argparse
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import glob
import re
from getpass import getpass
import traceback

from config import (
    DOWNLOAD_DIR, DIR_FINAL_BASE, CHROME_USER_DATA_DIR, DEXCOM_URL,
    CHROMEDRIVER_LOG, RAPPORTS, NOW_STR, DATE_DEBUT, DATE_FIN,
    LOG_RETENTION_DAYS,
    get_dexcom_credentials
)
from utils import (
    check_internet,
    attendre_disparition_overlay,
    get_last_downloaded_file,
    get_last_downloaded_nonlog_file,
    renomme_prefix,
    attendre_nouveau_bouton_telecharger,
    capture_screenshot,
    pause_on_error,
    cleanup_logs
)
from rapports import selection_rapport
from version import __version__

# Ajout du parser d'arguments
parser = argparse.ArgumentParser(description="Téléchargement des rapports Dexcom Clarity")
parser.add_argument('--debug', '-d', action='store_true', help='Activer le mode debug')
parser.add_argument('--days', type=int, choices=[7, 14, 30, 90], help='Nombre de jours à inclure dans le rapport (7, 14, 30, 90)')
parser.add_argument('--date_debut', type=str, help='Date de début (AAAA-MM-JJ)')
parser.add_argument('--date_fin', type=str, help='Date de fin (AAAA-MM-JJ)')
parser.add_argument('--rapports', nargs='+', help='Liste des rapports à traiter')
args = parser.parse_args()

# Gestion intelligente des dates
if args.days:
    date_fin = datetime.today() - timedelta(days=1)  # Date de fin = hier
    date_debut = date_fin - timedelta(days=args.days - 1)
    DATE_DEBUT = date_debut.strftime("%Y-%m-%d")
    DATE_FIN = date_fin.strftime("%Y-%m-%d")
else:
    DATE_DEBUT = args.date_debut or DATE_DEBUT  # DATE_DEBUT de config.py
    DATE_FIN = args.date_fin or DATE_FIN        # DATE_FIN de config.py

RAPPORTS = args.rapports or RAPPORTS  # RAPPORTS de config.py

DEBUG_MODE = args.debug

# Configuration du logger pour fichier et console
logger = logging.getLogger('dexcom_clarity')
logger.setLevel(logging.DEBUG if args.debug else logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

# Handler fichier
log_dir = os.path.dirname(CHROMEDRIVER_LOG)
os.makedirs(log_dir, exist_ok=True)
file_handler = logging.FileHandler(os.path.join(log_dir, f"clarity_download_{NOW_STR}.log"))
file_handler.setLevel(logging.DEBUG if args.debug else logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Handler console (optionnel, mais recommandé)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Ménage des logs (après activation du logging)
from config import CHROMEDRIVER_LOG, LOG_RETENTION_DAYS
from utils import cleanup_logs
import os

log_dir = os.path.dirname(CHROMEDRIVER_LOG) or "."
cleanup_logs(log_dir, LOG_RETENTION_DAYS, logger)

# Options Chrome
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

# Service ChromeDriver
chromedriver_service_args = ["--verbose"] if args.debug else []
service = ChromeService(
    log_path=CHROMEDRIVER_LOG,
    service_args=chromedriver_service_args
)

# Initialisation du WebDriver
driver = webdriver.Chrome(service=service, options=options)

# URL de la page Dexcom Clarity
url = DEXCOM_URL


def get_user_menu_button(driver, logger, args, timeout=10):
    """
    Retourne le bouton du menu utilisateur pour la déconnexion.

    Args:
        driver (WebDriver): Instance du navigateur Selenium.
        logger (Logger): Logger à utiliser pour les messages d'erreur.
        args (Namespace): Arguments de la ligne de commande (pour debug).
        timeout (int): Durée maximale d'attente en secondes.

    Returns:
        WebElement: Bouton du menu utilisateur.

    Raises:
        Exception: Si le bouton n'est pas trouvé ou cliquable.
    """
    try:
        xpath = ("(//button[.//span[@class='clarity-menu__primarylabel'] "
                "and .//span[@class='clarity-menu__trigger-item-down-arrow']])[last()]")
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
    except Exception as e:
        logger.error(f"Bouton utilisateur introuvable : {e}", exc_info=args.debug)
        raise


def click_home_user_button(driver, logger, timeout=10):
    """
    Clique sur le bouton 'Dexcom Clarity for Home Users' sur la page d'accueil.
    Arrête le script en cas d'échec.
    """
    try:
        xpath = "//input[@type='submit' and contains(@class, 'landing-page--button')]"
        button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        button.click()
        logger.debug("Le bouton 'Dexcom Clarity for Home Users' a été cliqué avec succès!")
    except Exception as e:
        time.sleep(2)
        capture_screenshot(driver, logger, "home_user_button_error", log_dir, NOW_STR)
        logger.error(f"Une erreur s'est produite au moment de cliquer sur le bouton 'Dexcom Clarity for Home Users' : {e}")
        logger.info("Arrêt du script suite à une erreur sur le bouton d'accueil.")
        sys.exit(1)


def saisir_identifiants(driver, logger, log_dir, NOW_STR):
    """
    Saisit les identifiants de connexion (nom d'utilisateur et mot de passe) sur la page Dexcom Clarity.

    Args:
        driver (WebDriver): Instance du navigateur Selenium.
        logger (Logger): Logger à utiliser pour les messages d'erreur.
        log_dir (str): Répertoire des logs.
        NOW_STR (str): Timestamp actuel sous forme de chaîne.

    Raises:
        SystemExit: Si une erreur critique se produit (ex: variables d'environnement manquantes).
    """
    try:
        if not check_internet():
            logger.error("Perte de connexion internet détectée avant la saisie des identifiants.")
            raise RuntimeError("Connexion internet requise pour poursuivre.")

        # Récupération des identifiants via config.py
        dexcom_username, dexcom_password, dexcom_country_code, dexcom_phone_number = get_dexcom_credentials()
        if not dexcom_username or not dexcom_password:
            logger.error("Les identifiants Dexcom sont manquants.")
            raise SystemExit(1)

        # Détection du type d'identifiant
        is_phone = re.fullmatch(r"\+?[1-9]\d{9,14}", dexcom_username.strip()) is not None

        if is_phone:
            country_code = dexcom_country_code
            phone_number = dexcom_phone_number
            if not country_code or not phone_number:
                logger.error("Variables DEXCOM_COUNTRY_CODE et DEXCOM_PHONE_NUMBER requises.")
                raise SystemExit(1)
            # Accès au mode téléphone (indépendant de la langue)
            phone_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//a[contains(@href, 'phone') or contains(@class, 'phone') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'téléphone') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'phone')]"
                ))
            )
            phone_link.click()

            # Champs téléphone
            country_code_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "countryCode"))
            )
            phone_number_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "phoneNumber"))
            )

            country_code_input.clear()
            country_code_input.send_keys(country_code)
            phone_number_input.clear()
            phone_number_input.send_keys(phone_number)

        else:
            # Sélection du mode courriel/nom d'utilisateur
            radio_buttons = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "radio-outer-circle"))
            )
            if radio_buttons:
                driver.execute_script("arguments[0].click();", radio_buttons[0])
                time.sleep(1)

            # Capture avant la recherche du champ username (en mode debug uniquement)
            if logger.isEnabledFor(logging.DEBUG):
                capture_screenshot(driver, logger, "avant_username_input", log_dir, NOW_STR)

            # Attendre que le champ soit présent
            try:
                username_input = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.ID, "usernameLogin"))
                )
            except Exception as e:
                logger.error("Champ usernameLogin introuvable après sélection du mode courriel/nom d'utilisateur.")
                if logger.isEnabledFor(logging.DEBUG):
                    capture_screenshot(driver, logger, "erreur_username_input", log_dir, NOW_STR)
                raise SystemExit(1)

            # Vérifier que le champ est visible et interactif
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of(username_input))
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "usernameLogin")))
            except Exception as e:
                logger.error("Champ usernameLogin non visible ou non interactif.")
                if logger.isEnabledFor(logging.DEBUG):
                    capture_screenshot(driver, logger, "username_non_interactif", log_dir, NOW_STR)
                raise SystemExit(1)

            # Scroll jusqu'au champ pour le rendre visible
            driver.execute_script("arguments[0].scrollIntoView(true);", username_input)
            time.sleep(0.5)

            # Clic dans le champ pour déclencher les scripts JS
            try:
                username_input.click()
            except Exception:
                driver.execute_script("arguments[0].click();", username_input)
            time.sleep(0.5)

            # Saisie classique
            username_input.clear()
            username_input.send_keys(dexcom_username)
            time.sleep(0.5)

            # Vérification et saisie forcée si nécessaire
            if username_input.get_attribute("value") != dexcom_username:
                logger.warning("La saisie classique a échoué, tentative via JavaScript.")
                driver.execute_script("arguments[0].value = arguments[1];", username_input, dexcom_username)

            # Déclencher un événement 'input' pour que le champ soit reconnu
            driver.execute_script("""
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, username_input)

            if logger.isEnabledFor(logging.DEBUG):
                capture_screenshot(driver, logger, "apres_saisie_username", log_dir, NOW_STR)

        # Bouton suivant
        next_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value]"))
        )
        next_button.click()
        time.sleep(2)

        # Saisie du mot de passe
        password_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_input.send_keys(dexcom_password)

        login_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value]"))
        )
        login_button.click()
        time.sleep(5)

        logger.info("Connexion réussie !")
        time.sleep(2)
        if logger.isEnabledFor(logging.DEBUG):
            capture_screenshot(driver, logger, "apres_connexion", log_dir, NOW_STR)

        # Après la connexion réussie, avant d'aller plus loin...
        try:
            # Attendre la présence éventuelle du bouton "Pas maintenant" (notNowButton)
            not_now_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "notNowButton"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", not_now_button)
            not_now_button.click()
            logger.debug("Bouton 'Pas maintenant' détecté et cliqué.")
            time.sleep(2)
        except Exception:
            # Si le bouton n'est pas présent, on continue simplement
            logger.debug("Aucun bouton 'Pas maintenant' à cliquer, poursuite du script.")

    except Exception as e:
        logger.error(f"Erreur lors de la saisie des identifiants ou de la connexion : {e}")
        raise SystemExit(1)


def pause_on_error():
    """
    Affiche un message et attend que l'utilisateur appuie sur Entrée avant de fermer la fenêtre du terminal.
    """
    if sys.stdin.isatty():
        input("\nAppuyez sur Entrée pour fermer...")


def main():
    """
    Fonction principale du script Dexcom Clarity Reports Downloader.
    Gère la connexion, la sélection des dates, le téléchargement des rapports et la déconnexion.
    """
    try:
        # Affichage de la version de Python si le mode debug est activé
        if args.debug:
            logger.debug(f"Version de Python : {sys.version}")
        logger.info(f"Version de l'application exécutée : {__version__}")
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

        # Recherchez et cliquez sur le bouton "Dexcom Clarity for Home Users"
        try:
            click_home_user_button(driver, logger)
            time.sleep(5)  # Augmenté à 5s
            logger.debug("Le bouton 'Dexcom Clarity for Home Users' a été cliqué avec succès!")
        except Exception as e:
            time.sleep(2)
            capture_screenshot(driver, logger, "home_user_button_error", log_dir, NOW_STR)
            logger.error(f"Une erreur s'est produite au moment de cliquer sur le bouton 'Dexcom Clarity for Home Users' : {e}")
            logger.info("Arrêt du script suite à une erreur sur le bouton d'accueil.")
            sys.exit(1)

        # Recherchez les champs de saisie pour le courriel/nom d'utilisateur ou le numéro de téléphone
        try:
            saisir_identifiants(driver, logger, log_dir, NOW_STR)

        except Exception as e:
            logger.error(f"Erreur lors de la saisie des identifiants ou de la connexion : {e}")
            sys.exit(1)

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
        selection_rapport(
            RAPPORTS,
            driver,
            logger,
            DOWNLOAD_DIR,
            DIR_FINAL_BASE,
            DATE_FIN,
            args
        )

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

            user_menu_button = get_user_menu_button(driver, logger, args)
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

    except Exception as e:
        logger.error(f"Erreur inattendue dans le script principal : {e}")
        traceback.print_exc()
        pause_on_error()
        sys.exit(1)
    finally:
        # Fermez le navigateur dans tous les cas
        try:
            driver.quit()
        except Exception as e:
            logger.warning(f"Erreur lors de la fermeture du navigateur : {e}", exc_info=args.debug)

        import glob
        files = glob.glob(os.path.join(DOWNLOAD_DIR, '*'))
        logger.info(f"Fichiers présents dans le dossier de téléchargement après la demande : {files}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Erreur critique lors de l'exécution du script : {e}")
        import traceback
        traceback.print_exc()
        pause_on_error()
        sys.exit(1)

