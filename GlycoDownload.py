#'''////////////////////////////////////////////////////////////////////////////////////////////////////
#'''<summary>
#'''FileName: GlycoDownload.py
#'''FileType: py Source file
#'''
#'''Author : Pierre Théberge
#'''Created On : 2025-03-03
#'''Last Modified On : 2025-10-16
#'''CopyRights : Pierre Théberge
#'''Description : Script principal pour l'automatisation du téléchargement des rapports Dexcom Clarity.
#'''              Centralisation de la configuration, gestion CLI avancée, robustesse accrue,
#'''              logs détaillés (console, fichier, JS), gestion des exceptions et de la déconnexion.
#'''Version : 0.2.6
#'''Modifications :
#'''Version   Date         Billet   Description
#'''0.0.0   2025-03-03    -        Version initiale.
#'''0.0.1	2025-03-07    -        Connectoin à Clarity et authentification
#''                       -            Utilisation de Chrome au lieu de Edge
#'''0.0.2   2025-03-20    -        Cliquer sur le sélecteur de dates et choisir la période
#'''0.0.3   2025-03-28    -        Ajout du traitement des rapports
#'''0.0.4   2025-04-07    -        Conversion à Python 3.13 et une erreur de syntaxe dans le code de la fonction traitement_rapport_apercu
#'''0.0.5   2025-04-11    -        Ajout de la sélection du rapport Apercu
#'''0.0.6   2025-04-16    -        Ajout du code pour télécharger un rapport.
#'''                      -            Reste à cliquer sur les boutons télécharger le rapport et
#'''                      -            enregistrer sous.
#'''0.0.7   2025-04-24    -        Retour à Python 3.12. Besoin Tensorflow et il n'est pas supporté par Python 3.13
#'''                      -            Cliquer sur le bouton "Enregistrer le rapport"
#'''                      -            Enlever la sélection du mode couleur (problème à avoir le bon xpath)
#'''0.0.8   2025-05-23    -        Terminé la fonction téléchargement_rapport
#'''                      -            Ajout de la fonction deplace_et_renomme_rapport
#'''                      -            Reconversion à Python 3.13
#'''0.0.9   2025-07-01    -        Ajout de l'option debug et ajout d'un fichier de log
#'''0.0.10  2025-07-02    -        Modification pour tenir compte d'une connexion internet lente et instable (4mb/s)Ajout de la fonction traitement_rapport
#'''                      -            Ajout de la fonction check_internet pour vérifier la connexion internet
#'''                      -            Ajout du traitement pour les rapports Modèles
#'''                      -            Dans la fonction deplace_et_renomme_rapport, ne pas tenir compte des fichiers *.log
#'''0.0.11  2025-07-03    -        La vérification de la connexion internet ne fonctionne pas avec NordVPN
#'''                      -            Ajout du traitement pour le rapport Superposition
#'''                      -            Rendre plus robuste le traitement du rapport Aperçu
#'''                      -            Ajout du traitement pour le rapport Quotidien
#'''                      -            Ajout du traitement pour le rapport AGP
#'''0.0.12  2025-07-08    -        Ajout du traitement pour le rapport Statistiques
#'''0.0.13  2025-07-13    -        Ajout du traitement pour le rapport Comparer
#'''0.0.14  2025-07-18    -        Ajout de l'exportation des données en format csv
#'''0.0.15  2025-07-21    -        Terminer la fonction traitement_export_csv
#'''                      -            Ajout des sous-rapport pour le rapport Comparer
#'''                      -            Les sous-rapports Superposition et Quotidien de comparer ne fonctioone pas.
#'''                      -                Ils produisent le même PDF que Tendances.
#'''                      -        Ajouter la déconnexion du compte avant de fermer le navigateur
#'''0.0.16  2025-07-25    -        Correction pour la déconnexion du compte
#'''                      -            Correction pour le bouton Fermer de la fenêtre modale Exporter
#'''0.0.17  2025-07-25    -        Correction pour le déconnexion du compte. Éliminer la référence au nom d'utilisateur.
#'''                      -            Ajout de TODO pour la correction du code.
#'''0.0.18  2025-07-30    -        Gestion des exceptions plus précise. Évite les except: nus. Précise toujours le type d'exception
#'''                      -            Factorisation des attentes sur les overlays/loaders. Crée une fonction utilitaire
#'''                      -                pour attendre la disparition des overlays, et utilise-la partout où c'est pertinent.
#'''                      -            Centralisation des paramètres et chemins. Définis tous les chemins, URLs, et paramètres en haut du script ou dans un fichier de config.
#'''                      -            Ajout d'une fonction main()
#'''                      -            Fermeture du navigateur dans un finally
#'''0.0.19  2025-08-04    -        Ajout de docstrings pour toutes les fonctions
#'''                      -            Logging cohérent. Utilise le logger pour tous les messages (pas de print).
#'''0.0.20  2025-08-05    -        Ajout d'une validation pour la présende des variables d'environnement nécessaires
#'''                      -            Crée un fichier config.py pour centraliser tous les paramètres, chemins, URLs, etc.
#'''                      -            Crée un fichier utils.py pour toutes les fonctions utilitaires (connexion internet, overlay, renommage, etc.).
#'''                      -            Crée un fichier rapports.py pour le traitement des rapports
#'''0.0.21  2025-08-06    -        Ajout d'un exemple de fichier de configuration "config_example.yaml"
#'''0.0.22  2025-08-13    -        Centralisation et normalisation des chemins, gestion CLI améliorée,
#'''                      -            logs JS navigateur, robustesse accrue sur la gestion des erreurs,
#'''                      -            factorisation des utilitaires, gestion propre des exceptions et de la déconnexion.
#'''0.0.23  2025-08-13    -        Capture d'écran centralisée via utils.py, délai avant capture,
#'''                      -            suppression des duplications de code, ajout de logs pour le diagnostic.
#'''0.1.0   2025-08-18    -        Robustesse saisie identifiant : sélection usernameLogin, vérification visibilité/interactivité,
#'''                      -            captures d'écran uniquement en mode debug, gestion du bouton 'Pas maintenant' après connexion,
#'''                      -            adaptation aux changements d'interface Dexcom, logs détaillés pour le diagnostic.
#'''0.1.1   2025-09-03             Ajout des logs.
#'''0.1.2   2025-09-04             Vérification des répertoires.
#'''0.1.3   2025-09-05             Correction de la récupération de la date de rapport.
#'''0.1.4   2025-09-05             Renommage du répertoire de sortie.
#'''0.1.5   2025-09-06             Répertoire de sortie dans config.yaml.
#'''0.1.6   2025-09-23             Gestion améliorée de la sélection des jours (days).
#'''0.1.7   2025-10-06             Détermination automatique de la version de chromedriver.
#'''0.2.0   2025-10-07             Réorganisation complète de la structure en modules.
#'''0.2.1   2025-10-09    ES-5     Ajout de la langue dans les arguments en CLI et au rapport.
#'''0.2.2   2025-10-11    ES-6     Les rapports sont indépendants de la langue de l'utilisateur.
#'''0.2.3   2025-10-14    ES-11    Ajout du rapport Statistiques horaires et amélioration de la robustesse d'accès aux rapports.
#'''                       ES-11    Utilisation de ChromeDriverManager pour télécharger automatiquement la bonne version de ChromeDriver.
#'''0.2.4   2025-10-16    ES-12    Synchronisation de version (aucun changement fonctionnel).
#'''0.2.5   2025-10-16    ES-10    Synchronisation de version (aucun changement fonctionnel).
#'''0.2.6   2025-10-21    ES-7     Amélioration du système d'aide (--help) avec description détaillée, exemples et groupes d'arguments.
#'''                      ES-7     Ajout de l'option --list-rapports pour afficher la liste des rapports disponibles.
#'''                      ES-7     Ajout de l'option --dry-run pour tester la configuration sans télécharger.
#'''                      ES-7     Ajout de la validation des dates avec messages d'erreur clairs.
#'''0.2.7   2025-10-27    ES-16    Ajout de la gestion des erreurs 502 (Bad Gateway) avec retry automatique.
#'''                      ES-16    Attente et réessai automatique (3 tentatives max) en cas d'erreur serveur temporaire.
#'''                      ES-16    Suivi et rapport des échecs de téléchargement avec raisons détaillées.
#'''                      ES-16    Amélioration de la robustesse face aux problèmes temporaires du serveur Dexcom.
#''' </summary>
#'''/////////////////////////////////////////////////////////////////////////////////////////////////////

