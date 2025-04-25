#'''////////////////////////////////////////////////////////////////////////////////////////////////////
#'''<summary>
#'''FileName: ClarityDownload.py
#'''FileType: py Source file
#'''
#'''Author : Pierre Théberge
#'''Created On : 2025-03-03
#'''Last Modified On : 2025-04-24
#'''CopyRights : Innovations Performances Technologies inc
#'''Description : Programme pour télécharger les différents rapports provenant de Clarity ainsi que les relevés bruts
#'''Version : 0.0.7
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
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import uuid

# Définition du log
logger = logging.getLogger('selenium')
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.ERROR)



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

# Initialisation du WebDriver
driver = webdriver.Chrome(service=service, options=options)

# URL de la page Dexcom Clarity
url = "https://clarity.dexcom.eu/?&locale=fr-CA"

def telechargement_rapport():
    logger.setLevel(logging.DEBUG)
    # Code pour telecharger le rapport
    print("Telechargement du rapport")
    # Ajoutez ici le code spécifique pour telecharger le rapport
    try:
        # Attendre que l'élément soit recréé
        WebDriverWait(driver=driver, timeout=20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "clarity-icon-button:nth-child(2)"))
        )
        selection_rapport_download_button = driver.find_element(By.CSS_SELECTOR, "clarity-icon-button:nth-child(2)")
        selection_rapport_download_button.click()
        time.sleep(4)
        print("Le bouton télécharger a été cliqué avec succès!")
    except Exception as e:
        print(f"Une erreur s'est produite lors du clique sur le bouton de télécharger : {e}")
        return
    # Choisir le rapport en couleur
#    try:
#        # Attendre que l'élément soit recréé
#        WebDriverWait(driver=driver, timeout=10).until(
#            EC.element_to_be_clickable((By.XPATH, "//*[@id='ember95']"))
#        )
#        selection_mode_couleur_button = driver.find_element(By.XPATH, "//*[@id='ember95']")
#        selection_mode_couleur_button.click()
#        time.sleep(2)
#        print("Le mode couleur a été sélectionné avec succès!")
#    except Exception as e:
#        print(f"Une erreur s'est produite lors de la sélection du mode couleur : {e}")
#        return
    # Cliquer sur le bouton Enregistrer le rapport
    try:
        # Attendre que l'élément soit recréé
        WebDriverWait(driver=driver, timeout=10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='ember108']/div/p[4]/button[1]"))
        )
        enregistrer_rapport_button = driver.find_element(By.XPATH, "//*[@id='ember108']/div/p[4]/button[1]")
        enregistrer_rapport_button.click()
        time.sleep(5)
        print("Le bouton Enregistrer le rapport a été cliqué avec succès!")
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'enregistrement du rapport : {e}")
        return

    logger.setLevel(logging.ERROR)

def traitement_rapport_apercu():
    # Code pour traiter le rapport "Aperçu"
    print("Traitement du rapport Aperçu")
    # Ajoutez ici le code spécifique pour traiter le rapport "Aperçu"
    try:
        # Attendre que l'élément soit présent
        selection_rapport_button = WebDriverWait(driver=driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='ember7']/clarity-sidebar/clarity-navigation-list/ul/clarity-navigation-list-item[1]/clarity-button/button"))
        )
        # Interagir avec l'élément
        selection_rapport_button.click()
        time.sleep(2)
    except Exception as e:
        print(f"Une erreur s'est produite lors de la sélection du rapport Aperçu : {e}")
        return
    telechargement_rapport()

def traitement_rapport_modeles():
    # Code pour traiter le rapport "Modèles"
    print("Traitement du rapport Modèles")
    # Ajoutez ici le code spécifique pour traiter le rapport "Modèles"

def traitement_rapport_superposition():
    # Code pour traiter le rapport "Superposition"
    print("Traitement du rapport Superposition")
    # Ajoutez ici le code spécifique pour traiter le rapport "Superposition"

def traitement_rapport_quotidien():
    # Code pour traiter le rapport "Quotidien"
    print("Traitement du rapport Quotidien")
    # Ajoutez ici le code spécifique pour traiter le rapport "Quotidien"

def traitement_rapport_comparer():
    # Code pour traiter le rapport "Comparer"
    print("Traitement du rapport Comparer")
    # Ajoutez ici le code spécifique pour traiter le rapport "Comparer"

def traitement_rapport_statistiques():
    # Code pour traiter le rapport "Statistiques"
    print("Traitement du rapport Statistiques")
    # Ajoutez ici le code spécifique pour traiter le rapport "Statistiques"

def traitement_rapport_agp():
    # Code pour traiter le rapport "AGP"
    print("Traitement du rapport AGP")
    # Ajoutez ici le code spécifique pour traiter le rapport "AGP"

