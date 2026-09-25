# Changelog

Toutes les modifications notables sont documentées ici.
Format : [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/) — versionnage [SemVer](https://semver.org/).

---

## [0.6.7] - 2026-09-25 — CR

### Corrigé
- `GlycoDownload.py` : l'exception finale d'`ouvrir_selecteur_dates` dit « non utilisable après
  N tentatives », comme le WARNING corrigé en 0.6.5. « non ouvert » était faux quand le panneau
  était présent mais jamais cliquable (revue Copilot). Aucune autre occurrence dans le code.
- `tests/test_glycodownload_selecteur_dates.py` (0.1.4) : message de l'exception vérifié ;
  panneau présent jamais cliquable (un seul clic) — 134 tests.

---

## [0.6.6] - 2026-09-25 — CR

### Corrigé
- `GlycoDownload.py` : `ouvrir_selecteur_dates` vérifie la présence de `start_date` avant chaque
  clic, y compris le premier. Un panneau laissé ouvert avant le lancement (connexion manuelle
  dans Launch) était refermé par la bascule (revue Copilot).
- `tests/test_glycodownload_selecteur_dates.py` (0.1.3) : texte exact du WARNING vérifié ;
  panneau déjà ouvert avant le 1er clic — 133 tests (revue Copilot).

---

## [0.6.5] - 2026-09-25 — CR

### Corrigé
- `GlycoDownload.py` : le WARNING d'échec du sélecteur de dates dit « non utilisable N s après
  la tentative X/3 ». Il annonçait « non ouvert … après le clic » même quand la protection
  de 0.6.4 avait sauté le clic parce que le panneau était présent.
- `tests/test_glycodownload_selecteur_dates.py` (0.1.2) : le test du panneau lent passait selon
  le nombre de vérifications internes de `WebDriverWait` (deux par attente). Il dépend
  désormais du constat de la protection : 1 clic, 1 capture, succès (revue Copilot).

---

## [0.6.4] - 2026-09-24 — CR

### Corrigé
- `GlycoDownload.py` : `ouvrir_selecteur_dates` rattrape `ElementClickInterceptedException` et
  clique par JavaScript, comme les autres clics du projet. L'exception sortait de la boucle et
  les 3 tentatives n'étaient pas garanties (revue Copilot).
- `GlycoDownload.py` : pas de nouveau clic si `start_date` est déjà dans le DOM. Le bouton
  est une bascule : un panneau lent à s'activer aurait été refermé (revue Copilot).
- `tests/test_glycodownload_selecteur_dates.py` : repli JavaScript, panneau présent sans
  nouveau clic — 132 tests.

---

## [0.6.3] - 2026-09-24 — ES-28

### Corrigé
- `GlycoDownload.py` : `ouvrir_selecteur_dates` clique de nouveau sur le bouton du sélecteur
  si le champ `start_date` n'apparaît pas dans les 10 s, jusqu'à 3 tentatives, avec WARNING
  et capture à chaque échec. Mitigation : le panneau restait fermé malgré un `ClickElement`
  réussi (21:34 et 23:09 le 2026-09-24). Les délais de chargement ne distinguent pas les
  échecs des réussites ; la cause reste inconnue.
- `tests/test_glycodownload_selecteur_dates.py` : ouverture au 1er clic, au 2e, jamais —
  130 tests.

---

## [0.6.2] - 2026-09-24 — ES-28

### Corrigé
- Justification du journal ChromeDriver par exécution (0.6.0) : l'ancien fichier unique ne
  grossissait pas. ChromeDriver l'écrase à chaque lancement (`--log-path` sans
  `--append-log`) ; ses 22 Mo venaient d'une seule exécution en debug (`--verbose`).
  Commentaire de `GlycoDownload.py`, README et entrée 0.6.0 corrigés.

### Contexte
- Le journal par exécution est conservé : il garde celui d'une exécution en échec après sa
  relance. Coût en debug : environ 20 Mo par exécution, bornés par `log_retention_days`.

---

## [0.6.1] - 2026-09-24 — ES-28

### Corrigé
- `GlycoDownload.py` : `close_browser_session` arrête le service ChromeDriver. `Browser.close`
  (CDP) et `close()` le laissaient tourner ; `Service.__del__` tentait de l'arrêter à la sortie
  de Python, sur un descripteur déjà invalide (WinError 6). La trace, invisible en `--windowed`,
  apparaît depuis la compilation en `--console` (0.6.0).