# TODO 11 Réparer le problème avec les rapports Comparer
# TODO 12 Exécuter l'application pour produire les rapports Comparer depuis 2024-08-19
# TODO 13 Appliquer la même solution pour obtenir des rapports séparés pour Modèle
# TODO 14 Rendre l'application indépendante de la langue de l'utilisateur.
# TODO 15 Améliorer le help

import sys
import argparse
import os
import logging
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
from webdriver_manager.chrome import ChromeDriverManager

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

# --- Gestion des arguments CLI et du help ---
def parse_args():
    """Parse les arguments de la ligne de commande."""
    import argparse
    from version import __version__
    
    description = """
GlycoReport Downloader v{version} - Téléchargement automatisé des rapports Dexcom Clarity

Ce script automatise le téléchargement des rapports glycémiques depuis votre compte
Dexcom Clarity. Il supporte plusieurs types de rapports, périodes personnalisables,
et exporte les données en PDF ou CSV.

Pour plus d'informations : https://github.com/pierrethb/GlycoReport-Downloader
    """.format(version=__version__)
    
    epilog = """
Exemples d'utilisation :
  Télécharger tous les rapports des 14 derniers jours (par défaut) :
    python GlycoDownload.py
    
  Télécharger uniquement le rapport Aperçu des 7 derniers jours :
    python GlycoDownload.py --days 7 --rapports "Aperçu"
    
  Télécharger plusieurs rapports pour une période spécifique :
    python GlycoDownload.py --date_debut 2025-01-01 --date_fin 2025-01-31 --rapports "Aperçu" "AGP"
    
  Mode debug avec tous les rapports des 30 derniers jours :
    python GlycoDownload.py --debug --days 30
    
  Simuler l'exécution sans télécharger (afficher la configuration) :
    python GlycoDownload.py --dry-run --days 7 --rapports "AGP"

Rapports disponibles : Aperçu, Modèles, Superposition, Quotidien, Comparer, Statistiques, AGP, Export
(Utilisez --list-rapports pour plus de détails)

Configuration :
  - Fichier : config.yaml (créé automatiquement au premier lancement)
  - Identifiants : .env (chiffré, nécessite la variable ENV_DEXCOM_KEY)
  - Logs : définis dans config.yaml (log_retention_days)

Pour toute question ou signalement de bug : GitHub Issues
    """
    
    parser = argparse.ArgumentParser(
        prog='GlycoReport-Downloader',
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Groupe des options générales
    general_group = parser.add_argument_group('options générales')
    general_group.add_argument(
        '--version', '-v',
        action='version',
        version=f'GlycoReport Downloader v{__version__}',
        help='Afficher la version et quitter'
    )
    general_group.add_argument(
        '--debug', '-d',
        action='store_true',
        help='Activer le mode debug (logs détaillés, captures d\'écran)'
    )
    general_group.add_argument(
        '--dry-run',
        action='store_true',
        help='Simuler l\'exécution sans télécharger (affiche la configuration)'
    )
    
    # Groupe des options de période
    period_group = parser.add_argument_group(
        'période des rapports',
        'Définir la période de téléchargement (par défaut : 14 derniers jours)'
    )
    period_group.add_argument(
        '--days',
        type=int,
        choices=[7, 14, 30, 90],
        metavar='N',
        help='Nombre de jours à inclure (7, 14, 30 ou 90)'
    )
    period_group.add_argument(
        '--date_debut',
        type=str,
        metavar='AAAA-MM-JJ',
        help='Date de début au format AAAA-MM-JJ (ex: 2025-01-01)'
    )
    period_group.add_argument(
        '--date_fin',
        type=str,
        metavar='AAAA-MM-JJ',
        help='Date de fin au format AAAA-MM-JJ (ex: 2025-01-31)'
    )
    
    # Groupe des options de rapports
    reports_group = parser.add_argument_group(
        'sélection des rapports',
        'Choisir les rapports à télécharger (par défaut : tous les rapports configurés)'
    )
    reports_group.add_argument(
        '--rapports',
        nargs='+',
        metavar='RAPPORT',
        help='Liste des rapports (ex: "Aperçu" "AGP" "Statistiques")'
    )
    reports_group.add_argument(
        '--list-rapports',
        action='store_true',
        help='Afficher la liste des rapports disponibles et quitter'
    )
    
    return parser, parser.parse_args()


def list_available_reports():
    """Affiche la liste des rapports disponibles avec leurs descriptions."""
    from colorama import Fore, Style, init
    init(autoreset=True)
    
    reports = {
        "Aperçu": "Vue d'ensemble de la glycémie sur la période sélectionnée",
        "Modèles": "Analyse des tendances et modèles glycémiques récurrents",
        "Superposition": "Superposition des jours pour identifier les patterns",
        "Quotidien": "Détail jour par jour de la glycémie",
        "Comparer": "Comparaison de différentes périodes (3 sous-rapports)",
        "Statistiques": "Statistiques détaillées quotidiennes et horaires (2 sous-rapports)",
        "AGP": "Profil glycémique ambulatoire (Ambulatory Glucose Profile)",
        "Export": "Export des données brutes au format CSV"
    }
    
    print(f"\n{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Rapports disponibles - GlycoReport Downloader{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}\n")
    
    for name, desc in reports.items():
        print(f"{Fore.GREEN}• {name:<15}{Style.RESET_ALL} {desc}")
    
    print(f"\n{Fore.YELLOW}Notes :{Style.RESET_ALL}")
    print(f"  • Le rapport 'Comparer' génère 3 fichiers PDF distincts")
    print(f"  • Le rapport 'Statistiques' génère 2 fichiers PDF (quotidien + horaire)")
    print(f"  • Le rapport 'Export' génère un fichier CSV avec toutes les données brutes")
    print(f"\n{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}\n")


def validate_dates(args):
    """Valide les dates fournies en arguments."""
    from datetime import datetime
    from colorama import Fore, Style, init
    init(autoreset=True)
    
    if args.date_debut:
        try:
            datetime.strptime(args.date_debut, "%Y-%m-%d")
        except ValueError:
            print(f"\n{Fore.RED}❌ Erreur : La date de début '{args.date_debut}' n'est pas valide.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Format attendu : AAAA-MM-JJ (ex: 2025-01-15){Style.RESET_ALL}\n")
            sys.exit(1)
    
    if args.date_fin:
        try:
            datetime.strptime(args.date_fin, "%Y-%m-%d")
        except ValueError:
            print(f"\n{Fore.RED}❌ Erreur : La date de fin '{args.date_fin}' n'est pas valide.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Format attendu : AAAA-MM-JJ (ex: 2025-01-31){Style.RESET_ALL}\n")
            sys.exit(1)
    
    if args.date_debut and args.date_fin:
        debut = datetime.strptime(args.date_debut, "%Y-%m-%d")
        fin = datetime.strptime(args.date_fin, "%Y-%m-%d")
        if debut > fin:
            print(f"\n{Fore.RED}❌ Erreur : La date de début ne peut pas être postérieure à la date de fin.{Style.RESET_ALL}\n")
            sys.exit(1)
    
    if args.days and (args.date_debut or args.date_fin):
        print(f"\n{Fore.YELLOW}⚠ Avertissement : --days est ignoré car --date_debut ou --date_fin est spécifié.{Style.RESET_ALL}")


# --- Fonctions utilitaires refactorisées ---
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
def click_home_user_button(driver, logger, log_dir, NOW_STR, timeout=10):
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

def setup_logger(debug, log_dir, now_str):
    # Créer le répertoire de logs s'il n'existe pas
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger('dexcom_clarity')
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    file_handler = logging.FileHandler(os.path.join(log_dir, f"clarity_download_{now_str}.log"))
    file_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


def main(args, logger, config):
    """
    Fonction principale du script GlycoReport-Downloader (refactorisée).
    Gère la connexion, la sélection des dates, le téléchargement des rapports et la déconnexion.
    """
    try:
        # Préparation des variables locales
        debug_mode = args.debug
        rapports = args.rapports or config['RAPPORTS']
        download_dir = config['DOWNLOAD_DIR']
        dir_final_base = config['DIR_FINAL_BASE']
        dexcom_url = config['DEXCOM_URL']
        chromedriver_log = config['CHROMEDRIVER_LOG']
        now_str = config['NOW_STR']
        log_dir = os.path.dirname(chromedriver_log) or "."

        # Gestion intelligente des dates
        if args.days:
            date_fin = datetime.today() - timedelta(days=1)
            date_debut = date_fin - timedelta(days=args.days - 1)
            date_debut_str = date_debut.strftime("%Y-%m-%d")
            date_fin_str = date_fin.strftime("%Y-%m-%d")
        else:
            date_debut_str = args.date_debut or config['DATE_DEBUT']
            date_fin_str = args.date_fin or config['DATE_FIN']

        # Ménage des logs (après activation du logging)
        from utils import cleanup_logs
        cleanup_logs(log_dir, config['LOG_RETENTION_DAYS'], logger)

        # Options Chrome
        options = Options()
        options.add_argument(f"--user-data-dir={config['CHROME_USER_DATA_DIR']}")
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
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)

        # Service ChromeDriver avec gestion automatique
        chromedriver_service_args = ["--verbose"] if debug_mode else []

        # Utilisation de webdriver-manager pour télécharger automatiquement la bonne version
        service = ChromeService(
            ChromeDriverManager().install(),
            log_path=chromedriver_log,
            service_args=chromedriver_service_args
        )

        # Initialisation du WebDriver
        driver = webdriver.Chrome(service=service, options=options)

        if debug_mode:
            logger.debug(f"Version de Python : {sys.version}")
        logger.info(f"Version de l'application exécutée : {__version__}")
        logger.info(f"Rapports à traiter : {rapports}")
        logger.info(f"Dossier de téléchargement : {download_dir}")

        # Vérification de la connexion internet avant d'ouvrir la page
        if not check_internet():
            logger.error("Perte de connexion internet détectée avant l'ouverture de la page Dexcom Clarity.")
            logger.info("Arrêt du script suite à une perte de connexion internet.")
            sys.exit(0)

        # Ouvrir la page de connexion
        driver.get(dexcom_url)
        wait = WebDriverWait(driver=driver, timeout=60)

        if not check_internet():
            logger.error("Perte de connexion internet détectée avant de cliquer sur le bouton d'accueil.")
            logger.info("Arrêt du script suite à une perte de connexion internet.")
            sys.exit(1)

        try:
            click_home_user_button(driver, logger, log_dir, now_str)
            time.sleep(5)
            logger.debug("Le bouton 'Dexcom Clarity for Home Users' a été cliqué avec succès!")
        except Exception as e:
            # La gestion d'erreur est déjà dans click_home_user_button
            raise

        try:
            saisir_identifiants(driver, logger, log_dir, now_str)
        except Exception as e:
            logger.error(f"Erreur lors de la saisie des identifiants ou de la connexion : {e}")
            sys.exit(1)

        time.sleep(10)

        try:
            if not check_internet():
                logger.error("Perte de connexion internet détectée avant la sélection des dates.")
                raise RuntimeError("Connexion internet requise pour poursuivre.")

            date_picker_button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@data-test-date-range-picker-toggle]"))
            )
            date_picker_button.click()
            logger.debug("Bouton du sélecteur de dates trouvé et cliqué.")
            time.sleep(5)

            if date_debut_str is None or date_fin_str is None:
                raise ValueError("Les variables DATE_DEBUT et DATE_FIN ne peuvent pas être None. Elles doivent être définies.")

            date_debut_input = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.NAME, "start_date"))
            )
            date_fin_input = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.NAME, "end_date"))
            )
            date_debut_input.clear()
            date_fin_input.clear()
            date_debut_input.send_keys(date_debut_str)
            date_fin_input.send_keys(date_fin_str)

            ok_button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-test-date-range-picker__ok-button]"))
            )
            ok_button.click()
            logger.debug("Bouton OK du sélecteur de dates cliqué.")
            time.sleep(5)

            logger.info(f"Date de début: {date_debut_str}")
            logger.info(f"Date de fin: {date_fin_str}")
            logger.info("Les dates ont été saisies avec succès !")

        except Exception as e:
            if not check_internet():
                logger.error("Perte de connexion internet détectée lors de la saisie des dates.")
            logger.error(f"Une erreur s'est produite lors de la saisie des dates : {e}")

        selection_rapport(
            rapports,
            driver,
            logger,
            download_dir,
            dir_final_base,
            date_fin_str,
            args
        )

        time.sleep(60)

        if debug_mode:
            boutons = driver.find_elements(By.XPATH, "//button")
            logger.info(f"{len(boutons)} boutons trouvés sur la page")
            for b in boutons:
                logger.debug(b.get_attribute("outerHTML"))

        try:
            user_menu_button = get_user_menu_button(driver, logger, args)
            user_menu_button.click()
            time.sleep(2)
            logout_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'cui-link__logout') and contains(., 'Déconnexion')]"))
            )
            logout_link.click()
            logger.info("Déconnexion effectuée avec succès.")
            time.sleep(3)
        except Exception as e:
            logger.warning(f"Impossible de se déconnecter proprement : {e}", exc_info=debug_mode)

    except Exception as e:
        logger.error(f"Erreur inattendue dans le script principal : {e}")
        traceback.print_exc()
        pause_on_error()
        sys.exit(1)
    finally:
        try:
            driver.quit()
        except Exception as e:
            logger.warning(f"Erreur lors de la fermeture du navigateur : {e}", exc_info=debug_mode)

        files = glob.glob(os.path.join(download_dir, '*'))
        logger.info(f"Fichiers présents dans le dossier de téléchargement après la demande : {files}")

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
    xpath = ("(//button[.//span[@class='clarity-menu__primarylabel'] "
            "and .//span[@class='clarity-menu__trigger-item-down-arrow']])[last()]")
    try:
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
    except Exception as e:
        logger.error(f"Bouton utilisateur introuvable : {e}", exc_info=args.debug)
        raise

