🎯 Les principes clés pour mieux me guider
1. Spécifier le format attendu
❌ "Modifie le readme"
✅ "Mets à jour le README.md bilingue (français puis anglais, structure identique)"

2. Donner des exemples concrets
❌ "Réorganise le fichier"
✅ "Ajoute une table des matières comme ceci : [exemple de structure]"

3. Établir des contraintes claires
✅ "La section anglaise doit être une traduction fidèle, PAS une copie du français"
✅ "Chaque section doit apparaître UNE SEULE FOIS dans chaque langue"
✅ "Vérifie qu'il n'y a pas de duplication avant de finaliser"

4. Demander validation par étapes
✅ "Liste d'abord les changements détectés, attends ma validation"
✅ "Propose la structure du README avant de modifier"
✅ "Montre-moi la section Nouveautés avant de tout mettre à jour"

5. Être explicite sur ce qui NE doit PAS changer
✅ "Conserve la notice 'An English version of this text follows the French text'"
✅ "Ne modifie pas les exemples de code existants"
✅ "Garde la même licence"

💡 Formulation idéale pour CETTE situation précise
CONTEXTE :
Le projet GlycoReport-Downloader passe en version 0.2.3.
Le README.md est bilingue (français/anglais, structure identique).

OBJECTIF :
Mettre à jour le README.md avec les nouveautés de la v0.2.3.

ÉTAPES :
1. Lis les fichiers sources (version.py, *.py, config_example.yaml) 
   et liste les changements depuis v0.2.2

2. Attends ma validation de la liste

3. Structure cible pour le README :
   - Notice bilingue préservée
   - Table des matières FR et EN
   - 21 sections identiques (ordre : Nouveautés, Historique, Architecture, 
     Description, Release, Limitations, Fonctionnalités, Installation, 
     Build, Distribution, Dates, Config, Chemins, Sécurité, Première fois, 
     CLI, Exemple aide, Tests, Notes, Auteur, Licence)
   - Français d'abord, puis anglais (traduction fidèle)

4. Mets à jour section par section, en commençant par "Nouveautés" et 
   "Historique des versions" (FR puis EN)

5. Vérifie l'absence de duplication avant chaque modification

6. Confirme la cohérence finale (21 sections × 2 langues)

CONTRAINTES :
- Section FR = 100% français
- Section EN = 100% anglais (traduction)
- Aucune duplication
- Ordre des sections strict et identique

CONTEXTE :
Le projet GlycoReport-Downloader passe en version 0.2.3.
Le README.md est bilingue (français/anglais, structure identique).

OBJECTIF :
Mettre à jour le README.md avec les nouveautés de la v0.2.3.

ÉTAPES :
1. Lis les fichiers sources (version.py, *.py, config_example.yaml) 
   et liste les changements depuis v0.2.2

2. Attends ma validation de la liste

3. Structure cible pour le README :
   - Notice bilingue préservée
   - Table des matières FR et EN
   - 21 sections identiques (ordre : Nouveautés, Historique, Architecture, 
     Description, Release, Limitations, Fonctionnalités, Installation, 
     Build, Distribution, Dates, Config, Chemins, Sécurité, Première fois, 
     CLI, Exemple aide, Tests, Notes, Auteur, Licence)
   - Français d'abord, puis anglais (traduction fidèle)

4. Mets à jour section par section, en commençant par "Nouveautés" et 
   "Historique des versions" (FR puis EN)

5. Vérifie l'absence de duplication avant chaque modification

6. Confirme la cohérence finale (21 sections × 2 langues)

CONTRAINTES :
- Section FR = 100% français
- Section EN = 100% anglais (traduction)
- Aucune duplication
- Ordre des sections strict et identique

Mets à jour README.md pour v0.2.3 en mode PROGRESSIF :

ÉTAPE 1 (analyse) :
- Lis version.py, GlycoDownload.py, rapports.py, utils.py, config_example.yaml
- Liste les changements détectés vs v0.2.2
- ATTENDS ma validation

ÉTAPE 2 (structure) :
- Propose la structure complète du README (21 sections × 2 langues)
- Confirme l'absence de duplication dans le fichier actuel
- ATTENDS ma validation

ÉTAPE 3 (mise à jour FR) :
- Mets à jour "Nouveautés" (français)
- Mets à jour "Historique des versions" (français)
- ATTENDS ma validation

ÉTAPE 4 (mise à jour EN) :
- Traduis "What's New" (anglais)
- Traduis "Version History" (anglais)
- ATTENDS ma validation

ÉTAPE 5 (finalisation) :
- Vérifie cohérence FR/EN
- Confirme : 21 sections × 2 langues, zéro duplication

CONTRAINTES STRICTES :
- Bilingue : FR complet puis EN complet
- Section FR = 100% français
- Section EN = 100% anglais (traduction fidèle)
- Notice "An English version..." préservée
- Vérifier absence duplication avant CHAQUE modification