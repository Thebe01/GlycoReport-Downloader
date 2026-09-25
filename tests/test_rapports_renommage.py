#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Format d'en-tête standard à respecter pour ce projet.
Voir .github/HEADER_TEMPLATE_PYTHON.md pour les détails.

Module        : tests/test_rapports_renommage.py
Type          : Python module
Auteur        : Pierre Théberge
Compagnie     : Innovations, Performances, Technologies inc.
Créé le       : 2026-09-24
Modifié le    : 2026-09-24
Version       : 0.1.0
Copyright     : Pierre Théberge

Description
-----------
Tests unitaires du renommage des rapports (relance sur WinError 32), du filtre
depuis de get_last_downloaded_report_file, du bilan et de pause_on_error.

Modifications
-------------
0.1.0 - 2026-09-24   ES-28 : Version initiale.

Paramètres
----------
N/A.

Exemple
-------
>>> pytest -q tests/test_rapports_renommage.py
"""

import logging
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import rapports
import utils
from rapports import _remplacer_avec_relance, calculer_rapports_manquants, ecrire_bilan
from utils import get_last_downloaded_report_file, pause_on_error


def _verrou():
    e = PermissionError(13, "fichier utilisé par un autre processus")
    e.winerror = 32
    return e


class _Horloge:
    """Horloge factice : time.sleep avance time.monotonic."""

    def __init__(self):
        self.t = 0.0

    def monotonic(self):
        return self.t

    def sleep(self, secondes):
        self.t += secondes


@pytest.fixture
def horloge(monkeypatch):
    h = _Horloge()
    monkeypatch.setattr(rapports.time, "monotonic", h.monotonic)
    monkeypatch.setattr(rapports.time, "sleep", h.sleep)
    return h


@pytest.fixture
def logger():
    return logging.getLogger("test_renommage")


# --- _remplacer_avec_relance ---

def test_renommage_direct(monkeypatch, horloge, logger):
    appels = []
    monkeypatch.setattr(rapports.os, "replace", lambda s, d: appels.append((s, d)))
    assert _remplacer_avec_relance("a.pdf", "b.pdf", logger) is True
    assert appels == [("a.pdf", "b.pdf")]


def test_relance_tant_que_verrou_puis_succes(monkeypatch, horloge, logger):
    resultats = [_verrou(), _verrou(), None]

    def faux_replace(s, d):
        r = resultats.pop(0)
        if r:
            raise r

    monkeypatch.setattr(rapports.os, "replace", faux_replace)
    assert _remplacer_avec_relance("a.pdf", "b.pdf", logger) is True
    assert resultats == []
    assert horloge.t == 4  # deux attentes de 2 s


def test_abandon_apres_delai_max(monkeypatch, horloge, logger, caplog):
    def toujours_verrouille(s, d):
        raise _verrou()

    monkeypatch.setattr(rapports.os, "replace", toujours_verrouille)
    with caplog.at_level(logging.ERROR, logger="test_renommage"):
        assert _remplacer_avec_relance("a.pdf", "b.pdf", logger, delai_max=120, intervalle=2) is False
    assert horloge.t == 120
    assert "Erreur lors du renommage" in caplog.text


def test_autre_erreur_sans_relance(monkeypatch, horloge, logger):
    appels = []

    def introuvable(s, d):
        appels.append(1)
        raise FileNotFoundError(2, "introuvable")

    monkeypatch.setattr(rapports.os, "replace", introuvable)
    assert _remplacer_avec_relance("a.pdf", "b.pdf", logger) is False
    assert len(appels) == 1
    assert horloge.t == 0


# --- get_last_downloaded_report_file(depuis=...) ---

def test_depuis_ecarte_les_fichiers_anterieurs(tmp_path, monkeypatch):
    ancien = tmp_path / "clarity_ancien.pdf"
    nouveau = tmp_path / "clarity_nouveau.pdf"
    ancien.write_bytes(b"%PDF")
    nouveau.write_bytes(b"%PDF")
    dates = {str(ancien): 100.0, str(nouveau): 200.0}
    monkeypatch.setattr(utils, "_date_creation", lambda p: dates[p])
    monkeypatch.setattr(utils.os.path, "getctime", lambda p: dates[p])

    assert get_last_downloaded_report_file(str(tmp_path), {".pdf"}, depuis=150.0) == str(nouveau)


def test_depuis_orphelin_seul_retourne_none(tmp_path, monkeypatch):
    orphelin = tmp_path / "clarity_orphelin.pdf"
    orphelin.write_bytes(b"%PDF")
    monkeypatch.setattr(utils, "_date_creation", lambda p: 100.0)

    assert get_last_downloaded_report_file(str(tmp_path), {".pdf"}, depuis=150.0) is None


def test_sans_depuis_comportement_inchange(tmp_path):
    fichier = tmp_path / "clarity.pdf"
    fichier.write_bytes(b"%PDF")
    assert get_last_downloaded_report_file(str(tmp_path), {".pdf"}) == str(fichier)


# --- Bilan ---

def test_manquants_tente_sans_succes():
    tentes = ["Statistiques-Quotidiennes", "Statistiques-Horaires"]
    reussis = {"Statistiques-Quotidiennes"}
    assert calculer_rapports_manquants(["Statistiques"], tentes, reussis) == ["Statistiques-Horaires"]


def test_manquants_demande_jamais_tente():
    assert calculer_rapports_manquants(["Aperçu", "AGP"], ["Aperçu"], {"Aperçu"}) == ["AGP"]


def test_manquants_sous_rapport_couvre_la_demande():
    tentes = ["Comparer-Tendances"]
    assert calculer_rapports_manquants(["Comparer"], tentes, {"Comparer-Tendances"}) == []


def test_ecrire_bilan_erreur_si_manquant(logger, caplog):
    rapports._bilan_reinitialiser()
    rapports._bilan_tente("Aperçu")
    rapports._bilan_tente("AGP")
    rapports._BILAN["reussis"].add("Aperçu")
    rapports._BILAN["sautes"].append("Comparer-Quotidien")
    with caplog.at_level(logging.INFO, logger="test_renommage"):
        manquants = ecrire_bilan(logger, ["Aperçu", "AGP"])
    assert manquants == ["AGP"]
    niveaux = {r.levelname for r in caplog.records}
    assert {"INFO", "WARNING", "ERROR"} <= niveaux
    rapports._bilan_reinitialiser()


# --- pause_on_error ---

class _Stdin:
    def __init__(self, tty):
        self._tty = tty

    def isatty(self):
        return self._tty


@pytest.mark.parametrize(
    "stdin, interactive, attendu",
    [
        (_Stdin(True), True, True),
        (_Stdin(True), False, False),   # tâche planifiée hors session : console, mais invisible
        (_Stdin(False), True, False),
        (None, True, False),            # exécutable --windowed : pas de stdin
    ],
)
def test_pause_seulement_en_mode_interactif(monkeypatch, stdin, interactive, attendu):
    appels = []
    monkeypatch.setattr(utils.sys, "stdin", stdin)
    monkeypatch.setattr(utils, "session_interactive", lambda: interactive)
    monkeypatch.setattr("builtins.input", lambda *a: appels.append(a))
    pause_on_error()
    assert bool(appels) is attendu
