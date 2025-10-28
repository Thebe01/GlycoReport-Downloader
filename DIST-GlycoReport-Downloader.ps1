#	FileName: DIST-GlycoReport-Downloader.ps1
#	FileType: PowerShell Source file
#
#	Auteur : Pierre Théberge
#	Créé le : 2025-09-03
#	Dernière modification le : 2025-10-27
#	CopyRights : Pierre Théberge
#	Description : Script pour générer l'exécutable, préparer le dossier dist et créer l'archive ZIP de distribution.
#
#	Version : 1.0.7
#	Modifications :
#	Version   Date          Billet  Description
#	1.0.0     2025-09-03            Version initiale.
#	1.0.1     2025-09-03            Correction pour que le zip soit créé dans le dossier dist.
#   1.0.2     2025-10-14    ES-12   Ajout de la colonne Billet dans le bloc des modifications.
#   1.0.3     2025-10-16    ES-12   Suppression de la copie du dossier chromedriver-win64 (ChromeDriverManager gère maintenant le téléchargement automatique).
#   1.0.4     2025-10-16    ES-12   Ajout des fichiers de migration (migrate.py, MIGRATION.md) dans la distribution.
#   1.0.5     2025-10-16    ES-12   Création d'un exécutable migrate.exe à partir de migrate.py pour simplifier l'utilisation.
#   1.0.6     2025-10-21    ES-7    Synchronisation de version (aucun changement fonctionnel).
#   1.0.7     2025-10-27    ES-17   Synchronisation de version (aucun changement fonctionnel).

$ErrorActionPreference = "Stop"

# 1. Générer l'exécutable principal avec PyInstaller
Write-Host "Étape 1 : Génération de l'exécutable GlycoReport-Downloader..."
pyinstaller --onefile --hidden-import=yaml --name "GlycoReport-Downloader" GlycoDownload.py

# 2. Générer l'exécutable de migration
Write-Host "Étape 2 : Génération de l'exécutable migrate..."
pyinstaller --onefile --hidden-import=yaml --hidden-import=colorama --name "migrate" migrate.py

# 3. Vérifier l'existence des fichiers à copier
# Note : migrate.py n'est PAS inclus dans la distribution (migrate.exe est généré à la place)
$files = @(".env.example", "config_example.yaml", "LICENSE.txt", "README.md", "MIGRATION.md")
foreach ($file in $files) {
    if (-Not (Test-Path $file)) {
        Write-Error "Fichier manquant : $file. Arrêt du script."
        exit 1
    }
}

# 4. Vérifier l'existence du dossier dist (créé par PyInstaller)
if (-Not (Test-Path "dist")) {
    Write-Error "Le dossier 'dist' n'existe pas (PyInstaller a échoué ?). Arrêt du script."
    exit 1
}

# 5. Vérifier l'existence de migrate.exe
if (-Not (Test-Path "dist\migrate.exe")) {
    Write-Error "Le fichier 'dist\migrate.exe' n'existe pas (PyInstaller a échoué ?). Arrêt du script."
    exit 1
}

# 6. Copier les fichiers dans le sous-répertoire dist
Write-Host "Étape 3 : Copie des fichiers dans dist..."
foreach ($file in $files) {
    Copy-Item $file dist\ -Force
}

# Note : Le dossier chromedriver-win64 n'est plus copié depuis la version 0.2.3
# ChromeDriverManager télécharge automatiquement la version appropriée de ChromeDriver
# Note : migrate.exe est généré par PyInstaller et sera automatiquement inclus dans le ZIP

# 7. Se placer dans le dossier dist
Write-Host "Étape 4 : Compression du dossier dist..."
Push-Location dist

# 8. Compresser tout le contenu du dossier dist dans un zip dans le sous-répertoire dist
Compress-Archive -Path * -DestinationPath GlycoReport-Downloader.zip -Force

# 9. Revenir au dossier d'origine
Pop-Location

Write-Host "Distribution prête ! (~10 MB plus légère grâce à ChromeDriverManager)"
Write-Host "Fichiers inclus : GlycoReport-Downloader.exe, migrate.exe, config_example.yaml, .env.example, MIGRATION.md, LICENSE.txt, README.md"
