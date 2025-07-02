#'''////////////////////////////////////////////////////////////////////////////////////////////////////
#'''<summary>
#'''FileName: ClarityDownload.py
#'''FileType: py Source file
#'''
#'''Author : Pierre Théberge
#'''Created On : 2025-03-03
#'''Last Modified On : 2025-07-02
#'''CopyRights : Innovations Performances Technologies inc
#'''Description : Programme pour télécharger les différents rapports provenant de Clarity ainsi que les relevés bruts
#'''                Le dossier de téléchargement est : C:\Users\thebe\Downloads\Dexcom_download
#'''                Le dossier final est C:\Users\thebe\OneDrive\Documents\Santé\Suivie glycémie et pression\AAAA
#'''Version : 0.0.10
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
#'''0.0.9   2025-07-01    Ajout de l'option debug et ajout d'un fichier de log
#'''0.0.10  2025-07-02    Modification pour tenir compte d'une connexion internet lente et instable (4mb/s)Ajout de la fonction traitement_rapport
#'''                      Ajout de la fonction check_internet pour vérifier la connexion internet
#'''                      Ajout du traitement pour les rapports Modèles
#'''                      Dans la fonction deplace_et_renomme_rapport, ne pas tenir compte des fichiers *.log
#'''</summary>
#'''/////////////////////////////////////////////////////////////////////////////////////////////////////

## TODO 1.1 Installer ChromeDriver sur mes 2 ordis. portable et bureau. Version 110.0.5481.177
## TODO 2 Ajouter le path \\ADMIN06\Download\Microsoft\EdgeDriver dans la variable d'environnement
## TODO 3 Pour désactiver la collecte de données de diagnostic pour Microsoft Edge WebDriver, définissez la variable d’environnement sur MSEDGEDRIVER_TELEMETRY_OPTOUT1
## TODO 4 Ajouter le chemin d'environnement: 'C:\Users\thebe\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts'
## TODO 9 Convertir à Python 3.13

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

# Ajout du parser d'arguments
parser = argparse.ArgumentParser(description="Téléchargement des rapports Dexcom Clarity")
parser.add_argument('--debug', '-d', action='store_true', help='Activer le mode debug')
args = parser.parse_args()

download_dir = r"C:\Users\thebe\Downloads\Dexcom_download"  # Mets ici ton dossier cible

# Création du répertoire de téléchargement s'il n'existe pas
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Création d'un nom de fichier log unique avec date et heure
now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = os.path.join(download_dir, f"clarity_download_{now}.log")

# Configuration du logger pour fichier et console
logger = logging.getLogger('dexcom_clarity')
logger.setLevel(logging.DEBUG if args.debug else logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

# Handler fichier
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Handler console (optionnel)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

date_debut = "2024-08-19"
date_fin = "2024-09-01"
rapports = ["Aperçu", "Modèles", "Superposition", "Quotidien", "Comparer", "Statistiques", "AGP"]

# Configuration du service ChromeDriver
service = ChromeService(log_path=os.path.join(os.getcwd(), "chromedriver.log"))

# Configuration des options Chrome
options = Options()
options.add_argument("--user-data-dir=C:/Users/thebe/AppData/Local/Google/Chrome/User Data/ClarityDownloadProfile")
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
    "download.default_directory": download_dir,  # Dossier de téléchargement
    "download.prompt_for_download": False,       # Pas de popup de confirmation
    "directory_upgrade": True,                   # Mise à jour du dossier si déjà ouvert
    "safebrowsing.enabled": True                 # Désactive l'avertissement de sécurité
}
options.add_experimental_option("prefs", prefs)

# Initialisation du WebDriver
driver = webdriver.Chrome(service=service, options=options)

# URL de la page Dexcom Clarity
url = "https://clarity.dexcom.eu/?&locale=fr-CA"

