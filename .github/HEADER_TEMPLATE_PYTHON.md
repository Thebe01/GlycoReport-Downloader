<!--
META:
    1.1.3 - 2026-11-04 - CR     : Configuration du journal dans le try de main() (point d'entrée et
                                  script autonome) : un échec du FileHandler passe par le
                                  traitement d'erreur documenté.
    1.1.2 - 2026-11-04 - CR     : importlib.metadata.version() prend le nom [project].name, pas celui
                                  du dépôt (sinon PackageNotFoundError) ; il lit la distribution
                                  installée, pas pyproject.toml. Sous-titres de la checklist en
                                  ### (MD036) ; code avec espace final retiré (MD038).
    1.1.1 - 2026-11-04 - CR     : Version initiale 0.0.0 limitée au script autonome (module de paquet :
                                  version du paquet à sa première livraison) ; cli.py importe
                                  __version__ (from . import __version__) sans le redéfinir ;
                                  basicConfig permis dans main() du point d'entrée, interdit au
                                  chargement d'un module (règles et checklist alignées) ; typage
                                  harmonisé à Python 3.10+ (X | None).
    1.1.0 - 2026-11-04 - PD-99  : Deux formes d'en-tête (module de paquet, script autonome PEP 723) ;
                                  version unique du paquet dans pyproject.toml ; Modifications en
                                  ordre descendant, une entrée seulement quand le fichier change ;
                                  champ Modifié le retiré ; platform.node() au lieu de os.uname()
                                  (plantage sous Windows) ; logging configuré au point d'entrée
                                  seulement ; typage 3.9+ (list, dict, X | None) ; ligne coding
                                  retirée ; exemples $ uv run ; liste de vérification ruff, mypy,
                                  pytest ; deux snippets VS Code ; bloc META inversé.
    1.0.6 - 2026-08-15 - CR     : Placeholder de billet ES-000 remplacé par BILLET000 dans l'exemple .MODIFICATIONS de la section 3, pour cohérence avec le reste du document.
    1.0.5 - 2026-04-21 - PD-198 : Harmonisation des exemples Modifications avec la règle du séparateur avant le deux-points.
    1.0.4 - 2026-04-21 - PD-198 : Harmonisation de la règle du séparateur avec le snippet VS Code (espace + padding dynamique).
    1.0.3 - 2026-04-21 - PD-198 : Clarification des règles d'alignement du ticket et du séparateur avant le deux-points.
    1.0.2 - 2026-04-21 - PD-198 : Retrait des crochets autour des numéros de billets; correction de la cohérence exemple/règle de largeur de la colonne ticket.
    1.0.1 - 2026-03-19 - ES-15  : Références mises à jour vers .github/ dans les exemples et le snippet.
    1.0.0 - 2026-01-29 - -      : Version initiale.
-->

# 🐍 Template d'en-tête Python - IPT inc

**Standard officiel pour le code Python**  
Innovations, Performances, Technologies inc.

La structure des dépôts (disposition `src/`, `pyproject.toml`, `uv`, `ruff`, `mypy`, `pytest`)
est décrite dans l'analyse « Structure des applications Python » du 2026-11-04. Ce document
ne couvre que l'en-tête et le code obligatoire d'un fichier.

---

## 🧭 Deux formes d'en-tête

| Forme | Quand | Champ `Version` | Numéro dans `Modifications` |
| --- | --- | --- | --- |
| **Module de paquet** | Fichier d'une application ou d'une bibliothèque (`src/<paquet>/`) | Absent | Version **du paquet** dans laquelle le fichier a changé |
| **Script autonome** | Fichier livré seul, dépendances déclarées en PEP 723 | Présent | Version **du script** |

**Pourquoi :** la version appartient à ce qu'on livre. Un module de paquet n'est jamais livré
seul ; sa version est celle du paquet, déclarée une seule fois dans `pyproject.toml`. Un
script autonome est livré seul, comme un script PowerShell : il porte sa propre version.

---

## 🎯 Module de paquet — Format obligatoire

```python
"""
Format d'en-tête standard à respecter pour ce projet.
Voir .github/HEADER_TEMPLATE_PYTHON.md pour les détails.

Module        : auth.py
Type          : Python module
Auteur        : Pierre Théberge
Compagnie     : Innovations, Performances, Technologies inc.
Créé le       : YYYY-MM-DD
Copyright     : Pierre Théberge

Description
-----------
[Description courte du module ici...]

Modifications
-------------
0.2.0 - YYYY-MM-DD   BILLET000 : Changement le plus récent.
0.1.0 - YYYY-MM-DD   BILLET000 : Initialisation.
"""

import logging

logger = logging.getLogger(__name__)
```

