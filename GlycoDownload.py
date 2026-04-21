#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Format d'en-tête standard à respecter pour ce projet.
Voir .github/HEADER_TEMPLATE_PYTHON.md pour les détails.

Module        : GlycoDownload.py
Type          : Python module
Auteur        : Pierre Théberge
Compagnie     : Innovations, Performances, Technologies inc.
Créé le       : 2025-03-03
Modifié le    : 2026-04-21
Version       : 0.5.11
Copyright     : Pierre Théberge

Description
-----------
Script principal (CLI + orchestration) pour automatiser le téléchargement des rapports Dexcom Clarity.

Modifications
-------------
0.0.0   - 2025-03-03   [N/A]   : Version initiale.
0.0.1   - 2025-03-07   [N/A]   : Connectoin à Clarity et authentification
0.0.2   - 2025-03-20   [N/A]   : Cliquer sur le sélecteur de dates et choisir la période
0.0.3   - 2025-03-28   [N/A]   : Ajout du traitement des rapports
0.0.4   - 2025-04-07   [N/A]   : Conversion à Python 3.13 et une erreur de syntaxe dans le code de la fonction traitement_rapport_apercu
0.0.5   - 2025-04-11   [N/A]   : Ajout de la sélection du rapport Apercu
0.0.6   - 2025-04-16   [N/A]   : Ajout du code pour télécharger un rapport.
0.0.7   - 2025-04-24   [N/A]   : Retour à Python 3.12. Besoin Tensorflow et il n'est pas supporté par Python 3.13
0.0.8   - 2025-05-23   [N/A]   : Terminé la fonction téléchargement_rapport
0.0.9   - 2025-07-01   [N/A]   : Ajout de l'option debug et ajout d'un fichier de log
0.0.10  - 2025-07-02   [N/A]   : Modification pour tenir compte d'une connexion internet lente et instable (4mb/s)
                                 Ajout de la fonction traitement_rapport
                                 Ajout de la fonction check_internet pour vérifier la connexion internet
                                 Ajout du traitement pour les rapports Modèles
                                 Dans la fonction deplace_et_renomme_rapport, ne pas tenir compte des fichiers *.log
0.0.11  - 2025-07-03   [N/A]   : La vérification de la connexion internet ne fonctionne pas avec NordVPN
                                 Ajout du traitement pour le rapport Superposition
                                 Rendre plus robuste le traitement du rapport Aperçu
                                 Ajout du traitement pour le rapport Quotidien
                                 Ajout du traitement pour le rapport AGP
0.0.12  - 2025-07-08   [N/A]   : Ajout du traitement pour le rapport Statistiques
0.0.13  - 2025-07-13   [N/A]   : Ajout du traitement pour le rapport Comparer
0.0.14  - 2025-07-18   [N/A]   : Ajout de l'exportation des données en format csv
0.0.15  - 2025-07-21   [N/A]   : Terminer la fonction traitement_export_csv
                                 Ajout des sous-rapport pour le rapport Comparer
                                 Les sous-rapports Superposition et Quotidien de comparer ne fonctioone pas.
                                 Ils produisent le même PDF que Tendances.
                                 Ajouter la déconnexion du compte avant de fermer le navigateur
0.0.16  - 2025-07-25   [N/A]   : Correction pour la déconnexion du compte
                                 Correction pour le bouton Fermer de la fenêtre modale Exporter
0.0.17  - 2025-07-25   [N/A]   : Correction pour le déconnexion du compte. Éliminer la référence au nom d'utilisateur.
                                 Ajout de TODO pour la correction du code.
0.0.18  - 2025-07-30   [N/A]   : Gestion des exceptions plus précise. Évite les except: nus. Précise toujours le type d'exception
                                 Factorisation des attentes sur les overlays/loaders. Crée une fonction utilitaire
                                 pour attendre la disparition des overlays, et utilise-la partout où c'est pertinent.
                                 Centralisation des paramètres et chemins. Définis tous les chemins, URLs, et paramètres en haut du script ou dans un fichier de config.
                                 Ajout d'une fonction main()
                                 Fermeture du navigateur dans un finally
0.0.19  - 2025-08-04   [N/A]   : Ajout de docstrings pour toutes les fonctions
                                 Logging cohérent. Utilise le logger pour tous les messages (pas de print).
0.0.20  - 2025-08-05   [N/A]   : Ajout d'une validation pour la présende des variables d'environnement nécessaires
                                 Crée un fichier config.py pour centraliser tous les paramètres, chemins, URLs, etc.
                                 Crée un fichier utils.py pour toutes les fonctions utilitaires (connexion internet, overlay, renommage, etc.).
                                 Crée un fichier rapports.py pour le traitement des rapports