def check_internet(host="8.8.8.8", port=53, timeout=3):
    """Retourne True si la connexion internet fonctionne, False sinon."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        return False

def get_last_downloaded_file(download_dir):
    """Retourne le chemin du fichier le plus récemment téléchargé dans le dossier donné."""
    files = [os.path.join(download_dir, f) for f in os.listdir(download_dir)]
    files = [f for f in files if os.path.isfile(f)]
    if not files:
        return None
    print(files)
    return max(files, key=os.path.getctime)

def renomme_prefix(prefix):
    nom, date, numero = prefix.split("_")
    nouveau_prefix = nom + "_" + date_fin + "_" + numero
    print("Nouveau préfix : ", nouveau_prefix)
    return nouveau_prefix


def deplace_et_renomme_rapport(nom_rapport):
    # Code pour deplacer et renommer le rapport
    logger.info(f"Deplacement et renommage du rapport {nom_rapport}")
    annee = date_fin[:4]
    dir_final = r"C:\Users\thebe\OneDrive\Documents\Santé\Suivie glycémie et pression"
    dir_final = os.path.join(dir_final, annee)
    
    # Création du répertoire s'il n'existe pas
    if not os.path.exists(dir_final):
        os.makedirs(dir_final)
        logger.debug(f"Répertoire créé : {dir_final}")

    # Exclure les fichiers .log lors de la recherche du dernier fichier téléchargé
    def get_last_downloaded_nonlog_file(download_dir):
        files = [os.path.join(download_dir, f) for f in os.listdir(download_dir)]
        files = [f for f in files if os.path.isfile(f) and not f.lower().endswith('.log')]
        if not files:
            return None
        return max(files, key=os.path.getctime)

    chemin_fichier_telecharge = get_last_downloaded_nonlog_file(download_dir)
    if chemin_fichier_telecharge:
        nom_fichier_telecharge = os.path.basename(chemin_fichier_telecharge)
        prefix, suffix = os.path.splitext(nom_fichier_telecharge)
        suffix = suffix[1:] if suffix.startswith('.') else suffix
        nouveau_prefix = renomme_prefix(prefix)
        nouveau_nom_fichier = nouveau_prefix + "_" + nom_rapport + "." + suffix
        destination = os.path.join(dir_final, nouveau_nom_fichier)
        # Ajout du log debug avant le renommage
        logger.debug(f"Renommage du fichier : {chemin_fichier_telecharge} -> {destination}")
        os.rename(chemin_fichier_telecharge, destination)
        logger.info(f"Le fichier {chemin_fichier_telecharge} a été renommé en {destination}")
    else:
        logger.error("Aucun fichier téléchargé trouvé (hors fichiers .log).")

def telechargement_rapport(nom_rapport):
    # Code pour telecharger le rapport
    logger.info(f"Telechargement du rapport {nom_rapport}")
    # Ajoutez ici le code spécifique pour telecharger le rapport
    try:
        # Attendre la disparition d'un overlay éventuel AVANT de cliquer
        try:
            WebDriverWait(driver, 60).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".overlay, .loader, .spinner"))
            )
        except:
            pass  # Si pas d'overlay, on continue

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
        logger.info("Le bouton Télécharger a été cliqué avec succès!")
    except Exception as e:
        logger.error(f"Une erreur s'est produite lors du clic sur le bouton Télécharger : {e}")
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
        logger.info("Le mode couleur a été sélectionné avec succès!")
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
        logger.info("Le bouton Enregistrer le rapport a été cliqué avec succès!")
        try:
            # Attendre que l'élément soit recréé
            WebDriverWait(driver,30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Fermer')]"))
            )
            fermer_fenetre_telechargement_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Fermer')]")
            fermer_fenetre_telechargement_button.click()
            time.sleep(30)
            logger.info("La fenêtre de téléchargement a été fermée.")
        except Exception as e:
            logger.error(f"Une erreur s'est produite lors de la fermeture de la fenêtre de téléchargement: {e}")
            return
    except Exception as e:
        logger.error(f"Une erreur s'est produite lors de l'enregistrement du rapport : {e}")
        return
    deplace_et_renomme_rapport(nom_rapport)


def traitement_rapport_apercu(nom_rapport):
    # Code pour traiter le rapport "Aperçu"
    logger.info(f"Traitement du rapport {nom_rapport}")
    # Ajoutez ici le code spécifique pour traiter le rapport "Aperçu"
    try:
        # Attendre que l'élément soit présent
        selection_rapport_button = WebDriverWait(driver=driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='ember7']/clarity-sidebar/clarity-navigation-list/ul/clarity-navigation-list-item[1]/clarity-button/button"))
        )
        # Interagir avec l'élément
        selection_rapport_button.click()
        time.sleep(2)
        telechargement_rapport(nom_rapport)
    except Exception as e:
        logger.error(f"Une erreur s'est produite lors de la sélection du rapport {nom_rapport} : {e}")
        return

def traitement_rapports_modeles(nom_rapport):
    # Code pour traiter les rapports "Modèles"
    # Il y a une possibilité de 3 rapports
    logger.info(f"Traitement des rapport {nom_rapport}")
    # Ajoutez ici le code spécifique pour traiter le rapport "Modèles"
    # Attendre que le bouton du rapport soit présent et cliquable via un attribut data-test ou le texte du bouton
    
    # Affichage de la page des rapports modèles
    try:
        # Exemple robuste : sélectionne le bouton par le texte visible (à adapter selon le rapport)
        xpath_rapport = f"//button[normalize-space()='{nom_rapport}']"
        selection_rapport_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, xpath_rapport))
        )
        # Faire défiler jusqu'au bouton pour s'assurer qu'il est visible
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", selection_rapport_button)
        time.sleep(1)
        try:
            selection_rapport_button.click()
        except Exception:
            # Si le clic classique échoue, utiliser JS
            driver.execute_script("arguments[0].click();", selection_rapport_button)
        time.sleep(2)
    except Exception as e:
        logger.error(f"Une erreur s'est produite lors de la page des rapports {nom_rapport} : {e}")
        return
    
    # Traitement du rapport Modèles de base
    # Exemple robuste : sélectionne le bouton par le texte visible dans le span interne
    nom_rapport = "Modeles"
    logger.info(f"Traitement des rapport {nom_rapport}")
    xpath_rapport = "//a[contains(@href, '/patterns/bestDay')]//button[contains(@class, 'bestDay')]"
    selection_rapport_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, xpath_rapport))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", selection_rapport_button)
    time.sleep(1)
    try:
        selection_rapport_button.click()
    except Exception:
        driver.execute_script("arguments[0].click();", selection_rapport_button)
    time.sleep(2)

    # Vérifier que le bouton est bien actif via la classe "active" sur le <a>
    xpath_actif = "//a[contains(@href, '/patterns/bestDay') and contains(@class, 'active')]"
    if driver.find_elements(By.XPATH, xpath_actif):
        logger.info("Le bouton du rapport 'Meilleure journée' est bien actif (en surbrillance). Téléchargement en cours.")
        telechargement_rapport("Modeles")
    else:
        logger.warning("Le bouton du rapport 'Meilleure journée' n'est pas actif après le clic. Téléchargement annulé.")

       # Traitement du rapport Modèles Haut le jour
    try:
        # Exemple robuste : sélectionne le bouton par le texte visible (à adapter selon le rapport)
        nom_rapport = "Modele-Haut-le-Jour"
        logger.info(f"Traitement du rapport {nom_rapport}")
        # Sélectionne le bouton par le texte visible dans le span interne
        # Vérifier l'existence du bouton du rapport "Hauts le jour"
        xpath_rapport = "//button[contains(@class, 'daytimeHighs') and .//span[@class='mdc-button__label' and normalize-space()='Hauts le jour']]"
        boutons = driver.find_elements(By.XPATH, xpath_rapport)
        if boutons:
            logger.info("Le rapport 'Hauts le jour' existe, traitement en cours.")
            selection_rapport_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, xpath_rapport))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", selection_rapport_button)
            time.sleep(1)
            try:
                selection_rapport_button.click()
            except Exception:
                driver.execute_script("arguments[0].click();", selection_rapport_button)
            time.sleep(2)
            # Vérifier que le bouton est bien en surbrillance (classe CSS 'mdc-button--active' par exemple)
            if "mdc-button--active" in selection_rapport_button.get_attribute("class"):
                logger.info("Le bouton du rapport 'Hauts le jour' est bien actif (en surbrillance). Téléchargement en cours.")
                telechargement_rapport("Modele-Haut-le-Jour")
            else:
                logger.warning("Le bouton du rapport 'Hauts le jour' n'est pas actif après le clic. Téléchargement annulé.")
        else:
            logger.info("Le rapport 'Hauts le jour' n'existe pas, aucun traitement effectué.")
    except Exception as e:
        logger.error(f"Une erreur s'est produite lors de la sélection du rapport 'Hauts le jour' : {e}")
        return

def traitement_rapport_superposition(nom_rapport):
    # Code pour traiter le rapport "Superposition"
    logger.info(f"Traitement du rapport {nom_rapport}")
    # Ajoutez ici le code spécifique pour traiter le rapport "Superposition"

def traitement_rapport_quotidien(nom_rapport):
    # Code pour traiter le rapport "Quotidien"
    logger.info(f"Traitement du rapport {nom_rapport}")
    # Ajoutez ici le code spécifique pour traiter le rapport "Quotidien"

def traitement_rapport_comparer(nom_rapport):
    # Code pour traiter le rapport "Comparer"
    logger.info(f"Traitement du rapport {nom_rapport}")
    # Ajoutez ici le code spécifique pour traiter le rapport "Comparer"

def traitement_rapport_statistiques(nom_rapport):
    # Code pour traiter le rapport "Statistiques"
    logger.info(f"Traitement du rapport {nom_rapport}")
    # Ajoutez ici le code spécifique pour traiter le rapport "Statistiques"

def traitement_rapport_agp(nom_rapport):
    # Code pour traiter le rapport "AGP"
    logger.info(f"Traitement du rapport {nom_rapport}")
    # Ajoutez ici le code spécifique pour traiter le rapport "AGP"

def selection_rapport(rapports):
    # Code pour traiter les rapports
    for rapport in rapports:
        if rapport == "Aperçu":
            # Code pour traiter le rapport "Aperçu"
            traitement_rapport_apercu(rapport)
        elif rapport == "Modèles":
            # Code pour traiter le rapport "Modèles"
            traitement_rapports_modeles(rapport)
        elif rapport == "Superposition":
            # Code pour traiter le rapport "Superposition"
            logger.info("Traitement du rapport Superposition")
            traitement_rapport_superposition(rapport)
        elif rapport == "Quotidien":
            # Code pour traiter le rapport "Quotidien"
            logger.info("Traitement du rapport Quotidien")
            traitement_rapport_quotidien(rapport)
        elif rapport == "Comparer":
            # Code pour traiter le rapport "Comparer"
            logger.info("Traitement du rapport Comparer")
            traitement_rapport_comparer(rapport)
        elif rapport == "Statistiques":
            # Code pour traiter le rapport "Statistiques"
            logger.info("Traitement du rapport Statistiques")
            traitement_rapport_statistiques(rapport)
        elif rapport == "AGP":
            # Code pour traiter le rapport "AGP"
            logger.info("Traitement du rapport AGP")
            traitement_rapport_agp(rapport)

if args.debug:
    logger.debug(f"Version de Python : {sys.version}")
    logger.debug(f"Rapports à traiter : {rapports}")


logger.info(f"Dossier de téléchargement : {download_dir}")

# Vérification de la connexion internet avant d'ouvrir la page
if not check_internet():
    logger.error("Perte de connexion internet détectée avant l'ouverture de la page Dexcom Clarity.")
    logger.info("Arrêt du script suite à une perte de connexion internet.")
    try:
        driver.quit()
    except Exception:
        pass
    sys.exit(0)

# Ouvrir la page de connexion
driver.get(url)

# Attendez que la page soit entièrement chargée
wait = WebDriverWait(driver=driver, timeout=60)  # Augmenté à 60s

# Vérification de la connexion internet avant de cliquer sur le bouton d'accueil
if not check_internet():
    logger.error("Perte de connexion internet détectée avant de cliquer sur le bouton d'accueil.")
    logger.info("Arrêt du script suite à une perte de connexion internet.")
    driver.quit()
    sys.exit(1)

# Recherchez et cliquez sur le bouton "Dexcom Clarity pour les utilisateurs à domicile"
try:
    bouton = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@value='Dexcom Clarity pour les utilisateurs à domicile']")))
    bouton.click()
    time.sleep(5)  # Augmenté à 5s
    logger.info("Le bouton pour utilisateurs à domicile a été cliqué avec succès!")
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

    if date_debut is None or date_fin is None:
        raise ValueError("Les variables date_debut et date_fin ne peuvent pas être None. Elles doivent être définies.")

    date_debut_input = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.NAME, "start_date"))
    )
    date_fin_input = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.NAME, "end_date"))
    )
    date_debut_input.clear()
    date_fin_input.clear()
    date_debut_input.send_keys(date_debut)
    date_fin_input.send_keys(date_fin)

    ok_button = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-test-date-range-picker__ok-button]"))
    )
    ok_button.click()
    logger.debug("Bouton OK du sélecteur de dates cliqué.")
    time.sleep(5)  # Augmenté à 5s

    logger.info(f"Date de début: {date_debut}")
    logger.info(f"Date de fin: {date_fin}")
    logger.info("Les dates ont été saisies avec succès !")

except Exception as e:
    if not check_internet():
        logger.error("Perte de connexion internet détectée lors de la saisie des dates.")
    logger.error(f"Une erreur s'est produite lors de la saisie des dates : {e}")

# Téléchargez les rapports
selection_rapport(rapports)

# Attendez un peu pour vous assurer que le téléchargement est terminé
time.sleep(120)  # Augmenté à 120s

# (optionnel) Derniers diagnostics AVANT de quitter
boutons = driver.find_elements(By.XPATH, "//button")
logger.info(f"{len(boutons)} boutons trouvés sur la page")
for b in boutons:
    logger.debug(b.get_attribute("outerHTML"))

# Fermez le navigateur
driver.quit()
