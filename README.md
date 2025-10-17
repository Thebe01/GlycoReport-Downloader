# GlycoReport Downloader

[![Licence: CC BY-NC 4.0](https://img.shields.io/badge/Licence-CC--BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/deed.fr)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
![Build Status](https://img.shields.io/badge/build-manuel-lightgrey)
![Version](https://img.shields.io/badge/version-0.2.4-blue)

An English version of this text follows the French text.

---

## Sommaire

- [Nouveautés](#version--024--16-octobre-2025)
- [Installation et utilisation](#installation-et-utilisation)
- [Configuration](#configuration)
- [Fonctionnalités principales](#fonctionnalités-principales)
- [Historique des versions](#historique-des-versions)
- [Tests unitaires](#tests-unitaires)
- [Notes](#notes)
- [Licence](#licence)
- [GlycoReport Downloader (English)](#glycoreport-downloader-english)

---

## Version : 0.2.4 — 16 octobre 2025

### Nouveautés

**Gestion automatique de ChromeDriver**

- Utilisation de ChromeDriverManager pour charger automatiquement la version
  courante de ChromeDriver (plus besoin de version spécifique)
- Suppression du paramètre obsolète `chromedriver_path` (nettoyage du code)
- Simplification de la distribution : le répertoire `chromedriver-win64/` n'est
  plus nécessaire
- Réduction de la taille du package de distribution (~10 MB en moins)

**Améliorations fonctionnelles**

- Correction de l'accès au rapport Statistiques horaires (xpath adapté,
  robustesse accrue)
- Le script est désormais indépendant de la langue de l'utilisateur (messages et
  sélecteurs)
- La période de rétention des logs par défaut passe à 30 jours
  (`log_retention_days: 30`)

**Améliorations techniques**

- Ajout de la colonne "Billet" dans les blocs d'historique des modifications
- Synchronisation des entêtes et commentaires de version dans tous les modules
- Corrections mineures et robustesse accrue sur la gestion des erreurs et la
  configuration

---

## Historique des versions

### 0.2.4 — 16 octobre 2025

- Suppression du paramètre obsolète `chromedriver_path` (non utilisé depuis
  v0.2.3).
- Nettoyage du code : `CHROMEDRIVER_PATH` retiré de la configuration.
- Simplification : le répertoire `chromedriver-win64/` n'est plus nécessaire.
- ChromeDriverManager gère automatiquement le téléchargement de la version
  appropriée.
- Réduction de la taille du package de distribution (~10 MB en moins).
- Aucun changement fonctionnel pour l'utilisateur.

### 0.2.3 — 14 octobre 2025

- Utilisation de ChromeDriverManager pour toujours charger la version courante.
- Correction du xpath pour le rapport Statistiques horaires (robustesse accrue).
- Indépendance de la langue utilisateur (sélecteurs et messages).
- Ajout de la colonne Billet dans les historiques de modifications.
- Période de rétention des logs portée à 30 jours par défaut.
- Synchronisation des entêtes et commentaires de version dans tous les modules.
- Corrections mineures et robustesse accrue.

### 0.2.2 — 29 août 2025

- Séparation stricte de la gestion des arguments CLI (désormais dans
  GlycoDownload.py).
- Affichage du help possible même sans fichiers de configuration.
- Plus aucun accès ni création de fichiers de config/env lors de l’affichage du
  help.
- Nettoyage des doublons de fonctions CLI.
- Synchronisation et nettoyage des entêtes de tous les modules.

### 0.2.1 — 29 août 2025

- Changement de nom du projet (anciennement Dexcom Clarity Reports Downloader).

### 0.2.0 — 28 août 2025

- `.env` chiffré à l’écriture et déchiffré à la volée.
- Clé d’encryption stockée dans une variable d’environnement système.
- Suppression de la saisie interactive des identifiants Dexcom.
- Sécurisation de la gestion des logs et des fichiers temporaires.

### 0.1.10 — 28 août 2025

- Le ménage des logs s'effectue désormais uniquement après l'activation du
  logging.
- Chaque suppression de log est loggée.

### 0.1.9 — 28 août 2025

- Vérification interactive de la clé `chromedriver_log` lors de la création de
  `config.yaml`.
- Empêche la saisie d'un dossier pour le log, exige un chemin de fichier.
- Correction de la robustesse de la configuration initiale.

### 0.1.8 — 27 août 2025

- Configuration interactive avancée pour `config.yaml` et `.env` lors du premier
  lancement.
- Copie minimale du profil Chrome lors de la configuration initiale.
- Ajout du paramètre `log_retention_days` (0 = conservation illimitée).
- Nettoyage automatique des logs selon la durée de rétention.
- Messages utilisateurs colorés et validation renforcée des paramètres.

### 0.1.7 — 25 août 2025

- Création automatique de `config.yaml` à partir de `config_example.yaml` si
  absent
- Gestion interactive des credentials si `.env` absent (demande à l'utilisateur,
  non conservé)
- Précision sur la présence de `chromedriver-win64` fourni

### 0.1.6 — 22 août 2025

- Synchronisation des versions dans tous les modules (bloc commentaires de
  version à jour)
- Ajout du module `version.py` (source unique de vérité pour la version)
- Log de la version exécutée au démarrage
- Correction des chemins YAML (utilisation systématique de `/`)
- Compatibilité interface Dexcom août 2025 (gestion de la page "Pas maintenant")
- Robustesse saisie identifiant et gestion avancée des erreurs
- Captures d’écran uniquement en mode debug
- Logs détaillés pour chaque étape critique
- Sélecteurs robustes pour les champs de connexion

---

## Architecture

- `GlycoDownload.py` : script principal, gestion CLI, help, logique métier.
- `config.py` : centralise la configuration et les credentials.
- `utils.py` : fonctions utilitaires.
- `rapports.py` : traitement des rapports.
- `tests/` : tests unitaires.
- `version.py` : numéro de version du projet.

## Description

GlycoReport Downloader est un outil automatisé permettant de télécharger,
organiser et archiver les rapports Dexcom Clarity pour un suivi glycémique
efficace. Le projet est conçu pour être portable, configurable et robuste, avec
une gestion avancée des logs, des erreurs et de la sécurité.

LA VERSION ACTUELLE NE SUPPORTE QUE LE FRANÇAIS. Une prochaine version devrait
être indépendante de la langue et afficher des messages en français pour les
usagers francophones et en anglais pour les autres.

---

## Release disponible

Une archive ZIP prête à l’emploi est disponible dans la section
[Releases](https://github.com/<ton-utilisateur>/<ton-repo>/releases) du projet
GitHub. Téléchargez l’archive `.zip` pour Windows, puis décompressez-la pour
obtenir tous les fichiers nécessaires (voir instructions ci-dessous).

---

## Limitations et avertissements

- Ce projet n’est ni affilié, ni supporté, ni approuvé par Dexcom, Inc.
- L’utilisation de cet outil se fait à vos risques et périls : respectez les
  conditions d’utilisation du service Dexcom Clarity.
- Ne partagez jamais votre clé d’encryption ou vos identifiants.
- Toute utilisation commerciale est strictement interdite sans autorisation
  écrite préalable.

Pour plus d’informations sur Dexcom Clarity :
[https://clarity.dexcom.eu](https://clarity.dexcom.eu)

---

## Fonctionnalités principales

- Téléchargement automatisé de tous les rapports Dexcom Clarity sélectionnés
- Configuration centralisée via un fichier `config.yaml` (non versionné)
- Exemple de configuration fourni dans `config_example.yaml`
- Prise en charge des chemins portables (`~` et `/`), normalisés automatiquement
- Prise en charge de l’authentification par courriel/nom d’usager **ou** par
  numéro de téléphone (avec code pays et numéro, via variables d’environnement)
- Gestion avancée des logs (application, navigateur, logs JS)
- Capture d’écran automatique avec délai en cas d’erreur critique (pour
  diagnostic, uniquement en mode debug)
- Sélection de la période, des rapports et du mode debug via la ligne de
  commande
- Robustesse accrue sur la gestion des erreurs, des téléchargements et de la
  configuration
- Compatible Windows (et adaptable Linux/Mac)
- Tests unitaires couvrant toutes les fonctions utilitaires

---

## Installation et utilisation

### Prérequis

- Windows 10 ou supérieur
- [Python 3.10+](https://www.python.org/downloads/) (pour l’utilisation en mode
  script)
- Google Chrome installé
- Droits administrateur pour définir la variable d’environnement système

### Procédure

1. **Téléchargez l'archive ZIP du release** depuis la page Releases du projet.
2. **Décompressez tout le contenu du ZIP** dans un dossier de votre choix (ex :
   `C:\GlycoReport-Downloader`).
   - Le dossier doit contenir :
     - `GlycoReport-Downloader.exe`
     - `config_example.yaml`
     - `.env.example`
     - `migrate.exe` (outil de migration, optionnel)
     - `MIGRATION.md` (documentation de migration, optionnel)
3. **Lancez `GlycoReport-Downloader.exe`** en double-cliquant ou via le
   terminal.
4. **Lors du premier lancement**, si les fichiers `config.yaml` ou `.env` sont
   absents, l'application vous informera et lancera la configuration initiale.
5. **Les fichiers de configuration seront créés dans le même dossier que
   l'exécutable.**

### Migration depuis une version antérieure

Si vous mettez à jour depuis une version < 0.2.3, un outil de migration est
disponible pour nettoyer automatiquement votre configuration :

**Windows :**

```powershell
.\migrate.exe
```

**Avec Python (toutes plateformes) :**

```bash
python migrate.py
```

Consultez le fichier [MIGRATION.md](MIGRATION.md) pour plus de détails sur le
processus de migration.

---

## Création de l'exécutable Windows

Pour générer l'exécutable à partir du code source, utilisez la commande suivante
:

**Bash/CMD :**

```sh
pyinstaller --onefile --hidden-import=yaml --name "GlycoReport-Downloader" GlycoDownload.py
```

**PowerShell :**

```powershell
pyinstaller --onefile --hidden-import=yaml --name "GlycoReport-Downloader" GlycoDownload.py
```

- L'option `--hidden-import=yaml` est nécessaire pour inclure le module PyYAML
  dans l'exécutable.
- L'exécutable sera généré dans le dossier `dist/` sous le nom
  `GlycoReport-Downloader.exe`.

---

## Création du package de distribution

Un script PowerShell automatisé (`DIST-GlycoReport-Downloader.ps1`) est fourni
pour faciliter la création d'un package prêt à distribuer. Ce script :

- Génère l'exécutable Windows avec PyInstaller
- Vérifie la présence de tous les fichiers nécessaires à la distribution
- Copie les fichiers `.env.example`, `config_example.yaml`, `LICENSE.txt`,
  `README.md` dans le dossier `dist`
- Crée une archive ZIP (`GlycoReport-Downloader.zip`) à la racine du projet à
  partir du contenu du dossier `dist`

**Note** : Depuis la version 0.2.3, ChromeDriverManager télécharge
automatiquement la version appropriée de ChromeDriver, il n'est donc plus
nécessaire d'inclure le dossier `chromedriver-win64` dans la distribution.

### Utilisation

Ouvre un terminal PowerShell à la racine du projet et exécute :

```powershell
[DIST-GlycoReport-Downloader.ps1]
```

---

## Gestion des dates par défaut

- **Par défaut**, si aucune date n'est fournie en argument ou dans le fichier
  `config.yaml`, la période utilisée sera les **14 derniers jours jusqu'à
  hier**.
- Vous pouvez surcharger ce comportement :
  - en passant `--days 7`, `--days 14`, `--days 30` ou `--days 90` en argument,
  - ou en définissant explicitement `date_debut` et `date_fin` dans
    `config.yaml`,
  - ou encore en passant `--date_debut` et `--date_fin` en argument.

Exemple :

- Si nous sommes le 2025-08-18 et que vous ne passez aucun paramètre, la période
  sera du 2025-08-04 au 2025-08-17.

---

## Configuration

La configuration du projet se fait principalement via deux fichiers :

- `config.yaml` : centralise les paramètres (dossiers, URL, rapports, rétention
  des logs, etc.)
- `.env` : stocke les identifiants Dexcom (chiffrés pour plus de sécurité)

Exemple de configuration dans `config.yaml` :

```yaml
chrome_user_data_dir: C:/Users/Utilisateur/Downloads/GlycoReport-Downloader/Profile
chromedriver_log: C:/Users/Utilisateur/Downloads/GlycoReport-Downloader/clarity_chromedriver.log
dexcom_url: "https://clarity.dexcom.eu"
download_dir: C:/Users/Utilisateur/Downloads/GlycoReport-Downloader
log_retention_days: 30
output_dir: C:/Users/Utilisateur/Downloads/GlycoReport-Downloader
rapports:
  [
    "Aperçu",
    "Modèles",
    "Superposition",
    "Quotidien",
    "Comparer",
    "Statistiques",
    "AGP",
    "Export",
  ]
```

La clé d'encryption pour le fichier `.env` est stockée dans la variable
d'environnement système `ENV_DEXCOM_KEY`.

---

## Normalisation systématique des chemins

Tous les chemins utilisés dans le projet (dossiers de téléchargement, profils,
logs, etc.) sont **normalisés automatiquement** :

- Les chemins commençant par `~` sont convertis en chemin absolu utilisateur.
- Les `/` sont utilisés partout pour garantir la portabilité (Windows, Mac,
  Linux).
- La normalisation est effectuée dans le code via `os.path.expanduser` et
  `os.path.abspath` (fonction centralisée dans `utils.py`).

**Exemple dans `config.yaml` :**

```yaml
chrome_user_data_dir: C:\Users\????????\Downloads\GlycoReport-Downloader\Profile
chromedriver_log: C:\Users\????????\Downloads\GlycoReport-Downloader\clarity_chromedriver.log
dexcom_url: "https://clarity.dexcom.eu"
download_dir: C:\Users\????????\Downloads\GlycoReport-Downloader
log_retention_days: 30
output_dir: C:\Users\????????\Downloads\GlycoReport-Downloader
rapports: ["Aperçu"]
```

---

## Sécurité et gestion des secrets

- Le fichier `.env` est **chiffré** à l’aide d’une clé Fernet générée
  automatiquement lors de la première configuration.
- La clé d’encryption est stockée dans une variable d’environnement système
  `ENV_DEXCOM_KEY` (créée via PowerShell).
- Les identifiants Dexcom ne sont **jamais affichés ni stockés en clair**.
- Si les identifiants sont absents ou incomplets dans le `.env`, le script
  s’arrête avec un message d’erreur explicite.
- **Aucune saisie interactive** des identifiants n’est proposée pour des raisons
  de sécurité.

## Procédure de première utilisation

1. Lancez le script. Une clé d’encryption sera générée et une commande
   PowerShell à copier/coller s’affichera.
2. Collez cette commande dans la fenêtre PowerShell qui s’ouvre, puis tapez
   `Exit`.
3. Relancez le script pour poursuivre la configuration.
4. Lors de la création du `.env`, les informations saisies seront chiffrées
   automatiquement.

---

## Paramètres de la ligne de commande

- `-h`, `--help` : Afficher l’aide et quitter.
- `--debug`, `-d` : Activer le mode debug.
- `--days {7,14,30,90}` : Nombre de jours à inclure dans le rapport (7, 14, 30,
  90).
- `--date_debut DATE_DEBUT` : Date de début (AAAA-MM-JJ).
- `--date_fin DATE_FIN` : Date de fin (AAAA-MM-JJ).
- `--rapports RAPPORTS [RAPPORTS ...]` : Liste des rapports à traiter (ex :
  `"Aperçu" "AGP"`).

**Remarque** : L’aide s’affiche toujours proprement, même si les fichiers de
configuration sont absents ou incomplets.

---

## Exemple d’aide

```text
usage:  [-h] [--debug] [--days {7,14,30,90}] [--date_debut DATE_DEBUT]
                        [--date_fin DATE_FIN] [--rapports RAPPORTS [RAPPORTS ...]]

options:
  -h, --help            afficher cette aide et quitter
  --debug, -d           Activer le mode debug
  --days {7,14,30,90}   Nombre de jours à inclure dans le rapport (7, 14, 30, 90)
  --date_debut DATE_DEBUT
                        Date de début (AAAA-MM-JJ)
  --date_fin DATE_FIN   Date de fin (AAAA-MM-JJ)
  --rapports RAPPORTS [RAPPORTS ...]
                        Liste des rapports à traiter
```

---

## Tests unitaires

Pour exécuter tous les tests unitaires sur les fonctions utilitaires du projet,
utilisez la commande suivante :

**Bash/CMD :**

```sh
pytest -v --log-cli-level=INFO tests/test_utils.py
```

**PowerShell :**

```powershell
pytest -v --log-cli-level=INFO tests/test_utils.py
```

- `-v` affiche le détail de chaque test exécuté (mode verbose).
- `--log-cli-level=INFO` affiche les messages de log générés par les fonctions
  testées.
- Cette commande permet de vérifier la robustesse et la portabilité de toutes
  les fonctions utilitaires du projet.

Assurez-vous d’avoir installé pytest :

**Bash/CMD :**

```sh
pip install pytest
```

**PowerShell :**

```powershell
pip install pytest
```

---

## Notes

- Les rapports sont organisés par année dans le dossier de destination.
- En cas de perte de connexion, le script gère les erreurs et reprend là où il
  s'est arrêté.
- Pour toute question, suggestion ou rapport de bug, ouvrez une issue sur
  GitHub.
- Merci de ne pas redistribuer ce code sans autorisation. Ce projet est fourni
  tel quel, sans garantie.

---

## Auteur

Pierre Théberge

---

## Licence

Ce projet est distribué sous licence
[Creative Commons Attribution - Pas d’Utilisation Commerciale 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/deed.fr).

Vous êtes autorisé à partager et adapter ce projet à des fins **non
commerciales**, à condition de créditer l’auteur. **Toute utilisation
commerciale est strictement interdite sans autorisation écrite préalable.**

Pour le texte complet de la licence, voir le fichier [LICENSE.txt](LICENSE.txt).

---

# GlycoReport Downloader (English)

## Summary

- [What's New](#whats-new-english)
- [Version History](#version-history-english)
- [Architecture](#architecture-english)
- [Description](#description-english)
- [Release Available](#release-available-english)
- [Limitations and Warnings](#limitations-and-warnings-english)
- [Main Features](#main-features-english)
- [Installation and Usage](#installation-and-usage-english)
- [Building the Windows Executable](#building-the-windows-executable-english)
- [Creating the Distribution Package](#creating-the-distribution-package-english)
- [Default Date Handling](#default-date-handling-english)
- [Configuration](#configuration-english)
- [Systematic Path Normalization](#systematic-path-normalization-english)
- [Security and Secret Management](#security-and-secret-management-english)
- [First-Time Use Procedure](#first-time-use-procedure-english)
- [Command Line Parameters](#command-line-parameters-english)
- [Example Help Output](#example-help-output-english)
- [Unit Tests](#unit-tests-english)
- [Notes](#notes-english)
- [Author](#author-english)
- [License](#license-english)

---

## What's New (English)

### Version: 0.2.4 — October 16, 2025

**Automatic ChromeDriver Management**

- Uses ChromeDriverManager to automatically load the current ChromeDriver
  version (no more version-specific issues)
- Removed obsolete `chromedriver_path` parameter (code cleanup)
- Simplified distribution: the `chromedriver-win64/` directory is no longer
  necessary
- Reduced distribution package size (~10 MB smaller)

**Functional Improvements**

- Fixed access to the Hourly Statistics report (adapted xpath, improved
  robustness)
- The script is now language-independent (selectors and messages)
- Default log retention period is now 30 days (`log_retention_days: 30`)

**Technical Improvements**

- Added the "Billet" column in change history blocks
- Synchronized headers and version comments in all modules
- Minor corrections and improved robustness in error and configuration
  management

---

## Version History (English)

### 0.2.4 — October 16, 2025

- Removed obsolete `chromedriver_path` parameter (unused since v0.2.3).
- Code cleanup: `CHROMEDRIVER_PATH` removed from configuration.
- Simplification: the `chromedriver-win64/` directory is no longer necessary.
- ChromeDriverManager automatically manages the download of the appropriate
  version.
- Reduced distribution package size (~10 MB smaller).
- No functional changes for the user.

### 0.2.3 — October 14, 2025

- Uses chromedriver manager to always load the current version.
- Fixed xpath for Hourly Statistics report (improved robustness).
- Language independence for selectors and messages.
- Added the Billet column in change histories.
- Default log retention period set to 30 days.
- Synchronized headers and version comments in all modules.
- Minor corrections and improved robustness.

### 0.2.2 — August 29, 2025

- Strict separation of CLI argument handling (now in GlycoDownload.py).
- Help can be displayed even if configuration files are missing.
- No access or creation of config/env files when displaying help.
- Cleanup of duplicate CLI functions.
- Synchronization and cleanup of all module headers.

### 0.2.1 — August 29, 2025

- Project renamed (formerly Dexcom Clarity Reports Downloader).

### 0.2.0 — August 28, 2025

- `.env` encrypted on write and decrypted on the fly.
- Encryption key stored in a system environment variable.
- Removal of interactive Dexcom credential entry.
- Secured management of logs and temporary files.

### 0.1.10 — August 28, 2025

- Log cleanup now only occurs after logging is enabled.
- Each log deletion is logged.

### 0.1.9 — August 28, 2025

- Interactive verification of the `chromedriver_log` key when creating
  `config.yaml`.
- Prevents entering a folder for the log, requires a file path.
- Improved robustness of initial configuration.

### 0.1.8 — August 27, 2025

- Advanced interactive configuration for `config.yaml` and `.env` on first
  launch.
- Minimal Chrome profile copy during initial setup.
- Added `log_retention_days` parameter (0 = unlimited retention).
- Automatic log cleanup according to retention period.
- Colored user messages and enhanced parameter validation.

### 0.1.7 — August 25, 2025

- Automatic creation of `config.yaml` from `config_example.yaml` if missing.
- Interactive credential management if `.env` is missing (prompt, not saved).
- Clarification on the presence of provided `chromedriver-win64`.

### 0.1.6 — August 22, 2025

- Version synchronization in all modules (up-to-date version comment blocks).
- Added `version.py` module (single source of truth for version).
- Log the running version at startup.
- YAML path corrections (systematic use of `/`).
- Dexcom interface compatibility August 2025 ("Not now" page handling).
- Robust username entry and advanced error handling.
- Screenshots only in debug mode.
- Detailed logs for each critical step.
- Robust selectors for login fields.

---

## Architecture (English)

- `GlycoDownload.py`: main script, CLI handling, help, business logic.
- `config.py`: centralizes configuration and credentials.
- `utils.py`: utility functions.
- `rapports.py`: report processing.
- `tests/`: unit tests.
- `version.py`: project version number.

## Description (English)

GlycoReport Downloader is an automated tool for downloading, organizing, and
archiving Dexcom Clarity reports for effective glycemic monitoring. The project
is designed to be portable, configurable, and robust, with advanced management
of logs, errors, and security.

**THE CURRENT VERSION SUPPORTS ONLY FRENCH.** A future version should be
language-independent and display messages in French for French-speaking users
and in English for others.

---

## Release Available (English)

A ready-to-use ZIP archive is available in the
[Releases](https://github.com/<your-username>/<your-repo>/releases) section of
the GitHub project. Download the `.zip` for Windows, then extract it to get all
necessary files (see instructions below).

---

## Limitations and Warnings (English)

- This project is neither affiliated with, supported by, nor endorsed by Dexcom,
  Inc.
- Use this tool at your own risk: comply with Dexcom Clarity's terms of service.
- Never share your encryption key or credentials.
- Any commercial use is strictly prohibited without prior written authorization.

For more information about Dexcom Clarity:
[https://clarity.dexcom.eu](https://clarity.dexcom.eu)

---

## Main Features (English)

- Automated download of all selected Dexcom Clarity reports
- Centralized configuration via a `config.yaml` file (not versioned)
- Example configuration provided in `config_example.yaml`
- Support for portable paths (`~` and `/`), automatically normalized
- Support for authentication by email/username **or** by phone number (with
  country code and number, via environment variables)
- Advanced log management (application, browser, JS logs)
- Automatic screenshot with delay in case of critical error (for diagnostics,
  debug mode only)
- Selection of period, reports, and debug mode via command line
- Increased robustness in error, download, and configuration management
- Windows compatible (and adaptable to Linux/Mac)
- Automatic use of the current chromedriver version (chromedriver manager)
- Improved robustness for Statistics report (adapted selectors, multilingual
  handling)
- Unit tests covering all utility functions

---

## Installation and Usage (English)

### Prerequisites

- Windows 10 or higher
- [Python 3.10+](https://www.python.org/downloads/) (for script mode)
- Google Chrome installed
- Administrator rights to set the system environment variable

### Procedure

1. **Download the ZIP archive from the release** page.
2. **Extract all ZIP contents** into a folder of your choice (e.g.,
   `C:\GlycoReport-Downloader`).
   - The folder should contain:
     - `GlycoReport-Downloader.exe`
     - `config_example.yaml`
     - `.env.example`
     - `migrate.exe` (migration tool, optional)
     - `MIGRATION.md` (migration documentation, optional)
3. **Run `GlycoReport-Downloader.exe`** by double-clicking or via the terminal.
4. **On first launch**, if `config.yaml` or `.env` files are missing, the
   application will inform you and start the initial configuration.
5. **Configuration files will be created in the same folder as the executable.**

### Migrating from an Earlier Version

If you are upgrading from a version < 0.2.3, a migration tool is available to
automatically clean up your configuration:

**Windows:**

```powershell
.\migrate.exe
```

**With Python (all platforms):**

```bash
python migrate.py
```

See the [MIGRATION.md](MIGRATION.md) file for details on the migration process.

---

## Building the Windows Executable (English)

To generate the executable from the source code, use:

**Bash/CMD:**

```sh
pyinstaller --onefile --hidden-import=yaml --name "GlycoReport-Downloader" GlycoDownload.py
```

**PowerShell:**

```powershell
pyinstaller --onefile --hidden-import=yaml --name "GlycoReport-Downloader" GlycoDownload.py
```

- The `--hidden-import=yaml` option is necessary to include the PyYAML module in
  the executable.
- The executable will be generated in the `dist/` folder as
  `GlycoReport-Downloader.exe`.

---

## Creating the Distribution Package (English)

An automated PowerShell script (`DIST-GlycoReport-Downloader.ps1`) is provided
to facilitate the creation of a ready-to-distribute package. This script:

- Generates the Windows executable with PyInstaller
- Checks for the presence of all necessary distribution files
- Copies `.env.example`, `config_example.yaml`, `LICENSE.txt`, `README.md` to
  the `dist` folder
- Creates a ZIP archive (`GlycoReport-Downloader.zip`) in the `dist` folder from
  its contents

**Note**: Since version 0.2.3, ChromeDriverManager automatically downloads the
appropriate ChromeDriver version, so it is no longer necessary to include the
`chromedriver-win64` folder in the distribution.

### Usage

Open a PowerShell terminal at the project root and run:

```powershell
.\DIST-GlycoReport-Downloader.ps1
```

---

## Default Date Handling (English)

- **By default**, if no date is provided as an argument or in the `config.yaml`
  file, the period used will be the **last 14 days up to yesterday**.
- You can override this behavior:
  - by passing `--days 7`, `--days 14`, `--days 30`, or `--days 90` as an
    argument,
  - or by explicitly setting `date_debut` and `date_fin` in `config.yaml`,
  - or by passing `--date_debut` and `--date_fin` as arguments.

Example:

- If today is 2025-08-18 and you pass no parameters, the period will be from
  2025-08-04 to 2025-08-17.

---

## Configuration (English)

Configuration is mainly handled via two files:

- `config.yaml`: centralizes parameters (folders, URL, reports, log retention,
  etc.)
- `.env`: stores Dexcom credentials (encrypted for enhanced security)

Example configuration in `config.yaml`:

```yaml
chrome_user_data_dir: C:/Users/YourUser/Downloads/GlycoReport-Downloader/Profile
chromedriver_log: C:/Users/YourUser/Downloads/GlycoReport-Downloader/clarity_chromedriver.log
dexcom_url: "https://clarity.dexcom.eu"
download_dir: C:/Users/YourUser/Downloads/GlycoReport-Downloader
log_retention_days: 30
output_dir: C:/Users/YourUser/Downloads/GlycoReport-Downloader
rapports:
  [
    "Aperçu",
    "Modèles",
    "Superposition",
    "Quotidien",
    "Comparer",
    "Statistiques",
    "AGP",
    "Export",
  ]
```

The encryption key for the `.env` file is stored in the system environment
variable `ENV_DEXCOM_KEY`.

---

## Systematic Path Normalization (English)

All paths used in the project (download folders, profiles, logs, etc.) are
**automatically normalized**:

- Paths starting with `~` are converted to absolute user paths.
- `/` is used everywhere to ensure portability (Windows, Mac, Linux).
- Normalization is done in the code via `os.path.expanduser` and
  `os.path.abspath` (centralized function in `utils.py`).

**Example in `config.yaml`**:

```yaml
chrome_user_data_dir: C:/Users/YourUser/Downloads/GlycoReport-Downloader/Profile
chromedriver_log: C:/Users/YourUser/Downloads/GlycoReport-Downloader/clarity_chromedriver.log
dexcom_url: "https://clarity.dexcom.eu"
download_dir: C:/Users/YourUser/Downloads/GlycoReport-Downloader
log_retention_days: 30
output_dir: C:/Users/YourUser/Downloads/GlycoReport-Downloader
rapports: ["Aperçu"]
```

---

## Security and Secret Management (English)

- The `.env` file is **encrypted** using a Fernet key automatically generated
  during the first configuration.
- The encryption key is stored in the system environment variable
  `ENV_DEXCOM_KEY` (created via PowerShell).
- Dexcom credentials are **never displayed or stored in plaintext**.
- If credentials are missing or incomplete in the `.env`, the script stops with
  an explicit error message.
- **No interactive input** of credentials is offered for security reasons.

## First-Time Use Procedure (English)

1. Run the script. An encryption key will be generated, and a PowerShell command
   to copy/paste will be displayed.
2. Paste this command into the PowerShell window that opens, then type `Exit`.
3. Rerun the script to continue the configuration.
4. When creating the `.env`, the entered information will be automatically
   encrypted.

---

## Command Line Parameters (English)

- `-h`, `--help`: Display help and exit.
- `--debug`, `-d`: Enable debug mode.
- `--days {7,14,30,90}`: Number of days to include in the report (7, 14, 30,
  90).
- `--date_debut DATE_DEBUT`: Start date (YYYY-MM-DD).
- `--date_fin DATE_FIN`: End date (YYYY-MM-DD).
- `--rapports RAPPORTS [RAPPORTS ...]`: List of reports to process (e.g.,
  `"Aperçu" "AGP"`).

**Note**: Help is always displayed neatly, even if configuration files are
missing or incomplete.

---

## Example Help Output (English)

```text
usage:  [-h] [--debug] [--days {7,14,30,90}] [--date_debut DATE_DEBUT]
                        [--date_fin DATE_FIN] [--rapports RAPPORTS [RAPPORTS ...]]

options:
  -h, --help            display this help and quit
  --debug, -d           Enable debug mode
  --days {7,14,30,90}   Number of days to include in the report (7, 14, 30, 90)
  --date_debut DATE_DEBUT
                        Start date (YYYY-MM-DD)
  --date_fin DATE_FIN   End date (YYYY-MM-DD)
  --rapports RAPPORTS [RAPPORTS ...]
                        List of reports to process
```

---

## Unit Tests (English)

To run all unit tests for the project's utility functions, use the following
command:

**Bash/CMD:**

```sh
pytest -v --log-cli-level=INFO tests/test_utils.py
```

**PowerShell:**

```powershell
pytest -v --log-cli-level=INFO tests/test_utils.py
```

- `-v` displays details of each executed test (verbose mode).
- `--log-cli-level=INFO` shows log messages generated by the tested functions.
- This command verifies the robustness and portability of all utility functions
  in the project.

Make sure pytest is installed:

**Bash/CMD:**

```sh
pip install pytest
```

**PowerShell:**

```powershell
pip install pytest
```

---

## Notes (English)

- Reports are organized by year in the destination folder.
- If the connection is lost, the script handles errors and resumes where it left
  off.
- For any questions, suggestions, or bug reports, please open an issue on
  GitHub.
- Please do not redistribute this code without authorization. This project is
  provided as is, without warranty.

---

## Author (English)

Pierre Théberge

---

## License (English)

This project is distributed under the
[Creative Commons Attribution - Non-Commercial Use 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/deed.fr).

You are allowed to share and adapt this project for **non-commercial** purposes,
provided that you credit the author. **Any commercial use is strictly prohibited
without prior written authorization.**

For the full text of the license, see the [LICENSE.txt](LICENSE.txt) file.
