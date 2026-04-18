#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Format d'en-tête standard à respecter pour ce projet.
Voir .github/HEADER_TEMPLATE_PYTHON.md pour les détails.

Module        : tests/test_config_validation.py
Type          : Python module
Auteur        : Pierre Théberge
Compagnie     : Innovations, Performances, Technologies inc.
Créé le       : 2026-04-17
Modifié le    : 2026-04-17
Version       : 0.1.0
Copyright     : Pierre Théberge

Description
-----------
Tests unitaires pour validate_config (config.py).

Couvre la validation du paramètre 'days' : type, valeurs autorisées {7,14,30,90},
avertissement si conflit avec date_debut/date_fin.

Modifications
-------------
0.1.0 - 2026-04-17   [ES-26] : Version initiale.

Paramètres
----------
N/A.

Exemple
-------
>>> pytest -q tests/test_config_validation.py
"""

import logging
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import validate_config

# Config minimale valide (satisfait tous les required_keys + URL)
_BASE = {
    "download_dir": "/tmp/test",
    "output_dir": "/tmp/test",
    "dexcom_url": "https://clarity.dexcom.eu",
    "chromedriver_log": "/tmp/chromedriver.log",
    "chrome_user_data_dir": "/tmp/chrome_profile",
    "rapports": ["Aperçu"],
    "log_retention_days": 30,
}


def _config(**kwargs):
    return {**_BASE, **kwargs}


class TestValidateConfigDays:
    """Tests pour la validation du paramètre 'days' dans validate_config."""

    # ------------------------------------------------------------------
    # Valeurs valides (pas de sys.exit)
    # ------------------------------------------------------------------

    def test_days_absent_passes(self):
        validate_config(_config())

    def test_days_none_passes(self):
        validate_config(_config(days=None))

    def test_days_int_7_passes(self):
        validate_config(_config(days=7))

    def test_days_int_14_passes(self):
        validate_config(_config(days=14))

    def test_days_int_30_passes(self):
        validate_config(_config(days=30))

    def test_days_int_90_passes(self):
        validate_config(_config(days=90))

    def test_days_string_14_passes(self):
        validate_config(_config(days="14"))

    def test_days_string_90_passes(self):
        validate_config(_config(days="90"))

    # ------------------------------------------------------------------
    # Valeur hors de l'ensemble autorisé → sys.exit(1)
    # ------------------------------------------------------------------

    def test_days_int_5_exits(self):
        with pytest.raises(SystemExit):
            validate_config(_config(days=5))

    def test_days_int_0_exits(self):
        with pytest.raises(SystemExit):
            validate_config(_config(days=0))

    def test_days_int_365_exits(self):
        with pytest.raises(SystemExit):
            validate_config(_config(days=365))

    def test_days_string_invalid_number_exits(self):
        with pytest.raises(SystemExit):
            validate_config(_config(days="5"))

    # ------------------------------------------------------------------
    # Type invalide → sys.exit(1)
    # ------------------------------------------------------------------

    def test_days_float_exits(self):
        with pytest.raises(SystemExit):
            validate_config(_config(days=14.0))

    def test_days_non_numeric_string_exits(self):
        with pytest.raises(SystemExit):
            validate_config(_config(days="quatorze"))

    def test_days_list_exits(self):
        with pytest.raises(SystemExit):
            validate_config(_config(days=[14]))

    # ------------------------------------------------------------------
    # Avertissement si conflit avec date_debut / date_fin
    # ------------------------------------------------------------------

    def test_days_with_date_debut_logs_warning(self, caplog):
        with caplog.at_level(logging.WARNING):
            validate_config(_config(days=14, date_debut="2025-01-01"))
        assert "days" in caplog.text.lower() or "prioritaire" in caplog.text.lower()

    def test_days_with_date_fin_logs_warning(self, caplog):
        with caplog.at_level(logging.WARNING):
            validate_config(_config(days=30, date_fin="2025-01-31"))
        assert "days" in caplog.text.lower() or "prioritaire" in caplog.text.lower()
