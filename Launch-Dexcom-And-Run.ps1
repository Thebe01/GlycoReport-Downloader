# Format d'en-tête standard à respecter pour ce projet.
# Voir .github/HEADER_TEMPLATE_POWERSHELL.md pour les détails.

<#
.SYNOPSIS
    Ouvre Chrome sur Dexcom Clarity puis lance GlycoReport-Downloader.

.DESCRIPTION
    Nom du fichier : Launch-Dexcom-And-Run.ps1
    Type           : PowerShell script
    Auteur         : Pierre Théberge
    Compagnie      : Innovations, Performances, Technologies inc.
    Créé le        : 2026-01-29
    Modifié le     : 2026-04-13
    Version        : 0.1.2
    Copyright      : Pierre Théberge

.MODIFICATIONS
    0.0.0 - 2026-01-29 - ES-19 : Version initiale.
    0.0.1 - 2026-02-02 - ES-19 : Normalisation du chemin du profil Chrome.
    0.0.2 - 2026-02-02 - ES-19 : Recherche de l'exécutable dans dist si absent.
    0.0.3 - 2026-02-02 - ES-19 : Fermeture de Chrome avant Selenium (profil partagé).
    0.0.4 - 2026-02-02 - ES-19 : Attache Selenium à Chrome (remote debugging).
    0.0.5 - 2026-03-26 - ES-20 : Mise en conformité de l'en-tête au format standard.
    0.1.0 - 2026-03-26 - ES-20 : Exposition de tous les paramètres GlycoDownload (debug, dry-run,
                                  days, date_debut, date_fin, rapports, list-rapports, attach-debugger,
                                  start-at-date-selection).
    0.1.1 - 2026-03-26 - ES-20 : Remplacement de -Debug par -GlycoDebug (conflit avec paramètre commun
                                  PowerShell -Debug), tout en conservant la transmission vers --debug.
    0.1.2 - 2026-04-13 - ES-20 : -StartAtDateSelection et -AttachDebugger rendus conditionnels via
                                  $PSBoundParameters; actifs par défaut, désactivables explicitement
                                  via -StartAtDateSelection:$false / -AttachDebugger:$false.

.PARAMETER ChromePath
    Chemin vers l'exécutable Chrome (par défaut: chrome.exe).

.PARAMETER ConfigPath
    Chemin du fichier config.yaml (par défaut: .\config.yaml).

.PARAMETER DebuggerPort
    Port de débogage distant Chrome (par défaut: 9222). Transmis à --debugger-port.

.PARAMETER GlycoDebug
    Active le mode debug de GlycoDownload (logs détaillés, captures d'écran). Transmis à --debug.

.PARAMETER DryRun
    Simule l'exécution sans télécharger. Transmis à --dry-run.

.PARAMETER StartAtDateSelection
    Démarre directement à la sélection des dates (connexion déjà effectuée). Transmis à --start-at-date-selection.
    Actif par défaut; désactivable via -StartAtDateSelection:$false.

.PARAMETER AttachDebugger
    Attache Selenium à un Chrome déjà lancé. Transmis à --attach-debugger.
    Actif par défaut; désactivable via -AttachDebugger:$false.

.PARAMETER Days
    Nombre de jours à inclure (7, 14, 30 ou 90). Transmis à --days.

.PARAMETER DateDebut
    Date de début au format AAAA-MM-JJ. Transmis à --date_debut.

.PARAMETER DateFin
    Date de fin au format AAAA-MM-JJ. Transmis à --date_fin.

.PARAMETER Rapports
    Liste des rapports à télécharger (ex: "Aperçu", "AGP"). Transmis à --rapports.

.PARAMETER ListRapports
    Affiche la liste des rapports disponibles et quitte. Transmis à --list-rapports.

.EXAMPLE
    PS> .\Launch-Dexcom-And-Run.ps1

.EXAMPLE
    PS> .\Launch-Dexcom-And-Run.ps1 -Days 30 -GlycoDebug

.EXAMPLE
    PS> .\Launch-Dexcom-And-Run.ps1 -DateDebut 2026-01-01 -DateFin 2026-01-31 -Rapports "Aperçu","AGP"
#>

[CmdletBinding()]
param(
    [Parameter()]
    [ValidateNotNullOrEmpty()]
    [string]$ChromePath = "chrome.exe",

    [Parameter()]
    [ValidateNotNullOrEmpty()]
    [string]$ConfigPath = ".\config.yaml",

    [Parameter()]
    [ValidateRange(1024, 65535)]
    [int]$DebuggerPort = 9222,

    [Parameter()]
    [switch]$GlycoDebug,

    [Parameter()]
    [switch]$DryRun,

    [Parameter()]
    [switch]$StartAtDateSelection,

    [Parameter()]
    [switch]$AttachDebugger,

    [Parameter()]
    [ValidateSet(7, 14, 30, 90)]
    [int]$Days,

    [Parameter()]
    [ValidatePattern('^\d{4}-\d{2}-\d{2}$')]
    [string]$DateDebut,

    [Parameter()]
    [ValidatePattern('^\d{4}-\d{2}-\d{2}$')]
    [string]$DateFin,

    [Parameter()]
    [string[]]$Rapports,

    [Parameter()]
    [switch]$ListRapports
)

#Requires -Version 5.1

# === Configuration stricte ===
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

# === Variables globales ===
$Script:ComputerName = $env:COMPUTERNAME
$Script:TimeStamp = (Get-Date).ToString("yyyy-MM-dd_HH-mm-ss", [System.Globalization.CultureInfo]::InvariantCulture)
$Script:StartTime = Get-Date

function Get-YamlValue {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Path,

        [Parameter(Mandatory)]
        [string]$Key
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        throw "config.yaml introuvable: $Path"
    }

    $pattern = "^\s*$Key\s*:\s*"
    $line = Get-Content -LiteralPath $Path | Select-String -Pattern $pattern | Select-Object -First 1
    if (-not $line) {
        return $null
    }

    $value = $line.Line -replace "^\s*$Key\s*:\s*", ""
    return $value.Trim('"', "'")
}

