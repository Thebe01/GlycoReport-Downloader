<!--
META:
    0.0.0 - 2026-07-31 - PD-206 : Version initiale. Extrait de HEADER_TEMPLATE_POWERSHELL.md
                                   pour adapter les règles aux modules (.psm1/.psd1), qui ne
                                   "s'exécutent" pas comme un script (pas de param() au niveau
                                   module, pas de lignes Début/Fin).
    0.0.1 - 2026-07-31 - CR      : Correction — l'absence de param() au niveau module n'est pas
                                    une impossibilité du langage (Import-Module -ArgumentList
                                    existe) mais une convention de ce standard ; justification
                                    ajoutée (fragilité de l'auto-chargement, pas de liaison
                                    nommée, invisible dans Get-Help). CompanyName de l'exemple de
                                    manifeste aligné sur la graphie officielle (avec virgules).
    0.0.2 - 2026-08-01 - PD-210  : Correction d'une affirmation fausse : le bloc <# ... #> en tête
                                    de .psm1 ne rend PAS le module visible via Get-Help
                                    <NomDuModule> (Get-Help traite un nom de module comme une
                                    recherche de fichier d'aide externe de type about, pas une
                                    lecture du .psm1) — constaté en convertissant IPT.PromptSync.psm1
                                    au vrai bloc <# #> et en testant Get-Help IPT.PromptSync (échec). Le
                                    bloc reste requis (lisibilité, cohérence avec les scripts),
                                    mais plus au motif erroné de l'aide fonctionnelle au niveau
                                    module. Get-Help Verb-Noun -Full sur une fonction exportée
                                    individuelle, lui, fonctionne bien.
    0.0.3 - 2026-08-01 - CR      : Précision du motif de fichier d'aide externe recherché par
                                    Get-Help <NomDuModule> — about_<NomDuModule>.help.txt sous un
                                    sous-dossier de culture (ex : en-US), pas about_*.help.txt.
                                    Retrait de la même approximation (about_*.help.txt) restée dans
                                    le texte de l'entrée 0.0.2. Accents restaurés dans cette même
                                    entrée (retirés par erreur).
-->

# 📘 Template d'en-tête PowerShell — Modules (.psm1 / .psd1) - IPT inc

**Standard officiel pour les modules PowerShell**
Innovations, Performances, Technologies inc.

Complète [HEADER_TEMPLATE_POWERSHELL.md](HEADER_TEMPLATE_POWERSHELL.md) (scripts `.ps1`). Un module
est chargé via `Import-Module` (du code peut s'exécuter à l'import), mais il n'a pas le même point
d'entrée qu'un script. Dans ce standard, on évite les paramètres au niveau module (`param()` /
`Import-Module -ArgumentList`) : sans `Import-Module` explicite (auto-chargement par découverte de
commande), ce `param()` ne reçoit jamais d'arguments, et `-ArgumentList` ne fait que du positionnel
— sans liaison nommée ni visibilité dans `Get-Help`. Privilégier des paramètres au niveau des
fonctions. Pas de `-WhatIf`/`-Confirm` au niveau module, pas de lignes Début/Fin : ces conventions
s'appliquent aux scripts appelants. Tout le reste — bloc d'aide réel, `.MODIFICATIONS`,
versionnement — s'applique de la même façon.

---

## 🎯 Fichier `.psm1` — Format obligatoire

```powershell
# Format d'en-tête standard à respecter pour ce projet.
# Voir .github/HEADER_TEMPLATE_POWERSHELL_MODULE.md pour les détails.

<#
.SYNOPSIS
    [Description courte du module en une ligne]

.DESCRIPTION
    Nom du fichier : NomDuModule.psm1
    Type           : PowerShell module
    Auteur         : Pierre Théberge
    Compagnie      : Innovations, Performances, Technologies inc.
    Créé le        : YYYY-MM-DD
    Modifié le     : YYYY-MM-DD
    Version        : 0.0.0
    Copyright      : Pierre Théberge

.MODIFICATIONS
    0.0.0 - YYYY-MM-DD - Billet-XXX  : Initialisation.
    0.1.0 - YYYY-MM-DD - -           : Ajout de la fonction Verb-Noun.
    0.1.1 - YYYY-MM-DD - PD-10000001 : Correction encodage UTF-8.
    1.0.0 - YYYY-MM-DD - -           : Version de production stable.
#>

#Requires -Version 5.1

# === Configuration stricte ===
Set-StrictMode -Version Latest
```

**Règles identiques au template script :**

- Vrai bloc d'aide `<# ... #>` — pas des lignes `#` individuelles. Un bloc `.DESCRIPTION`/
  `.MODIFICATIONS` écrit en commentaires `#` ligne par ligne se distingue mal du reste des
  commentaires et rompt la cohérence avec le format des scripts `.ps1`. Le bloc `<# ... #>` doit
  se trouver **avant** tout code exécutable (`Set-StrictMode`, fonctions, etc.), par convention de
  lisibilité — la référence humaine du fichier (`.DESCRIPTION`, `.MODIFICATIONS`) doit être la
  première chose lue.
  **Attention** : contrairement à un script (`Get-Help .\Script.ps1`) ou une fonction (`Get-Help
  Verb-Noun`), PowerShell n'expose PAS ce bloc de tête de `.psm1` via `Get-Help <NomDuModule>` —
  `Get-Help` traite un nom de module comme une recherche d'un fichier d'aide externe de type about
  (ex : `en-US\about_<NomDuModule>.help.txt`, sous un sous-dossier de culture du module), pas comme
  une lecture du `.psm1`. Une version précédente de ce document
  affirmait le contraire ; c'était une erreur (constatée en pratique sur IPT.PromptSync 0.4.0,
  PD-210 : `Get-Help IPT.PromptSync` échoue avec "could not find ... in a help file", même avec le
  bloc `<# ... #>` correctement placé avant tout code). Les fonctions exportées individuelles
  gardent leur propre bloc `<# ... #>` (juste avant/dans la fonction) : celui-là **est** exposé par
  `Get-Help Verb-Noun -Full` — c'est la seule granularité où l'aide fonctionnelle marche vraiment
  pour un module.
