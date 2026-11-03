#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Format d'en-tête standard à respecter pour ce projet.
Voir .github/HEADER_TEMPLATE_PYTHON.md pour les détails.

Module        : tests/test_requirements_lock.py
Type          : Python module
Auteur        : Pierre Théberge
Compagnie     : Innovations, Performances, Technologies inc.
Créé le       : 2026-10-29
Modifié le    : 2026-10-29
Version       : 0.0.0
Copyright     : Pierre Théberge

Description
-----------
Cohérence entre requirements.txt, requirements-dev.txt et requirements.lock.
DIST-GlycoReport-Downloader.ps1 exige que l'interpréteur de build corresponde au
lock ; ces tests garantissent que le lock respecte lui-même les bornes déclarées
(une borne relevée sans régénérer le lock, ou l'inverse, est détectée ici).

Modifications
-------------
0.0.0 - 2026-10-29   ES-30 : Version initiale.

Paramètres
----------
N/A (exécuté par pytest).

Exemple
-------
>>> python -m pytest -q tests/test_requirements_lock.py
"""

import os
import re

import pytest
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Même format que celui accepté par Assert-RequirementsLock (DIST-GlycoReport-Downloader.ps1).
LIGNE_LOCK = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)==(\S+)$")


def _lignes_utiles(nom_fichier):
    with open(os.path.join(RACINE, nom_fichier), encoding="utf-8") as fichier:
        for ligne in fichier:
            ligne = ligne.strip()
            if ligne and not ligne.startswith("#"):
                yield ligne


def _exigences():
    """Exigences directes de requirements.txt et requirements-dev.txt (sans -r)."""
    exigences = []
    for nom_fichier in ("requirements.txt", "requirements-dev.txt"):
        for ligne in _lignes_utiles(nom_fichier):
            if not ligne.startswith("-"):
                exigences.append(Requirement(ligne))
    return exigences


def _lock():
    versions = {}
    for ligne in _lignes_utiles("requirements.lock"):
        correspondance = LIGNE_LOCK.match(ligne)
        assert correspondance, f"Ligne invalide dans requirements.lock : {ligne}"
        versions[canonicalize_name(correspondance.group(1))] = correspondance.group(2)
    return versions


def test_lock_ne_contient_que_des_versions_exactes():
    assert _lock(), "requirements.lock est vide."


@pytest.mark.parametrize("exigence", _exigences(), ids=lambda e: e.name)
def test_lock_respecte_les_bornes(exigence):
    versions = _lock()
    nom = canonicalize_name(exigence.name)
    assert nom in versions, f"{exigence.name} absent de requirements.lock."
    assert exigence.specifier.contains(versions[nom], prereleases=True), (
        f"requirements.lock fige {exigence.name}=={versions[nom]}, hors de {exigence}."
    )


@pytest.mark.parametrize("nom", ["cryptography", "pyyaml"])
def test_dependances_critiques_bornees(nom):
    """Une majeure de cryptography ou de PyYAML peut rompre le chiffrement du .env ou la config."""
    exigence = next(e for e in _exigences() if canonicalize_name(e.name) == nom)
    assert any(spec.operator == "<" for spec in exigence.specifier), (
        f"{exigence} n'a pas de borne supérieure."
    )