- `tests/test_glycodownload_shutdown.py` : arrêt du service dans les deux branches, erreur
  absorbée, pilote sans service.

---

## [0.6.0] - 2026-09-24 — ES-28

### Corrigé
- `rapports.py` : `os.replace` relancé toutes les 2 s pendant 120 s au plus tant qu'il
  échoue avec WinError 32, pour le PDF comme pour l'Export. L'antivirus (Avast) analyse
  le fichier dès que Chrome lui donne son nom final et le garde ouvert : Statistiques-
  Horaires était resté à la racine le 2026-09-24.
- `utils.py` / `rapports.py` : `get_last_downloaded_report_file(depuis=...)` écarte les
  fichiers créés avant le clic de téléchargement. Un PDF orphelin ne peut plus être
  renommé sous le nom du rapport suivant.

### Ajouté
- Bilan de fin de traitement (`selection_rapport`) : rapports classés en INFO, sous-rapports
  Comparer sautés en WARNING, rapports manquants en ERROR. Écrit même après une perte réseau.
- Journal encadré par `Début GlycoReport-Downloader vX.Y.Z` et `Fin GlycoReport-Downloader vX.Y.Z`.
- Console ouverte jusqu'à la fin : exécutable compilé en `--console`
  (`DIST-GlycoReport-Downloader.ps1` 2.0.11) et lancé par appel direct dans
  `Launch-Dexcom-And-Run.ps1` (0.2.0), qui renvoie le code de sortie.
- Pause finale s'il manque un rapport ou si une ligne ERROR a été écrite. `pause_on_error`
  n'attend que si stdin est un terminal et la session interactive (WSF_VISIBLE) : une tâche
  planifiée hors session n'est jamais bloquée.
- `tests/test_rapports_renommage.py` : relance du renommage, filtre `depuis`, bilan,
  conditions de pause — 123 tests.

### Modifié
- Journal ChromeDriver propre à chaque exécution (`clarity_chromedriver_<horodatage>.log`),
  soumis à `log_retention_days`. L'ancien fichier unique était écrasé à chaque lancement.
- Erreurs JS du navigateur écrites en DEBUG au lieu d'ERROR.

### Retiré
- Liste des boutons de la page écrite avant la déconnexion (reste de débogage).
- Copie locale de `pause_on_error` dans `GlycoDownload.py` : celle d'`utils.py` fait foi.

---

## [0.5.25] - 2026-09-23 — CR

### Ajouté
- `tests/test_rapports_network.py` : test ciblant spécifiquement le bloc de fermeture de
  la modale d'export. C'est le seul des neuf sites réseau qui journalise **sans
  `return`** : le traitement y poursuivait jusqu'au déplacement du fichier, donc une
  erreur de transport produisait un rapport d'apparence valide. Les deux clics précédents
  réussissent, la coupure survient sur la fermeture, et une assertion vérifie le contexte
  réellement atteint — 108 tests.

### Contexte
- Le test de 0.5.24 couvrait le mécanisme dans `_handle_network_loss`, mais son test de
  flux passait par le site « clic du bouton Exporter » et non par la fermeture de modale.
  Vérifié : sans la relance de 0.5.24, ce nouveau test échoue sur ses deux assertions —
  aucune exception ne remonte et le fichier est déplacé.

---

## [0.5.24] - 2026-09-23 — CR

### Corrigé
- `rapports.py` : `_handle_network_loss` relance désormais les erreurs de transport
  qu'elle ne reconnaît pas, au lieu de retourner sans rien faire. Depuis que les neuf
  `except` des sites de perte réseau incluent `ProtocolError` et `RequestException`
  (0.5.23), une erreur de transport qui n'est ni un reset ni accompagnée d'une perte
  d'accès tombait dans cette fonction, en ressortait silencieusement, puis était avalée
  par l'appelant — qui journalise et sort. Le rapport était abandonné sans erreur
  visible, alors qu'avant 0.5.23 l'exception remontait au gestionnaire principal.

  Le flux d'export était le plus exposé : son bloc de fermeture de modale journalise en
  warning **sans `return`**, donc le traitement poursuivait vers `wait_for_csv_download`
  et le déplacement du fichier comme si le rapport était valide.

