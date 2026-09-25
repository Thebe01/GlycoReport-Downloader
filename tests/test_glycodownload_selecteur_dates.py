#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Format d'en-tête standard à respecter pour ce projet.
Voir .github/HEADER_TEMPLATE_PYTHON.md pour les détails.

Module        : tests/test_glycodownload_selecteur_dates.py
Type          : Python module
Auteur        : Pierre Théberge
Compagnie     : Innovations, Performances, Technologies inc.
Créé le       : 2026-09-24
Modifié le    : 2026-09-24
Version       : 0.1.0
Copyright     : Pierre Théberge

Description
-----------
Tests unitaires d'ouvrir_selecteur_dates (GlycoDownload.py) : nouveau clic quand le
panneau du sélecteur de dates ne s'ouvre pas. Pilote factice, aucun navigateur.

Modifications
-------------
0.1.0 - 2026-09-24   ES-28 : Version initiale.

Paramètres
----------
N/A.

Exemple
-------
>>> pytest -q tests/test_glycodownload_selecteur_dates.py
"""

import logging
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from selenium.common.exceptions import NoSuchElementException, TimeoutException  # noqa: E402
from selenium.webdriver.common.by import By  # noqa: E402

import GlycoDownload  # noqa: E402
from GlycoDownload import ouvrir_selecteur_dates  # noqa: E402


class _Element:
    def __init__(self, on_click=None):
        self._on_click = on_click

    def is_displayed(self):
        return True

    def is_enabled(self):
        return True

    def click(self):
        if self._on_click:
            self._on_click()


class _Driver:
    """Le panneau s'ouvre au clic numéro ouvre_au_clic (None : jamais)."""

    def __init__(self, ouvre_au_clic):
        self.ouvre_au_clic = ouvre_au_clic
        self.clics = 0
        self._bouton = _Element(on_click=self._clic)

    def _clic(self):
        self.clics += 1

    def find_element(self, by, value):
        if by == By.XPATH and "date-range-picker-toggle" in value:
            return self._bouton
        if by == By.NAME and value == "start_date":
            if self.ouvre_au_clic is not None and self.clics >= self.ouvre_au_clic:
                return _Element()
            raise NoSuchElementException("start_date absent")
        raise NoSuchElementException(value)


@pytest.fixture
def captures(monkeypatch):
    etapes = []
    monkeypatch.setattr(GlycoDownload, "capture_screenshot", lambda d, l, step, *a: etapes.append(step))
    return etapes


def _ouvrir(driver):
    ouvrir_selecteur_dates(
        driver, logging.getLogger("test_selecteur"), "log", "now",
        tentatives=3, attente_panneau=0.01, attente_bouton=0.01,
    )


def test_ouvert_au_premier_clic(captures):
    driver = _Driver(ouvre_au_clic=1)
    _ouvrir(driver)
    assert driver.clics == 1
    assert captures == []


def test_ouvert_au_deuxieme_clic(captures, caplog):
    driver = _Driver(ouvre_au_clic=2)
    with caplog.at_level(logging.INFO, logger="test_selecteur"):
        _ouvrir(driver)
    assert driver.clics == 2
    assert captures == ["selecteur_dates_tentative_1"]
    assert any(r.levelname == "WARNING" for r in caplog.records)
    assert "tentative 2" in caplog.text


def test_jamais_ouvert_leve_timeout(captures):
    driver = _Driver(ouvre_au_clic=None)
    with pytest.raises(TimeoutException):
        _ouvrir(driver)
    assert driver.clics == 3
    assert captures == [f"selecteur_dates_tentative_{i}" for i in (1, 2, 3)]
