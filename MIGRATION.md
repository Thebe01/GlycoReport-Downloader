# Guide de Migration - GlycoReport-Downloader

An English version of this text follows the French text.

---

## Sommaire (Français)

- [Description](#description)
- [Migration vers la version 0.2.4](#migration-vers-la-version-024)
  - [Changements de la version 0.2.4](#changements-de-la-version-024)
  - [Ce que fait le script](#ce-que-fait-le-script)
- [Utilisation](#utilisation)
- [Sécurité](#sécurité)
- [Exemple d'exécution](#exemple-dexécution)
- [Restauration en cas de problème](#restauration-en-cas-de-problème)
- [Questions fréquentes](#questions-fréquentes)
- [Support](#support)
- [Migration Guide (English)](#migration-guide-english)

---

## Description

Le script `migrate.py` permet de migrer automatiquement votre installation
existante de GlycoReport-Downloader vers la dernière version.

## Migration vers la version 0.2.4

### Changements de la version 0.2.4

Depuis la version 0.2.3, GlycoReport-Downloader utilise **ChromeDriverManager**
qui télécharge et gère automatiquement la version appropriée de ChromeDriver.
Cela rend obsolètes :

- Le paramètre `chromedriver_path` dans `config.yaml`
- Le répertoire `chromedriver-win64/` (~10 MB)

### Ce que fait le script

1. **Nettoie config.yaml**

   - Supprime le paramètre obsolète `chromedriver_path`
   - Crée un backup automatique avant modification

2. **Propose de supprimer chromedriver-win64/**
   - Demande confirmation avant suppression
   - Affiche la taille du répertoire
   - Libère environ 10 MB d'espace disque

## Utilisation

### Option 1 : Avec l'exécutable Windows (recommandé)

Si vous utilisez la distribution officielle, un exécutable est inclus :

**Windows :**

```powershell
.\migrate.exe
```

### Option 2 : Exécution directe avec Python

**Bash/CMD :**

```bash
python migrate.py
```

**PowerShell :**

```powershell
python migrate.py
```

### Option 3 : Depuis votre environnement virtuel

**PowerShell :**

```powershell
# Activer l'environnement virtuel
.\.venv\Scripts\Activate.ps1

# Exécuter le script
python migrate.py
```

**Bash :**

```bash
# Activer l'environnement virtuel (Linux/Mac)
source .venv/bin/activate

# Exécuter le script
python migrate.py
```

## Sécurité

- ✅ **Backups automatiques** : Le script crée un backup de `config.yaml` avant
  modification
- ✅ **Confirmation requise** : La suppression du répertoire nécessite votre
  confirmation
- ✅ **Messages colorés** : Utilise des couleurs pour faciliter la lecture
- ✅ **Réversible** : Les backups permettent de restaurer l'état précédent si
  nécessaire

## Exemple d'exécution

```text
=============================================================
  Migration vers GlycoReport-Downloader v0.2.4
=============================================================

ℹ Ce script va :
ℹ   1. Supprimer le paramètre obsolète 'chromedriver_path' de config.yaml
ℹ   2. Proposer de supprimer le répertoire 'chromedriver-win64'

ℹ Des backups seront créés avant toute modification.

Appuyez sur Entrée pour continuer...

=============================================================
ℹ ÉTAPE 1 : Nettoyage du fichier config.yaml
=============================================================
ℹ Le paramètre 'chromedriver_path' a été trouvé : ./chromedriver-win64/chromedriver.exe
✓ Backup créé : config.yaml.backup_20251016_143022
✓ Le paramètre 'chromedriver_path' a été supprimé de config.yaml

=============================================================
ℹ ÉTAPE 2 : Suppression du répertoire chromedriver-win64
=============================================================
ℹ Répertoire trouvé : C:\Users\...\chromedriver-win64
ℹ Taille : 10.45 MB

⚠️  ATTENTION ⚠️
⚠ Le répertoire 'chromedriver-win64' n'est plus nécessaire depuis la version 0.2.3.
⚠ ChromeDriverManager télécharge automatiquement la version appropriée de ChromeDriver.
⚠
⚠ Si vous utilisez ce répertoire pour d'autres applications, répondez 'non'.

ℹ Voulez-vous supprimer le répertoire chromedriver-win64 ? (oui/non) : oui
✓ Le répertoire chromedriver-win64 a été supprimé.
ℹ Espace libéré : ~10.45 MB

=============================================================
ℹ RÉSUMÉ DE LA MIGRATION
=============================================================
✓ config.yaml : Paramètre 'chromedriver_path' supprimé
✓ chromedriver-win64 : Répertoire supprimé

=============================================================
✓ Migration terminée !
=============================================================

ℹ Prochaines étapes :
ℹ   - ChromeDriverManager téléchargera automatiquement ChromeDriver au premier lancement
ℹ   - Aucune configuration supplémentaire n'est nécessaire
ℹ   - Vous pouvez lancer GlycoReport-Downloader normalement

Merci d'utiliser GlycoReport-Downloader !
```

## Restauration en cas de problème

Si vous souhaitez restaurer votre configuration précédente :

**Bash/CMD :**

```bash
# Restaurer config.yaml depuis le backup
copy config.yaml.backup_YYYYMMDD_HHMMSS config.yaml
```

**PowerShell :**

```powershell
# Restaurer config.yaml depuis le backup
Copy-Item config.yaml.backup_YYYYMMDD_HHMMSS config.yaml
```

## Questions fréquentes

### Dois-je exécuter ce script ?

- **OUI**, si vous migrez depuis une version < 0.2.3
- **NON**, si c'est une nouvelle installation de la version 0.2.4

### Que se passe-t-il si je conserve chromedriver-win64 ?

- L'application fonctionnera normalement
- Le répertoire occupera ~10 MB inutilement
- Vous pourrez le supprimer manuellement plus tard

### Puis-je annuler la migration ?

- Les modifications de `config.yaml` peuvent être restaurées depuis le backup
- La suppression du répertoire `chromedriver-win64/` n'est pas réversible (mais
  le répertoire n'est plus nécessaire)

## Support

Pour toute question ou problème, ouvrez une issue sur GitHub :
<https://github.com/Thebe01/GlycoReport-Downloader/issues>

---

---

# Migration Guide (English)

## Table of Contents (English)

- [Description (English)](#description-english)
- [Migration to Version 0.2.4](#migration-to-version-024)
  - [Version 0.2.4 Changes](#version-024-changes)
  - [What the Script Does](#what-the-script-does)
- [Usage](#usage-english)
- [Security](#security-english)
- [Execution Example](#execution-example)
- [Restore in Case of Problems](#restore-in-case-of-problems)
- [Frequently Asked Questions](#frequently-asked-questions)
- [Support (English)](#support-english)

---

## Description (English)

The `migrate.py` script allows you to automatically migrate your existing
GlycoReport-Downloader installation to the latest version.

## Migration to Version 0.2.4

### Version 0.2.4 Changes

Since version 0.2.3, GlycoReport-Downloader uses **ChromeDriverManager** which
automatically downloads and manages the appropriate version of ChromeDriver.
This makes the following obsolete:

- The `chromedriver_path` parameter in `config.yaml`
- The `chromedriver-win64/` directory (~10 MB)

### What the Script Does

1. **Cleans up config.yaml**

   - Removes the obsolete `chromedriver_path` parameter
   - Creates an automatic backup before modification

2. **Offers to delete chromedriver-win64/**
   - Requests confirmation before deletion
   - Displays the directory size
   - Frees up approximately 10 MB of disk space

## Usage (English)

### Option 1: With Windows Executable (recommended)

If you are using the official distribution, an executable is included:

**Windows:**

```powershell
.\migrate.exe
```

### Option 2: Direct Execution with Python

**Bash/CMD:**

```bash
python migrate.py
```

**PowerShell:**

```powershell
python migrate.py
```

### Option 3: From Your Virtual Environment

**PowerShell:**

```powershell
# Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# Run the script
python migrate.py
```

**Bash:**

```bash
# Activate the virtual environment (Linux/Mac)
source .venv/bin/activate

# Run the script
python migrate.py
```

## Security (English)

- ✅ **Automatic Backups**: The script creates a backup of `config.yaml` before
  modification
- ✅ **Confirmation Required**: Directory deletion requires your confirmation
- ✅ **Colored Messages**: Uses colors for easier reading
- ✅ **Reversible**: Backups allow restoring the previous state if necessary

## Execution Example

```text
=============================================================
  Migration to GlycoReport-Downloader v0.2.4
=============================================================

ℹ This script will:
ℹ   1. Remove the obsolete 'chromedriver_path' parameter from config.yaml
ℹ   2. Offer to delete the 'chromedriver-win64' directory

ℹ Backups will be created before any modification.

Press Enter to continue...

=============================================================
ℹ STEP 1: Cleaning up config.yaml file
=============================================================
ℹ The 'chromedriver_path' parameter was found: ./chromedriver-win64/chromedriver.exe
✓ Backup created: config.yaml.backup_20251016_143022
✓ The 'chromedriver_path' parameter has been removed from config.yaml

=============================================================
ℹ STEP 2: Deleting chromedriver-win64 directory
=============================================================
ℹ Directory found: C:\Users\...\chromedriver-win64
ℹ Size: 10.45 MB

⚠️  WARNING ⚠️
⚠ The 'chromedriver-win64' directory is no longer needed since version 0.2.3.
⚠ ChromeDriverManager automatically downloads the appropriate version of ChromeDriver.
⚠
⚠ If you use this directory for other applications, answer 'no'.

ℹ Do you want to delete the chromedriver-win64 directory? (yes/no): yes
✓ The chromedriver-win64 directory has been deleted.
ℹ Space freed: ~10.45 MB

=============================================================
ℹ MIGRATION SUMMARY
=============================================================
✓ config.yaml: 'chromedriver_path' parameter removed
✓ chromedriver-win64: Directory deleted

=============================================================
✓ Migration completed!
=============================================================

ℹ Next steps:
ℹ   - ChromeDriverManager will automatically download ChromeDriver on first launch
ℹ   - No additional configuration is required
ℹ   - You can run GlycoReport-Downloader normally

Thank you for using GlycoReport-Downloader!
```

## Restore in Case of Problems

If you want to restore your previous configuration:

**Bash/CMD:**

```bash
# Restore config.yaml from backup
copy config.yaml.backup_YYYYMMDD_HHMMSS config.yaml
```

**PowerShell:**

```powershell
# Restore config.yaml from backup
Copy-Item config.yaml.backup_YYYYMMDD_HHMMSS config.yaml
```

## Frequently Asked Questions

### Should I run this script?

- **YES**, if you are migrating from a version < 0.2.3
- **NO**, if this is a new installation of version 0.2.4

### What happens if I keep chromedriver-win64?

- The application will work normally
- The directory will occupy ~10 MB unnecessarily
- You can delete it manually later

### Can I undo the migration?

- Changes to `config.yaml` can be restored from the backup
- Deletion of the `chromedriver-win64/` directory is not reversible (but the
  directory is no longer needed)

## Support (English)

For any questions or issues, open an issue on GitHub:
<https://github.com/Thebe01/GlycoReport-Downloader/issues>