**Règles propres au module de paquet :**

- Pas de shebang, pas de champ `Version`. `__version__` n'est **défini** que dans `__init__.py`
  (plus bas) ; le point d'entrée l'importe (`from . import __version__`) sans le redéfinir.
- Pas de `logging.basicConfig` au chargement d'un module : la configuration du journal se fait
  seulement depuis `main()` du point d'entrée (`cli.py`).
- Sections `Paramètres` et `Exemple` seulement dans le module du point d'entrée (`cli.py`).

---

## 🎯 Script autonome — Format obligatoire

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""
Format d'en-tête standard à respecter pour ce projet.
Voir .github/HEADER_TEMPLATE_PYTHON.md pour les détails.

Module        : mon_script.py
Type          : Python script
Auteur        : Pierre Théberge
Compagnie     : Innovations, Performances, Technologies inc.
Créé le       : YYYY-MM-DD
Version       : 0.1.0
Copyright     : Pierre Théberge

Description
-----------
[Description courte du script ici...]

Modifications
-------------
0.1.0 - YYYY-MM-DD   BILLET000 : Ajout notifications email.
0.0.0 - YYYY-MM-DD   BILLET000 : Initialisation.

Paramètres
----------
--param : str
    Description du paramètre

Exemple
-------
$ uv run mon_script.py --param valeur
"""

import logging
import sys
from datetime import datetime

__version__ = "0.1.0"
__author__ = "Pierre Théberge"
__company__ = "Innovations, Performances, Technologies inc."
__copyright__ = "Pierre Théberge"

logger = logging.getLogger(__name__)

START_TIME = datetime.now()


def main() -> int:
    """Point d'entrée principal."""
    try:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logger.info("Démarrage - Version %s", __version__)
        # Code ici
        return 0
    except Exception:
        logger.exception("Erreur fatale")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

**Règles propres au script autonome :**

- Shebang en ligne 1, puis le bloc PEP 723 (`# /// script` … `# ///`), puis le docstring.
- Le bloc PEP 723 déclare la version de Python et les dépendances ; `uv run` les installe.
- `Version` dans l'en-tête et `__version__` portent la même valeur.

---

## 📋 Sections de l'en-tête

### 1. Bloc de métadonnées

```python
Module        : backup.py
Type          : Python module
Auteur        : Pierre Théberge
Compagnie     : Innovations, Performances, Technologies inc.
Créé le       : 2025-11-06
Copyright     : Pierre Théberge
```

**Règles :**

- Alignement sur `:` (14 espaces après le label)
- Date au format `YYYY-MM-DD`
- `Type` : `Python module` pour un module de paquet, `Python script` pour un script autonome
- `Version` (script autonome seulement) : version sémantique `MAJEUR.MINEUR.CORRECTIF`
- Pas de champ `Modifié le` : c'est la date de la première entrée de `Modifications`

### 2. Section Description

Description **courte** avec liste de fonctionnalités.

```python
Description
-----------
[Description en 1-2 phrases]

Fonctionnalités :
    - Fonctionnalité 1
    - Fonctionnalité 2
```

- Sections séparées par des traits `---` (13 caractères)

### 3. Section Modifications

Historique **du fichier**, lisible sans autre outil.

```python
Modifications
-------------
1.0.0 - 2025-11-15   BILLET000 : Version de production stable.
0.1.1 - 2025-11-09   BILLET000 : Correction encodage UTF-8.
0.1.0 - 2025-11-08   BILLET000 : Ajout paramètre --verbose.
                                 Description sur plusieurs lignes : le texte
                                 des lignes supplémentaires s'aligne sur le
                                 premier caractère de la description.
0.0.0 - 2025-11-06   BILLET000 : Initialisation.
```

**Règles d'ordre :**

- Ordre **descendant** : l'entrée la plus récente en tête du bloc.
- Fichier existant en ordre croissant : on inverse **tout le bloc** au moment où le fichier
  est modifié pour une autre raison, dans le même commit. Jamais de bloc à moitié inversé.
- Aucune correction de masse : un fichier qu'on ne touche pas garde son ordre.

**Règles de contenu :**