0.0.21  - 2025-08-06   [N/A]   : Ajout d'un exemple de fichier de configuration "config_example.yaml"
0.0.22  - 2025-08-13   [N/A]   : Centralisation et normalisation des chemins, gestion CLI améliorée,
                                 logs JS navigateur, robustesse accrue sur la gestion des erreurs,
                                 factorisation des utilitaires, gestion propre des exceptions et de la déconnexion.
0.0.23  - 2025-08-13   [N/A]   : Capture d'écran centralisée via utils.py, délai avant capture,
                                 suppression des duplications de code, ajout de logs pour le diagnostic.
0.1.0   - 2025-08-18   [N/A]   : Robustesse saisie identifiant : sélection usernameLogin, vérification visibilité/interactivité,
                                 captures d'écran uniquement en mode debug, gestion du bouton 'Pas maintenant' après connexion,
                                 adaptation aux changements d'interface Dexcom, logs détaillés pour le diagnostic.
0.1.1   - 2025-09-03   [N/A]   : Ajout des logs.
0.1.2   - 2025-09-04   [N/A]   : Vérification des répertoires.
0.1.3   - 2025-09-05   [N/A]   : Correction de la récupération de la date de rapport.
0.1.4   - 2025-09-05   [N/A]   : Renommage du répertoire de sortie.
0.1.5   - 2025-09-06   [N/A]   : Répertoire de sortie dans config.yaml.
0.1.6   - 2025-09-23   [N/A]   : Gestion améliorée de la sélection des jours (days).
0.1.7   - 2025-10-06   [N/A]   : Détermination automatique de la version de chromedriver.
0.2.0   - 2025-10-07   [N/A]   : Réorganisation complète de la structure en modules.
0.2.1   - 2025-10-09   [ES-5]  : Ajout de la langue dans les arguments en CLI et au rapport.
0.2.2   - 2025-10-11   [ES-6]  : Les rapports sont indépendants de la langue de l'utilisateur.
0.2.3   - 2025-10-14   [ES-11] : Ajout du rapport Statistiques horaires et amélioration de la robustesse d'accès aux rapports.
                                 Utilisation de ChromeDriverManager pour télécharger automatiquement la bonne version de ChromeDriver.
0.2.4   - 2025-10-16   [ES-12] : Synchronisation de version (aucun changement fonctionnel).
0.2.5   - 2025-10-16   [ES-10] : Synchronisation de version (aucun changement fonctionnel).
0.2.6   - 2025-10-21   [ES-7]  : Amélioration du système d'aide (--help) avec description détaillée, exemples et groupes d'arguments.
                                 Ajout de l'option --list-rapports pour afficher la liste des rapports disponibles.
                                 Ajout de l'option --dry-run pour tester la configuration sans télécharger.
                                 Ajout de la validation des dates avec messages d'erreur clairs.
0.2.7   - 2025-10-27   [ES-16] : Ajout de la gestion des erreurs 502 (Bad Gateway) avec retry automatique.
                                 Attente et réessai automatique (3 tentatives max) en cas d'erreur serveur temporaire.
                                 Suivi et rapport des échecs de téléchargement avec raisons détaillées.
                                 Amélioration de la robustesse face aux problèmes temporaires du serveur Dexcom.
0.2.8   - 2025-11-28   [ES-16] : Correction du sélecteur du bouton de connexion pour être indépendant de la langue.
                                 Utilisation de l'ID 'default-login-text' au lieu du texte du bouton.
                                 Ajout d'un fallback sur le type 'submit' pour plus de robustesse.
                                 Augmentation du timeout et amélioration des logs pour le bouton de connexion.
                                 Correction de la déconnexion bloquée par un overlay (clic JS forcé).
0.2.9   - 2025-11-28   [ES-16] : Ajout d'un fallback ultime pour la connexion : simulation de la touche ENTRÉE.
                                 Gestion du cas où le bouton de connexion est introuvable ou non cliquable.
                                 Correction des erreurs de portée de variables (debug_mode, download_dir).
                                 Correction du mode --dry-run (join, credentials).
                                 Amélioration de la connexion : détection automatique du champ login pour sauter l'étape de sélection du mode.
0.2.10  - 2025-12-17   [ES-17] : Sécurité : Masquage des informations sensibles (téléphone) dans la sortie --dry-run.
                                 Synchronisation de version.
0.2.11  - 2025-12-22   [ES-18] : Correction du délai d'attente pour la fermeture de la fenêtre de téléchargement (60s).
                                 Retour à Python 3.13 (après rollback v0.0.7)
