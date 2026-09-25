#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Format d'en-tête standard à respecter pour ce projet.
Voir .github/HEADER_TEMPLATE_PYTHON.md pour les détails.

Module        : auth.py
Type          : Python module
Auteur        : Pierre Théberge
Compagnie     : Innovations, Performances, Technologies inc.
Créé le       : 2026-09-25
Modifié le    : 2026-09-25
Version       : 0.7.0
Copyright     : Pierre Théberge

Description
-----------
Connexion à Dexcom Clarity : saisie de l'identifiant (courriel, nom d'utilisateur
ou téléphone) et du mot de passe, puis fermeture de l'invite « Pas maintenant ».

Modifications
-------------
0.7.0 - 2026-09-25   ES-29 : Extraction de saisir_identifiants depuis GlycoDownload.py.

Paramètres
----------
N/A (module importé par l'application).

Exemple
-------
>>> from auth import saisir_identifiants
>>> saisir_identifiants(driver, logger, log_dir, now_str)
"""

import re
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
    WebDriverException,
)

from constants import (
    ATTENTE_CLOUDFLARE,
    ATTENTE_ELEMENT,
    ATTENTE_OPTIONNELLE,
    ATTENTE_PAGE,
    PAUSE_ACTION,
    PAUSE_COURTE,
    PAUSE_SAISIE,
    PAUSE_UI,
)
from utils import (
    check_internet,
    capture_screenshot,
    attendre_verification_humaine_cloudflare,
)


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

        # Si une vérification Cloudflare est affichée, attendre la page de login
        # avant d'essayer de localiser le champ d'identifiant.
        try:
            attendre_verification_humaine_cloudflare(
                driver,
                logger,
                (
                    By.XPATH,
                    "//input[( @type='text' or @type='email' or @type='password') and not(@disabled)]",
                ),
                log_dir,
                NOW_STR,
                timeout=ATTENTE_CLOUDFLARE,
                poll_seconds=5.0,
                quiet_seconds=45.0,
                deep_scan_interval=20.0,
                debug=logger.isEnabledFor(logging.DEBUG),
            )
        except TimeoutException as e:
            logger.error(f"Attente Cloudflare avant login: {e}")
            logger.error(
                "La vérification humaine Cloudflare n'a pas été complétée dans le délai prévu "
                f"({ATTENTE_CLOUDFLARE // 60} minutes). L'application s'arrête avant de lire vos identifiants Dexcom."
            )
            logger.error(
                "Pistes de dépannage :\n"
                "  - Relancer le script avec l'option --debug pour obtenir plus de détails et des captures d'écran.\n"
                "  - Vérifier que votre profil Chrome permet d'accéder à Dexcom Clarity sans étape supplémentaire.\n"
                "  - Désactiver temporairement VPN, bloqueurs de pub ou extensions pouvant perturber Cloudflare.\n"
                "  - Réessayer plus tard : il peut s'agir d'un contrôle temporaire côté Cloudflare."
            )
            raise SystemExit(1)

        # Import différé : config valide .env et config.yaml dès son chargement,
        # ce qui ne doit pas arriver pour --help ou --list-rapports.
        from config import get_dexcom_credentials

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
            phone_link = WebDriverWait(driver, ATTENTE_ELEMENT).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//a[contains(@href, 'phone') or contains(@class, 'phone')]"
                ))
            )
            phone_link.click()

            # Champs téléphone
            country_code_input = WebDriverWait(driver, ATTENTE_ELEMENT).until(
                EC.presence_of_element_located((By.ID, "countryCode"))
            )
            phone_number_input = WebDriverWait(driver, ATTENTE_ELEMENT).until(
                EC.presence_of_element_located((By.ID, "phoneNumber"))
            )

            country_code_input.clear()
            country_code_input.send_keys(country_code)
            phone_number_input.clear()
            phone_number_input.send_keys(phone_number)

        else:
            # Sélection du mode courriel/nom d'utilisateur
            # MODIFICATION : Vérifier d'abord si le champ login est déjà visible (bypass de la sélection)
            login_field_already_visible = False
            try:
                WebDriverWait(driver, ATTENTE_OPTIONNELLE).until(
                    EC.visibility_of_element_located((By.ID, "usernameLogin"))
                )
                login_field_already_visible = True
                logger.debug("Champ d'identifiant détecté directement. Étape de sélection du mode ignorée.")
            except TimeoutException:
                pass

            if not login_field_already_visible:
                try:
                    radio_buttons = WebDriverWait(driver, ATTENTE_ELEMENT).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "radio-outer-circle"))
                    )
                    if radio_buttons:
                        driver.execute_script("arguments[0].click();", radio_buttons[0])
                        time.sleep(PAUSE_COURTE)
                except TimeoutException:
                    logger.debug("Boutons de sélection de mode non trouvés, tentative d'accès direct au login.")

            # Capture avant la recherche du champ username (en mode debug uniquement)
            if logger.isEnabledFor(logging.DEBUG):
                capture_screenshot(driver, logger, "avant_username_input", log_dir, NOW_STR)

            # Attendre que le champ soit présent (avec fallbacks si l'ID change)
            username_input = None
            username_locators = [
                (By.ID, "usernameLogin"),
                (By.NAME, "username"),
                (By.NAME, "email"),
                (By.CSS_SELECTOR, "input[type='email']"),
                (By.CSS_SELECTOR, "input[autocomplete='username']"),
                (By.CSS_SELECTOR, "input[id*='user'][type='text']"),
                (By.CSS_SELECTOR, "input[id*='email']"),
            ]
            for locator in username_locators:
                try:
                    username_input = WebDriverWait(driver, ATTENTE_ELEMENT).until(
                        EC.presence_of_element_located(locator)
                    )
                    if username_input is not None:
                        logger.debug(f"Champ d'identifiant trouvé via {locator}")
                        break
                except TimeoutException:
                    continue

            if username_input is None:
                current_url = getattr(driver, "current_url", "")
                try:
                    page_title = driver.title
                except WebDriverException:
                    page_title = ""
                logger.error(
                    "Champ usernameLogin introuvable après sélection du mode courriel/nom d'utilisateur. "
                    f"URL actuelle: {current_url} | Titre: {page_title}"
                )
                if logger.isEnabledFor(logging.DEBUG):
                    capture_screenshot(driver, logger, "erreur_username_input", log_dir, NOW_STR)
                raise SystemExit(1)

            # Vérifier que le champ est visible et interactif
            try:
                WebDriverWait(driver, ATTENTE_ELEMENT).until(EC.visibility_of(username_input))
                WebDriverWait(driver, ATTENTE_ELEMENT).until(EC.element_to_be_clickable(username_input))
            except TimeoutException as e:
                logger.error("Champ usernameLogin non visible ou non interactif.")
                if logger.isEnabledFor(logging.DEBUG):
                    capture_screenshot(driver, logger, "username_non_interactif", log_dir, NOW_STR)
                raise SystemExit(1)

            # Scroll jusqu'au champ pour le rendre visible
            driver.execute_script("arguments[0].scrollIntoView(true);", username_input)
            time.sleep(PAUSE_SAISIE)

            # Clic dans le champ pour déclencher les scripts JS
            try:
                username_input.click()
            except ElementClickInterceptedException:
                driver.execute_script("arguments[0].click();", username_input)
            time.sleep(PAUSE_SAISIE)

            # Saisie classique
            username_input.clear()
            username_input.send_keys(dexcom_username)
            time.sleep(PAUSE_SAISIE)

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
        next_button = WebDriverWait(driver, ATTENTE_PAGE).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value]"))
        )
        next_button.click()
        time.sleep(PAUSE_UI)

        # Saisie du mot de passe
        password_input = WebDriverWait(driver, ATTENTE_PAGE).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_input.send_keys(dexcom_password)

        # Clic sur le bouton de connexion
        # Utilisation de l'ID 'default-login-text' (indépendant de la langue et du type d'élément)
        # On cible l'élément avec cet ID, le clic se propagera au bouton parent si nécessaire
        try:
            logger.debug("Tentative de clic sur le bouton de connexion via ID 'default-login-text'...")
            login_button = WebDriverWait(driver, ATTENTE_OPTIONNELLE).until(
                EC.element_to_be_clickable((By.ID, "default-login-text"))
            )
            login_button.click()
        except (TimeoutException, ElementClickInterceptedException) as e:
            logger.warning(f"ID 'default-login-text' introuvable ou non cliquable ({e}), tentative via type='submit'")
            # Fallback : recherche par type submit (button ou input) si l'ID n'est pas trouvé
            try:
                login_button = WebDriverWait(driver, ATTENTE_ELEMENT).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'] | //input[@type='submit']"))
                )
                login_button.click()
            except (TimeoutException, ElementClickInterceptedException) as e2:
                logger.warning(f"Échec du clic sur le bouton de connexion (fallback inclus) : {e2}. Tentative avec la touche ENTRÉE.")
                # Dernier recours : appuyer sur Entrée dans le champ mot de passe
                password_input.send_keys(Keys.ENTER)

        time.sleep(PAUSE_ACTION)

        logger.info("Connexion réussie !")
        time.sleep(PAUSE_UI)
        if logger.isEnabledFor(logging.DEBUG):
            capture_screenshot(driver, logger, "apres_connexion", log_dir, NOW_STR)

        # Après la connexion réussie, avant d'aller plus loin...
        try:
            # Attendre la présence éventuelle du bouton "Pas maintenant" (notNowButton)
            not_now_button = WebDriverWait(driver, ATTENTE_OPTIONNELLE).until(
                EC.element_to_be_clickable((By.ID, "notNowButton"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", not_now_button)
            not_now_button.click()
            logger.debug("Bouton 'Pas maintenant' détecté et cliqué.")
            time.sleep(PAUSE_UI)
        except TimeoutException:
            # Si le bouton n'est pas présent, on continue simplement
            logger.debug("Aucun bouton 'Pas maintenant' à cliquer, poursuite du script.")

    except WebDriverException as e:
        logger.exception(f"Erreur lors de la saisie des identifiants ou de la connexion : {e}")
        raise SystemExit(1)