- Une entrée **seulement quand le fichier change**. Jamais d'entrée « bump de version ».
- Module de paquet : le numéro est la version **du paquet** dans laquelle le changement est
  livré. Un bump du paquet sans changement du fichier ne touche pas le fichier.
- Script autonome : le numéro est la version **du script**.
- La vue d'ensemble par version du paquet est dans `CHANGELOG.md`, à la racine du dépôt.

**Règles de format :**

- Colonne version : largeur fixe, complétée d'espaces pour aligner le séparateur
  (un espace après `0.0.9` quand `0.0.10` est présent)
- Colonne ticket : largeur fixe selon le billet le plus long du fichier;
  re-padder toutes les entrées si un billet plus long est ajouté
- Séparateur ticket/description : un espace avant `:`; les espaces
  supplémentaires éventuels proviennent uniquement du padding du ticket
- Continuation : indentation égale à la longueur du préfixe entier (version +
  date + ticket + deux-points)
- Utiliser uniquement des espaces (pas de tabulations)

**Règles versioning :**

- Script autonome : la version initiale est **toujours `0.0.0`**, jamais `1.0.0`. La version
  `1.0.0` marque le passage en production stable, pas la création.
- Module de paquet : l'entrée d'initialisation porte la version du paquet dans laquelle le
  fichier est livré pour la première fois (`0.0.0` pour un fichier créé avec le paquet).
- `MAJEUR` : Breaking changes (incompatibilité)
- `MINEUR` : Nouvelles fonctionnalités (compatible)
- `CORRECTIF` : Corrections de bugs uniquement

### 4. Section Paramètres

Documenter **tous** les arguments CLI. Script autonome, ou `cli.py` d'un paquet.

```python
Paramètres
----------
--location : str
    Chemin de destination de la sauvegarde (obligatoire)

--depth : str, optional
    Profondeur des tests ('quick', 'standard', 'deep')
    Défaut: 'deep'

--verbose : flag
    Active le mode verbeux avec logs détaillés
```

### 5. Section Exemple

Au moins **1 exemple** réaliste, préfixé de `$`, lancé par `uv run`.
Ne pas utiliser `>>>` : ce préfixe désigne du code Python que `pytest --doctest-modules`
tenterait d'exécuter.

```python
Exemple
-------
$ uv run backup --location /mnt/backup
Lance une sauvegarde complète vers /mnt/backup

$ uv run backup --location /mnt/backup --verbose
Lance la sauvegarde avec logs détaillés
```

`backup` est le point d'entrée déclaré dans `[project.scripts]` ; pour un script autonome,
`uv run mon_script.py`.

---

## 🔧 Code obligatoire

### 1. Version

**Module de paquet** — dans `__init__.py` seulement, lue dans les métadonnées de la
distribution **installée** :

```python
from importlib.metadata import version

__version__ = version("nom-du-projet")  # = [project].name de pyproject.toml
```

- L'argument est le nom **déclaré dans `[project].name`**, pas le nom du dépôt ni celui du
  paquet. Un autre nom lève `PackageNotFoundError` au chargement de `__init__.py`, et le point
  d'entrée ne démarre plus.