def selection_rapport(rapports):
    # Code pour traiter les rapports
    for rapport in rapports:
        if rapport == "Aperçu":
            # Code pour traiter le rapport "Aperçu"
            traitement_rapport_apercu()
        elif rapport == "Modèles":
            # Code pour traiter le rapport "Modèles"
            print("Traitement du rapport Modèles")
            traitement_rapport_modeles()
        elif rapport == "Superposition":
            # Code pour traiter le rapport "Superposition"
            print("Traitement du rapport Superposition")
            traitement_rapport_superposition()
        elif rapport == "Quotidien":
            # Code pour traiter le rapport "Quotidien"
            print("Traitement du rapport Quotidien")
            traitement_rapport_quotidien()
        elif rapport == "Comparer":
            # Code pour traiter le rapport "Comparer"
            print("Traitement du rapport Comparer")
            traitement_rapport_comparer()
        elif rapport == "Statistiques":
            # Code pour traiter le rapport "Statistiques"
            print("Traitement du rapport Statistiques")
            traitement_rapport_statistiques()
        elif rapport == "AGP":
            # Code pour traiter le rapport "AGP"
            print("Traitement du rapport AGP")
            traitement_rapport_agp()

print(f"Version de Python : {sys.version}")

# Ouvrir la page de connexion
driver.get(url)

# Attendez que la page soit entièrement chargée
wait = WebDriverWait(driver=driver, timeout=10)

# Recherchez et cliquez sur le bouton "Dexcom Clarity pour les utilisateurs à domicile"
try:
    bouton = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@value='Dexcom Clarity pour les utilisateurs à domicile']")))
    bouton.click()
    time.sleep(2)
    print("Le bouton pour utilisateurs à domicile a été cliqué avec succès!")
except Exception as e:
    print(f"Une erreur s'est produite au moment de cliquer sur le bouton pour utilisateurs à domicile : {e}")

# Recherchez les champs de saisie pour le courriel/nom d'utilisateur et le mot de passe
try:
    # Remplacez par les valeurs correctes pour les attributs id ou name
    username_input = driver.find_element(By.NAME, "username")  # Assurez-vous que l'attribut name est correct
    password_input = driver.find_element(By.NAME, "password")  # Assurez-vous que l'attribut name est correct

    # Entrez votre nom d'utilisateur et mot de passe à partir des variables d'environnement
    dexcom_username = os.getenv("DEXCOM_USERNAME")
    dexcom_password = os.getenv("DEXCOM_PASSWORD")

    if dexcom_username is None or dexcom_password is None:
        raise ValueError("Les variables d'environnement DEXCOM_USERNAME et DEXCOM_PASSWORD doivent être définies.")

    username_input.send_keys(dexcom_username)
    password_input.send_keys(dexcom_password)

    # Recherchez le bouton de connexion et cliquez dessus
    login_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Se connecter']")  # Assurez-vous que l'attribut value est correct
    login_button.click()
    time.sleep(2)

    print("Connexion réussie !")
except Exception as e:
    print(f"Une erreur s'est produite lors de la connexion : {e}")

# Attendez que la page soit entièrement chargée
time.sleep(5)

# Recherchez les champs de saisie des dates et entrez les nouvelles dates
try:
    # Attendre que l'élément soit présent
    date_picker_button = WebDriverWait(driver=driver, timeout=10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='ember12']/div/div/date-range-picker/div"))
    )
    # Interagir avec l'élément
    date_picker_button.click()
    time.sleep(2)

    if date_debut is None or date_fin is None:
        raise ValueError("Les variables date_debut et date_fin ne peuvent pas être None. Elles doivent être définies.")

    date_debut_input = driver.find_element(By.NAME, "start_date")
    date_fin_input = driver.find_element(By.NAME, "end_date")
    date_debut_input.clear()
    date_fin_input.clear()
    date_debut_input.send_keys(date_debut)
    date_fin_input.send_keys(date_fin)

    # Recherchez le bouton "OK" et cliquez dessus
    ok_button = driver.find_element(By.XPATH, "//*[@id='ember12']/div/div/date-range-picker/div[2]/p/button[1]")  # Assurez-vous que le texte est correct
    ok_button.click()
    time.sleep(4)

    print("Date de début: ", date_debut)
    print("Date de fin: ", date_fin)
    print("Les dates ont été saisies avec succès !")

except Exception as e:
    print(f"Une erreur s'est produite lors de la saisie des dates : {e}")

# Téléchargez les rapports
selection_rapport(rapports)

##TODO 8 Créer une fonction pour la sauvegarde des rapports et des données brutes

# Attendez un peu pour vous assurer que le téléchargement est terminé
time.sleep(100)

# Fermez le navigateur
driver.quit()
