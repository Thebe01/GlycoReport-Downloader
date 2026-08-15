# Format d'en-tête standard à respecter pour ce projet.
# Voir .github/HEADER_TEMPLATE_POWERSHELL.md pour les détails.

<#
.SYNOPSIS
    Génère les exécutables et crée l'installateur Inno Setup pour GlycoReport-Downloader.

.DESCRIPTION
    Nom du fichier : DIST-GlycoReport-Downloader.ps1
    Type           : PowerShell script
    Auteur         : Pierre Théberge
    Compagnie      : Innovations, Performances, Technologies inc.
    Créé le        : 2025-09-03
    Modifié le     : 2026-07-10
    Version        : 2.0.10
    Copyright      : Pierre Théberge

.MODIFICATIONS
    1.0.0  - 2025-09-03 - -     : Version initiale (ZIP).
    2.0.0  - 2025-12-21 - ES-18 : Passage à Inno Setup pour la distribution.
    2.0.1  - 2025-12-22 - ES-18 : Correction du chemin d'installation par défaut ({sd}\ipt).
    2.0.2  - 2025-12-22 - ES-18 : Correction variable inutilisée $appName.
                                  Correction warning architecture Inno Setup (x64compatible).
    2.0.3  - 2025-12-22 - ES-3  : Synchronisation de version.
    2.0.4  - 2026-01-29 - ES-19 : Ajout du script Launch-Dexcom-And-Run.ps1 dans la distribution.
    2.0.5  - 2026-03-26 - ES-20 : Mise en conformité de l'en-tête au format standard.
    2.0.6  - 2026-07-09 - ES-27 : Set-Location $PSScriptRoot (chemins relatifs fiables peu importe
                                  le répertoire courant d'appel). Vérification $LASTEXITCODE et
                                  fraîcheur des .exe générés après chaque appel PyInstaller (évite
                                  d'empaqueter un exécutable verrouillé/obsolète en cas d'échec
                                  silencieux). Vérification que la substitution de version dans
                                  le .iss a réellement eu lieu.
    2.0.7  - 2026-07-09 - ES-27 : Set-Content -NoNewline lors de la mise à jour du .iss — Get-Content
                                  -Raw capture déjà le retour à la ligne final du fichier, donc
                                  Set-Content sans -NoNewline en ajoutait un second à chaque
                                  exécution (ligne vide accumulée à chaque build).
    2.0.8  - 2026-07-09 - CR    : Lecture/écriture du .iss via [System.IO.File]::ReadAllText/
                                  WriteAllText (UTF-8 sans BOM explicite) au lieu de Get-Content/
                                  Set-Content — l'encodage par défaut de ces cmdlets n'est pas le
                                  même entre Windows PowerShell 5.1 et PowerShell 7+, ce qui pouvait
                                  corrompre les caractères accentués ou ajouter un BOM inattendu.
    2.0.9  - 2026-07-09 - CR    : Message d'erreur de substitution de version corrigé pour référencer
                                  $issFilePath (chemin absolu réellement lu/écrit) au lieu de
                                  $issFile (chemin relatif), pour faciliter le diagnostic si le
                                  script est invoqué depuis un autre répertoire.
    2.0.10 - 2026-07-10 - ES-28 : Correction d'un faux positif : la vérification de fraîcheur par
                                  date de modification (2.0.6) signalait à tort un .exe verrouillé
                                  quand PyInstaller sautait légitimement la régénération via son
                                  cache de build (script source inchangé, ex. migrate.py). Cette
                                  vérification de fraîcheur est retirée : la date de modification
                                  d'un .exe non reconstruit ne doit pas être perturbée (validé
                                  empiriquement — un rebuild sans changement laisse le fichier
                                  intact). Seul le code de sortie de PyInstaller ($LASTEXITCODE)
                                  est désormais vérifié pour détecter un échec de build.

.EXAMPLE
    PS> .\DIST-GlycoReport-Downloader.ps1
#>

$ErrorActionPreference = "Stop"

# Se placer dans le dossier du script : garantit la résolution correcte de tous les
# chemins relatifs ci-dessous, peu importe le répertoire courant depuis lequel le
# script est invoqué.
Set-Location -Path $PSScriptRoot

# --- Configuration ---
$appName = "GlycoReport-Downloader"
$versionFile = "version.py"
$issFile = "Setup\${appName}.iss"
$distDir = "dist"
$setupOutputDir = "dist_setup"

# Détection de l'interpréteur Python (venv ou global)
$venvPython = ".\.venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    $pythonCmd = (Resolve-Path $venvPython).Path
    Write-Host "Utilisation de l'environnement virtuel : $pythonCmd"
}
else {
    $pythonCmd = "python"
    Write-Host "Utilisation de l'interpréteur Python global"
}

# --- 1. Trouver Inno Setup Compiler (ISCC.exe) ---
Write-Host "Recherche de Inno Setup Compiler..."
$possiblePaths = @(
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
    "C:\Program Files\Inno Setup 6\ISCC.exe",
    "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe"
)

$isccPath = $null
foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        $isccPath = $path
        break
    }
}