0.2.12  - 2025-12-22   [ES-3]  : Réparer le problème avec les rapports Comparer.
0.2.13  - 2026-01-19   [ES-19] : Synchronisation de version (aucun changement fonctionnel).
0.2.14  - 2026-01-19   [ES-19] : Attente "vérification humaine" Cloudflare (pause + reprise automatique).
0.2.15  - 2026-01-19   [ES-19] : Robustesse post-connexion (attentes UI explicites) et ancre Cloudflare plus robuste.
0.2.16  - 2026-01-20   [ES-19] : Synchronisation de version (aucun changement fonctionnel).
0.2.17  - 2026-01-20   [ES-19] : Robustesse Cloudflare + debug config + logs (aucun changement fonctionnel majeur).
0.2.18  - 2026-01-20   [ES-19] : Synchronisation de version (aucun changement fonctionnel).
0.3.0   - 2026-01-29   [ES-19] : Ajout du point d'entrée --start-at-date-selection.
0.3.1   - 2026-02-02   [ES-19] : Robustesse de pause_on_error (stdin non interactif).
0.3.2   - 2026-02-02   [ES-19] : Filtrage des fichiers téléchargés par extension.
0.3.3   - 2026-02-02   [ES-19] : Normalisation des extensions attendues (téléchargements).
0.3.4   - 2026-02-12   [ES-3]  : Correction du téléchargement des sous-rapports Comparer.
0.3.5   - 2026-02-12   [ES-3]  : Forçage du download_dir et stabilisation Comparer.
0.3.6   - 2026-02-12   [ES-3]  : Stabilisation renforcée des sous-rapports Comparer.
0.3.15  - 2026-02-26   [ES-6]  : Harmonisation des XPath pour reduire la dependance a la langue du navigateur.
0.3.16  - 2026-03-19   [ES-15] : Synchronisation de version et documentation (retention logs par defaut a 30 jours).
0.3.17  - 2026-03-23   [ES-14] : Detection des pertes reseau pendant le traitement des rapports,
                                 tentative de reconnexion et arret propre de l'application en cas d'echec.
                                 Fermeture de l'onglet Dexcom en fin de traitement,
                                 et fermeture complete du navigateur si un seul onglet est ouvert.
0.3.18  - 2026-03-25   [ES-14] : Synchronisation de version apres durcissement du flux Export CSV
                                 pour les erreurs reseau en modale.
0.3.19  - 2026-03-25   [ES-14] : Fermeture navigateur: utilisation du mode debug effectif
                                 (args.debug ou config.DEBUG) pour les traces d'exception.
0.4.0   - 2026-04-14   [ES-20] : Synchronisation de version (tous les parametres CLI acceptes par
                                 GlycoDownload correspondent aux parametres exposes par Launch-Dexcom-And-Run.ps1).
0.5.0   - 2026-04-14   [ES-21] : Extraction de resolve_effective_date_range (fonction pure testable).
0.5.1   - 2026-04-15   [ES-22] : Synchronisation de version (aucun changement fonctionnel).
                                 Chaine de priorite : CLI dates > CLI --days > config days > config dates.
                                 Remplacement des deux blocs inline (main et dry-run) par des appels a cette fonction.
0.5.2   - 2026-04-15   [ES-25] : Saisie des dates : erreur fatale si Selenium echoue a entrer les
                                 dates dans l'UI Dexcom (au lieu de continuer silencieusement avec
                                 les dates par defaut de Dexcom).
0.5.3   - 2026-04-15   [ES-25] : Robustesse saisie des dates : element_to_be_clickable au lieu de
                                 presence_of_element_located; clic + clear + send_keys par champ
                                 sequentiellement (evite StaleElementReferenceException si re-render).
0.5.4   - 2026-04-15   [CR]    : Synchronisation de version (aucun changement fonctionnel).
0.5.5   - 2026-04-15   [CR]    : Dates CLI partielles : erreur explicite dans validate_dates si une
                                 seule date est fournie; garde defensif (ValueError) dans
                                 resolve_effective_date_range. Tests mis a jour en consequence.
0.5.6   - 2026-04-16   [ES-25] : Deconnexion : seconde attente overlay apres ouverture du menu
                                 utilisateur; JS fallback sur logout_link.click() pour contourner
                                 ElementClickInterceptedException.
0.5.7   - 2026-04-17   [ES-25] : Synchronisation de version (aucun changement fonctionnel).
0.5.8   - 2026-04-17   [ES-25] : Deconnexion : except Exception -> except
                                 ElementClickInterceptedException sur les clics menu
                                 utilisateur et logout_link; import ajoute.