function ConvertTo-AbsolutePath {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Path
    )

    $value = $Path.Trim('"', "'")
    if ($value -match '^\s*~') {
        $value = $value -replace '^\s*~', $HOME
    }

    $value = [Environment]::ExpandEnvironmentVariables($value)
    if (-not [System.IO.Path]::IsPathRooted($value)) {
        $value = Join-Path -Path (Get-Location) -ChildPath $value
    }

    return [System.IO.Path]::GetFullPath($value)
}

function Get-ExecutablePath {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$BaseDir
    )

    $candidates = @(
        (Join-Path -Path $BaseDir -ChildPath "GlycoReport-Downloader.exe"),
        (Join-Path -Path $BaseDir -ChildPath "dist\GlycoReport-Downloader.exe")
    )

    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate) {
            return $candidate
        }
    }

    return $null
}

try {
    $ConfigPath = ConvertTo-AbsolutePath -Path $ConfigPath
    $chromeUserDataDir = Get-YamlValue -Path $ConfigPath -Key "chrome_user_data_dir"
    if (-not $chromeUserDataDir) {
        throw "La clé 'chrome_user_data_dir' est absente de $ConfigPath."
    }
    $chromeUserDataDir = ConvertTo-AbsolutePath -Path $chromeUserDataDir
    if (-not (Test-Path -LiteralPath $chromeUserDataDir)) {
        New-Item -ItemType Directory -Path $chromeUserDataDir -Force | Out-Null
    }

    $dexcomUrl = Get-YamlValue -Path $ConfigPath -Key "dexcom_url"
    if (-not $dexcomUrl) {
        $dexcomUrl = "https://clarity.dexcom.eu"
    }

    Write-Host "Ouverture de Chrome avec le profil Selenium..." -ForegroundColor Cyan
    Start-Process -FilePath $ChromePath -ArgumentList @(
        "--user-data-dir=$chromeUserDataDir",
        "--remote-debugging-port=$DebuggerPort",
        $dexcomUrl
    )

    Write-Host "Connectez-vous dans Chrome, terminez la vérification Cloudflare si nécessaire." -ForegroundColor Yellow
    Read-Host "Appuyez sur Entrée pour lancer GlycoReport-Downloader"

    $baseDir = Get-Location
    $exePath = Get-ExecutablePath -BaseDir $baseDir
    if (-not $exePath) {
        throw "Exécutable introuvable. Recherché dans: $($baseDir.Path) et $($baseDir.Path)\dist"
    }

    Write-Host "Lancement de GlycoReport-Downloader..." -ForegroundColor Cyan

    # Construction dynamique des arguments transmis à GlycoDownload
    $glycoArgs = [System.Collections.Generic.List[string]]::new()

    # Comportement par défaut : actifs si non passés explicitement.
    # Désactivables via -StartAtDateSelection:$false / -AttachDebugger:$false.
    $shouldStartAtDateSelection = if ($PSBoundParameters.ContainsKey('StartAtDateSelection')) {
        [bool]$StartAtDateSelection
    }
    else {
        $true
    }
    $shouldAttachDebugger = if ($PSBoundParameters.ContainsKey('AttachDebugger')) {
        [bool]$AttachDebugger
    }
    else {
        $true
    }
    if ($shouldStartAtDateSelection) { $glycoArgs.Add("--start-at-date-selection") }
    if ($shouldAttachDebugger) { $glycoArgs.Add("--attach-debugger") }
    $glycoArgs.Add("--debugger-port")
    $glycoArgs.Add($DebuggerPort.ToString())
    if ($GlycoDebug) { $glycoArgs.Add("--debug") }
    if ($DryRun) { $glycoArgs.Add("--dry-run") }
    if ($ListRapports) { $glycoArgs.Add("--list-rapports") }
    if ($Days -gt 0) { $glycoArgs.Add("--days"); $glycoArgs.Add($Days.ToString()) }
    if ($DateDebut) { $glycoArgs.Add("--date_debut"); $glycoArgs.Add($DateDebut) }
    if ($DateFin) { $glycoArgs.Add("--date_fin"); $glycoArgs.Add($DateFin) }
    if ($Rapports) { $glycoArgs.Add("--rapports"); $Rapports | ForEach-Object { $glycoArgs.Add($_) } }

    Start-Process -FilePath $exePath -WorkingDirectory (Get-Location) -ArgumentList $glycoArgs
}
catch {
    Write-Error $_.Exception.Message
    exit 1
}
