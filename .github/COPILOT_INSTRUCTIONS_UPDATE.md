<!--
META:
    1.0.0 - 2026-01-29 - ES-19 : Procédure de mise à jour des instructions Copilot.
    1.0.1 - 2026-03-19 - ES-15 : Ajout de la section finale standard du document.
    1.0.2 - 2026-03-20 - ES-15 : Référence au repo via IPTDEVLIB_PROMPTS.
    1.0.3 - 2026-03-20 - ES-15 : Nom du document harmonisé avec le fichier.
    1.0.4 - 2026-03-20 - ES-15 : Clarification du fichier cible à modifier.
    1.0.5 - 2026-03-20 - ES-15 : Fallback harmonisé en notation PowerShell.
    1.0.6 - 2026-08-01 - CR    : Correction d'une régression introduite en 1.0.3 : le titre et la
                                  section « Contenu à ajouter » avaient été renommés vers
                                  COPILOT_INSTRUCTIONS_UPDATE.md (le nom de CE document) au lieu de
                                  copilot-instructions.md (le vrai fichier chargé par GitHub
                                  Copilot Chat/Review) — confirmé par l'historique git (commit
                                  c9cce9e, "harmonize document name"), qui montre la version 1.0.0
                                  référençant correctement copilot-instructions.md. Depuis 1.0.3,
                                  la procédure faisait ajouter la section de synchro dans un
                                  fichier que Copilot ne charge jamais. Ajout d'un prérequis pour
                                  couvrir le cas où copilot-instructions.md n'existe pas encore.
-->

# Mise à jour de copilot-instructions.md (repos consommateurs)

Objectif : appliquer les consignes de synchronisation des templates dans les
autres repos.

## Prérequis

- Accès au repo de référence des prompts via la variable d’environnement
  `IPTDEVLIB_PROMPTS` (avec fallback recommandé vers
  `$env:USERPROFILE\Sources\IPTDevLib\prompts`, cf.
  `.github/TEMPLATE_SYNC_CHECK.md`).
- Le fichier .github/TEMPLATE_SYNC_CHECK.md existe dans le repo consommateur.
- Le fichier .github/copilot-instructions.md existe dans le repo consommateur
  (le créer s’il est absent — c’est le fichier chargé par GitHub Copilot).

## Contenu à ajouter dans copilot-instructions.md

Ajouter une section **Synchronisation des templates** (ou mettre à jour
l’existante) dans le `.github/copilot-instructions.md` du repo consommateur
— le fichier que GitHub Copilot Chat/Review charge réellement, à ne pas
confondre avec ce document de procédure — avec les deux lignes suivantes :

- Voir [TEMPLATE_SYNC_CHECK.md](TEMPLATE_SYNC_CHECK.md) pour la procédure de
  comparaison avec la source officielle et la recommandation de mise à jour.
- La vérification doit être exécutée lorsqu’une conversation Copilot est activée
  dans ce repo.

## Points de contrôle

- Le lien ne doit pas contenir de double `.github`.
- La section est placée une seule fois dans le fichier.
- La formulation est identique dans tous les repos.

## Quand appliquer

- Lors de l’ajout de Copilot dans un repo existant.
- Lors d’une mise à jour des règles de synchronisation.

---

**Document créé le** : 2026-01-29  
**Version** : 1.0.6  
**Mainteneur** : Pierre Théberge  
**Compagnie** : Innovations, Performances, Technologies inc.
