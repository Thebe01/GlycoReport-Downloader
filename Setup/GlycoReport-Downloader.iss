; Script Inno Setup pour GlycoReport-Downloader
; Généré automatiquement

#define MyAppName "GlycoReport-Downloader"
#define MyAppVersion "0.2.14" ; Sera mis à jour par le script PowerShell
#define MyAppPublisher "Pierre Théberge"
#define MyAppURL "https://github.com/pierretheberge/GlycoReport-Downloader"
#define MyAppExeName "GlycoReport-Downloader.exe"

[Setup]
; NOTE: La valeur de AppId identifie cette application de manière unique.
; Ne l'utilisez pas pour d'autres applications.
AppId={{A1B2C3D4-E5F6-7890-1234-567890ABCDEF}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={sd}\ipt\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
PrivilegesRequired=lowest
; Le dossier de sortie pour l'installateur compilé
OutputDir=..\dist_setup
OutputBaseFilename=GlycoReport-Downloader_Setup_{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
; Architecture 64-bit
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; L'exécutable principal
Source: "..\dist\GlycoReport-Downloader.exe"; DestDir: "{app}"; Flags: ignoreversion
; Fichiers de configuration et documentation
Source: "..\dist\.env.example"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\config_example.yaml"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\MIGRATION.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\migrate.exe"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: config.yaml n'est pas inclus pour ne pas écraser la config utilisateur lors d'une mise à jour

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

