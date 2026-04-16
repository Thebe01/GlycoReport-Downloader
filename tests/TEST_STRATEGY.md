# Strategie de test (hors installation)

Objectif: valider GlycoReport-Downloader sans dependre d'une version installee
sur la machine. On teste depuis un dossier de test autonome contenant l'exe, le
script de lancement et le config.

## Principes

- Utiliser l'executable copie dans le dossier de test.
- Utiliser le script Launch-Dexcom-And-Run.ps1 copie dans le dossier de test.
- Utiliser le config.yaml present dans le dossier de test.
- Lancement via Launch-Dexcom-And-Run.ps1 pour lier Selenium au Chrome deja
  ouvert (remote debugging).

## Preparation (PowerShell)

```powershell
# Dossier de test autonome
$testRoot = "C:\Users\thebe\Downloads\Dexcom_download_test"
New-Item -ItemType Directory -Path $testRoot -Force | Out-Null
```

## Configuration de test

Utiliser le config.yaml present dans le dossier de test. Il doit pointer vers le
dossier de test:

- download_dir: $testRoot
- output_dir: $testRoot
- chromedriver_log: $testRoot\log\clarity_chromedriver.log

Si vous devez modifier le config.yaml, editez directement celui du dossier de
test ou utilisez un fichier alternatif avec le parametre -ConfigPath.

## Execution end-to-end (sans version installee)

```powershell
# Genere dist/GlycoReport-Downloader.exe
.\DIST-GlycoReport-Downloader.ps1

# Se placer dans le dossier de test
Set-Location -LiteralPath $testRoot

# Lance Chrome avec le profil configure, puis l'app en mode reprise
.\Launch-Dexcom-And-Run.ps1 -ConfigPath .\config.yaml
```

Etapes:

1. Chrome s'ouvre avec le profil configure. Connectez-vous a Dexcom Clarity.
2. Revenez au terminal et appuyez sur Entree.
3. L'app se lance en mode reprise (login deja effectue).

## Verification des resultats

- Les fichiers telecharges doivent etre dans $testRoot\<AAAA>.
- Les logs et screenshots sont dans $testRoot\log.
- Confirmer l'absence de .crdownload residuel avant verification.

## Tests unitaires cibles

Pour valider rapidement les scenarios critiques sans test E2E complet :

```powershell
# Tous les tests unitaires (script dedie, depuis tests/)
.\tests\Run-Tests.ps1

# Ou manuellement avec pytest
python -m pytest -v tests/

# Reconnexion reseau (succes puis echec)
python -m pytest -q tests/test_rapports_network.py

# Fermeture de session navigateur (1 onglet vs plusieurs onglets)
python -m pytest -q tests/test_glycodownload_shutdown.py

# Priorite des dates / parametre days (ES-21)
python -m pytest -q tests/test_glycodownload_dates.py

# Suite combinee
python -m pytest -q tests/test_rapports_network.py tests/test_glycodownload_shutdown.py tests/test_glycodownload_dates.py
```

Resultat attendu :

- Tous les tests passent (statut `passed`).
- Aucun traceback Python dans la sortie.

### Modules de test et couverture

| Fichier                              | Ce qui est teste                                             | Ticket |
|--------------------------------------|--------------------------------------------------------------|--------|
| `test_utils.py`                      | Utilitaires (chemins, internet, logs, screenshots, backoff)  | —      |
| `test_glycodownload_shutdown.py`     | `close_browser_session` (1 onglet / plusieurs onglets)       | ES-14  |
| `test_rapports_network.py`           | Retry reseau et `selection_rapport`                          | ES-14  |
| `test_glycodownload_dates.py`        | `resolve_effective_date_range` (chaine de priorite dates)    | ES-21  |

## Nettoyage

```powershell
Remove-Item -Recurse -Force $testRoot
```

## Notes

- L'app n'execute pas les telechargements tant que l'usager n'est pas connecte.
- Si un navigateur Chrome est deja ouvert avec le meme profil, fermez-le avant
  le test.
- Pour tester sans telechargement: utiliser --dry-run (pas besoin de login).
