#	FileName: DIST-GlycoReport-Downloader.ps1
#	FileType: PowerShell Source file
#
#	Auteur : Pierre Théberge
#	Créé le : 2025-09-03
#	Dernière modification le : 2026-01-29
#	CopyRights : Pierre Théberge
#	Description : Script pour générer les exécutables et créer l'installateur Inno Setup.
#
#	Version : 2.0.4
#	Modifications :
#	Version   Date          Billet  Description
#	1.0.0     2025-09-03            Version initiale (ZIP).
#   ...
#   2.0.0     2025-12-21    ES-18   Passage à Inno Setup pour la distribution.
#   2.0.1     2025-12-22    ES-18   Correction du chemin d'installation par défaut ({sd}\ipt).
#   2.0.2     2025-12-22    ES-18   Correction variable inutilisée $appName.
#                                   Correction warning architecture Inno Setup (x64compatible).
#   2.0.3     2025-12-22    ES-3    Synchronisation de version.
#   2.0.4     2026-01-29    ES-19   Ajout du script Launch-Dexcom-And-Run.ps1 dans la distribution.

$ErrorActionPreference = "Stop"

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
$issContent = Get-Content $issFile -Raw
# Remplacement de la ligne #define MyAppVersion "..."
# Utilisation d'une regex qui préserve les commentaires éventuels en fin de ligne
$newIssContent = $issContent -replace '(?m)^#define MyAppVersion "[^"]+"', "#define MyAppVersion ""$version"""
Set-Content -Path $issFile -Value $newIssContent
Write-Host "Fichier .iss mis à jour avec la version $version"

# --- 4. Générer les exécutables avec PyInstaller ---
Write-Host "Génération de l'exécutable principal ($appName)..."
# Nettoyage préalable si nécessaire (optionnel, mais recommandé pour éviter les conflits)
# Remove-Item -Path "$distDir\$appName.exe" -ErrorAction SilentlyContinue

& $pythonCmd -m PyInstaller --noconfirm --onefile --windowed --hidden-import=yaml --name "$appName" --distpath $distDir --workpath build --specpath . GlycoDownload.py

Write-Host "Génération de l'exécutable de migration (migrate)..."
& $pythonCmd -m PyInstaller --noconfirm --onefile --console --hidden-import=yaml --hidden-import=colorama --name "migrate" --distpath $distDir --workpath build --specpath . migrate.py

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
