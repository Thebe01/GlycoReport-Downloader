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
Modifié le    : 2026-09-25
Version       : 0.1.4
Copyright     : Pierre Théberge

Description
-----------
Tests unitaires d'ouvrir_selecteur_dates (GlycoDownload.py) : nouveau clic quand le
panneau du sélecteur de dates ne s'ouvre pas. Pilote factice, aucun navigateur.

Modifications
-------------
0.1.0 - 2026-09-24   ES-28 : Version initiale.
0.1.1 - 2026-09-24   CR    : Tests du repli JavaScript (clic intercepté) et de l'attente sans
                             nouveau clic quand le panneau est déjà présent.
0.1.2 - 2026-09-25   CR    : Panneau lent rendu déterministe : actif après le constat de la
                             protection, et non selon le nombre de vérifications de WebDriverWait.
0.1.3 - 2026-09-25   CR    : Texte du WARNING vérifié ; panneau déjà ouvert avant le 1er clic.
0.1.4 - 2026-09-25   CR    : Message de l'exception finale vérifié ; panneau présent jamais cliquable.

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

from selenium.common.exceptions import (  # noqa: E402
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.common.by import By  # noqa: E402

import GlycoDownload  # noqa: E402
from GlycoDownload import ouvrir_selecteur_dates  # noqa: E402


class _Element:
    def __init__(self, on_click=None, intercepte=False, actif=lambda: True):
        self._on_click = on_click
        self.intercepte = intercepte
        self._actif = actif

    def is_displayed(self):
        return True

    def is_enabled(self):
        return self._actif()

    def click(self):
        if self.intercepte:
            raise ElementClickInterceptedException("overlay")
        if self._on_click:
            self._on_click()


class _Driver:
    """Le panneau s'ouvre au clic numéro ouvre_au_clic (None : jamais).

    lent : start_date présent mais inactif tant que la protection (find_elements) ne
    l'a pas constaté ; indépendant du nombre de vérifications de WebDriverWait.
    """

    def __init__(self, ouvre_au_clic, intercepte=False, lent=False, inactif=False):
        self.ouvre_au_clic = ouvre_au_clic
        self.clics = 0
        self.lent = lent
        self.inactif = inactif
        self.constats = 0
        self.clics_js = 0
        self._bouton = _Element(on_click=self._clic, intercepte=intercepte)

    def execute_script(self, script, element):
        assert element is self._bouton
        self.clics_js += 1
        self._clic()

    def _clic(self):
        self.clics += 1

    def _panneau_ouvert(self):
        return self.ouvre_au_clic is not None and self.clics >= self.ouvre_au_clic

    def find_elements(self, by, value):
        if by == By.NAME and value == "start_date" and self._panneau_ouvert():
            self.constats += 1
            return [_Element()]
        return []

    def find_element(self, by, value):
        if by == By.XPATH and "date-range-picker-toggle" in value:
            return self._bouton
        if by == By.NAME and value == "start_date":
            if self._panneau_ouvert():
                return _Element(actif=lambda: not self.inactif and (not self.lent or self.constats > 0))
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
    with pytest.raises(TimeoutException, match="non utilisable après 3 tentatives"):
        _ouvrir(driver)
    assert driver.clics == 3
    assert captures == [f"selecteur_dates_tentative_{i}" for i in (1, 2, 3)]


def test_clic_intercepte_repli_javascript(captures):
    driver = _Driver(ouvre_au_clic=1, intercepte=True)
    _ouvrir(driver)
    assert driver.clics_js == 1
    assert captures == []


def test_panneau_present_pas_de_nouveau_clic(captures, caplog):
    # Le panneau s'ouvre au 1er clic mais start_date reste inactif un moment :
    # un 2e clic le refermerait (bascule).
    driver = _Driver(ouvre_au_clic=1, lent=True)
    with caplog.at_level(logging.WARNING, logger="test_selecteur"):
        _ouvrir(driver)
    assert driver.clics == 1
    assert driver.constats == 1
    assert captures == ["selecteur_dates_tentative_1"]
    avertissements = [r.getMessage() for r in caplog.records if r.levelname == "WARNING"]
    assert avertissements == ["Panneau du sélecteur de dates non utilisable 0.01 s après la tentative 1/3."]


def test_panneau_deja_ouvert_avant_le_premier_clic(captures):
    # Panneau laissé ouvert avant le lancement : aucun clic, sinon la bascule le refermerait.
    driver = _Driver(ouvre_au_clic=0)
    _ouvrir(driver)
    assert driver.clics == 0
    assert captures == []


def test_panneau_present_jamais_cliquable(captures):
    # Panneau présent mais inutilisable : un seul clic, puis attente sans clic ;
    # le message final ne doit pas prétendre que le panneau est fermé.
    driver = _Driver(ouvre_au_clic=1, inactif=True)
    with pytest.raises(TimeoutException, match="non utilisable après 3 tentatives"):
        _ouvrir(driver)
    assert driver.clics == 1
    assert captures == [f"selecteur_dates_tentative_{i}" for i in (1, 2, 3)]