if (-not $isccPath) {
    Write-Error "Inno Setup Compiler (ISCC.exe) introuvable. Veuillez installer Inno Setup 6."
    exit 1
}
Write-Host "Inno Setup trouvé : $isccPath"

# --- 2. Extraire la version ---
Write-Host "Lecture de la version..."
if (Test-Path $versionFile) {
    $versionContent = Get-Content $versionFile -Raw
    if ($versionContent -match '__version__\s*=\s*"([^"]+)"') {
        $version = $matches[1]
        Write-Host "Version détectée : $version"
    }
    else {
        Write-Error "Impossible de trouver la version dans $versionFile"
        exit 1
    }
}
else {
    Write-Error "$versionFile introuvable."
    exit 1
}

# --- 3. Mettre à jour le fichier .iss avec la version ---
Write-Host "Mise à jour du fichier .iss..."
# Lecture/écriture via les API .NET (et non Get-Content/Set-Content) : l'encodage UTF-8
# sans BOM du .iss (caractères accentués) doit être préservé de façon identique sous
# Windows PowerShell 5.1 et PowerShell 7+, dont les encodages par défaut divergent
# (Get-Content/Set-Content sans -Encoding ne sont pas déterministes entre les deux).
$issFilePath = Join-Path $PSScriptRoot $issFile
$issContent = [System.IO.File]::ReadAllText($issFilePath, [System.Text.Encoding]::UTF8)
# Remplacement de la ligne #define MyAppVersion "..."
# Utilisation d'une regex qui préserve les commentaires éventuels en fin de ligne
$newIssContent = $issContent -replace '(?m)^#define MyAppVersion "[^"]+"', "#define MyAppVersion ""$version"""
if ($newIssContent -notmatch [regex]::Escape("#define MyAppVersion ""$version""")) {
    Write-Error "Échec de la mise à jour de la version dans $issFilePath : le motif '#define MyAppVersion `"...`"' n'a pas été trouvé ou remplacé."
    exit 1
}
[System.IO.File]::WriteAllText($issFilePath, $newIssContent, [System.Text.UTF8Encoding]::new($false))
Write-Host "Fichier .iss mis à jour avec la version $version"

# --- 4. Générer les exécutables avec PyInstaller ---

# Vérifie qu'un appel PyInstaller s'est terminé correctement. On ne vérifie ni la
# suppression préalable ni la fraîcheur (date de modification) du .exe généré : quand
# le script source n'a pas changé depuis le dernier build, PyInstaller saute
# légitimement la régénération via son cache (build/<nom>/*.toc) et laisse le .exe
# existant intact, avec sa date de modification d'origine — c'est le comportement
# attendu et il ne faut pas le perturber (ni le signaler comme une erreur). Un vrai
# échec de build (dont un .exe verrouillé par une instance en cours d'exécution) se
# traduit par un code de sortie non nul de PyInstaller, détecté ci-dessous.
function Assert-PyInstallerOutput {
    param(
        [Parameter(Mandatory)][string]$ExePath,
        [Parameter(Mandatory)][string]$Label
    )
    if ($LASTEXITCODE -ne 0) {
        Write-Error "ÉCHEC : PyInstaller a retourné le code $LASTEXITCODE pour $Label."
        exit 1
    }
    if (-not (Test-Path $ExePath)) {
        Write-Error "ÉCHEC : $ExePath introuvable après la génération de $Label."
        exit 1
    }
}

Write-Host "Génération de l'exécutable principal ($appName)..."
& $pythonCmd -m PyInstaller --noconfirm --onefile --windowed --hidden-import=yaml --hidden-import=selenium.webdriver.chrome.webdriver --hidden-import=selenium.webdriver.chrome.service --hidden-import=selenium.webdriver.remote.webdriver --collect-submodules selenium --name "$appName" --distpath $distDir --workpath build --specpath . GlycoDownload.py
Assert-PyInstallerOutput -ExePath "$distDir\$appName.exe" -Label "l'exécutable principal ($appName)"

Write-Host "Génération de l'exécutable de migration (migrate)..."
& $pythonCmd -m PyInstaller --noconfirm --onefile --console --hidden-import=yaml --hidden-import=colorama --collect-submodules selenium --name "migrate" --distpath $distDir --workpath build --specpath . migrate.py
Assert-PyInstallerOutput -ExePath "$distDir\migrate.exe" -Label "l'exécutable de migration (migrate)"

# --- 4b. Copier les fichiers annexes dans dist ---
Write-Host "Copie des fichiers annexes dans $distDir..."
$filesToCopy = @("config_example.yaml", "README.md", "LICENSE.txt", "MIGRATION.md", ".env.example", "Launch-Dexcom-And-Run.ps1")
foreach ($file in $filesToCopy) {
    if (Test-Path $file) {
        Copy-Item $file $distDir -Force
    }
    else {
        Write-Warning "Fichier introuvable : $file"
    }
}

# --- 5. Compiler l'installateur avec Inno Setup ---
Write-Host "Compilation de l'installateur Inno Setup..."
& $isccPath $issFile

if ($LASTEXITCODE -eq 0) {
    Write-Host "SUCCÈS : L'installateur a été créé dans le dossier $setupOutputDir"
}
else {
    Write-Error "ÉCHEC : La compilation Inno Setup a échoué."
    exit 1
}
