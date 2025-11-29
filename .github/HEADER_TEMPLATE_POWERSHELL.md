# 📘 Template d'en-tête PowerShell - IPT inc.

**Standard officiel pour les scripts PowerShell**  
Innovations, Performances, Technologies inc.

---

## 🎯 Format obligatoire

```powershell
# Format d'en-tête standard à respecter pour ce projet.
# Voir HEADER_TEMPLATE_POWERSHELL.md pour les détails.
<#
.SYNOPSIS
    [Description courte du script en une ligne]

.DESCRIPTION
    Nom du fichier : NomDuScript.ps1
    Type           : PowerShell script
    Auteur         : Pierre Théberge
    Compagnie      : Innovations, Performances, Technologies inc.
    Créé le        : YYYY-MM-DD
    Modifié le     : YYYY-MM-DD
    Version        : 0.0.0
    Copyright      : Pierre Théberge

.MODIFICATIONS
    0.0.0 - YYYY-MM-DD - Billet-XX : Initialisation.

.PARAMETER Paramètre
    Description du paramètre

.EXAMPLE
    PS> .\NomDuScript.ps1 -Paramètre Valeur

.NOTES
    Prérequis : [liste des prérequis]

.LINK
    Documentation : [lien]
#>

[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory, HelpMessage = "Description")]
    [ValidateNotNullOrEmpty()]
    [string]$Paramètre
)

#Requires -Version 5.1

# === Configuration stricte ===
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

# === Variables globales ===
$Script:ComputerName = $env:COMPUTERNAME
$Script:TimeStamp = (Get-Date).ToString("yyyy-MM-dd_HH-mm-ss", [System.Globalization.CultureInfo]::InvariantCulture)
$Script:StartTime = Get-Date
```

---

## 📋 Sections obligatoires

### 1. `.SYNOPSIS`

Description **courte** (1 ligne) du script.

**Exemple :**

```powershell
.SYNOPSIS
    Sauvegarde complète Windows vers support NTFS local
```

### 2. `.DESCRIPTION`

Bloc de métadonnées **structuré** et **aligné** :

```powershell
.DESCRIPTION
    Nom du fichier : Sauvegarde-Windows.ps1
    Type           : PowerShell script
    Auteur         : Pierre Théberge
    Compagnie      : Innovations, Performances, Technologies inc.
    Créé le        : 2025-11-06
    Modifié le     : 2025-11-06
    Version        : 1.0.0
    Copyright      : Pierre Théberge
```

**Règles :**

- Alignement sur `:` (15 espaces après le label)
- Date au format `YYYY-MM-DD`
- Version sémantique `MAJEUR.MINEUR.CORRECTIF`

### 3. `.MODIFICATIONS`

Changelog **complet** avec chaque version documentée.

**Format :**

```powershell
.MODIFICATIONS
    0.0.0 - 2025-11-06 : Initialisation.
    0.1.0 - 2025-11-08 : Ajout paramètre -Verbose.
    0.1.1 - 2025-11-09 : Correction encodage UTF-8.
    1.0.0 - 2025-11-15 : Version de production stable.
```

**Règles versioning :**

- `MAJEUR` : Breaking changes (incompatibilité)
- `MINEUR` : Nouvelles fonctionnalités (compatible)
- `CORRECTIF` : Corrections de bugs uniquement

### 4. `.PARAMETER`

Documenter **tous** les paramètres avec description claire.

**Format :**

```powershell
.PARAMETER BackupLocation
    Chemin vers le support de sauvegarde (ex: E:, \\serveur\share)

.PARAMETER TestDepth
    Niveau de profondeur des tests : 'Quick', 'Standard', 'Deep'
    - Quick : Vérification basique
    - Standard : + métadonnées
    - Deep : + validation complète
```

### 5. `.EXAMPLE`

Au moins **1 exemple** réaliste. Préfixe `PS>` obligatoire.

**Format :**

