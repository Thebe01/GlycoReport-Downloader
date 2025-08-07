#'''////////////////////////////////////////////////////////////////////////////////////////////////////
#'''<summary>
#'''FileName: ClarityDownload.py
#'''FileType: py Source file
#'''
#'''Author : Pierre Théberge
#'''Created On : 2025-03-03
#'''Last Modified On : 2025-08-06
#'''CopyRights : Innovations Performances Technologies inc
#'''Description : Programme pour télécharger les différents rapports provenant de Clarity ainsi que les relevés bruts
#'''                Le dossier de téléchargement est : C:\Users\thebe\Downloads\Dexcom_download
#'''                Le dossier final est C:\Users\thebe\OneDrive\Documents\Santé\Suivie glycémie et pression\AAAA
#'''Version : 0.0.21
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
#''' </summary>
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
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import (
    DOWNLOAD_DIR, DIR_FINAL_BASE, CHROME_USER_DATA_DIR, DEXCOM_URL,
    CHROMEDRIVER_LOG, RAPPORTS, NOW_STR
)
from utils import (
    check_internet,
    attendre_disparition_overlay,
    get_last_downloaded_file,
    get_last_downloaded_nonlog_file,
    renomme_prefix,
    attendre_nouveau_bouton_telecharger
)
from rapports import selection_rapport

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
elif args.date_debut and args.date_fin:
    DATE_DEBUT = args.date_debut
    DATE_FIN = args.date_fin
else:
    # Par défaut, 14 derniers jours
    date_fin = datetime.today() - timedelta(days=1)
    date_debut = date_fin - timedelta(days=14 - 1)
    DATE_DEBUT = date_debut.strftime("%Y-%m-%d")
    DATE_FIN = date_fin.strftime("%Y-%m-%d")

if args.rapports:
    RAPPORTS = args.rapports

# Configuration du logger pour fichier et console
logger = logging.getLogger('dexcom_clarity')
logger.setLevel(logging.DEBUG if args.debug else logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

# Handler fichier
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

file_handler = logging.FileHandler(os.path.join(DOWNLOAD_DIR, f"clarity_download_{NOW_STR}.log"))
file_handler.setLevel(logging.DEBUG if args.debug else logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Handler console (optionnel, mais recommandé)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

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
service = ChromeService(log_path=CHROMEDRIVER_LOG)

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
            if not dexcom_username or not dexcom_password:
                logger.error("Les variables d'environnement DEXCOM_USERNAME et/ou DEXCOM_PASSWORD ne sont pas définies. Veuillez les renseigner avant d'exécuter le script.")
                sys.exit(1)

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

    finally:
        # Fermez le navigateur dans tous les cas
        try:
            driver.quit()
        except Exception as e:
            logger.warning(f"Erreur lors de la fermeture du navigateur : {e}", exc_info=args.debug)

if __name__ == "__main__":
    main()