### Ajouté
- `tests/test_rapports_network.py` : relance d'une erreur de transport non reconnue par
  `_handle_network_loss`, et garantie qu'aucun fichier n'est déplacé quand une telle
  erreur survient dans le flux d'export — 107 tests.

### Contexte
- Les deux constats d'une revue Copilot sur la PR de 0.5.23 se ramenaient à ce seul
  défaut. La revue situait par ailleurs le premier au mauvais endroit : elle visait un
  `except` qui appelle bien `_handle_network_loss`, et non le bloc best-effort de
  fermeture de modale laissé volontairement inchangé, qui journalise en DEBUG et reste
  limité aux exceptions Selenium.

---

## [0.5.23] - 2026-09-23 — ES-28

### Corrigé
- Les coupures de connexion par l'hôte distant (`ConnectionResetError` 10054)
  échappaient entièrement au dispositif de reconnexion. Trois causes cumulées,
  corrigées ensemble :
  - `GlycoDownload.py` : `ChromeDriverManager().install()` n'était couvert par aucun
    retry. Cet appel télécharge le driver via `requests`, avant l'ouverture du
    navigateur et donc en amont de tout le dispositif réseau de `rapports.py`. Il passe
    désormais par `retry_on_network_error` (3 essais, backoff exponentiel borné).
  - `rapports.py` : un reset remonte en `urllib3.exceptions.ProtocolError` brute depuis
    Selenium (`remote_connection` n'enveloppe pas les erreurs urllib3) ou en
    `requests.exceptions.RequestException` depuis webdriver-manager. Ni l'une ni l'autre
    n'est une exception Selenium, et `ProtocolError` n'est même pas une `OSError` : les
    neuf `except` des sites de perte réseau ne les voyaient pas et l'exception remontait
    jusqu'au gestionnaire `except Exception` de `main()`. Ils incluent désormais
    `ERREURS_TRANSPORT_RESEAU`.
  - `rapports.py` : `_handle_network_loss` ne déclenchait un retry que si
    `check_internet()` était faux. Lors d'un reset, l'accès internet répond
    normalement — c'est l'hôte distant qui a fermé la connexion — donc la fonction
    retournait en silence et le rapport était abandonné sans erreur visible.

### Ajouté
- `utils.py` : `is_connection_reset` parcourt la chaîne complète d'une exception
  (`args`, `__cause__`, `__context__`) pour reconnaître un reset, qui n'arrive jamais nu
  — urllib3 l'emballe, puis requests le réemballe.
- `utils.py` : `retry_on_network_error`, pour les appels réseau effectués hors de
  Selenium, où aucune reconnexion n'est câblée.
- `tests/test_utils.py` et `tests/test_rapports_network.py` : couverture des deux
  helpers, du reset doublement emballé, des chaînes `__cause__` et cycliques, et de la
  conversion d'une `ProtocolError` en retry par `telechargement_rapport` — 105 tests.
- `requirements.txt` : `requests` et `urllib3` déclarés explicitement. Ils n'étaient
  que des dépendances transitives (de webdriver-manager et de selenium), mais
  `utils.py` les importe désormais en direct pour `RequestException` et
  `ProtocolError` — rien ne garantissait leur présence si ces deux paquets changeaient
  de pile HTTP.

### Contexte
- Incident du 2026-09-15 à 14:02:12, resté sans diagnostic : un reset pendant le
  téléchargement du driver a tué une exécution complète avant tout téléchargement de
  rapport. Le journal ne contenait que la ligne « Erreur inattendue dans le script
  principal » — aucune trace de tentative de reconnexion, celle-ci n'ayant jamais été
  appelée. Le second essai manuel, à 14:17, a réussi sans changement.

---

## [0.5.22] - 2026-08-20 — ES-34

### Corrigé
- `CHANGELOG.md` : casse des liens de référence harmonisée
  (`releases/tag/v0.x.y` → `releases/tag/V0.x.y`). Les tags du dépôt sont créés en
  `V` majuscule et GitHub est sensible à la casse sur ce segment d'URL : les 24
  liens en minuscule renvoyaient un 404 (vérifié : `v0.5.19` → 404,
  `V0.5.19` → 200).

  **Limite connue** : sur 27 définitions de liens, seules `V0.5.19`, `V0.5.14` et
  `V0.5.3` correspondent à des tags existants. Les 23 autres désignent des versions
  qui n'ont jamais été taguées — dont `0.5.20` et `0.5.21`, dont la publication a
  été abandonnée — et restent sans cible, indépendamment de la casse.

---

## [0.5.21] - 2026-08-18 — ES-34

### Corrigé
- `utils.py` : `cleanup_logs` purge désormais aussi les dumps DOM (`.html`), en plus
  des `.log` et `.png`. Introduits en `0.5.20`, ils échappaient entièrement à
  `log_retention_days`. Un dump est un instantané d'une page Clarity connectée — il
  porte le nom du patient — donc leur accumulation illimitée n'était pas seulement un
  problème d'espace disque.
- `tests/test_utils.py` : accents rétablis dans deux docstrings françaises.
- `README.md` : `--verbose` n'est pas une option CLI de l'application ; c'est
  l'argument transmis à ChromeDriver via `service_args` sous `--debug`. Formulation
  des notes 0.5.20 corrigée (FR et EN).

### Ajouté
- `tests/test_utils.py` : couverture de la purge des `.html` par `cleanup_logs`,
  incluant la garantie que les extensions non gérées ne sont jamais supprimées —
  92 tests.

---

## [0.5.20] - 2026-08-18 — ES-34

### Corrigé
- `GlycoDownload.py` : `ChromeService(log_path=...)` remplacé par `log_output=...`.
  Selenium 4 a retiré le paramètre `log_path` ; il était avalé silencieusement par
  `**kwargs`, sans aucun avertissement. Conséquence : la clé `chromedriver_log` de
  `config.yaml` était inopérante, le journal ChromeDriver n'était jamais écrit et le
  `--verbose` de `service_args` restait sans effet. Le dossier de destination est
  désormais créé avant l'ouverture du journal.

### Ajouté
- `GlycoDownload.py` : sur échec de la saisie des dates, l'URL courante, une capture
  d'écran et un dump du DOM sont enregistrés. Ce chemin d'erreur ne laissait aucune
  trace exploitable, alors que les champs du sélecteur de dates (`start_date` /
  `end_date`) sont fournis par Dexcom et changent sans préavis : sans DOM, impossible
  de distinguer un attribut renommé d'un panneau qui ne s'ouvre pas.
- `utils.py` : `capture_page_source` — enregistre le DOM courant pour le diagnostic.
  Le DOM est lu **avant** l'ouverture du fichier : en mode `"w"`, un échec de lecture
  laisserait un `.html` vide, indiscernable d'une page réellement vide.
- `tests/test_utils.py` : couverture de `capture_page_source` (écriture UTF-8 et
  absence de fichier résiduel quand la lecture du DOM échoue) — 91 tests.

---

## [0.5.19] - 2026-08-15 — CR

### Corrigé
- `Setup/GlycoReport-Downloader.iss` : `AppId` placeholder remplacé par un GUID
  réel — un placeholder séquentiel expose à une collision de clé de
  désinstallation avec un autre projet.

  **Migration** : l'`AppId` est l'identité de l'application pour Windows. Les
  postes installés jusqu'à `0.5.18` ne verront pas cette version comme une mise
  à niveau : une seconde entrée apparaîtra dans « Applications installées » et
  l'ancienne restera orpheline sous la clé
  `A1B2C3D4-E5F6-7890-1234-567890ABCDEF`. Avec `PrivilegesRequired=lowest`, la
  désinstallation manuelle se fait sous `HKCU`.

---

## [0.5.18] - 2026-07-10 — CR

### Corrigé
- `Setup/GlycoReport-Downloader.iss` : `-NoProfile` ajouté aux 3 invocations
  `powershell.exe` (2× `[Icons]` + `[Run]`) — évite de charger le profil
  PowerShell de l'utilisateur (effets de bord, surface d'attaque).

