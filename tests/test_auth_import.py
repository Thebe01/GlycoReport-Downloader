#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Format d'en-tête standard à respecter pour ce projet.
Voir .github/HEADER_TEMPLATE_PYTHON.md pour les détails.

Module        : tests/test_auth_import.py
Type          : Python module
Auteur        : Pierre Théberge
Compagnie     : Innovations, Performances, Technologies inc.
Créé le       : 2026-09-25
Modifié le    : 2026-09-25
Version       : 0.7.0
Copyright     : Pierre Théberge

Description
-----------
Garanties d'import du module auth.py, sans navigateur. Le chemin de connexion
n'est pas testable en exécution réelle : Cloudflare bloque la saisie automatisée,
l'application démarre donc après une connexion manuelle (mode reprise).

Modifications
-------------
0.7.0 - 2026-09-25   ES-29 : Version initiale.

Paramètres
----------
N/A (exécuté par pytest).

Exemple
-------
>>> python -m pytest -q tests/test_auth_import.py
"""

import os
import subprocess
import sys

import auth
import GlycoDownload

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_glycodownload_utilise_saisir_identifiants_de_auth():
    """GlycoDownload appelle la fonction déplacée, pas une copie restée sur place."""
    assert GlycoDownload.saisir_identifiants is auth.saisir_identifiants


def test_import_auth_ne_charge_pas_config():
    """config valide .env et config.yaml dès son import : auth ne doit pas le charger.

    Exécuté dans un processus séparé, car d'autres tests ont déjà importé config.
    """
    code = "import sys, auth, GlycoDownload; print('config' in sys.modules)"
    resultat = subprocess.run(
        [sys.executable, "-c", code],
        cwd=RACINE,
        capture_output=True,
        text=True,
        check=True,
    )
    assert resultat.stdout.strip() == "False"
