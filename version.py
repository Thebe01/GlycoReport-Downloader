#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Format d'en-tête standard à respecter pour ce projet.
Voir .github/HEADER_TEMPLATE_PYTHON.md pour les détails.

Module        : version.py
Type          : Python module
Auteur        : Pierre Théberge
Compagnie     : Innovations, Performances, Technologies inc.
Créé le       : 2025-08-22
Modifié le    : 2026-02-12
Version       : 0.3.13
Copyright     : Pierre Théberge

Description
-----------
Source unique de vérité pour la version de l'application.

Modifications
-------------
0.2.15 - 2026-01-19   [ES-19] : Synchronisation de version (aucun changement fonctionnel).
0.2.16 - 2026-01-20   [ES-19] : Bump de version patch (release 0.2.16).
0.2.17 - 2026-01-20   [ES-19] : Bump de version patch (release 0.2.17).
0.2.18 - 2026-01-20   [ES-19] : Bump de version patch (release 0.2.18).
0.3.0  - 2026-01-29   [ES-19] : Bump de version minor (release 0.3.0).
0.3.1  - 2026-02-02   [ES-19] : Bump de version patch (release 0.3.1).
0.3.2  - 2026-02-02   [ES-19] : Bump de version patch (release 0.3.2).
0.3.3  - 2026-02-02   [ES-19] : Bump de version patch (release 0.3.3).
0.3.4  - 2026-02-12   [ES-3]  : Bump de version patch (release 0.3.4).
0.3.5  - 2026-02-12   [ES-3]  : Bump de version patch (release 0.3.5).
0.3.6  - 2026-02-12   [ES-3]  : Bump de version patch (release 0.3.6).
0.3.7  - 2026-02-12   [ES-3]  : Attente contenu graphique + délai génération PDF Comparer.
0.3.8  - 2026-02-12   [ES-3]  : Fermeture/réouverture modale Comparer entre sous-rapports.
0.3.9  - 2026-02-12   [ES-3]  : Navigation /overview et /reports avec dates pour Comparer.
0.3.10 - 2026-02-12   [ES-3]  : Retry clics Comparer et navigation overview->reports.
0.3.11 - 2026-02-12   [ES-3]  : Navigation URL base /i pour Comparer.
0.3.12 - 2026-02-12   [ES-3]  : Acces direct /compare/overlay et /compare/daily.
0.3.13 - 2026-02-12   [ES-3]  : Comparer: telecharger Tendances seulement (bug Dexcom).

Paramètres
----------
N/A.

Exemple
-------
>>> from version import __version__
>>> print(__version__)
"""

__version__ = "0.3.13"