---

## [0.5.17] - 2026-07-10 — CR

### Corrigé
- `utils.py` : message de `attendre_disparition_overlay` corrigé — "Aucun
  overlay/loader détecté" était trompeur pour un `TimeoutException` (qui
  signifie au contraire que l'overlay est resté présent jusqu'à l'échéance) ;
  message reformulé et valeur du timeout ajoutée.

---

## [0.5.16] - 2026-07-10 — ES-28

### Corrigé
- `Setup/GlycoReport-Downloader.iss` : les raccourcis Menu Démarrer et Bureau
  (`[Icons]`) pointaient directement vers `GlycoReport-Downloader.exe` au
  lieu de `Launch-Dexcom-And-Run.ps1` (seule l'entrée `[Run]`
  post-installation le faisait). Alignés sur `powershell.exe` +
  `Launch-Dexcom-And-Run.ps1`, en conservant l'icône de l'exe via
  `IconFilename`. `WorkingDir={app}` ajouté aux 3 entrées (`Icons` + `Run`) :
  absent auparavant, ce qui aurait fait résoudre les chemins relatifs du
  script (`config.yaml`, exécutable) depuis le dossier de `powershell.exe`
  (`System32`) plutôt que le dossier d'installation.

---

## [0.5.15] - 2026-07-10 — ES-28