```powershell
.EXAMPLE
    PS> .\Sauvegarde-Windows.ps1 -BackupLocation "E:"
    Lance une sauvegarde complète sur le lecteur E:

.EXAMPLE
    PS> .\Sauvegarde-Windows.ps1 -BackupLocation "E:" -Silent
    Lance la sauvegarde en mode silencieux
```

### 6. `.NOTES` (optionnel mais recommandé)

Prérequis, contraintes, avertissements.

**Format :**

```powershell
.NOTES
    Prérequis :
    - Exécution en tant qu'administrateur
    - Windows Server Backup installé
    - Support NTFS obligatoire
    - Windows 10/11 ou Windows Server 2019+
```

### 7. `.LINK` (optionnel)

Liens vers documentation.

**Format :**

```powershell
.LINK
    https://docs.microsoft.com/windows-server/administration/windows-commands/wbadmin

.LINK
    Documentation interne : https://intranet.ipt.local/docs
```

---

## 🔧 Code obligatoire après l'en-tête

### 1. Déclaration des paramètres

```powershell
[CmdletBinding(SupportsShouldProcess)]  # Si modification système
param(
    [Parameter(Mandatory, HelpMessage = "Description claire")]
    [ValidateNotNullOrEmpty()]
    [string]$Paramètre1,

    [Parameter(HelpMessage = "Description paramètre optionnel")]
    [ValidateSet('Option1', 'Option2', 'Option3')]
    [string]$Paramètre2 = 'Option1',

    [Parameter(HelpMessage = "Active une fonctionnalité")]
    [switch]$EnableFeature
)
```

**Règles :**

- `[CmdletBinding()]` obligatoire si paramètres
- `SupportsShouldProcess` si le script modifie le système (support
  `-WhatIf`/`-Confirm`)
- `HelpMessage` pour chaque paramètre
- Validation appropriée (`ValidateNotNullOrEmpty`, `ValidateSet`,
  `ValidateRange`, etc.)

### 2. Prérequis PowerShell

```powershell
#Requires -Version 5.1
#Requires -RunAsAdministrator  # Si nécessaire
#Requires -Modules ModuleName   # Si nécessaire
```

### 3. Configuration stricte (OBLIGATOIRE)

```powershell
# === Configuration stricte ===
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
```

**Pourquoi :**

- `Stop` : Arrête le script à la première erreur
- `StrictMode` : Détecte les erreurs de syntaxe cachées

### 4. Variables globales standard

```powershell
# === Variables globales ===
$Script:ComputerName = $env:COMPUTERNAME
$Script:TimeStamp = (Get-Date).ToString("yyyy-MM-dd_HH-mm-ss", [System.Globalization.CultureInfo]::InvariantCulture)
$Script:StartTime = Get-Date
```

**⚠️ IMPORTANT :** Toujours utiliser `InvariantCulture` pour les timestamps !

---

## 📐 Conventions de code

### Timestamps et dates

**✅ BON :**

```powershell
# Nom de fichier log
$timestamp = (Get-Date).ToString("yyyy-MM-dd_HH-mm-ss", [System.Globalization.CultureInfo]::InvariantCulture)

# Log horodaté
$logTime = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss", [System.Globalization.CultureInfo]::InvariantCulture)
```

**❌ MAUVAIS :**

```powershell
# Ne fonctionne pas sur toutes les locales !
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
```

### Fonction de logging standard

```powershell
function Write-Log {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory, Position = 0)]
        [AllowEmptyString()]
        [string]$Message,

        [Parameter()]
        [ValidateSet('Info', 'Warning', 'Error', 'Success', 'Header')]
        [string]$Level = 'Info'
    )

    $Stamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss", [System.Globalization.CultureInfo]::InvariantCulture)
    $LogMessage = "$Stamp [$Level] $Message"

    $LogMessage | Out-File -FilePath $Script:LogFile -Append -Encoding utf8

    if (-not [string]::IsNullOrWhiteSpace($Message)) {
        $Color = switch ($Level) {
            'Warning' { 'Yellow' }
            'Error' { 'Red' }
            'Success' { 'Green' }
            'Header' { 'Cyan' }
            default { 'White' }
        }
        Write-Host $Message -ForegroundColor $Color
    }
}
```