0.5.9   - 2026-04-17   [ES-25] : Synchronisation de version (aucun changement fonctionnel).
0.5.10  - 2026-04-17   [ES-26] : Synchronisation de version (aucun changement fonctionnel).
0.5.11  - 2026-04-21   [ES-28] : Synchronisation de version (aucun changement fonctionnel).

Paramètres
----------
Voir --help pour la liste complète des options CLI.

Exemple
-------
>>> python GlycoDownload.py --dry-run
"""

# TODO 11 Réparer le problème avec les rapports Comparer
# TODO 12 Exécuter l'application pour produire les rapports Comparer depuis 2024-08-19
# TODO 13 Appliquer la même solution pour obtenir des rapports séparés pour Modèle
# TODO 14 Rendre l'application indépendante de la langue de l'utilisateur.

import sys
import argparse
import os
import logging
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
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
    cleanup_logs,
    attendre_verification_humaine_cloudflare
)
from rapports import selection_rapport, NetworkRecoveryFailedError
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

    Démarrer après connexion (sélection des dates seulement) :
        python GlycoDownload.py --start-at-date-selection

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
    general_group.add_argument(
        '--start-at-date-selection',
        action='store_true',
        help='Démarrer directement avant la sélection des dates (login déjà effectué)'
    )
    general_group.add_argument(
        '--attach-debugger',
        action='store_true',
        help='Attacher Selenium à un Chrome déjà lancé en mode debug (remote debugging)'
    )
    general_group.add_argument(
        '--debugger-port',
        type=int,
        default=9222,
        metavar='PORT',
        help='Port du debugger Chrome (défaut : 9222)'
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


def resolve_effective_date_range(
    args_days, args_date_debut, args_date_fin,
    config_days, config_date_debut, config_date_fin,
    today=None,
):
    """
    Résout la période effective selon la chaîne de priorité :
      1. CLI date_debut + date_fin (les deux fournis)
      2. CLI --days
      3. config.yaml days
      4. config.yaml date_debut / date_fin

    Args:
        args_days (int | None): Valeur de --days passée en CLI.
        args_date_debut (str | None): --date_debut passée en CLI.
        args_date_fin (str | None): --date_fin passée en CLI.
        config_days (int | None): Valeur de days dans config.yaml.
        config_date_debut (str | None): date_debut dans config.yaml.
        config_date_fin (str | None): date_fin dans config.yaml.
        today (datetime | None): Date de référence (None = aujourd'hui).

    Returns:
        tuple[str, str]: (date_debut_str, date_fin_str) au format AAAA-MM-JJ.
    """
    if today is None:
        today = datetime.today()

    # Garde défensif : validate_dates doit avoir rejeté les dates partielles en amont.
    if bool(args_date_debut) != bool(args_date_fin):
        raise ValueError(
            f"Les dates CLI doivent être fournies ensemble ou aucune "
            f"(date_debut={args_date_debut!r}, date_fin={args_date_fin!r})."
        )

    if args_date_debut and args_date_fin:
        return args_date_debut, args_date_fin

    effective_days = args_days or config_days
    if effective_days:
        date_fin = today - timedelta(days=1)
        date_debut = date_fin - timedelta(days=effective_days - 1)
        return date_debut.strftime("%Y-%m-%d"), date_fin.strftime("%Y-%m-%d")

    return config_date_debut, config_date_fin


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
    
    # Dates partielles : les deux doivent être fournies ensemble ou aucune.
    if bool(args.date_debut) != bool(args.date_fin):
        manquante = "--date_fin" if args.date_debut else "--date_debut"
        fournie   = "--date_debut" if args.date_debut else "--date_fin"
        print(f"\n{Fore.RED}❌ Erreur : {fournie} est fournie sans {manquante}.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Les deux dates doivent être spécifiées ensemble ou aucune.{Style.RESET_ALL}\n")
        sys.exit(1)

    if args.days and (args.date_debut or args.date_fin):
        print(f"\n{Fore.YELLOW}⚠ Avertissement : --days est ignoré car --date_debut et --date_fin sont spécifiées.{Style.RESET_ALL}")


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
                timeout=600,
                poll_seconds=5.0,
                quiet_seconds=45.0,
                deep_scan_interval=20.0,
                debug=logger.isEnabledFor(logging.DEBUG),
            )
        except Exception as e:
            logger.error(f"Attente Cloudflare avant login: {e}")
            logger.error(
                "La vérification humaine Cloudflare n'a pas été complétée dans le délai prévu "
                "(10 minutes). L'application s'arrête avant de lire vos identifiants Dexcom."
            )
            logger.error(
                "Pistes de dépannage :\n"
                "  - Relancer le script avec l'option --debug pour obtenir plus de détails et des captures d'écran.\n"
                "  - Vérifier que votre profil Chrome permet d'accéder à Dexcom Clarity sans étape supplémentaire.\n"
                "  - Désactiver temporairement VPN, bloqueurs de pub ou extensions pouvant perturber Cloudflare.\n"
                "  - Réessayer plus tard : il peut s'agir d'un contrôle temporaire côté Cloudflare."
            )
            raise SystemExit(1)

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
                    "//a[contains(@href, 'phone') or contains(@class, 'phone')]"
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
            # MODIFICATION : Vérifier d'abord si le champ login est déjà visible (bypass de la sélection)
            login_field_already_visible = False
            try:
                WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.ID, "usernameLogin"))
                )
                login_field_already_visible = True
                logger.debug("Champ d'identifiant détecté directement. Étape de sélection du mode ignorée.")
            except Exception:
                pass

            if not login_field_already_visible:
                try:
                    radio_buttons = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "radio-outer-circle"))
                    )
                    if radio_buttons:
                        driver.execute_script("arguments[0].click();", radio_buttons[0])
                        time.sleep(1)
                except Exception:
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
                    username_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(locator)
                    )
                    if username_input is not None:
                        logger.debug(f"Champ d'identifiant trouvé via {locator}")
                        break
                except Exception:
                    continue

            if username_input is None:
                current_url = getattr(driver, "current_url", "")
                try:
                    page_title = driver.title
                except Exception:
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
                WebDriverWait(driver, 10).until(EC.visibility_of(username_input))
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(username_input))
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

        # Clic sur le bouton de connexion
        # Utilisation de l'ID 'default-login-text' (indépendant de la langue et du type d'élément)
        # On cible l'élément avec cet ID, le clic se propagera au bouton parent si nécessaire
        try:
            logger.debug("Tentative de clic sur le bouton de connexion via ID 'default-login-text'...")
            login_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "default-login-text"))
            )
            login_button.click()
        except Exception as e:
            logger.warning(f"ID 'default-login-text' introuvable ou non cliquable ({e}), tentative via type='submit'")
            # Fallback : recherche par type submit (button ou input) si l'ID n'est pas trouvé
            try:
                login_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'] | //input[@type='submit']"))
                )
                login_button.click()
            except Exception as e2:
                logger.warning(f"Échec du clic sur le bouton de connexion (fallback inclus) : {e2}. Tentative avec la touche ENTRÉE.")
                # Dernier recours : appuyer sur Entrée dans le champ mot de passe
                password_input.send_keys(Keys.ENTER)

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
        logger.exception(f"Erreur lors de la saisie des identifiants ou de la connexion : {e}")
        raise SystemExit(1)
def click_home_user_button(driver, logger, log_dir, NOW_STR, timeout=10, required=True):
    """
    Clique sur le bouton 'Dexcom Clarity for Home Users' sur la page d'accueil.

    Args:
        driver: Instance Selenium WebDriver.
        logger: Logger Python de l'appelant.
        log_dir (str): Dossier de destination pour les screenshots d'erreur.
        NOW_STR (str): Horodatage formaté utilisé dans les noms de fichiers de screenshot.
        timeout (int): Délai d'attente maximum (en secondes) pour trouver le bouton. Défaut : 10.
        required (bool): Si True, loggue en erreur + screenshot et lève une exception.
                         Si False, loggue en warning et retourne False sans lever. Défaut : True.

    Returns:
        bool: True si le bouton a été cliqué, False sinon.
    """
    try:
        xpath = (
            "//input[@type='submit' and ("
            "contains(@class, 'landing-page--button') "
            ")]"
        )
        button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        button.click()
        logger.debug("Le bouton 'Dexcom Clarity for Home Users' a été cliqué avec succès!")
        return True
    except Exception as e:
        if required:
            time.sleep(2)
            capture_screenshot(driver, logger, "home_user_button_error", log_dir, NOW_STR)
            logger.error(f"Une erreur s'est produite au moment de cliquer sur le bouton 'Dexcom Clarity for Home Users' : {e}")
            raise
        logger.warning(
            "Bouton 'Dexcom Clarity for Home Users' introuvable en mode reprise; poursuite du flux sans clic."
        )
        return False

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


def close_browser_session(driver, logger, debug=False):
    """Ferme proprement la session navigateur selon le nombre d'onglets ouverts."""
    if driver is None:
        return

    try:
        handles = list(driver.window_handles or [])
    except Exception:
        handles = []

    try:
        if len(handles) <= 1:
            logger.info("Fermeture du navigateur (dernier onglet).")
            try:
                # Ferme l'instance Chrome connectée via CDP (inclut le mode attach-debugger).
                driver.execute_cdp_cmd("Browser.close", {})
            except Exception as close_exc:
                logger.debug("Fermeture CDP impossible, fallback driver.quit(): %s", close_exc)
                driver.quit()
        else:
            logger.info("Plusieurs onglets détectés: fermeture de l'onglet courant uniquement.")
            try:
                driver.close()
            except Exception as close_exc:
                logger.debug("Fermeture de l'onglet impossible, fallback driver.quit(): %s", close_exc)
                driver.quit()
    except Exception as e:
        logger.warning(f"Erreur lors de la fermeture du navigateur : {e}", exc_info=debug)


def main(args, logger, config):
    """
    Fonction principale du script GlycoReport-Downloader (refactorisée).
    Gère la connexion, la sélection des dates, le téléchargement des rapports et la déconnexion.
    """
    driver = None
    download_dir = None
    try:
        # Préparation des variables locales
        debug_mode = bool(args.debug or config.get("DEBUG", False))
        rapports = args.rapports or config['RAPPORTS']
        download_dir = config['DOWNLOAD_DIR']
        dir_final_base = config['DIR_FINAL_BASE']
        dexcom_url = config['DEXCOM_URL']
        chromedriver_log = config['CHROMEDRIVER_LOG']
        now_str = config['NOW_STR']
        log_dir = os.path.dirname(chromedriver_log) or "."

        # Gestion intelligente des dates — priorité : CLI > config.yaml > défaut
        date_debut_str, date_fin_str = resolve_effective_date_range(
            args.days, args.date_debut, args.date_fin,
            config.get('DAYS'), config['DATE_DEBUT'], config['DATE_FIN'],
        )

        # Ménage des logs (après activation du logging)
        from utils import cleanup_logs
        cleanup_logs(log_dir, config['LOG_RETENTION_DAYS'], logger)

        # Options Chrome
        options = Options()
        if args.attach_debugger:
            debugger_address = f"127.0.0.1:{args.debugger_port}"
            options.add_experimental_option("debuggerAddress", debugger_address)
        else:
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
        options.add_argument("--disable-features=PaintHolding,NetworkServiceInProcess")
        options.add_argument("--remote-allow-origins=*")
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

        # Forcer le dossier de téléchargement (utile même en mode attach-debugger)
        try:
            os.makedirs(download_dir, exist_ok=True)
            driver.execute_cdp_cmd(
                "Page.setDownloadBehavior",
                {"behavior": "allow", "downloadPath": download_dir},
            )
        except Exception as e:
            logger.warning(f"Impossible de forcer download_dir via CDP: {e}")

        if debug_mode:
            logger.debug(f"Version de Python : {sys.version}")
            try:
                logger.debug(f"Arguments CLI: {vars(args)}")
            except Exception:
                logger.debug("Arguments CLI: indisponibles")
            logger.debug(
                "Configuration (sanitisée): "
                f"DOWNLOAD_DIR={download_dir} | "
                f"DIR_FINAL_BASE={dir_final_base} | "
                f"DEXCOM_URL={dexcom_url} | "
                f"CHROMEDRIVER_LOG={chromedriver_log} | "
                f"CHROME_USER_DATA_DIR={config['CHROME_USER_DATA_DIR']} | "
                f"RAPPORTS={rapports} | "
                f"DATE_DEBUT={date_debut_str} | DATE_FIN={date_fin_str} | "
                f"LOG_RETENTION_DAYS={config['LOG_RETENTION_DAYS']}"
            )
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

        if args.start_at_date_selection:
            logger.info("Mode reprise: démarrage avant sélection des dates (login déjà effectué).")

            # Tentative rapide: la page principale est déjà accessible ?
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@data-test-date-range-picker-toggle]"))
                )
            except Exception:
                # Si la page d'accueil est encore affichée, essayer le bouton Home User.
                try:
                    clicked = click_home_user_button(driver, logger, log_dir, now_str, required=False)
                    if clicked:
                        time.sleep(5)
                except Exception:
                    logger.warning("Bouton Home User introuvable lors du mode reprise.")

            # Attendre l'ancre de la page principale (sélecteur de dates)
            try:
                attendre_verification_humaine_cloudflare(
                    driver,
                    logger,
                    (By.XPATH, "//div[@data-test-date-range-picker-toggle]"),
                    log_dir,
                    now_str,
                    timeout=600,
                    poll_seconds=2.0,
                    debug=debug_mode,
                )
            except Exception as e:
                logger.error(
                    "Impossible d'atteindre la page principale en mode reprise. "
                    "Assurez-vous d'être déjà connecté dans le même profil Chrome."
                )
                raise SystemExit(1)
        else:
            # Si une vérification Cloudflare apparaît, laisser l'utilisateur la compléter puis reprendre.
            # Ancre : bouton "Dexcom Clarity for Home Users" (landing page)
            attendre_verification_humaine_cloudflare(
                driver,
                logger,
                (By.XPATH, "//input[@type='submit' and contains(@class, 'landing-page--button')]"),
                log_dir,
                now_str,
                timeout=600,
                poll_seconds=2.0,
                debug=debug_mode,
            )

            if not check_internet():
                logger.error("Perte de connexion internet détectée avant de cliquer sur le bouton d'accueil.")
                logger.info("Arrêt du script suite à une perte de connexion internet.")
                sys.exit(1)

            try:
                click_home_user_button(driver, logger, log_dir, now_str, required=True)
                time.sleep(5)
                logger.debug("Le bouton 'Dexcom Clarity for Home Users' a été cliqué avec succès!")
            except Exception as e:
                # La gestion d'erreur est déjà dans click_home_user_button
                raise

            # Silence total après le clic Home User pour réduire les interactions
            # pendant la vérification Cloudflare.
            logger.info("Pause silencieuse 45s après le bouton Home User (Cloudflare)")
            time.sleep(45)

            try:
                saisir_identifiants(driver, logger, log_dir, now_str)
            except Exception as e:
                logger.error(f"Erreur lors de la saisie des identifiants ou de la connexion : {e}")
                sys.exit(1)

            # Après connexion, Dexcom peut rediriger/afficher une vérification humaine.
            # Ancre : sélecteur de dates (page principale).
            attendre_verification_humaine_cloudflare(
                driver,
                logger,
                (By.XPATH, "//div[@data-test-date-range-picker-toggle]"),
                log_dir,
                now_str,
                timeout=600,
                poll_seconds=2.0,
                debug=debug_mode,
            )

        try:
            if not check_internet():
                logger.error("Perte de connexion internet détectée avant la sélection des dates.")
                raise RuntimeError("Connexion internet requise pour poursuivre.")

            # Stabilisation post-connexion : attendre que l'UI principale soit interactive.
            # (Évite un délai arbitraire long, tout en restant robuste sur connexions lentes.)
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@data-test-date-range-picker-toggle]"))
            )
            time.sleep(2)

            date_picker_button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@data-test-date-range-picker-toggle]"))
            )
            date_picker_button.click()
            logger.debug("Bouton du sélecteur de dates trouvé et cliqué.")
            time.sleep(5)

            if date_debut_str is None or date_fin_str is None:
                raise ValueError("Les variables DATE_DEBUT et DATE_FIN ne peuvent pas être None. Elles doivent être définies.")

            date_debut_input = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.NAME, "start_date"))
            )
            date_debut_input.click()
            date_debut_input.clear()
            date_debut_input.send_keys(date_debut_str)

            date_fin_input = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.NAME, "end_date"))
            )
            date_fin_input.click()
            date_fin_input.clear()
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
            raise RuntimeError(
                f"La saisie des dates a échoué ({date_debut_str} → {date_fin_str}). "
                "Le rapport ne sera pas téléchargé avec des dates incorrectes."
            ) from e

        try:
            selection_rapport(
                rapports,
                driver,
                logger,
                download_dir,
                dir_final_base,
                date_fin_str,
                date_debut_str,
                args
            )
        except NetworkRecoveryFailedError as e:
            logger.error("Arrêt de l'application: %s", e)
            raise SystemExit(1)

        time.sleep(60)

        if debug_mode:
            boutons = driver.find_elements(By.XPATH, "//button")
            logger.info(f"{len(boutons)} boutons trouvés sur la page")
            for b in boutons:
                logger.debug(b.get_attribute("outerHTML"))

        try:
            # Attendre que tout overlay disparaisse avant de tenter la déconnexion
            attendre_disparition_overlay(driver, 10, logger=logger, debug=debug_mode)
            
            user_menu_button = get_user_menu_button(driver, logger, args)
            
            # Tentative de clic standard, puis JS uniquement si le clic est intercepté
            try:
                user_menu_button.click()
            except ElementClickInterceptedException as e:
                logger.debug(f"Clic standard intercepté sur le menu utilisateur : {e}, tentative via JS.")
                driver.execute_script("arguments[0].click();", user_menu_button)

            time.sleep(2)
            # Seconde attente overlay : le menu peut provoquer un nouvel overlay
            attendre_disparition_overlay(driver, 10, logger=logger, debug=debug_mode)
            logout_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'cui-link__logout')]"))
            )
            # Tentative de clic standard, puis JS uniquement si un overlay intercepte le clic
            try:
                logout_link.click()
            except ElementClickInterceptedException as e:
                logger.debug(f"Clic standard intercepté sur le lien logout : {e}, tentative via JS.")
                driver.execute_script("arguments[0].click();", logout_link)
            logger.info("Déconnexion effectuée avec succès.")
            time.sleep(3)
        except Exception as e:
            logger.warning(f"Impossible de se déconnecter proprement : {e}", exc_info=debug_mode)

    except Exception as e:
        logger.error(f"Erreur inattendue dans le script principal : {e}")
        traceback.print_exc()
        pause_on_error()
    finally:
        close_browser_session(driver, logger, debug=bool(args.debug or config.get("DEBUG", False)))

        if download_dir:
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
    try:
        stdin = getattr(sys, "stdin", None)
        if stdin is not None and getattr(stdin, "isatty", lambda: False)():
            input("\nAppuyez sur Entrée pour fermer...")
    except Exception:
        pass

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
            LOG_RETENTION_DAYS, DAYS, get_dexcom_credentials
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
        
        # Déterminer la période selon les arguments — priorité : CLI > config.yaml > défaut
        date_debut_str, date_fin_str = resolve_effective_date_range(
            args.days, args.date_debut, args.date_fin,
            config.DAYS, config.DATE_DEBUT, config.DATE_FIN,
        )
        
        # Déterminer les rapports à télécharger
        rapports = args.rapports if args.rapports else config.RAPPORTS
        
        # Sécurisation pour l'affichage (conversion en liste si nécessaire)
        if rapports is None:
            rapports_str = "Aucun"
        elif isinstance(rapports, list):
            rapports_str = ', '.join(str(r) for r in rapports)
        else:
            rapports_str = str(rapports)

        # Afficher la configuration en mode dry-run
        print(f"\n{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}MODE DRY-RUN : Aucun téléchargement ne sera effectué{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}\n")
        
        print(f"{Fore.GREEN}Configuration détectée :{Style.RESET_ALL}\n")
        print(f"  {Fore.YELLOW}• Période :{Style.RESET_ALL} {date_debut_str} → {date_fin_str}")
        print(f"  {Fore.YELLOW}• Rapports :{Style.RESET_ALL} {rapports_str}")
        print(f"  {Fore.YELLOW}• Dossier de téléchargement :{Style.RESET_ALL} {config.DOWNLOAD_DIR}")
        print(f"  {Fore.YELLOW}• Dossier de destination :{Style.RESET_ALL} {config.DIR_FINAL_BASE}")
        print(f"  {Fore.YELLOW}• Mode debug :{Style.RESET_ALL} {'Activé' if args.debug else 'Désactivé'}")
        print(f"  {Fore.YELLOW}• Rétention des logs :{Style.RESET_ALL} {config.LOG_RETENTION_DAYS} jours")
        print(f"  {Fore.YELLOW}• URL Dexcom :{Style.RESET_ALL} {config.DEXCOM_URL}")
        print(f"  {Fore.YELLOW}• ChromeDriver log :{Style.RESET_ALL} {config.CHROMEDRIVER_LOG}")
        print(f"  {Fore.YELLOW}• Profil Chrome :{Style.RESET_ALL} {config.CHROME_USER_DATA_DIR}")
        
        # Vérifier les credentials
        try:
            username, password, country_code, phone_number = get_dexcom_credentials()
            print(f"\n  {Fore.GREEN}✓ Credentials Dexcom détectés{Style.RESET_ALL}")
            print(f"    {Fore.YELLOW}• Type d'authentification :{Style.RESET_ALL} ", end="")
            
            if country_code and phone_number:
                # Masquage des données sensibles pour la sécurité
                print(f"Numéro de téléphone (Masqué)")
            elif username:
                print(f"Email/Nom d'utilisateur")
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
    
    debug_flag = bool(args.debug or getattr(config, "DEBUG", False))
    logger = setup_logger(
        debug_flag,
        os.path.dirname(config.CHROMEDRIVER_LOG) or ".",
        config.NOW_STR
    )
    
    # ============================================
    # ÉTAPE 7 : Exécution de la fonction principale
    # ============================================
    
    main(args, logger, config.__dict__)  # ← Correction : config.__dict__ au lieu de config