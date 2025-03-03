#'''////////////////////////////////////////////////////////////////////////////////////////////////////
#'''<summary>
#'''FileName: ClarityDownload.py
#'''FileType: py Source file
#'''
#'''Author : Pierre Théberge
#'''Created On : 2025-03-03
#'''Last Modified On : 2025-03-03
#'''CopyRights : Innovations Performances Technologies inc
#'''Description : Programme pour télécharger les différents rapports provenant de Clarity ainsi que les relevés bruts
#'''Version : 0.0.0
#'''Modifications :
#'''Version   Date          Description
#'''0.0.0	2025-03-03    Version initiale.
#'''</summary>
#'''/////////////////////////////////////////////////////////////////////////////////////////////////////

## TODO 1 Installer edgedriver sur mes 2 ordis. portable et bureau. Version 134.0.3124.39 
## TODO 2 Ajouter le path \\ADMIN06\Microsoft\EdgeDriver dans la variable d'environnement
## TODO 3 Pour désactiver la collecte de données de diagnostic pour Microsoft Edge WebDriver, définissez la variable d’environnement sur MSEDGEDRIVER_TELEMETRY_OPTOUT1
## TODO 4 Ajouter le chemin d'environnement: 'C:\Users\thebe\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Chemin vers EdgeDriver (assurez-vous de le modifier en fonction de l'emplacement de votre EdgeDriver)
driver_path = '\\ADMIN06\Microsoft\EdgeDriver'
driver = webdriver.Edge(driver_path)

# URL de la page Dexcom Clarity
## TODO 5 Ajouter l'url de la page de Login de Clarity
url = 'https://clarity.dexcom.eu/#/agp?dates=2024-08-05%2F2024-08-19'
driver.get(url)

# Attendez que la page soit entièrement chargée
wait = WebDriverWait(driver, 10)

# Connectez-vous si nécessaire (vous devrez peut-être adapter cette partie du code en fonction de la page de connexion)
# Par exemple :
# username_input = wait.until(EC.presence_of_element_located((By.ID, 'username')))
# username_input.send_keys('your_username')
# password_input = wait.until(EC.presence_of_element_located((By.ID, 'password')))
# password_input.send_keys('your_password')
# login_button = wait.until(EC.element_to_be_clickable((By.ID, 'login_button')))
# login_button.click()

## TODO 6 Demander à l'usager les dates de début et de fin pour les rapports.
# Attendez que l'icône de téléchargement soit présente et cliquez dessus
download_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'selector_of_download_icon')))
download_icon.click()

##TODO 7 Créer une fonction pour le téléchargement de chacun des rapports et le téléchargement des données brutes

##TODO 8 Créer une fonction pour la sauvegarde des rapports et des données brutes

# Attendez un peu pour vous assurer que le téléchargement est terminé
time.sleep(5)

# Fermez le navigateur
driver.quit()
