#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Format d'en-tête standard à respecter pour ce projet.
Voir .github/HEADER_TEMPLATE_PYTHON.md pour les détails.

Module        : version.py
Type          : Python module
Auteur        : Pierre Théberge
Compagnie     : Innovations, Performances, Technologies inc.
Créé le       : 2025-08-22
Modifié le    : 2026-08-15
Version       : 0.5.19
Copyright     : Pierre Théberge

Description
-----------
Source unique de vérité pour la version de l'application.

Modifications
-------------
0.2.15 - 2026-01-19   [ES-19] : Synchronisation de version (aucun changement fonctionnel).
0.2.16 - 2026-01-20   [ES-19] : Bump de version patch (release 0.2.16).
0.2.17 - 2026-01-20   [ES-19] : Bump de version patch (release 0.2.17).
0.2.18 - 2026-01-20   [ES-19] : Bump de version patch (release 0.2.18).
0.3.0  - 2026-01-29   [ES-19] : Bump de version minor (release 0.3.0).
0.3.1  - 2026-02-02   [ES-19] : Bump de version patch (release 0.3.1).
0.3.2  - 2026-02-02   [ES-19] : Bump de version patch (release 0.3.2).
0.3.3  - 2026-02-02   [ES-19] : Bump de version patch (release 0.3.3).
0.3.4  - 2026-02-12   [ES-3]  : Bump de version patch (release 0.3.4).
0.3.5  - 2026-02-12   [ES-3]  : Bump de version patch (release 0.3.5).
0.3.6  - 2026-02-12   [ES-3]  : Bump de version patch (release 0.3.6).
0.3.7  - 2026-02-12   [ES-3]  : Attente contenu graphique + délai génération PDF Comparer.
0.3.8  - 2026-02-12   [ES-3]  : Fermeture/réouverture modale Comparer entre sous-rapports.
0.3.9  - 2026-02-12   [ES-3]  : Navigation /overview et /reports avec dates pour Comparer.
0.3.10 - 2026-02-12   [ES-3]  : Retry clics Comparer et navigation overview->reports.
0.3.11 - 2026-02-12   [ES-3]  : Navigation URL base /i pour Comparer.
0.3.12 - 2026-02-12   [ES-3]  : Acces direct /compare/overlay et /compare/daily.
0.3.13 - 2026-02-12   [ES-3]  : Comparer: telecharger Tendances seulement (bug Dexcom).
0.3.14 - 2026-02-13   [ES-11] : Ajout suffixe de periode dans les noms de fichiers.
0.3.15 - 2026-02-26   [ES-6]  : Bump de version patch et harmonisation XPath independants de la langue.
0.3.16 - 2026-03-19   [ES-15] : Bump de version patch, retention des logs par defaut a 30 jours et synchronisation documentation.
0.3.17 - 2026-03-23   [ES-14] : Bump de version patch et robustesse reseau pendant le traitement des rapports
                                (reconnexion automatique ou arret propre en cas d'echec).
                                Fermeture de l'onglet en fin de traitement et fermeture complete du navigateur
                                si un seul onglet est ouvert.
0.3.18 - 2026-03-25   [ES-14] : Bump de version patch et durcissement de la gestion des pertes reseau
                                dans le flux Export CSV (modale + fermeture).
0.3.19 - 2026-03-25   [ES-14] : Bump de version patch et cohérence du mode debug effectif
                                lors de la fermeture de session navigateur.
                                Durcissement du retry réseau dans selection_rapport
                                (max 2 retries puis NetworkRecoveryFailedError explicite).
0.4.0  - 2026-04-14   [ES-20] : Bump de version minor. Exposition de tous les paramètres CLI
                                dans Launch-Dexcom-And-Run.ps1; correction de -StartAtDateSelection
                                et -AttachDebugger (actifs par défaut, désactivables explicitement).
0.5.0  - 2026-04-14   [ES-21] : Bump de version minor. Ajout du paramètre days dans config.yaml.
                                Chaîne de priorité : CLI dates > CLI --days > config days > config dates.
                                Extraction de resolve_effective_date_range (fonction pure testable).
0.5.1  - 2026-04-15   [ES-22] : Synchronisation de version (aucun changement fonctionnel).
0.5.2  - 2026-04-15   [ES-25] : Saisie des dates : erreur fatale si Selenium echoue (plus de
                                continuite silencieuse avec les dates par defaut de Dexcom).
0.5.3  - 2026-04-15   [ES-25] : Robustesse saisie des dates : element_to_be_clickable, clic + clear
                                + send_keys par champ sequentiellement.
0.5.4  - 2026-04-15   [CR]    : Validation de 'days' dans config.yaml (type, valeurs autorisees,
                                avertissement si conflit avec date_debut/date_fin).
0.5.5  - 2026-04-15   [CR]    : Dates CLI partielles refusees explicitement (validate_dates +
                                garde defensif dans resolve_effective_date_range).
0.5.6  - 2026-04-16   [ES-25] : Deconnexion : JS fallback sur logout_link +
                                seconde attente overlay apres menu utilisateur.
0.5.7  - 2026-04-17   [ES-25] : Fermeture modale Export : xpath_fermer ancre dans
                                <export-dialog> (conditions data-test obsoletes supprimees) ;
                                attente explicite de disparition du composant apres clic Fermer.
0.5.8  - 2026-04-17   [ES-25] : Deconnexion : narrowing except Exception ->
                                ElementClickInterceptedException sur clics menu et logout.
0.5.9  - 2026-04-17   [ES-25] : Fermeture modale Export : EC.invisibility_of_element_located
                                remplace par until_not(presence_of_element_located) pour
                                garantir le retrait du DOM (et non seulement l'invisibilite).
0.5.10 - 2026-04-17   [ES-26] : Structure dépôt : ajout CHANGELOG.md,
                                requirements-dev.txt (pytest/pyinstaller séparés de
                                requirements.txt); CLAUDE.md local uniquement (.gitignore).
                                Couverture de tests : ajout de test_config_validation.py,
                                test_rapports_period.py et TestValidateDates dans
                                test_glycodownload_dates.py (81 tests).
0.5.11 - 2026-04-21   [ES-28] : Sécurité : subprocess.Popen(shell=True) remplacé par
                                Popen(["powershell.exe"], creationflags=CREATE_NEW_CONSOLE)
                                dans config.py — élimine le risque d'injection shell.
0.5.12 - 2026-04-21   [ES-28] : Robustesse : remplacement de tous les except Exception par
                                des exceptions spécifiques (TimeoutException,
                                ElementClickInterceptedException, WebDriverException,
                                StaleElementReferenceException, OSError, URLError,
                                InvalidToken, ValueError, etc.) dans les 4 modules.
0.5.13 - 2026-06-11   [ES-27] : rapports.py : locale.getdefaultlocale() remplacé par
                                locale.getlocale() (déprécié depuis Python 3.11).
0.5.13 - 2026-06-25   [ES-27] : Conservation de la période sélectionnée après Comparer-Tendances :
                                capture de l'URL d'entrée, fallback DATE_DEBUT/DATE_FIN,
                                double vérification avant téléchargement, retour page d'origine.
0.5.14 - 2026-07-09   [CR]    : rapports.py : locale.setlocale(LC_CTYPE, "") appelé avant
                                locale.getlocale() — sans cet appel, getlocale() retournait
                                (None, None) et le suffixe "j" n'était jamais détecté en
                                environnement francophone. Limité à LC_CTYPE (pas LC_ALL) et
                                restauration de la locale précédente après lecture pour éviter
                                tout effet de bord sur le formatage des nombres/dates ailleurs
                                dans le processus. Requête initiale de la locale courante
                                également protégée par locale.Error (previous_locale reste
                                None si elle échoue, la restauration finale est alors ignorée).
0.5.14 - 2026-07-09   [CR]    : rapports.py : Comparer-Tendances : except Exception remplacé
                                par WebDriverException (lectures driver.current_url) et
                                ValueError/TypeError (parsing URL/date) dans
                                traitement_rapport_comparer.
0.5.15 - 2026-07-10   [ES-28] : utils.py : attendre_disparition_overlay : logger.debug remplacé
                                par logger.warning pour le TimeoutException — invisible en
                                usage normal (niveau de log par défaut INFO) avec logger.debug.
0.5.16 - 2026-07-10   [ES-28] : Setup/GlycoReport-Downloader.iss : raccourcis Menu Démarrer et
                                Bureau ([Icons]) pointaient directement vers
                                GlycoReport-Downloader.exe au lieu de Launch-Dexcom-And-Run.ps1
                                (seul le [Run] post-installation le faisait). Alignés sur
                                powershell.exe + Launch-Dexcom-And-Run.ps1 (IconFilename
                                conservé sur l'exe pour l'icône affichée). WorkingDir={app}
                                ajouté sur les 3 entrées (Icons + Run) — absent auparavant,
                                le répertoire de travail par défaut de Inno Setup pour un
                                Filename=powershell.exe est le dossier de powershell.exe
                                (System32), pas {app}, ce qui aurait empêché le script de
                                trouver config.yaml et l'exécutable via ses chemins relatifs.
0.5.17 - 2026-07-10   [CR]    : utils.py : attendre_disparition_overlay : message du
                                logger.warning corrigé — "Aucun overlay/loader détecté" était
                                trompeur pour un TimeoutException (qui signifie au contraire
                                que l'overlay est resté présent jusqu'à l'échéance) ; message
                                + valeur du timeout.
0.5.18 - 2026-07-10   [CR]    : Setup/GlycoReport-Downloader.iss : -NoProfile ajouté aux 3
                                invocations powershell.exe (2x [Icons] + [Run]) — évite de
                                charger le profil PowerShell de l'utilisateur (effets de bord,
                                surface d'attaque) pour un lancement applicatif déterministe.
0.5.19 - 2026-08-15   [CR]    : Setup/GlycoReport-Downloader.iss : AppId placeholder remplacé
                                par un GUID réel (valeur dans le .iss, source unique de vérité)
                                — un placeholder séquentiel expose à une collision de clé de
                                désinstallation avec un autre projet. L'AppId étant l'identité
                                de l'application pour Windows, les postes installés jusqu'à
                                0.5.18 ne verront pas celle-ci comme une mise à niveau ; leur
                                entrée orpheline se retrouve sous la clé de désinstallation
                                A1B2C3D4-E5F6-7890-1234-567890ABCDEF.

Paramètres
----------
N/A.

Exemple
-------
>>> from version import __version__
>>> print(__version__)
"""

__version__ = "0.5.19"