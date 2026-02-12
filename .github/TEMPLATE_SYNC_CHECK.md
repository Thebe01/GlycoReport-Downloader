<!--
META:
   1.0.0 - 2026-01-29 - ES-19 : Version initiale.
   1.0.1 - 2026-02-11 - PD-188 : Chemin de référence via variable d’environnement.
   1.0.2 - 2026-02-11 - PD-188 : $repoRoot via REPO_ROOT ou détection Git.
   1.0.3 - 2026-02-11 - PD-188 : Templates optionnels selon le repo.
   1.0.4 - 2026-02-11 - PD-188 : Message d’erreur REPO_ROOT corrigé.
-->

# Vérification des templates d’en-tête

But : s’assurer que les templates locaux restent identiques à la version de
référence.

## Source de référence

Répertoire :
$env:IPTDEVLIB_PROMPTS (ex.
$env:USERPROFILE\Sources\IPTDevLib\prompts)

## Fichiers à comparer

- .github/HEADER_TEMPLATE_PYTHON.md (optionnel selon le repo)
- .github/HEADER_TEMPLATE_POWERSHELL.md (optionnel selon le repo)
- .github/TEMPLATE_SYNC_CHECK.md (toujours présent)

## Procédure attendue

1. Comparer le contenu de chaque template avec la version de référence.
2. Lister les différences trouvées (ordre, contenu, ponctuation, sections
   manquantes).
3. Si des écarts sont détectés, suggérer une mise à jour du repo pour s’aligner
   sur la source.
4. Ne pas modifier automatiquement sans validation explicite.

## Procédure PowerShell (pwsh)

### 1) Comparer les fichiers (diff)

```powershell
$repoRoot = $env:REPO_ROOT
if ([string]::IsNullOrWhiteSpace($repoRoot)) {
   try {
      $repoRoot = (git -C $PWD rev-parse --show-toplevel 2>$null).Trim()
   } catch {
      $repoRoot = $null
   }
}
if ([string]::IsNullOrWhiteSpace($repoRoot)) {
   throw 'REPO_ROOT non défini. Définis $env:REPO_ROOT ou exécute depuis un repo Git.'
}
$officialRoot = $env:IPTDEVLIB_PROMPTS
if ([string]::IsNullOrWhiteSpace($officialRoot)) {
   $officialRoot = Join-Path $env:USERPROFILE "Sources\IPTDevLib\prompts"
}

$pairs = @(
   @{ Name = "Python"; Repo = Join-Path $repoRoot ".github\HEADER_TEMPLATE_PYTHON.md"; Official = Join-Path $officialRoot "HEADER_TEMPLATE_PYTHON.md" },
   @{ Name = "PowerShell"; Repo = Join-Path $repoRoot ".github\HEADER_TEMPLATE_POWERSHELL.md"; Official = Join-Path $officialRoot "HEADER_TEMPLATE_POWERSHELL.md" },
   @{ Name = "TemplateSync"; Repo = Join-Path $repoRoot ".github\TEMPLATE_SYNC_CHECK.md"; Official = Join-Path $officialRoot "TEMPLATE_SYNC_CHECK.md" }
)

foreach ($p in $pairs) {
   "===== $($p.Name) ====="
   if (-not (Test-Path -LiteralPath $p.Repo)) {
      "(Ignoré) Fichier absent dans ce repo : $($p.Repo)"
      continue
   }
   Compare-Object (Get-Content -LiteralPath $p.Official) (Get-Content -LiteralPath $p.Repo) -IncludeEqual:$false |
      Select-Object @{n='Side';e={$_.SideIndicator}}, @{n='Line';e={$_.InputObject}}
}
```

### 2) Synchroniser depuis la source officielle (après validation)

```powershell
$repoRoot = $env:REPO_ROOT
if ([string]::IsNullOrWhiteSpace($repoRoot)) {
   try {
      $repoRoot = (git -C $PWD rev-parse --show-toplevel 2>$null).Trim()
   } catch {
      $repoRoot = $null
   }
}
if ([string]::IsNullOrWhiteSpace($repoRoot)) {
   throw 'REPO_ROOT non défini. Définis $env:REPO_ROOT ou exécute depuis un repo Git.'
}
$officialRoot = $env:IPTDEVLIB_PROMPTS
if ([string]::IsNullOrWhiteSpace($officialRoot)) {
   $officialRoot = Join-Path $env:USERPROFILE "Sources\IPTDevLib\prompts"
}

$pairs = @(
   @{ Name = "Python"; Repo = Join-Path $repoRoot ".github\HEADER_TEMPLATE_PYTHON.md"; Official = Join-Path $officialRoot "HEADER_TEMPLATE_PYTHON.md" },
   @{ Name = "PowerShell"; Repo = Join-Path $repoRoot ".github\HEADER_TEMPLATE_POWERSHELL.md"; Official = Join-Path $officialRoot "HEADER_TEMPLATE_POWERSHELL.md" },
   @{ Name = "TemplateSync"; Repo = Join-Path $repoRoot ".github\TEMPLATE_SYNC_CHECK.md"; Official = Join-Path $officialRoot "TEMPLATE_SYNC_CHECK.md" }
)

foreach ($p in $pairs) {
   if (-not (Test-Path -LiteralPath $p.Repo)) {
      "(Ignoré) Fichier absent dans ce repo : $($p.Repo)"
      continue
   }
   Copy-Item -LiteralPath $p.Official -Destination $p.Repo -Force
}
```

## Quand exécuter la vérification

- Après une mise à jour de IPTDevLib\prompts.
- Avant une release du repo.
