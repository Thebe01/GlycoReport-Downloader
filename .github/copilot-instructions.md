# Instructions Copilot (GlycoReport-Downloader)

## Contexte projet

- Outil Windows (Python 3.10+) qui automatise le téléchargement des rapports
  Dexcom Clarity via Selenium/Chrome.
- **Entrée principale**: [GlycoDownload.py](../GlycoDownload.py) (CLI +
  orchestration).
- **Traitement rapports**: [rapports.py](../rapports.py) (sélection +
  sous-rapports + download/rename).
- **Config + secrets**: [config.py](../config.py) (lit/valide `config.yaml`,
  gère `.env` chiffré).
- **Utilitaires**: [utils.py](../utils.py) (normalisation chemins, overlays,
  fichiers téléchargés, screenshots, cleanup logs).

## Workflows développeur (Windows)

- Installer les deps: `pip install -r requirements.txt`
- Lancer le script (mode dev): `python GlycoDownload.py`
- Tester la config sans exécuter Selenium: `python GlycoDownload.py --dry-run`
- Lister les rapports disponibles: `python GlycoDownload.py --list-rapports`
- Tests unitaires (utilitaires):
  `pytest -v --log-cli-level=INFO tests/test_utils.py`
- Build exe + installateur:
  - Exe rapide:
    `pyinstaller --onefile --hidden-import=yaml --name "GlycoReport-Downloader" GlycoDownload.py`
  - Build complet (PyInstaller + Inno Setup):
    [DIST-GlycoReport-Downloader.ps1](../DIST-GlycoReport-Downloader.ps1)

## Conventions de configuration / secrets

- `config.yaml` est **utilisateur** (non versionné) et est créé à partir de
  [config_example.yaml](../config_example.yaml) si absent.
- `.env` contient les identifiants Dexcom et est **chiffré**; la clé Fernet est
  stockée dans la variable d’environnement système `ENV_DEXCOM_KEY` (voir
  [README.md](../README.md)).
- Ne jamais logger/afficher des secrets; `--dry-run` doit masquer les valeurs
  sensibles.
- Les chemins sont normalisés via `utils.normalize_path` (support de `~`,
  chemins absolus); conserver ce pattern quand on ajoute de nouveaux chemins.

## Synchronisation des templates

procédure de comparaison avec la source officielle et la recommandation de mise
à jour. Voir [TEMPLATE_SYNC_CHECK.md](TEMPLATE_SYNC_CHECK.md) pour la procédure
de comparaison La vérification doit être exécutée lorsqu’une conversation
Copilot est activée dans ce repo.

## Patterns Selenium / robustesse

- Utiliser `WebDriverWait` + `expected_conditions` (timeouts souvent 30–60s) et
  `attendre_disparition_overlay(driver, ...)` avant actions sensibles.
- Pattern clic robuste utilisé partout:
  - scroll into view → `element.click()` → fallback
    `driver.execute_script("arguments[0].click();", element)`.
- Pour les sélecteurs, préférer les attributs stables (ex: `data-test-*`) plutôt
  que le texte (voir `traitement_export_csv` dans
  [rapports.py](../rapports.py)).
- Les fichiers téléchargés sont détectés via `get_last_downloaded_nonlog_file`
  qui ignore `.log` et `.crdownload` (important pour éviter les faux positifs).

## Debugging rapide Selenium

> Note: ce projet est Windows-first. Quand tu fournis des commandes “shell”,
> donne des exemples en **PowerShell (pwsh)** (pas en bash).

- Activer le mode debug: `python GlycoDownload.py --debug`
  - Log applicatif détaillé (niveau DEBUG) dans le dossier de logs.
  - Screenshots automatiques sur certaines erreurs/étapes (uniquement en debug).
- Où trouver les logs / artefacts:
  - `chromedriver_log` (dans `config.yaml`) est le fichier log ChromeDriver.
  - Le dossier de logs est dérivé de `chromedriver_log` (voir
    `log_dir = os.path.dirname(chromedriver_log)` dans `GlycoDownload.py`).
  - Log applicatif: `clarity_download_<timestamp>.log` dans ce dossier.
  - Screenshots: `screenshot_<step>_<timestamp>.png` dans ce dossier (via
    `capture_screenshot` dans `utils.py`).
- Où trouver les fichiers:
  - Dossier de téléchargement Selenium: `download_dir` (dans `config.yaml`).
  - Sortie finale (rapports déplacés/renommés): `output_dir/<YYYY>/...`.
- Vérifications rapides:
  - Confirmer l’absence de `.crdownload` pendant l’attente de fin de
    téléchargement.
  - En cas d’erreur UI (overlay/interception), forcer le pattern “scroll → click
    → JS click fallback”.
