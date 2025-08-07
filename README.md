# Dexcom Clarity Reports Downloader

Ce projet permet de télécharger automatiquement les différents rapports Dexcom Clarity ainsi que les relevés bruts, et de les organiser dans des dossiers structurés.

## Fonctionnalités principales

- Téléchargement automatisé de tous les rapports Dexcom Clarity (Aperçu, Modèles, Superposition, Quotidien, Statistiques, AGP, Export)
- Gestion robuste des erreurs et de la connexion internet
- Centralisation des paramètres et chemins
- Déplacement et renommage automatique des fichiers téléchargés
- Déconnexion propre du compte Dexcom Clarity

---

## Prérequis

- Python 3.12 ou 3.13
- Google Chrome installé
- [ChromeDriver](https://chromedriver.chromium.org/downloads) compatible avec votre version de Chrome
- Modules Python : `selenium`, `python-dotenv` (optionnel mais recommandé pour le développement local)

---

## Installation

1. Clonez ce dépôt ou copiez les fichiers dans un dossier local.
2. Installez les dépendances nécessaires :

   ```bash
   pip install selenium python-dotenv
   ```

3. Téléchargez et placez `chromedriver.exe` dans le dossier du projet ou dans votre PATH.

---

## Configuration des paramètres

Tous les chemins, URLs et paramètres sont centralisés en haut du fichier `ClarityDownload.py`.
Vous pouvez les modifier selon vos besoins :

- `DOWNLOAD_DIR` : Dossier temporaire de téléchargement
- `DIR_FINAL_BASE` : Dossier final pour les rapports
- `CHROME_USER_DATA_DIR` : Profil Chrome dédié
- `DEXCOM_URL` : URL Dexcom Clarity
- `CHROMEDRIVER_LOG` : Fichier log ChromeDriver
- `RAPPORTS` : Liste des rapports à traiter
- `DATE_DEBUT`, `DATE_FIN` : Période des rapports

## Configuration

1. Copiez `config_example.yaml` en `config.yaml` et adaptez les chemins, rapports, etc.
2. Copiez `.env.example` en `.env` et renseignez vos identifiants Dexcom.
3. Pour les besoins courants, utilisez les options CLI :
   - `--days 14` pour les 14 derniers jours
   - `--date_debut` et `--date_fin` pour des dates précises
   - `--rapports` pour choisir les rapports à générer

---

## Utilisation des credentials (identifiants)

**Pour des raisons de sécurité, le script ne stocke jamais les identifiants (courriel/mot de passe) en clair dans le code source.
Il attend que les variables d'environnement suivantes soient définies :**

- `DEXCOM_USERNAME` : l'adresse courriel de connexion Dexcom Clarity
- `DEXCOM_PASSWORD` : le mot de passe associé

### Comment définir les variables d'environnement ?

#### 1. Avec un fichier `.env` (recommandé pour le développement local)

Créez un fichier `.env` à la racine du projet avec :

```TEXT
DEXCOM_USERNAME=mon_email@example.com
DEXCOM_PASSWORD=mon_mot_de_passe
```

Le script chargera automatiquement ces variables si vous utilisez la librairie `python-dotenv`.

#### 2. En ligne de commande

**Windows (cmd) :**

```TEXT
set DEXCOM_USERNAME=mon_email@example.com
set DEXCOM_PASSWORD=mon_mot_de_passe

**PowerShell :**
```TEXT
$env:DEXCOM_USERNAME="mon_email@example.com"
$env:DEXCOM_PASSWORD="mon_mot_de_passe"

```TEXT
$env:DEXCOM_USERNAME="mon_email@example.com"
$env:DEXCOM_PASSWORD="mon_mot_de_passe"
```

**Linux/macOS :**

```TEXT
export DEXCOM_USERNAME=mon_email@example.com
export DEXCOM_PASSWORD=mon_mot_de_passe


### Sécurité

- **Ne versionnez jamais le fichier `.env`** (ajoutez-le à votre `.gitignore`).
- **Ne logguez jamais les credentials** dans les fichiers de log ou la console.

---

## Lancement du script

```bash
python ClarityDownload.py
```

Pour activer le mode debug (logs détaillés) :

```bash
python ClarityDownload.py --debug
```

---

## Notes

- Le script crée automatiquement les dossiers nécessaires pour organiser les rapports par année.
- En cas de problème de connexion internet, le script s’arrête proprement.
- Pour toute question ou contribution, n'hésitez pas à ouvrir une issue sur GitHub.
- Merci de respecter les droits d'auteur et de ne pas redistribuer ce code sans autorisation.
- Ce script est fourni "tel quel" sans garantie d'aucune sorte. Utilisez-le à vos propres risques.
- Pour toute question ou contribution, n'hésitez pas à ouvrir une issue sur GitHub.

## Gestion des dates par défaut

- **Par défaut**, si aucune date n'est fournie en argument ou dans le fichier `config.yaml`, la période utilisée sera les **14 derniers jours jusqu'à hier**.
- Vous pouvez surcharger ce comportement :
  - en passant `--days 7`, `--days 14`, `--days 30` ou `--days 90` en argument,
  - ou en définissant explicitement `date_debut` et `date_fin` dans `config.yaml`,
  - ou encore en passant `--date_debut` et `--date_fin` en argument.

Exemple :

- Si nous sommes le 2025-08-06 et que vous ne passez aucun paramètre, la période sera du 2025-07-24 au 2025-08-05.

---
