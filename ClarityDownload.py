#'''////////////////////////////////////////////////////////////////////////////////////////////////////
#'''<summary>
#'''FileName: ClarityDownload.py
#'''FileType: py Source file
#'''
#'''Author : Pierre Théberge
#'''Created On : 2025-03-03
#'''Last Modified On : 2025-03-20
#'''CopyRights : Innovations Performances Technologies inc
#'''Description : Programme pour télécharger les différents rapports provenant de Clarity ainsi que les relevés bruts
#'''Version : 0.0.2
#'''Modifications :
#'''Version   Date          Description
#'''0.0.0	2025-03-03    Version initiale.
#'''0.0.1	2025-03-07    Connectoin à Clarity et authentification
#''                       Utilisation de Chrome au lieu de Edge
#'''0.0.2   2025-03-20    Cliquer sur le sélecteur de dates
#'''</summary>
#'''/////////////////////////////////////////////////////////////////////////////////////////////////////

## TODO 1 Installer edgedriver sur mes 2 ordis. portable et bureau. Version 134.0.3124.39 
## TODO 1.1 Installer ChromeDriver sur mes 2 ordis. portable et bureau. Version 110.0.5481.177
## TODO 2 Ajouter le path \\ADMIN06\Download\Microsoft\EdgeDriver dans la variable d'environnement
## TODO 3 Pour désactiver la collecte de données de diagnostic pour Microsoft Edge WebDriver, définissez la variable d’environnement sur MSEDGEDRIVER_TELEMETRY_OPTOUT1
## TODO 4 Ajouter le chemin d'environnement: 'C:\Users\thebe\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts'

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import uuid

date_debut = "2025-01-01"
date_fin = "2025-01-14"

# Chemin vers ChromeDriver (assurez-vous de le modifier en fonction de l'emplacement de votre ChromeDriver)
#driver_path = 'path_to_chromedriver'
service = ChromeService()
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=C:/Users/thebe/AppData/Local/Google/Chrome/User Data/ClarityDownloadProfile")

# Ajoutez un argument unique pour éviter les conflits de session
unique_profile = f"C:/Users/thebe/AppData/Local/Google/Chrome/User Data/ClarityDownloadProfile_{uuid.uuid4()}"
options.add_argument(f"--user-data-dir={unique_profile}")

driver = webdriver.Chrome(service=service, options=options)

# URL de la page Dexcom Clarity
## TODO 5 Ajouter l'url de la page de Login de Clarity
url = "https://clarity.dexcom.eu/?&locale=fr-CA"
driver.get(url)

# Attendez que la page soit entièrement chargée
wait = WebDriverWait(driver, 10)

# Recherchez et cliquez sur le bouton "Dexcom Clarity pour les utilisateurs à domicile"
try:
    bouton = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@value='Dexcom Clarity pour les utilisateurs à domicile']")))
    bouton.click()
    print("Le bouton a été cliqué avec succès!")
except Exception as e:
    print(f"Une erreur s'est produite : {e}")

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

    print("Connexion réussie !")
except Exception as e:
    print(f"Une erreur s'est produite lors de la connexion : {e}")

# Attendez que la page soit entièrement chargée
wait = WebDriverWait(driver, 15)

## TODO 6 Choisir les dates de début et de fin pour les rapports.
# Recherchez les champs de saisie des dates et entrez les nouvelles dates
try:
    # Attendre que l'élément soit présent
    date_picker_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='ember12']/div/div/date-range-picker/div"))
    )
    # Interagir avec l'élément
    date_picker_button.click()

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

    print("Les dates ont été saisies avec succès !")

except Exception as e:
    print(f"Une erreur s'est produite lors de la saisie des dates : {e}")
##TODO 7 Créer une fonction pour le téléchargement de chacun des rapports et le téléchargement des données brutes

##TODO 8 Créer une fonction pour la sauvegarde des rapports et des données brutes

# Attendez un peu pour vous assurer que le téléchargement est terminé
time.sleep(10)

# Fermez le navigateur
#driver.quit()
