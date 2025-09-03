#	FileName: DIST-GlycoReport-Downloader.ps1
#	FileType: PowerShell Source file
#
#	Auteur : Pierre Théberge
#	Créé le : 2025-09-03
#	Dernière modification le : 2025-09-03
#	CopyRights : Pierre Théberge
#	Description : Script pour générer l'exécutable, préparer le dossier dist et créer l'archive ZIP de distribution.
#
#	Version : 1.0.0
#	Modifications :
#	Version   Date          Description
#	1.0.0     2025-09-03    Version initiale.
#

$ErrorActionPreference = "Stop"

# 1. Générer l'exécutable avec PyInstaller
Write-Host "Étape 1 : Génération de l'exécutable..."
pyinstaller --onefile --hidden-import=yaml --name "GlycoReport-Downloader" GlycoDownload.py

# 2. Vérifier l'existence des fichiers à copier
$files = @(".env.example", "config_example.yaml", "LICENSE.txt", "README.md")
foreach ($file in $files) {
    if (-Not (Test-Path $file)) {
        Write-Error "Fichier manquant : $file. Arrêt du script."
        exit 1
    }
}

# 3. Vérifier l'existence du dossier chromedriver-win64
if (-Not (Test-Path "chromedriver-win64")) {
    Write-Error "Dossier manquant : chromedriver-win64. Arrêt du script."
    exit 1
}

# 4. Vérifier l'existence du dossier dist (créé par PyInstaller)
if (-Not (Test-Path "dist")) {
    Write-Error "Le dossier 'dist' n'existe pas (PyInstaller a échoué ?). Arrêt du script."
    exit 1
}

# 5. Copier les fichiers dans le sous-répertoire dist
Write-Host "Étape 2 : Copie des fichiers dans dist..."
foreach ($file in $files) {
    Copy-Item $file dist\ -Force
}

# 6. Copier le dossier chromedriver-win64 dans dist (avec tout son contenu)
Write-Host "Étape 3 : Copie du dossier chromedriver-win64..."
Copy-Item chromedriver-win64 dist\chromedriver-win64 -Recurse -Force

# 7. Se placer dans le dossier dist
Write-Host "Étape 4 : Compression du dossier dist..."
Push-Location dist

# 8. Compresser tout le contenu du dossier dist dans un zip à la racine du projet
Compress-Archive -Path * -DestinationPath ../GlycoReport-Downloader.zip -Force

# 9. Revenir au dossier d'origine
Pop-Location

Write-Host "Distribution prête !"