- `version()` ne lit pas `pyproject.toml` : la distribution doit être installée (`uv sync`
  l'installe en mode éditable).

Le point d'entrée (`cli.py`) l'importe sans la redéfinir :

```python
from . import __version__
```

**Script autonome** — après les imports :

```python
__version__ = "0.1.0"
__author__ = "Pierre Théberge"
__company__ = "Innovations, Performances, Technologies inc."
__copyright__ = "Pierre Théberge"
__status__ = "Development"  # "Development", "Production", "Deprecated"
```

### 2. Imports

```python
import argparse
import logging
import platform
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
```

**Ordre des imports** (appliqué par `ruff`) :

1. Bibliothèque standard Python
2. Bibliothèques tierces (séparées par ligne vide)
3. Imports locaux du projet (séparées par ligne vide)

### 3. Journal

Chaque module obtient son journal ; seul le point d'entrée le configure.

```python
# Dans chaque module
logger = logging.getLogger(__name__)
```

```python
# Dans le point d'entrée (cli.py ou script autonome), appelé au début de main()
def configurer_journal() -> None:
    """Configure la sortie du journal : fichier + console."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(
                f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
                encoding="utf-8",
            ),
            logging.StreamHandler(sys.stdout),
        ],
    )
```

**Pourquoi :**

- Un `basicConfig` au chargement d'un module crée un fichier journal à chaque `import`, y
  compris pendant les tests.
- Double sortie : fichier + console ; format horodaté cohérent ; UTF-8 pour les accents.
- Messages par arguments (`logger.info("Version %s", v)`), pas par f-string : le texte n'est
  formaté que si le niveau est actif.

### 4. Constantes globales

```python
COMPUTER_NAME = platform.node()
START_TIME = datetime.now()
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
```

**Règles :**

- Noms en MAJUSCULES avec underscore
- `platform.node()` pour le nom machine : fonctionne sous Windows et Linux
  (`os.uname()` n'existe pas sous Windows)

### 5. Fonction main() (point d'entrée)

```python
def main() -> int:
    """
    Point d'entrée principal.

    Returns:
        int: Code de sortie (0 = succès, 1+ = erreur)
    """
    try:
        # Dans le try : un echec du FileHandler (dossier non inscriptible)
        # passe par le traitement d'erreur ci-dessous.
        configurer_journal()
        logger.info("Démarrage - Version %s", __version__)
        logger.info("Machine: %s", COMPUTER_NAME)

        # Code principal ici

        logger.info("Terminé avec succès - Durée: %s", datetime.now() - START_TIME)
        return 0

    except KeyboardInterrupt:
        logger.warning("Interrompu par l'utilisateur (Ctrl+C)")
        return 130  # Code standard pour SIGINT

    except Exception:
        logger.exception("Erreur fatale")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

- Paquet : `main()` vit dans `cli.py`, qui importe `from . import __version__` (utilisé par
  `main()` et `parse_arguments()`). Le point d'entrée est déclaré dans `pyproject.toml` :
  `[project.scripts]` → `nom = "nom_du_paquet.cli:main"`.
- Script autonome : `main()` vit dans le script.

**Codes de sortie standard :**

- `0` : Succès
- `1` : Erreur générale
- `130` : Interruption par l'utilisateur (Ctrl+C)

---

## 📐 Conventions de code

### Timestamps et dates

```python
# Nom de fichier log
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Log horodaté
log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ISO 8601 complet
iso_time = datetime.now().isoformat()
```

- Fichiers : `YYYY-MM-DD_HH-MM-SS` (underscores)
- Logs : `YYYY-MM-DD HH:MM:SS` (espace et deux-points)

### Parser d'arguments (argparse)

```python
def parse_arguments() -> argparse.Namespace:
    """Parse les arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--location", type=str, required=True,
                        help="Chemin de destination (obligatoire)")
    parser.add_argument("--depth", type=str, choices=["quick", "standard", "deep"],
                        default="deep", help="Profondeur des tests (défaut: 'deep')")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Active le mode verbeux")
    parser.add_argument("--version", action="version",
                        version=f"%(prog)s {__version__}")
    return parser.parse_args()
```

### Type hints (obligatoires, vérifiés par mypy)

Syntaxe Python 3.10+ : types natifs (`list`, `dict`) et `X | None`, jamais `List`, `Dict` ni
`Optional`. `X | None` exige Python 3.10 à l'exécution ; le standard vise Python 3.14
(`requires-python`), donc sans `from __future__ import annotations`.

```python
def calculer_total(montants: list[float], taux: float = 0.15) -> float:
    """
    Calcule le total avec taxes.

    Args:
        montants: Montants avant taxes
        taux: Taux de taxes (défaut: 0.15)

    Returns:
        float: Montant total
    """
    return sum(montants) * (1 + taux)


def lire_config(chemin: Path | None = None) -> dict[str, Any]:
    """Lit la configuration ; chemin par défaut si None."""
    ...
```

### Gestion d'erreurs

```python
try:
    result = operation_risquee(param)

except FileNotFoundError as e:
    logger.error("Fichier introuvable: %s", e)
    return 1

except PermissionError as e:
    logger.error("Permission refusée: %s", e)
    return 1

except Exception:
    logger.exception("Erreur inattendue")
    return 1

finally:
    if temp_file and temp_file.exists():
        temp_file.unlink()
```

---

## ✅ Checklist de validation

Avant de commiter du code Python :

### Les deux formes

- [ ] Docstring d'en-tête avec bloc de métadonnées aligné (14 espaces)
- [ ] Sections séparées par traits `---` (13 caractères)
- [ ] `Modifications` : entrée la plus récente en tête (bloc entier inversé s'il était croissant)
- [ ] `Modifications` : une entrée seulement si le fichier a changé
- [ ] Imports organisés (standard → tiers → local)
- [ ] Type hints en syntaxe 3.10+ ; docstrings sur toutes les fonctions
- [ ] Aucune ligne `# -*- coding: utf-8 -*-`

### Module de paquet

- [ ] Pas de champ `Version` ; `__version__` défini seulement dans `__init__.py` (via
      `importlib.metadata`, avec le nom `[project].name`), importé par `cli.py`
      (`from . import __version__`)
- [ ] `logger = logging.getLogger(__name__)` ; aucun `basicConfig` au chargement ; configuration
      seulement depuis `main()` du point d'entrée (`cli.py`)
- [ ] Version du paquet bumpée dans `pyproject.toml` et entrée ajoutée dans `CHANGELOG.md`

### Script autonome

- [ ] Shebang en ligne 1, bloc PEP 723 avant le docstring
- [ ] `Version` de l'en-tête == `__version__`
- [ ] Sections `Paramètres` et `Exemple` complètes

### Outils (avant PR)

- [ ] `uv run ruff check`
- [ ] `uv run ruff format --check`
- [ ] `uv run mypy src` (ou `uv run mypy mon_script.py`)
- [ ] `uv run pytest`

---

## 📝 Snippets VS Code

Dans VS Code, `headerpy` (module de paquet) ou `headerpyscript` (script autonome) puis `Tab` :

```json
{
  "En-tête Python — module de paquet": {
    "prefix": "headerpy",
    "body": [
      "\"\"\"",
      "Format d'en-tête standard à respecter pour ce projet.",
      "Voir .github/HEADER_TEMPLATE_PYTHON.md pour les détails.",
      "",
      "Module        : ${TM_FILENAME}",
      "Type          : Python module",
      "Auteur        : Pierre Théberge",
      "Compagnie     : Innovations, Performances, Technologies inc.",
      "Créé le       : ${CURRENT_YEAR}-${CURRENT_MONTH}-${CURRENT_DATE}",
      "Copyright     : Pierre Théberge",
      "",
      "Description",
      "-----------",
      "${1:Description courte du module ici...}",
      "",
      "Modifications",
      "-------------",
      "${2:0.0.0} - ${CURRENT_YEAR}-${CURRENT_MONTH}-${CURRENT_DATE}   BILLET000 : Initialisation.",
      "\"\"\"",
      "",
      "import logging",
      "",
      "logger = logging.getLogger(__name__)"
    ]
  },
  "En-tête Python — script autonome": {
    "prefix": "headerpyscript",
    "body": [
      "#!/usr/bin/env python3",
      "# /// script",
      "# requires-python = \">=3.14\"",
      "# dependencies = []",
      "# ///",
      "\"\"\"",
      "Format d'en-tête standard à respecter pour ce projet.",
      "Voir .github/HEADER_TEMPLATE_PYTHON.md pour les détails.",
      "",
      "Module        : ${TM_FILENAME}",
      "Type          : Python script",
      "Auteur        : Pierre Théberge",
      "Compagnie     : Innovations, Performances, Technologies inc.",
      "Créé le       : ${CURRENT_YEAR}-${CURRENT_MONTH}-${CURRENT_DATE}",
      "Version       : ${2:0.0.0}",
      "Copyright     : Pierre Théberge",
      "",
      "Description",
      "-----------",
      "${1:Description courte du script ici...}",
      "",
      "Modifications",
      "-------------",
      "${2:0.0.0} - ${CURRENT_YEAR}-${CURRENT_MONTH}-${CURRENT_DATE}   BILLET000 : Initialisation.",
      "",
      "Paramètres",
      "----------",
      "${3:--param} : ${4:Description du paramètre}",
      "",
      "Exemple",
      "-------",
      "$ uv run ${TM_FILENAME} ${3:--param}",
      "\"\"\""
    ]
  }
}
```

---

## 🔗 Ressources

- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [PEP 621 - Métadonnées de projet dans pyproject.toml](https://peps.python.org/pep-0621/)
- [PEP 723 - Métadonnées de script en ligne](https://peps.python.org/pep-0723/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [Semantic Versioning](https://semver.org/)

---

**Document créé le** : 2025-11-06  
**Version** : 1.1.3  
**Mainteneur** : Pierre Théberge  
**Compagnie** : Innovations, Performances, Technologies inc.