def pause_on_error():
    """
    Affiche un message et attend que l'utilisateur appuie sur Entrée avant de fermer la fenêtre du terminal.
    """
    if sys.stdin.isatty():
        input("\nAppuyez sur Entrée pour fermer...")

# --- Point d'entrée du script ---
if __name__ == "__main__":
    # ============================================
    # ÉTAPE 1 : Parse des arguments (léger, pas d'import config)
    # ============================================
    parser, args = parse_args()
    
    # ============================================
    # ÉTAPE 2 : Gestion des options qui N'ONT PAS besoin de config
    # (Ces options s'exécutent AVANT la validation de .env et config.yaml)
    # ============================================
    
    # Note : --help et --version sont gérés automatiquement par argparse
    # et terminent le programme AVANT d'arriver ici
    
    # Option --list-rapports
    if hasattr(args, 'list_rapports') and args.list_rapports:
        list_available_reports()
        sys.exit(0)
    
    # ============================================
    # ÉTAPE 3 : Import de config (validation de .env et config.yaml)
    # (À partir d'ici, .env et config.yaml DOIVENT être valides)
    # ============================================
    
    try:
        from config import (
            DOWNLOAD_DIR, DIR_FINAL_BASE, CHROME_USER_DATA_DIR, DEXCOM_URL,
            CHROMEDRIVER_LOG, RAPPORTS, NOW_STR, DATE_DEBUT, DATE_FIN,
            LOG_RETENTION_DAYS, get_dexcom_credentials
        )
        import config
    except Exception as e:
        from colorama import Fore, Style, init
        init(autoreset=True)
        print(f"\n{Fore.RED}❌ Erreur lors du chargement de la configuration :{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{str(e)}{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}💡 Vérifiez que les fichiers config.yaml et .env existent et sont valides.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}   Pour afficher l'aide : python GlycoDownload.py --help{Style.RESET_ALL}\n")
        sys.exit(1)
    
    # ============================================
    # ÉTAPE 4 : Validation des arguments (nécessite config)
    # ============================================
    
    validate_dates(args)
    
    # ============================================
    # ÉTAPE 5 : Option --dry-run (NÉCESSITE config)
    # ============================================
    
    if hasattr(args, 'dry_run') and args.dry_run:
        from colorama import Fore, Style, init
        from datetime import datetime, timedelta
        init(autoreset=True)
        
        # Déterminer la période selon les arguments
        if args.date_debut and args.date_fin:
            date_debut_str = args.date_debut
            date_fin_str = args.date_fin
        elif args.days:
            fin = datetime.now() - timedelta(days=1)
            debut = fin - timedelta(days=args.days - 1)
            date_debut_str = debut.strftime("%Y-%m-%d")
            date_fin_str = fin.strftime("%Y-%m-%d")
        else:
            date_debut_str = config.DATE_DEBUT
            date_fin_str = config.DATE_FIN
        
        # Déterminer les rapports à télécharger
        rapports = args.rapports if args.rapports else config.RAPPORTS
        
        # Afficher la configuration en mode dry-run
        print(f"\n{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}MODE DRY-RUN : Aucun téléchargement ne sera effectué{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}\n")
        
        print(f"{Fore.GREEN}Configuration détectée :{Style.RESET_ALL}\n")
        print(f"  {Fore.YELLOW}• Période :{Style.RESET_ALL} {date_debut_str} → {date_fin_str}")
        print(f"  {Fore.YELLOW}• Rapports :{Style.RESET_ALL} {', '.join(rapports)}")
        print(f"  {Fore.YELLOW}• Dossier de téléchargement :{Style.RESET_ALL} {config.DOWNLOAD_DIR}")
        print(f"  {Fore.YELLOW}• Dossier de destination :{Style.RESET_ALL} {config.DIR_FINAL_BASE}")
        print(f"  {Fore.YELLOW}• Mode debug :{Style.RESET_ALL} {'Activé' if args.debug else 'Désactivé'}")
        print(f"  {Fore.YELLOW}• Rétention des logs :{Style.RESET_ALL} {config.LOG_RETENTION_DAYS} jours")
        print(f"  {Fore.YELLOW}• URL Dexcom :{Style.RESET_ALL} {config.DEXCOM_URL}")
        print(f"  {Fore.YELLOW}• ChromeDriver log :{Style.RESET_ALL} {config.CHROMEDRIVER_LOG}")
        print(f"  {Fore.YELLOW}• Profil Chrome :{Style.RESET_ALL} {config.CHROME_USER_DATA_DIR}")
        
        # Vérifier les credentials
        try:
            credentials = get_dexcom_credentials()
            print(f"\n  {Fore.GREEN}✓ Credentials Dexcom détectés{Style.RESET_ALL}")
            print(f"    {Fore.YELLOW}• Type d'authentification :{Style.RESET_ALL} ", end="")
            if credentials.get('email'):
                print(f"Email/Nom d'utilisateur")
            elif credentials.get('country_code') and credentials.get('phone_number'):
                print(f"Numéro de téléphone ({credentials['country_code']} {credentials['phone_number']})")
            else:
                print(f"{Fore.RED}Inconnu (configuration incomplète){Style.RESET_ALL}")
        except Exception as e:
            print(f"\n  {Fore.RED}✗ Erreur lors de la lecture des credentials : {e}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Fin du mode dry-run{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}\n")
        
        print(f"{Fore.GREEN}💡 Pour exécuter réellement le téléchargement, relancez sans --dry-run{Style.RESET_ALL}\n")
        
        sys.exit(0)
    
    # ============================================
    # ÉTAPE 6 : Setup du logger (exécution normale)
    # ============================================
    
    logger = setup_logger(
        args.debug, 
        os.path.dirname(config.CHROMEDRIVER_LOG) or ".", 
        config.NOW_STR
    )
    
    # ============================================
    # ÉTAPE 7 : Exécution de la fonction principale
    # ============================================
    
    main(args, logger, config.__dict__)  # ← Correction : config.__dict__ au lieu de config