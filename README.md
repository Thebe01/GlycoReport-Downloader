# Dexcom Clarity Reports Downloader

## Version : 0.2.0 — 28 août 2025

### Nouveautés

- Le fichier `.env` est désormais chiffré à l’écriture et déchiffré à la volée lors de la lecture.
- La clé d’encryption est stockée dans une variable d’environnement système `ENV_DEXCOM_KEY`.
- Suppression de la saisie interactive des identifiants Dexcom : le script s’arrête si les identifiants sont absents ou incomplets.
- Sécurisation de la gestion des logs et des fichiers temporaires.

### Architecture

- `config.py` : centralise la configuration et les credentials
- `utils.py` : fonctions utilitaires
- `ClarityDownload.py` : script principal, utilise uniquement les variables/fonctions exposées par les modules

## Description

Dexcom Clarity Reports Downloader est un outil automatisé permettant de télécharger, organiser et archiver les rapports Dexcom Clarity pour un suivi glycémique efficace.
Le projet est conçu pour être portable, configurable et robuste, avec une gestion avancée des logs, des erreurs et de la sécurité.

---

## Release disponible

Une version exécutable prête à l’emploi est disponible dans la section [Releases](https://github.com/<ton-utilisateur>/<ton-repo>/releases) du projet GitHub.
Téléchargez le fichier `.exe` pour Windows ainsi que les fichiers nécessaires (voir instructions ci-dessous).

---

## Historique des versions

### 0.2.0 — 28 août 2025

- `.env` chiffré à l’écriture et déchiffré à la volée.
- Clé d’encryption stockée dans une variable d’environnement système.
- Suppression de la saisie interactive des identifiants Dexcom.
- Sécurisation de la gestion des logs et des fichiers temporaires.

### 0.1.10 — 28 août 2025

- Le ménage des logs s'effectue désormais uniquement après l'activation du logging.
- Chaque suppression de log est loggée.

### 0.1.9 — 28 août 2025

- Vérification interactive de la clé `chromedriver_log` lors de la création de `config.yaml`.
- Empêche la saisie d'un dossier pour le log, exige un chemin de fichier.
- Correction de la robustesse de la configuration initiale.

### 0.1.8 — 27 août 2025

- Configuration interactive avancée pour `config.yaml` et `.env` lors du premier lancement.
- Copie minimale du profil Chrome lors de la configuration initiale.
- Ajout du paramètre `log_retention_days` (0 = conservation illimitée).
- Nettoyage automatique des logs selon la durée de rétention.
- Messages utilisateurs colorés et validation renforcée des paramètres.

### 0.1.7 — 25 août 2025

- Création automatique de `config.yaml` à partir de `config_example.yaml` si absent
- Gestion interactive des credentials si `.env` absent (demande à l'utilisateur, non conservé)
- Précision sur la présence de `chromedriver-win64` fourni

### 0.1.6 — 22 août 2025

- Synchronisation des versions dans tous les modules (bloc commentaires de version à jour)
- Ajout du module `version.py` (source unique de vérité pour la version)
- Log de la version exécutée au démarrage
- Correction des chemins YAML (utilisation systématique de `/`)
- Compatibilité interface Dexcom août 2025 (gestion de la page "Pas maintenant")
- Robustesse saisie identifiant et gestion avancée des erreurs
- Captures d’écran uniquement en mode debug
- Logs détaillés pour chaque étape critique
- Sélecteurs robustes pour les champs de connexion

---

## Fonctionnalités principales

- Téléchargement automatisé de tous les rapports Dexcom Clarity sélectionnés
- Configuration centralisée via un fichier `config.yaml` (non versionné)
- Exemple de configuration fourni dans `config_example.yaml`
- Prise en charge des chemins portables (`~` et `/`), normalisés automatiquement
- Prise en charge de l’authentification par courriel/nom d’usager **ou** par numéro de téléphone (avec code pays et numéro, via variables d’environnement)
- Gestion avancée des logs (application, navigateur, logs JS)
- Capture d’écran automatique avec délai en cas d’erreur critique (pour diagnostic, uniquement en mode debug)
- Sélection de la période, des rapports et du mode debug via la ligne de commande
- Robustesse accrue sur la gestion des erreurs, des téléchargements et de la configuration
- Compatible Windows (et adaptable Linux/Mac)
- Tests unitaires couvrant toutes les fonctions utilitaires

---

## Installation et utilisation

1. **Téléchargez l’archive ZIP du release** depuis la page Releases du projet.
2. **Décompressez tout le contenu du ZIP** dans un dossier de votre choix (ex : `C:\DexcomClarityDownloader`).
   - Le dossier doit contenir :
     - `DexcomClarityDownloader.exe`
     - `config_example.yaml`
     - `.env.example`
     - le dossier `chromedriver-win64`
3. **Lancez `DexcomClarityDownloader.exe`** en double-cliquant ou via le terminal.
4. **Lors du premier lancement**, si les fichiers `config.yaml` ou `.env` sont absents, l’application vous informera et lancera la configuration initiale.
5. **Les fichiers de configuration seront créés dans le même dossier que l’exécutable.**

---

## Gestion des dates par défaut

- **Par défaut**, si aucune date n'est fournie en argument ou dans le fichier `config.yaml`, la période utilisée sera les **14 derniers jours jusqu'à hier**.
- Vous pouvez surcharger ce comportement :
  - en passant `--days 7`, `--days 14`, `--days 30` ou `--days 90` en argument,
  - ou en définissant explicitement `date_debut` et `date_fin` dans `config.yaml`,
  - ou encore en passant `--date_debut` et `--date_fin` en argument.

Exemple :

- Si nous sommes le 2025-08-18 et que vous ne passez aucun paramètre, la période sera du 2025-08-04 au 2025-08-17.

---

## Normalisation systématique des chemins

Tous les chemins utilisés dans le projet (dossiers de téléchargement, profils, logs, etc.) sont **normalisés automatiquement** :

- Les chemins commençant par `~` sont convertis en chemin absolu utilisateur.
- Les `/` sont utilisés partout pour garantir la portabilité (Windows, Mac, Linux).
- La normalisation est effectuée dans le code via `os.path.expanduser` et `os.path.abspath` (fonction centralisée dans `utils.py`).

**Exemple dans `config.yaml` :**

```yaml
chrome_user_data_dir: C:\Users\????????\Downloads\DexcomClarityDownloader\Profile
chromedriver_log: C:\Users\????????\Downloads\DexcomClarityDownloader\clarity_chromedriver.log
chromedriver_path: ./chromedriver-win64/chromedriver.exe
dexcom_url: "https://clarity.dexcom.eu"
download_dir: C:\Users\????????\Downloads\DexcomClarityDownloader
log_retention_days: 15
output_dir: C:\Users\????????\Downloads\DexcomClarityDownloader
rapports: ["Aperçu"]
```

---

## Sécurité et gestion des secrets

- Le fichier `.env` est **chiffré** à l’aide d’une clé Fernet générée automatiquement lors de la première configuration.
- La clé d’encryption est stockée dans une variable d’environnement système `ENV_DEXCOM_KEY` (créée via PowerShell).
- Les identifiants Dexcom ne sont **jamais affichés ni stockés en clair**.
- Si les identifiants sont absents ou incomplets dans le `.env`, le script s’arrête avec un message d’erreur explicite.
- **Aucune saisie interactive** des identifiants n’est proposée pour des raisons de sécurité.

## Procédure de première utilisation

1. Lancez le script. Une clé d’encryption sera générée et une commande PowerShell s’affichera.
2. Collez cette commande dans la fenêtre PowerShell qui s’ouvre, puis tapez `Exit`.
3. Relancez le script pour poursuivre la configuration.
4. Lors de la création du `.env`, les informations saisies seront chiffrées automatiquement.

## Tests unitaires

Pour exécuter tous les tests unitaires sur les fonctions utilitaires du projet, utilisez la commande suivante :

```sh
pytest -v --log-cli-level=INFO tests/test_utils.py
```

- `-v` affiche le détail de chaque test exécuté (mode verbose).
- `--log-cli-level=INFO` affiche les messages de log générés par les fonctions testées.
- Cette commande permet de vérifier la robustesse et la portabilité de toutes les fonctions utilitaires du projet.

Assurez-vous d’avoir installé pytest :

```sh
pip install pytest
```

---

---

## Création de l'exécutable Windows

Pour générer l'exécutable à partir du code source, utilisez la commande suivante :

```sh
pyinstaller --onefile --hidden-import=yaml --name "DexcomClarityDownloader" [ClarityDownload.py](http://_vscodecontentref_/1)
```

**(http://_vscodecontentref_/2) pour que la procédure soit complète et fidèle à la réalité de ton projet.**

## Notes

- Les rapports sont organisés par année dans le dossier de destination.
- En cas de perte de connexion, le script gère les erreurs et reprend là où il s'est arrêté.
- Pour toute question, suggestion ou rapport de bug, ouvrez une issue sur GitHub.
- Merci de ne pas redistribuer ce code sans autorisation. Ce projet est fourni tel quel, sans garantie.

---

## Auteur

Pierre Théberge

---

## Licence

Projet privé, tous droits réservés.