- Checklist de dépannage (symptôme → action):
  - Overlay/loader qui ne disparaît jamais → augmenter les timeouts et appeler
    `attendre_disparition_overlay(...)` avant chaque clic sensible.
  - `ElementClickIntercepted` / clic ignoré → `scrollIntoView` puis clic JS
    (`driver.execute_script("arguments[0].click();", element)`).
  - Élément introuvable après navigation → valider l’URL (`driver.current_url`),
    attendre un sélecteur “ancre” (`WebDriverWait`), puis seulement chercher le
    bouton.
  - Mauvais sélecteur lié à la langue → préférer `data-test-*`, `id` ou `href`
    stables plutôt que le texte visible.
  - Téléchargement “bloqué” → vérifier la présence de `.crdownload`; si ça
    persiste, augmenter l’attente et confirmer que `download_dir` correspond au
    profil Chrome utilisé.
  - Mauvais fichier renommé/déplacé → s’assurer que
    `get_last_downloaded_nonlog_file` ne voit pas un ancien fichier (vider
    `download_dir` en test ou filtrer plus strictement).
  - Session expirée / redirection login → relancer avec `--debug`, vérifier le
    log appli + `chromedriver_log`, et capturer un screenshot au moment de la
    redirection.

- Commandes PowerShell utiles (diagnostic rapide):

  ```powershell
  # Se placer à la racine du repo
  Set-Location -LiteralPath "C:\Users\thebe\OneDrive\Sources\GlycoReport-Downloader"

  # Extraire rapidement des chemins depuis config.yaml (supporte lignes avec ou sans guillemets)
  $chromedriverLog = (Get-Content .\config.yaml | Select-String '^\s*chromedriver_log\s*:' | Select-Object -First 1).Line -replace '^\s*chromedriver_log\s*:\s*', '' -replace '^["'']|["'']$', ''
  $downloadDir     = (Get-Content .\config.yaml | Select-String '^\s*download_dir\s*:'     | Select-Object -First 1).Line -replace '^\s*download_dir\s*:\s*', ''     -replace '^["'']|["'']$', ''

  # Déduire le dossier de logs (même logique que dans l'app: dirname(chromedriver_log))
  $logDir = Split-Path -Parent $chromedriverLog

  # Dernier log applicatif (les 200 dernières lignes)
  Get-ChildItem $logDir -Filter 'clarity_download_*.log' |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1 |
    Get-Content -Tail 200

  # Rechercher des erreurs fréquentes dans les logs applicatifs
  Select-String -Path (Join-Path $logDir 'clarity_download_*.log') -Pattern 'ERROR|Traceback|SEVERE|TimeoutException|ElementClickIntercepted' -CaseSensitive:$false

  # Lister les screenshots les plus récents
  Get-ChildItem $logDir -Filter 'screenshot_*.png' |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 20

  # Vérifier si un téléchargement est encore en cours (.crdownload)
  Get-ChildItem $downloadDir -Filter '*.crdownload' | Sort-Object LastWriteTime -Descending

  # Dernier fichier téléchargé (hors .log et .crdownload)
  Get-ChildItem $downloadDir -File |
    Where-Object { $_.Extension -ne '.log' -and $_.Extension -ne '.crdownload' } |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
  ```

- Pour isoler un problème de config sans Selenium:
  `python GlycoDownload.py --dry-run`
- Ne jamais logger de secrets (identifiants Dexcom); même en debug,
  masquer/éviter toute valeur sensible.

## Organisation des sorties

- Les rapports sont renommés/déplacés via `deplace_et_renomme_rapport` dans
  [rapports.py](../rapports.py); la sortie est rangée par année
  (`output_dir/<YYYY>/...`).
- Les noms de rapports attendus sont en français (ex: "Aperçu", "AGP", "Export")
  et la logique de dispatch est centralisée dans `selection_rapport`.

## Packaging / migration

- L’installateur Inno Setup est défini dans
  [Setup/GlycoReport-Downloader.iss](../Setup/GlycoReport-Downloader.iss).
- Ne pas inclure `config.yaml` dans l’installateur (évite d’écraser la config
  utilisateur).
- Migration: [migrate.py](../migrate.py) (et l’exe `migrate.exe`) — doc dans
  [MIGRATION.md](../MIGRATION.md).

## Changements fréquents (à respecter)

- La version source de vérité est [version.py](../version.py) (`__version__`).
  Si vous modifiez la version, garder les entêtes synchronisés.
- Éviter d’introduire de nouvelles dépendances si une utilitaire existe déjà
  dans [utils.py](../utils.py) ou un flux dans [config.py](../config.py).