### Gestion d'erreurs

```powershell
try {
    # Code risqué
    $result = Invoke-Something -Path $Path
}
catch {
    Write-Log "❌ Erreur : $($_.Exception.Message)" -Level Error
    Write-Log "   Ligne : $($_.InvocationInfo.ScriptLineNumber)" -Level Error
    exit 1
}
finally {
    # Nettoyage (optionnel)
    Remove-Item $tempFile -ErrorAction SilentlyContinue
}
```

---

## ✅ Checklist de validation

Avant de commiter un script PowerShell :

- [ ] En-tête complet avec toutes les sections obligatoires
- [ ] `.SYNOPSIS` clair et concis (1 ligne)
- [ ] `.DESCRIPTION` avec métadonnées alignées
- [ ] `.MODIFICATIONS` à jour avec dernière version
- [ ] `.PARAMETER` pour tous les paramètres
- [ ] `.EXAMPLE` avec au moins 1 cas d'usage réel
- [ ] `[CmdletBinding()]` présent si paramètres
- [ ] `SupportsShouldProcess` si modification système
- [ ] `#Requires -Version 5.1` spécifié
- [ ] `$ErrorActionPreference = 'Stop'` activé
- [ ] `Set-StrictMode -Version Latest` activé
- [ ] Timestamps utilisent `InvariantCulture`
- [ ] Variables globales avec préfixe `$Script:`
- [ ] Fonction `Write-Log` pour logging
- [ ] Gestion d'erreurs avec try/catch
- [ ] Code testé et fonctionnel

---

## 📝 Snippet VS Code

Dans VS Code, tapez `headerps` puis `Tab` :

```json
{
  "Bloc d'en-tête PowerShell": {
    "prefix": "headerps",
    "body": [
      "# Format d'en-tête standard à respecter pour ce projet.",
      "# Voir HEADER_TEMPLATE_POWERSHELL.md pour les détails.",
      "",
      "<#",
      ".SYNOPSIS",
      "${1:Description courte du script ici...}",
      "",
      ".DESCRIPTION",
      "Nom du fichier : ${TM_FILENAME}",
      "Type           : PowerShell script",
      "Auteur         : Pierre Théberge",
      "Compagnie      : Innovations, Performances, Technologies inc.",
      "Créé le        : ${CURRENT_YEAR}-${CURRENT_MONTH}-${CURRENT_DATE}",
      "Modifié le     : ${2:${CURRENT_YEAR}-${CURRENT_MONTH}-${CURRENT_DATE}}",
      "Version        : ${3:0.0.0}",
      "Copyright      : Pierre Théberge",
      "",
      ".MODIFICATIONS",
      "${3:0.0.0} - ${CURRENT_YEAR}-${CURRENT_MONTH}-${CURRENT_DATE} - Billet-XX : Initialisation.",
      "",
      ".PARAMETER",
      "${4:Paramètre} - ${5:Description du paramètre}",
      "",
      ".EXAMPLE",
      "PS> .\\${TM_FILENAME} ${4:Paramètre}",
      "#>"
    ]
  }
}
```

---

## 🔗 Ressources

- [PowerShell Comment-Based Help](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_comment_based_help)
- [PowerShell Best Practices](https://docs.microsoft.com/en-us/powershell/scripting/developer/cmdlet/strongly-encouraged-development-guidelines)
- [Semantic Versioning](https://semver.org/)

---

**Document créé le** : 2025-11-06  
**Version** : 1.0.0  
**Mainteneur** : Pierre Théberge  
**Compagnie** : Innovations, Performances, Technologies inc.
