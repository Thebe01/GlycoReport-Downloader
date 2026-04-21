# Changelog

Toutes les modifications notables sont documentées ici.
Format : [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/) — versionnage [SemVer](https://semver.org/).

---

## [0.5.12] - 2026-04-21 — ES-28

### Modifié
- Robustesse : tous les blocs `except Exception` remplacés par des exceptions spécifiques
  (`TimeoutException`, `ElementClickInterceptedException`, `WebDriverException`,
  `StaleElementReferenceException`, `OSError`, `URLError`, `InvalidToken`, `ValueError`, etc.)
  dans les quatre modules (`GlycoDownload.py`, `rapports.py`, `utils.py`, `config.py`).

---

## [0.5.11] - 2026-04-21 — ES-28

### Corrigé
- Sécurité : `subprocess.Popen("start powershell", shell=True)` remplacé par
  `subprocess.Popen(["powershell.exe"], creationflags=CREATE_NEW_CONSOLE)` dans `config.py` —
  élimine le risque d'injection shell.

---

## [0.5.10] - 2026-04-17 — ES-26

### Modifié
- `CHANGELOG.md` et `requirements-dev.txt` ajoutés au dépôt.
- `pytest` et `pyinstaller` déplacés de `requirements.txt` vers `requirements-dev.txt`.
- `CLAUDE.md` retiré du dépôt (instructions IA locales uniquement, ajouté à `.gitignore`).
- Couverture de tests : `test_config_validation.py`, `test_rapports_period.py`,
  `TestValidateDates` dans `test_glycodownload_dates.py` — 81 tests au total.

---

## [0.5.9] - 2026-04-17 — ES-25

### Corrigé
- Fermeture modale Export : `EC.invisibility_of_element_located` remplacé par
  `until_not(presence_of_element_located)` pour garantir le retrait du DOM
  (et non seulement l'invisibilité CSS).

---

## [0.5.8] - 2026-04-17 — ES-25

### Corrigé
- Déconnexion : `except Exception` remplacé par `except ElementClickInterceptedException`
  sur les clics menu utilisateur et logout_link ; import ajouté.

---

## [0.5.7] - 2026-04-17 — ES-25

### Corrigé
- Fermeture modale Export : `xpath_fermer` ancré dans `<export-dialog>` (custom element) —
  conditions `data-test-*` obsolètes supprimées (Dexcom les a retirées).
- Attente explicite de disparition du composant après clic Fermer (évite que la déconnexion
  suivante soit interceptée par l'overlay résiduel).

---

## [0.5.6] - 2026-04-16 — ES-25

### Corrigé
- Déconnexion : seconde attente overlay après ouverture du menu utilisateur.
- JS fallback sur `logout_link.click()` pour contourner `ElementClickInterceptedException`.

---

## [0.5.5] - 2026-04-15 — CR

### Ajouté
- `validate_dates` : erreur explicite (`sys.exit(1)`) si une seule date CLI est fournie
  (dates partielles refusées).
- Garde défensif (`ValueError`) dans `resolve_effective_date_range` pour les dates partielles.

---

## [0.5.4] - 2026-04-15 — CR

### Ajouté
- Validation du paramètre `days` dans `config.yaml` : type, valeurs autorisées `{7, 14, 30, 90}`,
  avertissement si conflit avec `date_debut` / `date_fin`.

---

## [0.5.3] - 2026-04-15 — ES-25

### Corrigé
- Saisie des dates : `element_to_be_clickable` au lieu de `presence_of_element_located` ;
  clic + clear + send_keys par champ séquentiellement (évite `StaleElementReferenceException`).

---

## [0.5.2] - 2026-04-15 — ES-25

### Corrigé
- Saisie des dates : erreur fatale si Selenium échoue à entrer les dates dans l'UI Dexcom
  (au lieu de continuer silencieusement avec les dates par défaut de Dexcom).

---

## [0.5.0] - 2026-04-14 — ES-21

### Ajouté
- Paramètre `days` dans `config.yaml` : fenêtre glissante sans fixer de dates explicites.
- Chaîne de priorité : CLI dates > CLI `--days` > config `days` > config dates.
- Extraction de `resolve_effective_date_range` (fonction pure, testable sans Selenium).

---

## [0.4.0] - 2026-04-14 — ES-20

### Ajouté
- Tous les paramètres CLI de `GlycoDownload.py` exposés dans `Launch-Dexcom-And-Run.ps1`.
- Correction des flags `-StartAtDateSelection` et `-AttachDebugger` (actifs par défaut,
  désactivables explicitement).

---

## [0.3.x] - 2026-01-29 → 2026-03-25

### 0.3.19 (ES-14)
- Fermeture navigateur : utilisation du mode debug effectif pour les traces d'exception.
- Durcissement du retry réseau dans `selection_rapport` (max 2 retries, puis `NetworkRecoveryFailedError`).

### 0.3.18 (ES-14)
- Durcissement de la gestion des pertes réseau dans le flux Export CSV (modale + fermeture).

### 0.3.17 (ES-14)
- Détection des pertes réseau pendant le traitement des rapports.
- Tentative de reconnexion automatique ; arrêt propre en cas d'échec.
- Fermeture de l'onglet Dexcom en fin de traitement ; fermeture complète si un seul onglet ouvert.

### 0.3.16 (ES-15)
- Rétention des logs par défaut à 30 jours (config + documentation).

### 0.3.15 (ES-6)
- Harmonisation des XPath pour réduire la dépendance à la langue du navigateur.

### 0.3.13 (ES-3)
- Rapport Comparer : téléchargement de Tendances seulement (contournement bug Dexcom).

### 0.3.14 (ES-11)
- Ajout du suffixe de période dans les noms de fichiers téléchargés.

### 0.3.12 → 0.3.6 (ES-3)
- Stabilisation des sous-rapports Comparer (navigation, fermeture/réouverture modale,
  retry clics, accès direct `/compare/overlay` et `/compare/daily`).

### 0.3.0 (ES-19)
- Ajout du point d'entrée `--start-at-date-selection`.

---

## [0.2.x] - 2025-10-07 → 2026-01-20

### Points marquants
- **0.2.0** : Réorganisation complète en modules (`config.py`, `rapports.py`, `utils.py`).
- **0.2.2 (ES-6)** : Rapports indépendants de la langue de l'interface utilisateur.
- **0.2.3 (ES-11)** : Rapport Statistiques horaires ; `ChromeDriverManager` automatique.
- **0.2.6 (ES-7)** : `--help` détaillé, `--list-rapports`, `--dry-run`, validation des dates.
- **0.2.7 (ES-16)** : Retry automatique sur erreurs 502 ; suivi des échecs de téléchargement.
- **0.2.14 (ES-19)** : Attente vérification humaine Cloudflare (pause + reprise automatique).

---

## [0.1.x] - 2025-08-18 → 2025-09-23

### Points marquants
- **0.1.0** : Robustesse saisie identifiant, captures d'écran en mode debug uniquement,
  gestion du bouton "Pas maintenant" après connexion.
- **0.1.6** : Gestion améliorée de la sélection des jours.
- **0.1.7** : Détermination automatique de la version de ChromeDriver.

---

## [0.0.x] - 2025-03-03 → 2025-08-13 — Développement initial

### Points marquants
- **0.0.1** : Connexion à Dexcom Clarity et authentification.
- **0.0.9** : Option `--debug` et fichier de log.
- **0.0.10** : Gestion connexion lente/instable, vérification internet, rapports Modèles.
- **0.0.11** : Rapports Superposition, Quotidien, AGP.
- **0.0.13** : Rapport Comparer (avec sous-rapports).
- **0.0.14** : Export CSV.
- **0.0.18** : Gestion d'exceptions précise, factorisation, fonction `main()`.
- **0.0.20** : Extraction en modules (`config.py`, `utils.py`, `rapports.py`).

---

[0.5.12]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/v0.5.12
[0.5.11]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/v0.5.11
[0.5.10]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/v0.5.10
[0.5.9]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/v0.5.9
[0.5.8]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/v0.5.8
[0.5.7]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/v0.5.7
[0.5.6]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/v0.5.6
[0.5.5]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/v0.5.5
[0.5.4]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/v0.5.4
[0.5.3]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/v0.5.3
[0.5.2]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/v0.5.2
[0.5.0]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/v0.5.0
[0.4.0]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/v0.4.0
[0.3.x]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/v0.3.19
[0.2.x]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/v0.2.18
[0.1.x]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/v0.1.7
[0.0.x]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/v0.0.23
