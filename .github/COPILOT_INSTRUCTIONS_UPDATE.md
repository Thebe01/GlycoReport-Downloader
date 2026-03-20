<!--
META:
    1.0.0 - 2026-01-29 - ES-19 : Procédure de mise à jour des instructions Copilot.
    1.0.1 - 2026-03-19 - ES-15 : Ajout de la section finale standard du document.
    1.0.2 - 2026-03-20 - ES-15 : Référence au repo via IPTDEVLIB_PROMPTS.
    1.0.3 - 2026-03-20 - ES-15 : Nom du document harmonisé avec le fichier.
    1.0.4 - 2026-03-20 - ES-15 : Clarification du fichier cible à modifier.
    1.0.5 - 2026-03-20 - ES-15 : Fallback harmonisé en notation PowerShell.
-->

# Mise à jour de COPILOT_INSTRUCTIONS_UPDATE.md (repos consommateurs)

Objectif : appliquer les consignes de synchronisation des templates dans les
autres repos.

## Prérequis

- Accès au repo de référence des prompts via la variable d’environnement
  `IPTDEVLIB_PROMPTS` (avec fallback recommandé vers
  `$env:USERPROFILE\Sources\IPTDevLib\prompts`, cf.
  `.github/TEMPLATE_SYNC_CHECK.md`).
- Le fichier .github/TEMPLATE_SYNC_CHECK.md existe dans le repo consommateur.

## Contenu à ajouter dans COPILOT_INSTRUCTIONS_UPDATE.md

Ajouter une section **Synchronisation des templates** (ou mettre à jour
l’existante) avec les deux lignes suivantes :

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
**Version** : 1.0.5  
**Mainteneur** : Pierre Théberge  
**Compagnie** : Innovations, Performances, Technologies inc.
