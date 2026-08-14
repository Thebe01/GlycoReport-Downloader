<!--
META:
    1.0.0 - 2026-01-29 - -         : Version initiale.
    1.0.1 - 2026-01-29 - ES-19     : Ajout des variables standard.
    1.0.2 - 2026-03-19 - ES-15     : Références .github/ et ajout de la référence dans l'exemple .DESCRIPTION.
    1.0.3 - 2026-03-20 - ES-15     : Suppression des lignes de consigne dans l'exemple .DESCRIPTION.
    1.0.4 - 2026-04-21 - ES-28     : Correction alignement exemple section 3; règles alignement billet et normalisation longueur version.
    1.0.5 - 2026-06-08 - SUP1-1159 : Ajout convention Début/Fin : afficher le nom et la version du script en
                                     première et dernière ligne d'exécution (checklist + section code obligatoire).
    1.0.6 - 2026-06-08 - SUP1-1159 : Lignes Début/Fin : Write-Output → Write-Host -ForegroundColor Green.
    1.0.7 - 2026-06-08 - SUP1-1159 : $Script:NomScript — valeur dynamique via $PSCommandPath au lieu
                                     d'un nom codé en dur (évite divergence si renommage).
    1.0.8 - 2026-07-03 - OBS-78    : Clarification convention Début/Fin — la ligne Fin doit
                                     précéder toute pause interactive de fermeture (Read-Host,
                                     pause); la mesure de durée porte sur le travail effectif du
                                     script, pas sur l'attente utilisateur.
    1.0.9 - 2026-07-16 - PD-202    : Ajout règle explicite — la version initiale d'un script est
                                     toujours 0.0.0 (jamais 1.0.0). La version 1.0.0 marque le
                                     passage en production stable (checklist + section .MODIFICATIONS).
    1.1.0 - 2026-07-30 - PD-207    : Lignes Début/Fin encadrées d'un try/finally (Fin s'affiche à
                                     chaque point de sortie) ; ajout de la pause interactive finale
                                     (Read-Host) conditionnée à Test-InteractiveSession — volontairement
                                     sans la contrainte ConsoleHost, pour fonctionner aussi dans le
                                     terminal intégré VS Code ; ajout des règles d'encodage fichier
                                     (.ps1 en UTF-8 avec BOM) et console (ASCII pur pour les scripts
                                     serveurs) — recoupe SUP1-1190. Formule reprise telle qu'éprouvée
                                     dans le module IPT.PromptSync (PD-206).
    1.1.1 - 2026-07-31 - PD-206    : Ajout d'un renvoi vers HEADER_TEMPLATE_POWERSHELL_MODULE.md
                                     (variante pour modules .psm1/.psd1) en tête de document et
                                     dans les Ressources.
    1.1.2 - 2026-07-31 - CR        : Reformulation du renvoi vers HEADER_TEMPLATE_POWERSHELL_MODULE.md
                                     — « un module ne s'exécute pas comme un script » pouvait laisser
                                     croire à une contrainte du langage, alors que c'est une convention
                                     de ce standard (un .psm1 exécute bien du code à l'import).
-->

# 📘 Template d'en-tête PowerShell - IPT inc

**Standard officiel pour les scripts PowerShell**  
Innovations, Performances, Technologies inc.

Pour les modules (`.psm1`/`.psd1`), voir [HEADER_TEMPLATE_POWERSHELL_MODULE.md](HEADER_TEMPLATE_POWERSHELL_MODULE.md) — gabarit adapté (différences de ce standard : pas de `param()` au niveau module, pas de lignes Début/Fin).

---

## 🎯 Format obligatoire

```powershell
# Format d'en-tête standard à respecter pour ce projet.
# Voir .github/HEADER_TEMPLATE_POWERSHELL.md pour les détails.

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
    0.0.0 - YYYY-MM-DD - Billet-XXX  : Initialisation.
    0.1.0 - YYYY-MM-DD - -           : Ajout paramètre -Verbose.
    0.1.1 - YYYY-MM-DD - PD-10000001 : Correction encodage UTF-8.
    1.0.0 - YYYY-MM-DD - -           : Version de production stable.

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
    0.0.0 - 2025-11-06 - Billet-XX  : Initialisation.
    0.1.0 - 2025-11-08 - -          : Ajout paramètre -Verbose.
    0.1.1 - 2025-11-09 - PD-100     : Correction encodage UTF-8.
    1.0.0 - 2025-11-15 - -          : Version de production stable.
```

**Règles d'alignement :**

- Le `:` doit être à la même colonne pour toutes les entrées du script.
- Padder le champ billet selon le billet le plus long du script (re-padder
  toutes les entrées si un billet plus long est ajouté).
- Si la longueur du numéro de version change (ex : `0.0.9` → `0.0.10`), ajouter
  un espace après les versions courtes pour normaliser la largeur du champ
  (noter l'espace supplémentaire après `0.0.9`) :

  ```powershell
    0.0.9  - 2025-11-14 - PD-100     : Correction d'un bug.
    0.0.10 - 2025-11-15 - PD-100     : Ajout d'une fonctionnalité.
  ```

**Règles versioning :**

- La version initiale d'un script est **toujours `0.0.0`** (entrée
  `Initialisation` dans `.MODIFICATIONS`), jamais `1.0.0`. La version
  `1.0.0` marque le passage en production stable, pas la création.
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
$Script:NomScript = [System.IO.Path]::GetFileName($PSCommandPath)
$Script:Version   = "0.0.0"
```

**⚠️ IMPORTANT :** Toujours utiliser `InvariantCulture` pour les timestamps !

### 5. Lignes Début / Fin et pause interactive (OBLIGATOIRE)

La **première** ligne d'exécution (après la vérification admin si présente) doit afficher le nom et la version du script, et la **dernière** doit les afficher à nouveau — dans un `try/finally` pour garantir que la ligne `Fin` s'affiche à **chaque** point de sortie (fin normale, erreur, `exit`), pas seulement en fin de script nominale :

```powershell
function Test-InteractiveSession {
    # Session réellement interactive ? Volontairement SANS la contrainte
    # $Host.Name -eq 'ConsoleHost' : la pause doit aussi fonctionner dans le
    # terminal intégré de VS Code (où $Host.Name vaut 'Visual Studio Code Host').
    # try/catch : [Console]::IsInputRedirected peut lever une exception dans un
    # contexte sans handle console (ex. service Windows). Cet appel se fait avant
    # le try/finally d'affichage Debut/Fin plus bas ; sans ce try/catch ici, une
    # telle exception ferait échouer le script avant même la ligne Debut.
    try {
        return [Environment]::UserInteractive -and (-not [Console]::IsInputRedirected)
    }
    catch {
        return $false
    }
}

$Script:IsInteractive = Test-InteractiveSession

try {
    Write-Host "$((Get-Date).ToString('yyyy-MM-dd HH:mm:ss', [System.Globalization.CultureInfo]::InvariantCulture)) Debut $($Script:NomScript) $($Script:Version)" -ForegroundColor Green

    # ... corps du script ...
}
finally {
    Write-Host "$((Get-Date).ToString('yyyy-MM-dd HH:mm:ss', [System.Globalization.CultureInfo]::InvariantCulture)) Fin $($Script:NomScript) $($Script:Version)" -ForegroundColor Green

    if ($Script:IsInteractive) {
        Write-Host ""
        Read-Host "Appuyez sur Entree pour fermer la fenetre"
    }
}
```

**Pourquoi :** Permet d'identifier immédiatement quel script a tourné, quelle version, et d'en mesurer la durée dans les logs — y compris pour les tâches planifiées, où les lignes Début/Fin s'affichent dans tous les cas.

**Pause finale interactive :** la pause (`Read-Host`) est **conditionnée** à `Test-InteractiveSession`, pour qu'un script lancé par une tâche planifiée ne bloque jamais en attente d'une touche. Elle permet à l'usager de voir le résultat avant la fermeture de la fenêtre quand le script est lancé depuis un menu (ex. `Menu-ScriptIPT-locaux.ps1`). Le texte de la pause reste en ASCII pur (voir section « 🔤 Règles d'encodage »).

---

## 🔤 Règles d'encodage

Deux mécanismes distincts, à ne pas confondre (recoupe SUP1-1190) :

1. **Lecture du fichier `.ps1`** dépend du BOM. Sans BOM, PowerShell 5.1 lit le fichier selon la page de code ANSI (CP1252 sur poste fr).
   - Enregistrer tout `.ps1` en **UTF-8 avec BOM**.
   - Aucun caractère non-ASCII dans le **code exécutable** (tirets cadratins, guillemets typographiques, caractères semi-graphiques cassent l'analyse). Les accents dans les **commentaires** sont sans danger, à condition que le BOM soit présent.

2. **Affichage console** dépend de trois couches qui ne se synchronisent PAS automatiquement : `[Console]::OutputEncoding` (encodage .NET), la page de code de la console (`chcp`), et la police (couverture de glyphes). Forcer seulement la première sur un système désaligné aggrave l'affichage.

**Règle d'affichage selon la cible d'exécution** (la distinction est OÙ le script tourne, pas quel langage) :

- **Scripts destinés aux postes usagers** (menu, VS Code, console interactive en UTF-8, où les trois couches sont alignées) : `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8` en tête est permis et recommandé.
- **Scripts destinés aux serveurs** (tâches planifiées, console en page de code OEM 850, police non garantie TrueType) : **ASCII pur** dans toutes les sorties (`Write-Host`, `Write-Output`, logs). Ne **pas** forcer `[Console]::OutputEncoding` : sur un système en 850, cela aggrave l'affichage (un `é` encodé en UTF-8 devient deux glyphes parasites relus en 850).
- Un même script lancé aux deux endroits doit s'en tenir à l'ASCII dans ses sorties.

**Pourquoi :** confusion vécue entre les deux mécanismes — le charabia des accents sur les postes usagers venait de `[Console]::OutputEncoding` en IBM850 sur Server 2019, pas du BOM (soupçonné à tort). Voir SUP1-1190 pour le détail par machine.

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
    Write-Log "Erreur : $($_.Exception.Message)" -Level Error
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
- [ ] Version initiale `0.0.0` (jamais `1.0.0`)
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
- [ ] Ligne `Debut NomScript Version` en première ligne d'exécution
- [ ] Ligne `Fin NomScript Version` dans un `finally` (s'affiche à chaque point de sortie)
- [ ] Pause interactive finale (`Read-Host`) conditionnée à `Test-InteractiveSession` (jamais de blocage en tâche planifiée)
- [ ] `.ps1` enregistré en UTF-8 avec BOM ; ASCII pur dans le code exécutable
- [ ] Sorties console (`Write-Host`, logs) en ASCII pur pour les scripts destinés aux serveurs
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
      "# Voir .github/HEADER_TEMPLATE_POWERSHELL.md pour les détails.",
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

- [HEADER_TEMPLATE_POWERSHELL_MODULE.md](HEADER_TEMPLATE_POWERSHELL_MODULE.md) — variante pour les modules (`.psm1`/`.psd1`)
- [PowerShell Comment-Based Help](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_comment_based_help)
- [PowerShell Best Practices](https://docs.microsoft.com/en-us/powershell/scripting/developer/cmdlet/strongly-encouraged-development-guidelines)
- [Semantic Versioning](https://semver.org/)

---

**Document créé le** : 2025-11-06  
**Version** : 1.1.2  
**Mainteneur** : Pierre Théberge  
**Compagnie** : Innovations, Performances, Technologies inc.