### Corrigé
- `utils.py` : `attendre_disparition_overlay` loggait le `TimeoutException` en
  `DEBUG` (invisible en usage normal, niveau de log par défaut `INFO`) —
  remplacé par `WARNING` pour rester visible sans activer `--debug`.
  Constat identifié lors de l'audit de code ES-26.

### Note
- `migrate.py` (versionné indépendamment de l'application, toujours en
  1.0.1) n'a subi aucun changement de code. Son exécutable distribué
  (`migrate.exe`) a néanmoins dû être recompilé suite à la mise à jour de
  l'outil de build PyInstaller (6.16.0 → 6.21.0) utilisé pour la
  distribution.

---

## [0.5.14] - 2026-07-09 — CR

### Corrigé
- `rapports.py` : `locale.setlocale(LC_CTYPE, "")` appelé avant `locale.getlocale()` —
  sans cet appel, `getlocale()` retournait `(None, None)` et le suffixe "j" n'était
  jamais détecté en environnement francophone. Limité à `LC_CTYPE` (pas `LC_ALL`)
  et restauration de la locale précédente après lecture, pour éviter tout effet
  de bord sur le formatage des nombres/dates ailleurs dans le processus. Requête
  initiale de la locale courante également protégée (`previous_locale` reste
  `None` si elle échoue, la restauration finale est alors ignorée).
- `rapports.py` (Comparer-Tendances) : `except Exception` remplacé par
  `WebDriverException` (lectures `driver.current_url`) et `ValueError`/`TypeError`
  (parsing URL/date) dans `traitement_rapport_comparer`.

---

## [0.5.13] - 2026-06-25 — ES-27

### Modifié
- Maintenance : `locale.getdefaultlocale()` remplacé par `locale.getlocale()` dans
  `rapports.py` (déprécié depuis Python 3.11).
- Robustesse : conservation de la période sélectionnée après Comparer-Tendances
  (capture de l'URL d'entrée, fallback DATE_DEBUT/DATE_FIN, réapplication avant
  téléchargement).

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

[0.6.7]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.6.7
[0.6.6]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.6.6
[0.6.5]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.6.5
[0.6.4]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.6.4
[0.6.3]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.6.3
[0.6.2]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.6.2
[0.6.1]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.6.1
[0.6.0]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.6.0
[0.5.25]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.25
[0.5.24]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.24
[0.5.23]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.23
[0.5.22]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.22
[0.5.21]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.21
[0.5.20]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.20
[0.5.19]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.19
[0.5.18]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.18
[0.5.17]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.17
[0.5.16]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.16
[0.5.15]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.15
[0.5.14]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.14
[0.5.13]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.13
[0.5.12]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.12
[0.5.11]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.11
[0.5.10]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.10
[0.5.9]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.9
[0.5.8]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.8
[0.5.7]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.7
[0.5.6]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.6
[0.5.5]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.5
[0.5.4]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.4
[0.5.3]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.3
[0.5.2]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.2
[0.5.0]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.5.0
[0.4.0]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.4.0
[0.3.x]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.3.19
[0.2.x]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.2.18
[0.1.x]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.1.7
[0.0.x]: https://github.com/Thebe01/GlycoReport-Downloader/releases/tag/V0.0.23
