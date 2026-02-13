# GlycoReport Downloader

[![Licence: CC BY-NC 4.0](https://img.shields.io/badge/Licence-CC--BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/deed.fr)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
![Build Status](https://img.shields.io/badge/build-manuel-lightgrey)
![Version](https://img.shields.io/badge/version-0.3.13-blue)

An English version of this text follows the French text.

Note: La version francaise est la source de verite. La version anglaise est une
traduction stricte de la version francaise.

---

## Sommaire

- [Nouveautés](#version--0313--12-f%C3%A9vrier-2026)
- [Installation et utilisation](#installation-et-utilisation)
- [Configuration](#configuration)
- [Fonctionnalités principales](#fonctionnalités-principales)
- [Historique des versions](#historique-des-versions)
- [Tests unitaires](#tests-unitaires)
- [Notes](#notes)
- [Licence](#licence)
- [GlycoReport Downloader (English)](#glycoreport-downloader-english)

---

## Version : 0.3.13 — 12 février 2026

### Nouveautés (0.3.13)

**Correctifs :**

- Comparer: téléchargement limité à Tendances (bug Dexcom sur Superposition et
  Quotidien), avec avertissement dans les logs.

---

## Version : 0.3.12 — 12 février 2026

### Nouveautés (0.3.12)

**Correctifs :**

- Accès direct aux sous-rapports Comparer via /compare/overlay et
  /compare/daily.

---

## Version : 0.3.11 — 12 février 2026

### Nouveautés (0.3.11)

**Correctifs :**

- Navigation via l'URL base
  [https://clarity.dexcom.eu/i](https://clarity.dexcom.eu/i) pour Comparer.

---

## Version : 0.3.10 — 12 février 2026

### Nouveautés (0.3.10)

**Correctifs :**

- Retry des clics Comparer (stale element) et navigation overview -> reports.

---

## Version : 0.3.9 — 12 février 2026

### Nouveautés (0.3.9)

**Correctifs :**

- Navigation vers l'aperçu avec dates, puis retour /reports pour éviter le gel
  Comparer.

---

## Version : 0.3.8 — 12 février 2026

### Nouveautés (0.3.8)

**Correctifs :**

- Fermeture/réouverture de la modale Comparer entre chaque sous-rapport pour
  forcer la régénération des PDF.

---

## Version : 0.3.7 — 12 février 2026

### Nouveautés (0.3.7)

**Correctifs :**

- Attente du contenu graphique et délai supplémentaire pour génération PDF
  (sous-rapports Comparer).

---

## Version : 0.3.6 — 12 février 2026

### Nouveautés (0.3.6)

**Correctifs :**

- Stabilisation renforcée des sous-rapports Comparer.

---

## Version : 0.3.5 — 12 février 2026

### Nouveautés (0.3.5)

**Correctifs :**

- Stabilisation des sous-rapports Comparer.
- Forçage du dossier de téléchargement via Chrome (download_dir).

---

## Version : 0.3.4 — 12 février 2026

### Nouveautés (0.3.4)

**Correctifs :**

- Correction du téléchargement des sous-rapports Comparer.

---

## Version : 0.3.3 — 2 février 2026

### Nouveautés (0.3.3)

**Correctifs :**

- Normalisation des extensions attendues (téléchargements).

---

## Version : 0.3.2 — 2 février 2026

### Nouveautés (0.3.2)

**Correctifs :**

- Filtrage des fichiers téléchargés par extension.

---

## Version : 0.3.1 — 2 février 2026

### Nouveautés (0.3.1)

**Correctifs :**

- Robustesse de `pause_on_error` en contexte non interactif.
- Améliorations du script `Launch-Dexcom-And-Run.ps1` (chemins, attache
  Chrome/Selenium, exe).

---

## Version : 0.3.0 — 29 janvier 2026

### Nouveautés (0.3.0)

**Démarrage assisté :**

- Ajout du point d'entrée `--start-at-date-selection` (reprise après connexion).
- Ajout du script `Launch-Dexcom-And-Run.ps1` pour ouvrir Chrome avec le profil
  et lancer l'app.

---

## Historique des versions

### 0.3.13 — 12 février 2026

- Comparer: téléchargement limité à Tendances (bug Dexcom sur Superposition et
  Quotidien), avec avertissement dans les logs.

### 0.3.12 — 12 février 2026

- Accès direct aux sous-rapports Comparer via /compare/overlay et
  /compare/daily.

### 0.3.11 — 12 février 2026

- Navigation via l'URL base
  [https://clarity.dexcom.eu/i](https://clarity.dexcom.eu/i) pour Comparer.

### 0.3.10 — 12 février 2026

- Retry des clics Comparer (stale element) et navigation overview -> reports.

### 0.3.9 — 12 février 2026

- Navigation vers l'aperçu avec dates, puis retour /reports pour éviter le gel
  Comparer.

### 0.3.8 — 12 février 2026

- Fermeture/réouverture de la modale Comparer entre chaque sous-rapport pour
  forcer la régénération des PDF.

### 0.3.7 — 12 février 2026

- Attente du contenu graphique et délai supplémentaire pour génération PDF
  (sous-rapports Comparer).

### 0.3.6 — 12 février 2026

- Stabilisation renforcée des sous-rapports Comparer.

### 0.3.5 — 12 février 2026

- Stabilisation des sous-rapports Comparer.
- Forçage du dossier de téléchargement via Chrome (download_dir).

### 0.3.4 — 12 février 2026

- Correction du téléchargement des sous-rapports Comparer.

### 0.3.3 — 2 février 2026

- Normalisation des extensions attendues (téléchargements).

### 0.3.2 — 2 février 2026

- Filtrage des fichiers téléchargés par extension.

### 0.3.1 — 2 février 2026

- Robustesse de `pause_on_error` en contexte non interactif.
- Améliorations du script `Launch-Dexcom-And-Run.ps1` (chemins, attache
  Chrome/Selenium, exe).

### 0.3.0 — 29 janvier 2026

- Ajout du point d'entrée `--start-at-date-selection` (reprise après connexion).
- Ajout du script `Launch-Dexcom-And-Run.ps1` pour ouvrir Chrome avec le profil
  et lancer l'app.

### 0.2.18 — 20 janvier 2026

- Backoff exponentiel pendant les challenges Cloudflare persistants.
- Pause manuelle explicite (Entrée) lors d’une vérification Cloudflare.
- Validation plus robuste de `deep_scan_interval`.
- Test unitaire du helper de backoff.
- Correctif de test (`log_file` dans la portée adéquate).
- Ajout d’un audit Cloudflare et d’un playbook opérateur.

### 0.2.17 — 20 janvier 2026

- Pause silencieuse 45s après le bouton Home User pour réduire les interactions
  pendant la vérification Cloudflare.
- Arrêt propre si la vérification Cloudflare n'est pas résolue avant le login.
- Prise en compte du paramètre `debug` dans `config.yaml`.
- Durcissement des paramètres Cloudflare (validation quiet/deep scan).

### 0.2.16 — 20 janvier 2026

- Atténuation des interactions Selenium pendant la vérification Cloudflare
  (fenêtre "quiet" par défaut ~30s) pour limiter le polling/scan DOM.

### 0.2.15 — 19 janvier 2026

- Validation renforcée de `dexcom_url` : parsing d'URL + allowlist de hosts
  Dexcom (HTTPS uniquement, sous-domaines autorisés).

### 0.2.14 — 19 janvier 2026

- Ajout d'une attente "vérification humaine" Cloudflare (pause + reprise
  automatique) basée sur une ancre UI.

### 0.2.13 — 19 janvier 2026

- Mise à jour des instructions Copilot (debug Selenium, commandes PowerShell).
- Synchronisation de version.

### 0.2.11 — 22 décembre 2025

- Passage à Inno Setup pour la distribution (installateur `.exe`).
- Correction du timeout pour les rapports volumineux (Superposition).
- Exclusion des fichiers `.crdownload` dans la détection des téléchargements.
- Mise à jour de la documentation et des entêtes.

### 0.2.7 — 27 octobre 2025

- Ajout de `check_for_502_errors` pour détecter les erreurs 502 dans les logs du
  navigateur.
- Ajout de `wait_for_page_load_with_retry` pour gérer les erreurs temporaires
  avec retry automatique.
- Note : ces helpers ne sont pas présents dans le code actuel (jusqu'à la
  version 0.2.15).

### 0.2.6 — 21 octobre 2025

- Amélioration majeure de l'aide CLI (`--help`) : description détaillée,
  exemples pratiques, groupes d'arguments
- Ajout de `--list-rapports` : affiche la liste des rapports disponibles avec
  descriptions détaillées
- Ajout de `--dry-run` : simule l'exécution et affiche la configuration sans
  effectuer de téléchargement
- Validation robuste des dates avec messages d'erreur explicites (format,
  cohérence)
- Les options `--help`, `--version`, et `--list-rapports` fonctionnent désormais
  avant la validation de `config.yaml` et `.env`
- Expérience utilisateur améliorée avec messages colorés et informatifs
- Synchronisation des versions dans tous les modules

### 0.2.5 — 16 octobre 2025

- Amélioration de la fonction `cleanup_logs` : suppression automatique des
  captures d'écran (`.png`) en plus des fichiers `.log`
- Les fichiers `.png` plus anciens que la période de rétention
  (`log_retention_days`) sont maintenant nettoyés automatiquement
- Ajout de tests unitaires pour valider la suppression des captures d'écran
  anciennes
- Synchronisation des versions dans tous les modules

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
[Releases](https://github.com/thebe01/GlycoReport-Downloader/releases) du projet
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
  script uniquement)
- Google Chrome installé
- Droits administrateur pour définir la variable d’environnement système (si
  nécessaire pour le chiffrement)

### Procédure

1. **Téléchargez l'installateur** (`GlycoReport-Downloader_Setup_x.x.x.exe`)
   depuis la page Releases du projet.
1. **Exécutez l'installateur**.

- L'installation se fait par défaut dans `C:\ipt\GlycoReport-Downloader` (ou sur
  le disque système correspondant).
- Aucune élévation de privilèges n'est requise (sauf si vous choisissez un
  dossier protégé).

1. **Lancez l'application** via le script `Launch-Dexcom-And-Run.ps1` (proposé
   en fin d'installation), ou via le raccourci créé dans le dossier
   d'installation.

- Requiert `chrome_user_data_dir` dans `config.yaml`.
- Requiert `GlycoReport-Downloader.exe` à la racine du dossier courant ou dans
  `dist/`.

1. **Lors du premier lancement**, si les fichiers `config.yaml` ou `.env` sont
   absents, l'application vous informera et lancera la configuration initiale.

### Migration depuis une version antérieure

Si vous mettez à jour depuis une version < 0.2.3, un outil de migration est
disponible pour nettoyer automatiquement votre configuration. L'installateur
inclut cet outil.

**Note :** l'outil de migration (`migrate.py` / `migrate.exe`) est versionné
indépendamment (v1.0.1) et ne suit pas la version principale de l'application.

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
- Compile l'installateur Inno Setup (`.iss`)
- Génère l'installateur final dans le dossier `dist_setup` (ex:
  `GlycoReport-Downloader_Setup_x.x.x.exe`)
- Copie `config_example.yaml`, `README.md`, `LICENSE.txt`, `MIGRATION.md`,
  `.env.example` et `Launch-Dexcom-And-Run.ps1` dans `dist/`.

**Prérequis pour la compilation :**

- [Inno Setup 6](https://jrsoftware.org/isinfo.php) doit être installé.

**Note** : Depuis la version 0.2.3, ChromeDriverManager télécharge
automatiquement la version appropriée de ChromeDriver, il n'est donc plus
nécessaire d'inclure le dossier `chromedriver-win64` dans la distribution.

### Utilisation

Ouvre un terminal PowerShell à la racine du projet et exécute :

```powershell
.\DIST-GlycoReport-Downloader.ps1
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
debug: false
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
1. Collez cette commande dans la fenêtre PowerShell qui s’ouvre, puis tapez
   `Exit`.
1. Relancez le script pour poursuivre la configuration.
1. Lors de la création du `.env`, les informations saisies seront chiffrées
   automatiquement.

---

## Paramètres de la ligne de commande

- `-h`, `--help` : Afficher l'aide et quitter.
- `-v`, `--version` : Afficher la version et quitter.
- `-d`, `--debug` : Activer le mode debug (logs détaillés, captures d'écran).
- `--dry-run` : Simuler l'exécution sans télécharger (affiche la configuration).
- `--days {7,14,30,90}` : Nombre de jours à inclure dans le rapport (7, 14, 30
  ou 90).
- `--date_debut AAAA-MM-JJ` : Date de début au format AAAA-MM-JJ (ex:
  2025-01-01).
- `--date_fin AAAA-MM-JJ` : Date de fin au format AAAA-MM-JJ (ex: 2025-01-31).
- `--rapports RAPPORT [RAPPORT ...]` : Liste des rapports à traiter (ex :
  `"Aperçu" "AGP" "Statistiques"`).
- `--list-rapports` : Afficher la liste des rapports disponibles avec
  descriptions et quitter.

**Remarque** : L'aide s'affiche toujours proprement, même si les fichiers de
configuration sont absents ou incomplets. Les options `--help`, `--version` et
`--list-rapports` fonctionnent avant la validation de la configuration.

---

## Exemple d’aide

```text
usage: GlycoReport-Downloader [-h] [--version] [--debug] [--dry-run]
                               [--days N] [--date_debut YYYY-MM-DD]
                               [--date_fin YYYY-MM-DD]
                               [--rapports REPORT [REPORT ...]]
                               [--list-rapports]

GlycoReport Downloader v0.2.6 - Automated Dexcom Clarity report download

This script automates the download of glycemic reports from your
Dexcom Clarity account. It supports multiple report types, customizable periods,
and exports data in PDF or CSV format.

For more information: [https://github.com/thebe01/GlycoReport-Downloader](https://github.com/thebe01/GlycoReport-Downloader)

general options:
  -h, --help            Show this help message and exit
  --version, -v         Display version and exit
  --debug, -d           Enable debug mode (detailed logs, screenshots)
  --dry-run             Simulate execution without downloading (displays configuration)

report period:
  Define the download period (default: last 14 days)

  --days N              Number of days to include (7, 14, 30 or 90)
  --date_debut YYYY-MM-DD
                        Start date in YYYY-MM-DD format (e.g., 2025-01-01)
  --date_fin YYYY-MM-DD
                        End date in YYYY-MM-DD format (e.g., 2025-01-31)

report selection:
  Choose reports to download (default: all configured reports)

  --rapports REPORT [REPORT ...]
                        List of reports (e.g., "Aperçu" "AGP" "Statistiques")
  --list-rapports       Display list of available reports and exit

Usage examples:
  Download all reports for the last 14 days (default):
    python GlycoDownload.py

  Download only the Overview report for the last 7 days:
    python GlycoDownload.py --days 7 --rapports "Aperçu"

  Download multiple reports for a specific period:
    python GlycoDownload.py --date_debut 2025-01-01 --date_fin 2025-01-31 --rapports "Aperçu" "AGP"

  Debug mode with all reports for the last 30 days:
    python GlycoDownload.py --debug --days 30

  Test configuration without downloading:
    python GlycoDownload.py --dry-run

Available reports: Aperçu, Modèles, Superposition, Quotidien, Comparer, Statistiques, AGP, Export
(Use --list-rapports for more details)

Configuration:
  - File: config.yaml (automatically created on first launch)
  - Credentials: .env (encrypted, requires ENV_DEXCOM_KEY variable)
  - Logs: defined in config.yaml (log_retention_days)

For questions or bug reports: [https://github.com/thebe01/GlycoReport-Downloader/issues](https://github.com/thebe01/GlycoReport-Downloader/issues)
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

**Note tests fonctionnels :** l'application n'exécute pas le téléchargement tant
que l'usager n'est pas connecté. Pour les tests end-to-end, lancez d'abord
`Launch-Dexcom-And-Run.ps1`, terminez la connexion, puis laissez le script
relancer l'app (mode reprise).

Voir aussi: [tests/TEST_STRATEGY.md](tests/TEST_STRATEGY.md).

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

## GlycoReport Downloader (English)

Note: The French version is the source of truth. The English version is a strict
translation of the French version.

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

### Version: 0.3.13 — February 12, 2026

**Fixes:**

- Comparer: download limited to Trends (Dexcom bug on Overlay and Daily), with a
  log warning.

### Version: 0.3.12 — February 12, 2026

**Fixes:**

- Directly open Comparer sub-reports via /compare/overlay and /compare/daily.

### Version: 0.3.11 — February 12, 2026

**Fixes:**

- Navigate via base URL
  [https://clarity.dexcom.eu/i](https://clarity.dexcom.eu/i) for Comparer.

### Version: 0.3.10 — February 12, 2026

**Fixes:**

- Retry Comparer clicks (stale element) and navigate overview -> reports.

### Version: 0.3.9 — February 12, 2026

**Fixes:**

- Navigate to overview with dates, then back to /reports to avoid Comparer
  freeze.

### Version: 0.3.8 — February 12, 2026

**Fixes:**

- Close/reopen Comparer modal between each sub-report to force PDF regeneration.

### Version: 0.3.7 — February 12, 2026

**Fixes:**

- Wait for graphic content and additional delay for PDF generation (Comparer
  sub-reports).

### Version: 0.3.6 — February 12, 2026

**Fixes:**

- Further stabilized Comparer sub-reports.

### Version: 0.3.5 — February 12, 2026

**Fixes:**

- Stabilized Comparer sub-reports.
- Forced Chrome download directory (download_dir).

### Version: 0.3.4 — February 12, 2026

**Fixes:**

- Fixed Comparer sub-report downloads.

### Version: 0.3.3 — February 2, 2026

**Fixes:**

- Normalized expected download extensions.

### Version: 0.3.2 — February 2, 2026

**Fixes:**

- Filtered downloaded files by extension.

### Version: 0.3.1 — February 2, 2026

**Fixes:**

- Hardened `pause_on_error` in non-interactive contexts.
- Improved `Launch-Dexcom-And-Run.ps1` (paths, Chrome/Selenium attach, exe
  lookup).

### Version: 0.3.0 — January 29, 2026

**Assisted startup:**

- Added `--start-at-date-selection` entry point (resume after login).
- Added `Launch-Dexcom-And-Run.ps1` to open Chrome with the profile and launch
  the app.

### Version: 0.2.18 — January 20, 2026

**Cloudflare robustness:**

- Exponential backoff during persistent challenges.
- Explicit manual pause (Enter) on Cloudflare verification.
- More robust `deep_scan_interval` validation.

**Quality / tests:**

- Unit test for the backoff helper.
- Test fix (`log_file` scope).

**Documentation:**

- Added a Cloudflare audit and operator playbook.

### Version: 0.2.16 — January 20, 2026

**Selenium Robustness Improvements:**

- During Cloudflare “human verification”, the script temporarily reduces
  Selenium interactions (a default ~30s “quiet” window) to limit polling/DOM
  scanning.

**Documentation & Dev Improvements:**

- Version bump (release 0.2.16).

### Version: 0.2.15 — January 19, 2026

**Security & Validation Improvements:**

- Stronger `dexcom_url` validation: URL parsing + Dexcom host allowlist (HTTPS
  only, subdomains allowed).

### Version: 0.2.14 — January 19, 2026

- Added a Cloudflare “human verification” wait (pause + auto-resume) based on a
  stable UI anchor.

### Version: 0.2.13 — January 19, 2026

- Updated Copilot instructions (Selenium debugging, PowerShell commands).
- Version synchronization.

### Version: 0.2.11 — December 22, 2025

**New Windows Installer:**

- Distribution via Inno Setup installer (`.exe`) for simplified installation.
- Default installation in `{sd}\ipt\GlycoReport-Downloader` (system drive, user
  folder).
- Automatic creation of shortcuts and uninstallation management.
- No longer requires administrator rights for installation.

**Technical Improvements:**

- Increased timeout for download window closure (60s) to handle large reports
  (e.g., Overlay).
- Exclusion of temporary `.crdownload` files when detecting the last downloaded
  file.
- Header updates and version synchronization (ES-18).

### Version: 0.2.6 — October 21, 2025

**CLI Help and Options Improvements:**

- Help (`--help`) completely redesigned with detailed description, usage
  examples, and organized argument groups
- New `--list-rapports` option to display the complete list of available reports
  with descriptions
- New `--dry-run` option to simulate execution and display configuration without
  downloading
- Enhanced date validation with explicit and colored error messages
- Help options now work **before** configuration file validation

**Log Cleanup Improvements:**

- Screenshot files (`.png` files) generated in debug mode are now automatically
  deleted during log cleanup according to the configured retention period
- Improved disk space management

---

## Version History (English)

### 0.3.13 — February 12, 2026

- Comparer: download limited to Trends (Dexcom bug on Overlay and Daily), with a
  log warning.

### 0.3.12 — February 12, 2026

- Directly open Comparer sub-reports via /compare/overlay and /compare/daily.

### 0.3.11 — February 12, 2026

- Navigate via base URL
  [https://clarity.dexcom.eu/i](https://clarity.dexcom.eu/i) for Comparer.

### 0.3.10 — February 12, 2026

- Retry Comparer clicks (stale element) and navigate overview -> reports.

### 0.3.9 — February 12, 2026

- Navigate to overview with dates, then back to /reports to avoid Comparer
  freeze.

### 0.3.8 — February 12, 2026

- Close/reopen Comparer modal between each sub-report to force PDF regeneration.

### 0.3.7 — February 12, 2026

- Wait for graphic content and additional delay for PDF generation (Comparer
  sub-reports).

### 0.3.6 — February 12, 2026

- Further stabilized Comparer sub-reports.

### 0.3.5 — February 12, 2026

- Stabilized Comparer sub-reports.
- Forced Chrome download directory (download_dir).

### 0.3.4 — February 12, 2026

- Fixed Comparer sub-report downloads.

### 0.3.3 — February 2, 2026

- Normalized expected download extensions.

### 0.3.2 — February 2, 2026

- Filtered downloaded files by extension.

### 0.3.1 — February 2, 2026

- Hardened `pause_on_error` in non-interactive contexts.
- Improved `Launch-Dexcom-And-Run.ps1` (paths, Chrome/Selenium attach, exe
  lookup).

### 0.3.0 — January 29, 2026

- Added `--start-at-date-selection` entry point (resume after login).
- Added `Launch-Dexcom-And-Run.ps1` to open Chrome with the profile and launch
  the app.

### 0.2.18 — January 20, 2026

- Exponential backoff during persistent Cloudflare challenges.
- Explicit manual pause (Enter) on Cloudflare verification.
- More robust `deep_scan_interval` validation.
- Backoff helper unit test.
- Test fix (`log_file` scope).
- Added a Cloudflare audit and operator playbook.

### 0.2.17 — January 20, 2026

- 45s silent pause after the Home User button to reduce interactions during
  Cloudflare verification.
- Clean stop if Cloudflare verification is not resolved before login.
- `debug` is now honored from `config.yaml`.
- Stronger Cloudflare parameter validation (quiet/deep scan).

### 0.2.16 — January 20, 2026

- During Cloudflare “human verification”, the script temporarily reduces
  Selenium interactions (a default ~30s “quiet” window) to limit polling/DOM
  scanning.

### 0.2.15 — January 19, 2026

- Stronger `dexcom_url` validation: URL parsing + Dexcom host allowlist (HTTPS
  only, subdomains allowed).

### 0.2.14 — January 19, 2026

- Added a Cloudflare “human verification” wait (pause + auto-resume) based on a
  stable UI anchor.

### 0.2.13 — January 19, 2026

- Updated Copilot instructions (Selenium debugging, PowerShell commands).
- Version synchronization.

### 0.2.11 — December 22, 2025

- Switched to Inno Setup for distribution (`.exe` installer).
- Fixed timeout for large reports (Overlay).
- Excluded `.crdownload` files from download detection.
- Updated documentation and headers.

### 0.2.7 — October 27, 2025

- Added `check_for_502_errors` to detect 502 errors in browser logs.
- Added `wait_for_page_load_with_retry` to handle temporary errors with
  automatic retry.
- Note: these helpers are not present in the current codebase (up to version
  0.2.15).

### 0.2.6 — October 21, 2025

- Major CLI help improvement (`--help`): detailed description, practical
  examples, argument groups
- Added `--list-rapports`: displays list of available reports with detailed
  descriptions
- Added `--dry-run`: simulates execution and displays configuration without
  downloading
- Robust date validation with explicit error messages (format, consistency)
- Options `--help`, `--version`, and `--list-rapports` now work before
  validating `config.yaml` and `.env`
- Improved user experience with colored and informative messages
- Version synchronization across all modules

### 0.2.5 — October 16, 2025

- Enhanced `cleanup_logs` function: automatic deletion of screenshots (`.png`)
  in addition to `.log` files
- `.png` files older than the retention period (`log_retention_days`) are now
  automatically cleaned up
- Added unit tests to validate deletion of old screenshots
- Version synchronization across all modules

### 0.2.4 — October 16, 2025

- Removed obsolete `chromedriver_path` parameter (unused since v0.2.3).
- Code cleanup: `CHROMEDRIVER_PATH` removed from configuration.
- Simplification: the `chromedriver-win64/` directory is no longer necessary.
- ChromeDriverManager automatically manages the download of the appropriate
  version.
- Reduced distribution package size (~10 MB smaller).
- No functional changes for the user.

### 0.2.3 — October 14, 2025

- Uses ChromeDriverManager to always load the current version.
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
[Releases](https://github.com/thebe01/GlycoReport-Downloader/releases) section
of the GitHub project. Download the `.zip` for Windows, then extract it to get
all necessary files (see instructions below).

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
- [Python 3.10+](https://www.python.org/downloads/) (for script mode only)
- Google Chrome installed
- Administrator rights to set the system environment variable (if necessary for
  encryption)

### Procedure

1. **Download the installer** (`GlycoReport-Downloader_Setup_x.x.x.exe`) from
   the project Releases page.
1. **Run the installer**.

- Installation defaults to `C:\ipt\GlycoReport-Downloader` (or corresponding
  system drive).
- No privilege elevation is required (unless you choose a protected folder).

1. **Launch the application** via `Launch-Dexcom-And-Run.ps1` (offered at the
   end of the installer), or via the created shortcut in the installation
   folder.

- Requires `chrome_user_data_dir` in `config.yaml`.
- Requires `GlycoReport-Downloader.exe` at the current folder root or in
  `dist/`.

1. **On first launch**, if `config.yaml` or `.env` files are missing, the
   application will inform you and start the initial configuration.

### Migrating from an Earlier Version

If you are upgrading from a version < 0.2.3, a migration tool is available to
automatically clean up your configuration. The installer includes this tool.

**Note:** the migration tool (`migrate.py` / `migrate.exe`) is versioned
independently (v1.0.1) and does not follow the main application version.

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
- Compiles the Inno Setup installer (`.iss`)
- Generates the final installer in the `dist_setup` folder (e.g.,
  `GlycoReport-Downloader_Setup_x.x.x.exe`)
- Copies `config_example.yaml`, `README.md`, `LICENSE.txt`, `MIGRATION.md`,
  `.env.example`, and `Launch-Dexcom-And-Run.ps1` into `dist/`.

**Prerequisites for compilation:**

- [Inno Setup 6](https://jrsoftware.org/isinfo.php) must be installed.

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
1. Paste this command into the PowerShell window that opens, then type `Exit`.
1. Rerun the script to continue the configuration.
1. When creating the `.env`, the entered information will be automatically
   encrypted.

---

## Command Line Parameters (English)

- `-h`, `--help`: Display help and exit.
- `-v`, `--version`: Display version and exit.
- `-d`, `--debug`: Enable debug mode (detailed logs, screenshots).
- `--dry-run`: Simulate execution without downloading (displays configuration).
- `--days {7,14,30,90}`: Number of days to include in the report (7, 14, 30,
  90).
- `--date_debut DATE_DEBUT`: Start date (YYYY-MM-DD).
- `--date_fin DATE_FIN`: End date (YYYY-MM-DD).
- `--rapports RAPPORTS [RAPPORTS ...]`: List of reports to process (e.g.,
  `"Aperçu" "AGP" "Statistiques"`).
- `--list-rapports`: Display the list of available reports with descriptions and
  exit.

**Note**: Help is always displayed neatly, even if configuration files are
missing or incomplete. The `--help`, `--version`, and `--list-rapports` options
work before configuration validation.

---

## Example Help Output (English)

```text
usage: GlycoReport-Downloader [-h] [--version] [--debug] [--dry-run]
                               [--days N] [--date_debut YYYY-MM-DD]
                               [--date_fin YYYY-MM-DD]
                               [--rapports REPORT [REPORT ...]]
                               [--list-rapports]

GlycoReport Downloader v0.2.6 - Automated Dexcom Clarity report download

This script automates the download of glycemic reports from your
Dexcom Clarity account. It supports multiple report types, customizable periods,
and exports data in PDF or CSV format.

For more information: https://github.com/thebe01/GlycoReport-Downloader

general options:
  -h, --help            Show this help message and exit
  --version, -v         Display version and exit
  --debug, -d           Enable debug mode (detailed logs, screenshots)
  --dry-run             Simulate execution without downloading (displays configuration)

report period:
  Define the download period (default: last 14 days)

  --days N              Number of days to include (7, 14, 30 or 90)
  --date_debut YYYY-MM-DD
                        Start date in YYYY-MM-DD format (e.g., 2025-01-01)
  --date_fin YYYY-MM-DD
                        End date in YYYY-MM-DD format (e.g., 2025-01-31)

report selection:
  Choose reports to download (default: all configured reports)

  --rapports REPORT [REPORT ...]
                        List of reports (e.g., "Aperçu" "AGP" "Statistiques")
  --list-rapports       Display list of available reports and exit

Usage examples:
  Download all reports for the last 14 days (default):
    python GlycoDownload.py

  Download only the Overview report for the last 7 days:
    python GlycoDownload.py --days 7 --rapports "Aperçu"

  Download multiple reports for a specific period:
    python GlycoDownload.py --date_debut 2025-01-01 --date_fin 2025-01-31 --rapports "Aperçu" "AGP"

  Debug mode with all reports for the last 30 days:
    python GlycoDownload.py --debug --days 30

  Test configuration without downloading:
    python GlycoDownload.py --dry-run

Available reports: Aperçu, Modèles, Superposition, Quotidien, Comparer, Statistiques, AGP, Export
(Use --list-rapports for more details)

Configuration:
  - File: config.yaml (automatically created on first launch)
  - Credentials: .env (encrypted, requires ENV_DEXCOM_KEY variable)
  - Logs: defined in config.yaml (log_retention_days)

For questions or bug reports: https://github.com/thebe01/GlycoReport-Downloader/issues
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

- `-v` shows detailed output for each test (verbose mode).
- `--log-cli-level=INFO` shows log messages produced by the tested functions.
- This command helps verify the robustness and portability of all the project's
  utility functions.

**Functional test note:** the app does not proceed until the user is logged in.
For end-to-end tests, run `Launch-Dexcom-And-Run.ps1` first, complete the login,
then let the script relaunch the app (resume mode).

See also: [tests/TEST_STRATEGY.md](tests/TEST_STRATEGY.md).

Make sure you have installed pytest:

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