- `.SYNOPSIS` obligatoire, même pour un module.
- Alignement `.DESCRIPTION` sur `:` (15 espaces après le label), version sémantique
  `MAJEUR.MINEUR.CORRECTIF`, version initiale toujours `0.0.0` — mêmes règles que
  [HEADER_TEMPLATE_POWERSHELL.md](HEADER_TEMPLATE_POWERSHELL.md#2-description).
- `.MODIFICATIONS` complet, une entrée par version, alignement sur `:` à la même colonne pour
  toutes les entrées, padding du champ billet et de la version selon les mêmes règles que le
  template script.
- `#Requires -Version 5.1` et `Set-StrictMode -Version Latest` obligatoires.

**Ce qui ne s'applique PAS aux modules (contrairement aux scripts) :**

- Pas de `[CmdletBinding(SupportsShouldProcess)]`/`param()` au niveau module — seulement sur les
  fonctions individuelles qui en ont besoin.
- Pas de `$ErrorActionPreference = 'Stop'` au niveau module : ce réglage est scope-local au module
  et n'affecte pas l'appelant : le fixer ici donnerait une fausse impression de contrôle. Chaque
  script appelant garde la responsabilité de son propre `$ErrorActionPreference`.
- Pas de lignes Début/Fin (`Write-Host ... Début/Fin ...`) : un module n'a pas de point d'entrée
  unique à chronométrer — c'est le script appelant qui exécute et affiche Début/Fin.
- Pas de `$Script:NomScript`/`$Script:Version`/`$Script:StartTime` : ces variables de convention
  servent à l'affichage Début/Fin d'un script, qui n'existe pas ici.

En fin de fichier, exporter explicitement l'API publique :

```powershell
Export-ModuleMember -Function 'Verb-Noun1', 'Verb-Noun2'
```

---

## 🎯 Fichier `.psd1` — Format obligatoire

Le manifeste est un fichier de données PowerShell (`@{ ... }`), pas un script : PowerShell ne lit
pas d'aide `Get-Help` dedans, donc pas de bloc `.SYNOPSIS`/`.DESCRIPTION`/`.MODIFICATIONS` à y
dupliquer. L'historique de version complet reste dans le `.psm1` (`RootModule`) — source unique
pour éviter que les deux fichiers divergent.

```powershell
#
# Manifeste du module NomDuModule
#
# ATTENTION ENCODAGE : enregistrer ce fichier en UTF-8 AVEC BOM. PowerShell 5.1
# lit sinon selon la page de code ANSI (CP1252 sur les postes fr), ce qui
# corromprait tout caractère accentué. Les accents sont tolérés dans les
# champs de métadonnées ci-dessous (Author, Copyright, CompanyName,
# Description) — l'enjeu est la lecture du manifeste en ANSI sans BOM.
#

@{
    RootModule        = 'NomDuModule.psm1'
    ModuleVersion     = '0.0.0'
    GUID              = 'généré une seule fois via [guid]::NewGuid()'
    Author            = 'Pierre Théberge'
    CompanyName       = 'Innovations, Performances, Technologies inc.'
    Copyright         = 'Pierre Théberge'
    Description       = 'Description courte du module.'

    PowerShellVersion = '5.1'

    FunctionsToExport = @('Verb-Noun1', 'Verb-Noun2')
    CmdletsToExport   = @()
    VariablesToExport = @()
    AliasesToExport   = @()
}
```

**Règles :**

- `ModuleVersion` **doit** être bumpée dans le même commit/PR que `Version` dans le `.psm1` —
  sinon `Import-Module`/`Get-Module` rapportent une version qui ne correspond plus au changelog
  réel du module.
- `Author`/`CompanyName`/`Copyright`/`Description` portent les métadonnées nativement (champs du
  manifeste), pas besoin de les répéter dans un commentaire `.DESCRIPTION` séparé.
- `FunctionsToExport` explicite (pas `'*'`) — doit lister exactement ce que `Export-ModuleMember`
  exporte côté `.psm1`.

---

## ✅ Checklist de validation

Avant de commiter un module PowerShell (`.psm1` + `.psd1`) :

- [ ] `.psm1` : vrai bloc d'aide `<# ... #>` (pas de `#` ligne par ligne) avant tout code
- [ ] `.psm1` : `.SYNOPSIS` présent
- [ ] `.psm1` : `.DESCRIPTION` avec métadonnées alignées, version initiale `0.0.0`
- [ ] `.psm1` : `.MODIFICATIONS` à jour avec dernière version, alignement respecté
- [ ] `.psm1` : `#Requires -Version 5.1` et `Set-StrictMode -Version Latest`
- [ ] `.psm1` : `Export-ModuleMember` explicite en fin de fichier
- [ ] `.psd1` : `ModuleVersion` == `Version` du `.psm1` (même PR)
- [ ] `.psd1` : `FunctionsToExport` synchronisé avec `Export-ModuleMember`
- [ ] Code testé et fonctionnel (`Import-Module -Force` sans erreur)

---

**Document créé le** : 2026-07-31
**Version** : 0.0.3
**Mainteneur** : Pierre Théberge
**Compagnie** : Innovations, Performances, Technologies inc.
