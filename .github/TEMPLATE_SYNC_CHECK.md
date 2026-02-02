<!--
META:
   1.0.0 - 2026-01-29 - ES-19 : Version initiale.
-->

# Vérification des templates d’en-tête

But : s’assurer que les templates locaux restent identiques à la version de
référence.

## Source de référence

Répertoire : C:\Users\thebe\OneDrive\Sources\IPTDevLib\prompts

## Fichiers à comparer

- .github/HEADER_TEMPLATE_PYTHON.md
- .github/HEADER_TEMPLATE_POWERSHELL.md
- .github/TEMPLATE_SYNC_CHECK.md

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
$repoRoot = "C:\Users\thebe\OneDrive\Sources\GlycoReport-Downloader"
$officialRoot = "C:\Users\thebe\OneDrive\Sources\IPTDevLib\prompts"

$pairs = @(
   @{ Name = "Python"; Repo = Join-Path $repoRoot ".github\HEADER_TEMPLATE_PYTHON.md"; Official = Join-Path $officialRoot "HEADER_TEMPLATE_PYTHON.md" },
   @{ Name = "PowerShell"; Repo = Join-Path $repoRoot ".github\HEADER_TEMPLATE_POWERSHELL.md"; Official = Join-Path $officialRoot "HEADER_TEMPLATE_POWERSHELL.md" },
   @{ Name = "TemplateSync"; Repo = Join-Path $repoRoot ".github\TEMPLATE_SYNC_CHECK.md"; Official = Join-Path $officialRoot "TEMPLATE_SYNC_CHECK.md" }
)

foreach ($p in $pairs) {
   "===== $($p.Name) ====="
   Compare-Object (Get-Content -LiteralPath $p.Official) (Get-Content -LiteralPath $p.Repo) -IncludeEqual:$false |
      Select-Object @{n='Side';e={$_.SideIndicator}}, @{n='Line';e={$_.InputObject}}
}
```

### 2) Synchroniser depuis la source officielle (après validation)

```powershell
$repoRoot = "C:\Users\thebe\OneDrive\Sources\GlycoReport-Downloader"
$officialRoot = "C:\Users\thebe\OneDrive\Sources\IPTDevLib\prompts"

Copy-Item -LiteralPath (Join-Path $officialRoot "HEADER_TEMPLATE_PYTHON.md") -Destination (Join-Path $repoRoot ".github\HEADER_TEMPLATE_PYTHON.md") -Force
Copy-Item -LiteralPath (Join-Path $officialRoot "HEADER_TEMPLATE_POWERSHELL.md") -Destination (Join-Path $repoRoot ".github\HEADER_TEMPLATE_POWERSHELL.md") -Force
Copy-Item -LiteralPath (Join-Path $officialRoot "TEMPLATE_SYNC_CHECK.md") -Destination (Join-Path $repoRoot ".github\TEMPLATE_SYNC_CHECK.md") -Force
```

## Quand exécuter la vérification

- Après une mise à jour de IPTDevLib\prompts.
- Avant une release du repo.
