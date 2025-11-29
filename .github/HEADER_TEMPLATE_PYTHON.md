# 🐍 Template d'en-tête Python - IPT inc.

**Standard officiel pour les scripts Python**  
Innovations, Performances, Technologies inc.

---

## 🎯 Format obligatoire

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Format d'en-tête standard à respecter pour ce projet.
Voir HEADER_TEMPLATE_PYTHON.md pour les détails.

Module        : mon_script.py
Type          : Python module
Auteur        : Pierre Théberge
Compagnie     : Innovations, Performances, Technologies inc.
Créé le       : YYYY-MM-DD
Modifié le    : YYYY-MM-DD
Version       : 0.0.0
Copyright     : Pierre Théberge

Description
-----------
[Description courte du module ici...]

Modifications
-------------
0.0.0 - YYYY-MM-DD   [BILLET000] : Initialisation.
0.1.0 - YYYY-MM-DD   [BILLET000] : Ajout notifications email.
1.0.0 - YYYY-MM-DD   [BILLET000] : Version de production stable.

Paramètres
----------
param : Description du paramètre

Exemple
-------
>>> python mon_script.py --param valeur
"""

__version__ = "0.0.0"
__author__ = "Pierre Théberge"
__company__ = "Innovations, Performances, Technologies inc."
__copyright__ = "Pierre Théberge"

import sys
import logging
from datetime import datetime

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

START_TIME = datetime.now()


def main() -> int:
    """Point d'entrée principal."""
    try:
        logger.info(f"Démarrage - Version {__version__}")
        # Code ici
        return 0
    except Exception as e:
        logger.error(f"Erreur: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

---

## 📋 Sections obligatoires

### 1. Shebang et encoding (OBLIGATOIRE)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
```

**Pourquoi :**

- `#!/usr/bin/env python3` : Compatibilité Unix/Linux
- `# -*- coding: utf-8 -*-` : Support des caractères accentués

### 2. Docstring module

Docstring complet avec sections **structurées** et **séparées** :

```python
"""
Format d'en-tête standard à respecter pour ce projet.
Voir HEADER_TEMPLATE_PYTHON.md pour les détails.

Module        : backup_script.py
Type          : Python module
Auteur        : Pierre Théberge
Compagnie     : Innovations, Performances, Technologies inc.
Créé le       : 2025-11-06
Modifié le    : 2025-11-06
Version       : 1.0.0
Copyright     : Pierre Théberge

Description
-----------
Script de sauvegarde automatisée avec validation d'intégrité.

Fonctionnalités :
    - Sauvegarde incrémentielle
    - Vérification d'intégrité
    - Notifications par email

Modifications
-------------
0.0.0 - 2025-11-06   [BILLET000] : Initialisation.
0.1.0 - 2025-11-08   [BILLET000] : Ajout notifications email.
1.0.0 - 2025-11-15   [BILLET000] : Version de production stable.

Paramètres
----------
--location : Chemin de destination de la sauvegarde
--verbose : Active le mode verbeux

Exemple
-------
>>> python backup_script.py --location /mnt/backup
Lance une sauvegarde complète vers /mnt/backup

>>> python backup_script.py --location /mnt/backup --verbose
Lance la sauvegarde avec logs détaillés
"""
```

**Règles :**

- Alignement sur `:` (14 espaces après le label)
- Sections séparées par des traits `---` (13 caractères)
- Date au format `YYYY-MM-DD`
- Version sémantique `MAJEUR.MINEUR.CORRECTIF`

### 3. Section Description

Description **courte** avec liste de fonctionnalités.

**Format :**

```python
Description
-----------
[Description en 1-2 phrases]

Fonctionnalités :
    - Fonctionnalité 1
    - Fonctionnalité 2
    - Fonctionnalité 3
```

### 4. Section Modifications

Changelog **complet** avec chaque version documentée.

**Format :**

```python
Modifications
-------------
0.0.0 - 2025-11-06   [BILLET000] : Initialisation.
0.1.0 - 2025-11-08   [BILLET000] : Ajout paramètre --verbose.
0.1.1 - 2025-11-09   [BILLET000] : Correction encodage UTF-8.
1.0.0 - 2025-11-15   [BILLET000] : Version de production stable.
```

**Règles versioning :**

- `MAJEUR` : Breaking changes (incompatibilité)
- `MINEUR` : Nouvelles fonctionnalités (compatible)
- `CORRECTIF` : Corrections de bugs uniquement

### 5. Section Paramètres

Documenter **tous** les arguments CLI.

**Format :**

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

### 6. Section Exemple

Au moins **1 exemple** réaliste avec préfixe `>>>`.

**Format :**

```python
Exemple
-------
>>> python backup_script.py --location /mnt/backup
Lance une sauvegarde complète vers /mnt/backup

>>> python backup_script.py --location /mnt/backup --depth quick
Lance une validation rapide de la sauvegarde

>>> python backup_script.py --location /mnt/backup --verbose
Lance la sauvegarde avec logs détaillés
```

---

## 🔧 Code obligatoire après le docstring

### 1. Variables de métadonnées (OBLIGATOIRE)

```python
__version__ = "0.0.0"
__author__ = "Pierre Théberge"
__company__ = "Innovations, Performances, Technologies inc."
__copyright__ = "Pierre Théberge"
__status__ = "Development"  # "Development", "Production", "Deprecated"
```

**Règles :**

- Version sémantique entre guillemets
- `__status__` : "Development", "Production", ou "Deprecated"

### 2. Imports standards

```python
import sys
import os
import logging
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
```

**Ordre des imports :**

1. Bibliothèque standard Python
2. Bibliothèques tierces (séparées par ligne vide)
3. Imports locaux du projet (séparées par ligne vide)

### 3. Configuration logging (OBLIGATOIRE)

```python
# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(
            f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
            encoding='utf-8'
        ),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)
```

**Pourquoi :**

- Double sortie : fichier + console
- Format horodaté cohérent
- Encodage UTF-8 pour caractères accentués

### 4. Constantes globales

```python
# Constantes globales
COMPUTER_NAME = os.environ.get('COMPUTERNAME', os.uname().nodename)
START_TIME = datetime.now()
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
```

**Règles :**

- Noms en MAJUSCULES avec underscore
- Valeurs par défaut sensées
- Compatibilité Windows/Linux pour nom machine

### 5. Fonction main() (OBLIGATOIRE)

```python
def main() -> int:
    """
    Point d'entrée principal du script.

    Returns:
        int: Code de sortie (0 = succès, 1+ = erreur)

    Raises:
        KeyboardInterrupt: Si interrompu par l'utilisateur
        Exception: Toute autre erreur fatale
    """
    try:
        logger.info(f"Démarrage - Version {__version__}")
        logger.info(f"Machine: {COMPUTER_NAME}")

        # Code principal ici

        duration = datetime.now() - START_TIME
        logger.info(f"Terminé avec succès - Durée: {duration}")
        return 0

    except KeyboardInterrupt:
        logger.warning("Script interrompu par l'utilisateur (Ctrl+C)")
        return 130  # Code standard pour SIGINT

    except Exception as e:
        logger.error(f"Erreur fatale: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

**Codes de sortie standard :**

- `0` : Succès
- `1` : Erreur générale
- `130` : Interruption par l'utilisateur (Ctrl+C)

---

## 📐 Conventions de code

### Timestamps et dates

**✅ BON :**

```python
# Nom de fichier log
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Log horodaté
log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# ISO 8601 complet
iso_time = datetime.now().isoformat()
```

**Format recommandé :**

- Fichiers : `YYYY-MM-DD_HH-MM-SS` (underscores)
- Logs : `YYYY-MM-DD HH:MM:SS` (espace et deux-points)

### Parser d'arguments (argparse)

```python
def parse_arguments() -> argparse.Namespace:
    """
    Parse les arguments de la ligne de commande.

    Returns:
        argparse.Namespace: Arguments parsés
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--location',
        type=str,
        required=True,
        help='Chemin de destination (obligatoire)'
    )

    parser.add_argument(
        '--depth',
        type=str,
        choices=['quick', 'standard', 'deep'],
        default='deep',
        help="Profondeur des tests (défaut: 'deep')"
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Active le mode verbeux'
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )

    return parser.parse_args()
```

### Type hints (fortement recommandé)

```python
def calculer_total(montants: List[float], tva: float = 0.20) -> float:
    """
    Calcule le total avec TVA.

    Args:
        montants: Liste des montants HT
        tva: Taux de TVA (défaut: 0.20 = 20%)

    Returns:
        float: Montant total TTC
    """
    total_ht = sum(montants)
    return total_ht * (1 + tva)
```

### Gestion d'erreurs

```python
try:
    # Code risqué
    result = operation_risquee(param)

except FileNotFoundError as e:
    logger.error(f"Fichier introuvable: {e}")
    return 1

except PermissionError as e:
    logger.error(f"Permission refusée: {e}")
    return 1

except Exception as e:
    logger.error(f"Erreur inattendue: {e}", exc_info=True)
    return 1

finally:
    # Nettoyage (optionnel)
    if temp_file and temp_file.exists():
        temp_file.unlink()
```

---

## ✅ Checklist de validation

Avant de commiter un script Python :

- [ ] Shebang `#!/usr/bin/env python3` en ligne 1
- [ ] Encoding `# -*- coding: utf-8 -*-` en ligne 2
- [ ] Docstring complet avec toutes les sections
- [ ] Sections séparées par traits `---` (13 caractères)
- [ ] Métadonnées alignées (14 espaces)
- [ ] Section Modifications à jour avec dernière version
- [ ] Section Paramètres documente tous les arguments
- [ ] Section Exemple avec au moins 1 cas d'usage réel
- [ ] Variables `__version__`, `__author__`, `__company__`, `__copyright__`
      définies
- [ ] Imports organisés (standard → tiers → local)
- [ ] Logging configuré avec fichier + console
- [ ] Fonction `main() -> int` avec gestion d'erreurs
- [ ] `if __name__ == "__main__":` présent
- [ ] Type hints sur les fonctions
- [ ] Docstrings sur toutes les fonctions
- [ ] Code testé et fonctionnel

---

## 📝 Snippet VS Code

Dans VS Code, tapez `headerpy` puis `Tab` :

```json
{
  "Bloc d'en-tête Python": {
    "prefix": "headerpy",
    "body": [
      "\"\"\"",
      "Format d'en-tête standard à respecter pour ce projet.",
      "Voir HEADER_TEMPLATE_PYTHON.md pour les détails.",
      "",
      "Module        : ${TM_FILENAME}",
      "Type          : Python module",
      "Auteur        : Pierre Théberge",
      "Compagnie     : Innovations, Performances, Technologies inc.",
      "Créé le       : ${CURRENT_YEAR}-${CURRENT_MONTH}-${CURRENT_DATE}",
      "Modifié le    : ${2:${CURRENT_YEAR}-${CURRENT_MONTH}-${CURRENT_DATE}}",
      "Version       : ${3:0.0.0}",
      "Copyright     : Pierre Théberge",
      "",
      "Description",
      "-------------",
      "${1:Description courte du module ici...}",
      "",
      "Modifications",
      "--------------",
      "${3:0.0.0} - ${CURRENT_YEAR}-${CURRENT_MONTH}-${CURRENT_DATE}   [BILLET000] : Initialisation.",
      "",
      "Paramètres",
      "-----------",
      "${4:param} : ${5:Description du paramètre}",
      "",
      "Exemple",
      "-------",
      ">>> python ${TM_FILENAME} ${4:param}",
      "\"\"\""
    ]
  }
}
```

---

## 🔗 Ressources

- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [Python Type Hints (PEP 484)](https://peps.python.org/pep-0484/)
- [Semantic Versioning](https://semver.org/)

---

**Document créé le** : 2025-11-06  
**Version** : 1.0.0  
**Mainteneur** : Pierre Théberge  
**Compagnie** : Innovations, Performances, Technologies inc.
