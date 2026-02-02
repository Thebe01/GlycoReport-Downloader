# Format d'en-tête standard à respecter pour ce projet.
# Voir HEADER_TEMPLATE_POWERSHELL.md pour les détails.
<#
.SYNOPSIS
    Ouvre Chrome sur Dexcom Clarity puis lance GlycoReport-Downloader.

.DESCRIPTION
    Nom du fichier : Launch-Dexcom-And-Run.ps1
    Type           : PowerShell script
    Auteur         : Pierre Théberge
    Compagnie      : Innovations, Performances, Technologies inc.
    Créé le        : 2026-01-29
    Modifié le     : 2026-02-02
    Version        : 0.0.4
    Copyright      : Pierre Théberge

.MODIFICATIONS
    0.0.0 - 2026-01-29 - ES-19 : Version initiale.
    0.0.1 - 2026-02-02 - ES-19 : Normalisation du chemin du profil Chrome.
    0.0.2 - 2026-02-02 - ES-19 : Recherche de l'exécutable dans dist si absent.
    0.0.3 - 2026-02-02 - ES-19 : Fermeture de Chrome avant Selenium (profil partagé).
    0.0.4 - 2026-02-02 - ES-19 : Attache Selenium à Chrome (remote debugging).

.PARAMETER ChromePath
    Chemin vers l'exécutable Chrome (par défaut: chrome.exe).

.PARAMETER ConfigPath
    Chemin du fichier config.yaml (par défaut: .\config.yaml).

.EXAMPLE
    PS> .\Launch-Dexcom-And-Run.ps1
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
    [int]$DebuggerPort = 9222
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
    Start-Process -FilePath $exePath -WorkingDirectory (Get-Location) -ArgumentList @(
        "--start-at-date-selection",
        "--attach-debugger",
        "--debugger-port",
        $DebuggerPort
    )
}
catch {
    Write-Error $_.Exception.Message
    exit 1
}
