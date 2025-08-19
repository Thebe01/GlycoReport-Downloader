# Dexcom Clarity Reports Downloader

## Description

Dexcom Clarity Reports Downloader est un outil automatisé permettant de télécharger, organiser et archiver les rapports Dexcom Clarity pour un suivi glycémique efficace.
Le projet est conçu pour être portable, configurable et robuste, avec une gestion avancée des logs, des erreurs et de la sécurité.

---

## Nouveautés et changements récents (18 août 2025)

- **Compatibilité interface Dexcom août 2025** : adaptation à la nouvelle page intermédiaire ("Pas maintenant") après connexion.
- **Robustesse saisie identifiant** : sélection fiable du champ `usernameLogin`, vérification visibilité/interactivité, gestion des overlays et délais.
- **Captures d’écran** : désormais uniquement en mode debug pour éviter l’encombrement.
- **Logs détaillés** : diagnostics enrichis pour chaque étape critique (présence champ, clics, erreurs Selenium, etc.).
- **Gestion du bouton "Pas maintenant"** : détection et clic automatique, indépendant de la langue.
- **Sélecteurs robustes** : prise en charge des changements d’ID ou de structure HTML pour les champs de connexion.
- **Gestion avancée des erreurs** : captures et logs lors de toute anomalie, arrêt propre du script.

---

## Fonctionnalités principales

- Téléchargement automatisé de tous les rapports Dexcom Clarity sélectionnés
- Configuration centralisée via un fichier `config.yaml` (non versionné)
- Création interactive de `config.yaml` si absent (basé sur `config_example.yaml`)
- Prise en charge des chemins portables (`~` et `/`), normalisés automatiquement
- Prise en charge de l’authentification par courriel/nom d’usager **ou** par numéro de téléphone (avec code pays et numéro, via variables d’environnement)
- Gestion avancée des logs (application, navigateur, logs JS)
- Capture d’écran automatique avec délai en cas d’erreur critique (pour diagnostic, uniquement en mode debug)
- Sélection de la période, des rapports et du mode debug via la ligne de commande
- Robustesse accrue sur la gestion des erreurs, des téléchargements et de la configuration
- Compatible Windows (et adaptable Linux/Mac)
- Tests unitaires couvrant toutes les fonctions utilitaires

---

## Installation

1. **Cloner le dépôt**

   ```sh
   git clone <url_du_depot>
   cd Dexcom-Clarity-Reports
   ```

2. **Installer les dépendances**

   ```sh
   pip install -r requirements.txt
   ```

3. **Configurer ChromeDriver**
   - Téléchargez [ChromeDriver](https://chromedriver.chromium.org/downloads) correspondant à votre version de Chrome.
   - Placez `chromedriver.exe` dans le dossier du projet ou dans un dossier inclus dans votre `PATH`.

4. **Configurer le fichier `.env`**
   - Renommez `.env.example` en `.env`.
   - Remplissez vos identifiants Dexcom Clarity :

     ```env
     DEXCOM_USERNAME=mon_email@example.com
     DEXCOM_PASSWORD=mon_mot_de_passe
     # Pour l'authentification par téléphone, ajoutez aussi :
     DEXCOM_COUNTRY_CODE=+1
     DEXCOM_PHONE_NUMBER=5141234567
     ```

   - Si vous utilisez l’authentification par téléphone, les variables `DEXCOM_COUNTRY_CODE` et `DEXCOM_PHONE_NUMBER` sont obligatoires.

---

## Utilisation

Pour exécuter le script avec les paramètres par défaut :

```sh
python ClarityDownload.py
```

### Options de ligne de commande

- `--days` : Nombre de jours à télécharger (ex: `--days 7`)
- `--date_debut` et `--date_fin` : Définir une période précise
- `--rapports` : Choisir les rapports à générer (ex: `--rapports Aperçu,Statistiques`)
- `--debug` : Activer le mode debug pour des logs détaillés et les captures d’écran

Exemple pour télécharger les rapports des 7 derniers jours en mode debug :

```sh
python ClarityDownload.py --days 7 --debug
```

- Si vous utilisez un numéro de téléphone pour vous connecter, assurez-vous que les variables `DEXCOM_COUNTRY_CODE` et `DEXCOM_PHONE_NUMBER` sont bien renseignées dans votre `.env`.

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
download_dir: "~/Downloads/Dexcom_download"
output_dir: "C:/Users/thebe/OneDrive/Documents/Santé/Suivie glycémie et pression"
chromedriver_log: "~/Downloads/Dexcom_download/clarity_chromedriver.log"
chrome_user_data_dir: "~/Chrome_Clarity_Profile"
```

---

## Sécurité et robustesse

- Chargement sécurisé de la configuration (`yaml.safe_load`)
- Validation stricte des types et de la présence des paramètres essentiels
- Validation explicite de la présence des variables d’environnement nécessaires selon le mode d’authentification choisi (courriel/nom d’usager ou téléphone)
- Vérification des droits d’accès au fichier de configuration
- Jamais de log ou d’exposition de secrets
- Jamais d’utilisation de `eval` ou `exec` sur des données de config
- Gestion avancée des erreurs et logs détaillés (console, fichier, logs JS navigateur)
- Capture d’écran automatique avec délai en cas d’erreur critique (fonction centralisée dans `utils.py`, uniquement en mode debug)
- Log du contenu du dossier de téléchargement après chaque tentative

---

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

## Notes

- Les rapports sont organisés par année dans le dossier de destination.
- En cas de perte de connexion, le script gère les erreurs et reprend là où il s'est arrêté.
- Pour toute question, suggestion ou rapport de bug, ouvrez une issue sur GitHub.
- Merci de ne pas redistribuer ce code sans autorisation. Ce projet est fourni tel quel, sans garantie.

---

## Auteur

Pierre Théberge  
Innovations Performances Technologies inc

---

## Licence

Projet privé, tous droits réservés.
