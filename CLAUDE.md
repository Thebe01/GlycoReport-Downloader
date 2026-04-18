# CLAUDE.md — GlycoReport-Downloader

## Nature du projet

Application Windows desktop qui automatise le téléchargement de rapports Dexcom Clarity via Selenium.
Distribuée comme exécutable PyInstaller + installateur Inno Setup. **Pas une librairie PyPI.**

Langue du code source : français (logs, commentaires, docstrings).

## Architecture

| Fichier | Rôle |
|---|---|
| `GlycoDownload.py` | Point d'entrée CLI, orchestration, résolution des dates |
| `config.py` | Chargement et validation de `config.yaml` |
| `rapports.py` | Téléchargement des rapports Dexcom (Selenium) |
| `utils.py` | Utilitaires : chemins, internet, logs, screenshots, backoff |
| `version.py` | **Source unique de vérité** pour la version |

## Règle de version — CRITIQUE

La version doit être synchronisée dans **5 endroits** à chaque bump :

1. `version.py` — `__version__ = "X.Y.Z"` et header docstring
2. `GlycoDownload.py` — header docstring (Version + Modifié le + entrée Modifications)
3. `rapports.py` — idem
4. `config.py` — idem
5. `utils.py` — idem

Et dans le `README.md` : badge version + ancre Sommaire + sections FR/EN Nouveautés/Historique.

Ne jamais bumper un seul fichier. Toujours tous les cinq.

## Format des en-têtes Python

Voir [.github/HEADER_TEMPLATE_PYTHON.md](.github/HEADER_TEMPLATE_PYTHON.md) pour le format complet.

Points clés :
- Shebang + encoding lignes 1-2 obligatoires
- Métadonnées alignées sur 14 espaces après le label
- Section `Modifications` : colonne ticket en **8 caractères** (ex. `[ES-14] `, `[N/A]   `)
- Continuation multi-ligne : indentation égale à la longueur du préfixe entier

## Format des entrées de changelog

```
X.Y.Z  - YYYY-MM-DD   [ES-XX]  : Description.
```

Exemples de padding ticket (8 chars) :
- `[ES-14] ` (7 + 1 espace)
- `[N/A]   ` (5 + 3 espaces)
- `[CR]    ` (4 + 4 espaces)

## Tests

**Règle absolue : aucun test Selenium.** Uniquement du code pur testable sans navigateur.

Runner : `.\tests\Run-Tests.ps1` (PowerShell) ou `python -m pytest -v tests/`

| Fichier test | Ce qui est testé | Ticket |
|---|---|---|
| `test_utils.py` | Utilitaires (chemins, internet, logs, screenshots, backoff) | — |
| `test_glycodownload_shutdown.py` | `close_browser_session` (1 onglet / plusieurs onglets) | ES-14 |
| `test_rapports_network.py` | Retry réseau et `selection_rapport` | ES-14 |
| `test_glycodownload_dates.py` | `resolve_effective_date_range` + `validate_dates` | ES-21 |
| `test_rapports_period.py` | `get_period_suffix` (locale, dates, args.days) | ES-26 |
| `test_config_validation.py` | `validate_config` — paramètre `days` | ES-26 |

`days=0` est falsy en Python — traité comme "non fourni", repli sur le calcul par dates.

## Distribution

```powershell
# Compiler l'exécutable
.\DIST-GlycoReport-Downloader.ps1

# Lancer en mode test (Chrome déjà ouvert)
.\Launch-Dexcom-And-Run.ps1 -ConfigPath .\config.yaml
```

Dossier de test autonome recommandé : `C:\Users\thebe\Downloads\Dexcom_download_test`

Voir [tests/TEST_STRATEGY.md](tests/TEST_STRATEGY.md) pour la procédure complète.

## Jira

- Instance : innovationspt.atlassian.net
- Projet : **ES**
- Cloud ID : `a97ffa05-cc62-4208-b8c9-32fc05df87eb`
- Tickets actifs connus : ES-20 (CLI params), ES-21 (days), ES-25 (Selenium fixes), ES-26 (tests), ES-27 (locale deprecation)

## Décisions techniques importantes

### Chaîne de priorité des dates (ES-21)
1. CLI `--date-debut` + `--date-fin` (les deux obligatoires si l'un est fourni)
2. CLI `--days`
3. `config.yaml` → `days`
4. `config.yaml` → `date_debut` / `date_fin`

Valeurs autorisées pour `days` : `{7, 14, 30, 90}` seulement.

### XPath export-dialog (ES-25)
```python
xpath_fermer = "//export-dialog//button[normalize-space()='Fermer' or normalize-space()='Close']"
```
Ancré dans `<export-dialog>` custom element — ne pas utiliser `data-test-*` (Dexcom les supprime).

Après le clic Fermer, attendre le retrait du DOM avec `until_not(presence_of_element_located)`,
**pas** `invisibility_of_element_located` (qui ne garantit que la visibilité CSS, pas le retrait DOM).

### Gestion des exceptions Selenium
- Utiliser `ElementClickInterceptedException` (et non `except Exception`) pour les clics avec fallback JS.
- Utiliser `except TimeoutException` pour les attentes WebDriverWait.
- `except Exception` trop large masque `StaleElementReferenceException` et autres erreurs légitimes.

### locale (ES-27 — à implémenter)
`locale.getdefaultlocale()` est déprécié depuis Python 3.11 et sera retiré en 3.15.
Remplacer par `locale.getlocale()[0]` dans `rapports.py`.

## Commandes utiles

```bash
# Vérifier la version courante
python -c "from version import __version__; print(__version__)"

# Lancer tous les tests unitaires
python -m pytest -v tests/

# Lancer un fichier de test spécifique
python -m pytest -q tests/test_glycodownload_dates.py
```
