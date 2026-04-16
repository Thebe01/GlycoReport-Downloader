# Format d'en-tête standard à respecter pour ce projet.
# Voir .github/HEADER_TEMPLATE_POWERSHELL.md pour les détails.

<#
.SYNOPSIS
    Exécute la suite de tests unitaires GlycoReport-Downloader.

.DESCRIPTION
    Nom du fichier : Run-Tests.ps1
    Type           : PowerShell script
    Auteur         : Pierre Théberge
    Compagnie      : Innovations, Performances, Technologies inc.
    Créé le        : 2026-04-14
    Modifié le     : 2026-04-14
    Version        : 0.0.0
    Copyright      : Pierre Théberge

.MODIFICATIONS
    0.0.0 - 2026-04-14 - ES-21 : Version initiale.
    0.0.1 - 2026-04-14 - ES-21 : Sortie detaillee (-v) par defaut; ajout de -Bref pour le mode compact.

.PARAMETER Filtre
    Filtre pytest (-k) pour n'executer qu'un sous-ensemble de tests.
    Ex: -Filtre "network or shutdown"

.PARAMETER Bref
    Mode compact (-q) : affiche uniquement le resume final. Par defaut : sortie detaillee (-v).

.EXAMPLE
    PS> .\Run-Tests.ps1
    PS> .\Run-Tests.ps1 -Bref
    PS> .\Run-Tests.ps1 -Filtre "dates"
    PS> .\Run-Tests.ps1 -Filtre "network or shutdown" -Bref
#>

param(
    [string] $Filtre = "",
    [switch] $Bref
)

$ErrorActionPreference = "Stop"

# --- Resolution de l'environnement virtuel ---
# Le script est dans tests/ — la racine du projet est un niveau au-dessus.
$projectRoot = Split-Path $PSScriptRoot -Parent
$venvPython  = Join-Path $projectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Error "Environnement virtuel introuvable : $venvPython`nCreez-le avec : python -m venv .venv && .venv\Scripts\pip install -r requirements.txt"
    exit 1
}

# --- Construction des arguments pytest ---
$pytestArgs = @("tests/")

if ($Bref) {
    $pytestArgs += "-q"
} else {
    $pytestArgs += "-v"
}

if ($Filtre -ne "") {
    $pytestArgs += "-k"
    $pytestArgs += $Filtre
}

# --- Execution ---
Write-Host ""
Write-Host "=== GlycoReport-Downloader — Tests unitaires ===" -ForegroundColor Cyan
Write-Host "Python : $venvPython" -ForegroundColor DarkGray
Write-Host "Args   : $($pytestArgs -join ' ')" -ForegroundColor DarkGray
Write-Host ""

Set-Location $projectRoot
& $venvPython -m pytest @pytestArgs

$exitCode = $LASTEXITCODE

Write-Host ""
if ($exitCode -eq 0) {
    Write-Host "Tous les tests ont reussi." -ForegroundColor Green
} else {
    Write-Host "Des tests ont echoue (code $exitCode)." -ForegroundColor Red
}

exit $exitCode
