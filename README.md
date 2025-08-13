# Dexcom Clarity Reports Downloader

## Description
Dexcom Clarity Reports Downloader est un outil automatisé permettant de télécharger, organiser et archiver les rapports Dexcom Clarity pour un suivi glycémique efficace.  
Le projet est conçu pour être portable, configurable et robuste, avec une gestion avancée des logs et des erreurs.

---

## Fonctionnalités principales

- Téléchargement automatisé de tous les rapports Dexcom Clarity sélectionnés
- Configuration centralisée via un fichier `config.yaml` (non versionné)
- Prise en charge des chemins portables (`~` et `/`)
- Gestion avancée des logs (application et navigateur)
- Sélection de la période, des rapports et du mode debug via la ligne de commande
- Robustesse accrue sur la gestion des erreurs et des téléchargements
- Compatible Windows (et adaptable Linux/Mac)

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
     ```

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
- `--debug` : Activer le mode debug pour des logs détaillés

Exemple pour télécharger les rapports des 7 derniers jours en mode debug :

```sh
python ClarityDownload.py --days 7 --debug
```

---

## Notes

- Les rapports sont organisés par année dans le dossier de destination.
- En cas de perte de connexion, le script gère les erreurs et reprend là où il s'est arrêté.
- Pour toute question, suggestion ou rapport de bug, ouvrez une issue sur GitHub.
- Merci de ne pas redistribuer ce code sans autorisation. Ce projet est fourni tel quel, sans garantie.

---

## Gestion des dates par défaut

- **Par défaut**, si aucune date n'est fournie en argument ou dans le fichier `config.yaml`, la période utilisée sera les **14 derniers jours jusqu'à hier**.
- Vous pouvez surcharger ce comportement :
  - en passant `--days 7`, `--days 14`, `--days 30` ou `--days 90` en argument,
  - ou en définissant explicitement `date_debut` et `date_fin` dans `config.yaml`,
  - ou encore en passant `--date_debut` et `--date_fin` en argument.

Exemple :

- Si nous sommes le 2025-08-06 et que vous ne passez aucun paramètre, la période sera du 2025-07-24 au 2025-08-05.

---
