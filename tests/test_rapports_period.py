#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Format d'en-tête standard à respecter pour ce projet.
Voir .github/HEADER_TEMPLATE_PYTHON.md pour les détails.

Module        : tests/test_rapports_period.py
Type          : Python module
Auteur        : Pierre Théberge
Compagnie     : Innovations, Performances, Technologies inc.
Créé le       : 2026-04-17
Modifié le    : 2026-07-09
Version       : 0.1.2
Copyright     : Pierre Théberge

Description
-----------
Tests unitaires pour get_period_suffix (rapports.py).

Modifications
-------------
0.1.0 - 2026-04-17   [ES-26] : Version initiale.
0.1.1 - 2026-06-11   [ES-27] : Mocks mis à jour vers locale.getlocale() (locale.getdefaultlocale()
                               déprécié depuis Python 3.11).
0.1.2 - 2026-07-09   [CR]    : Ajout de tests pour la capture/restauration de
                               setlocale(LC_CTYPE) : restauration de la valeur précédente,
                               usage exclusif de LC_CTYPE (jamais LC_ALL), résilience si
                               setlocale échoue à la lecture ou à la restauration.

Paramètres
----------
N/A.

Exemple
-------
>>> pytest -q tests/test_rapports_period.py
"""

import locale
import os
import sys
import types

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rapports import get_period_suffix


def _args(days=None):
    return types.SimpleNamespace(days=days)


class TestGetPeriodSuffix:

    # ------------------------------------------------------------------
    # Priorité args.days
    # ------------------------------------------------------------------

    def test_uses_args_days_when_provided(self):
        suffix = get_period_suffix("2025-01-01", "2025-01-31", _args(days=14))
        assert suffix is not None
        assert suffix.startswith("14")

    def test_args_days_zero_falls_back_to_dates(self):
        # days=0 est falsy → repli sur le calcul depuis les dates (14 jours)
        suffix = get_period_suffix("2025-01-01", "2025-01-14", _args(days=0))
        assert suffix is not None
        assert suffix.startswith("14")

    def test_args_days_negative_returns_none(self):
        assert get_period_suffix("2025-01-01", "2025-01-31", _args(days=-5)) is None

    # ------------------------------------------------------------------
    # Calcul depuis date_debut / date_fin
    # ------------------------------------------------------------------

    def test_calculates_14_days_from_dates(self):
        # 2025-01-01 à 2025-01-14 inclus = 14 jours
        suffix = get_period_suffix("2025-01-01", "2025-01-14", _args())
        assert suffix is not None
        assert suffix.startswith("14")

    def test_single_day_period(self):
        suffix = get_period_suffix("2025-01-01", "2025-01-01", _args())
        assert suffix is not None
        assert suffix.startswith("1")

    def test_invalid_date_format_returns_none(self):
        assert get_period_suffix("01-01-2025", "2025-01-31", _args()) is None

    # ------------------------------------------------------------------
    # Valeurs manquantes
    # ------------------------------------------------------------------

    def test_missing_date_debut_returns_none(self):
        assert get_period_suffix(None, "2025-01-31", _args()) is None

    def test_missing_date_fin_returns_none(self):
        assert get_period_suffix("2025-01-01", None, _args()) is None

    def test_both_dates_missing_returns_none(self):
        assert get_period_suffix(None, None, _args()) is None

    def test_none_args_uses_dates(self):
        suffix = get_period_suffix("2025-01-01", "2025-01-07", None)
        assert suffix is not None
        assert suffix.startswith("7")

    # ------------------------------------------------------------------
    # Locale — unité j (français) vs d (autres)
    # ------------------------------------------------------------------

    def test_unit_j_for_french_locale(self, monkeypatch):
        monkeypatch.setattr(locale, "getlocale", lambda cat=None: ("fr_CA", "UTF-8"))
        suffix = get_period_suffix("2025-01-01", "2025-01-14", _args())
        assert suffix == "14j"

    def test_unit_d_for_english_locale(self, monkeypatch):
        monkeypatch.setattr(locale, "getlocale", lambda cat=None: ("en_US", "UTF-8"))
        suffix = get_period_suffix("2025-01-01", "2025-01-14", _args())
        assert suffix == "14d"

    def test_unit_d_when_locale_is_none(self, monkeypatch):
        monkeypatch.setattr(locale, "getlocale", lambda cat=None: (None, None))
        suffix = get_period_suffix("2025-01-01", "2025-01-14", _args())
        assert suffix == "14d"

    # ------------------------------------------------------------------
    # Locale — capture/restauration de setlocale(LC_CTYPE) (ES-27 / CR)
    # ------------------------------------------------------------------

    def test_setlocale_restores_previous_locale(self, monkeypatch):
        calls = []

        def fake_setlocale(category, loc=None):
            calls.append((category, loc))
            return "C" if loc is None else loc

        monkeypatch.setattr(locale, "setlocale", fake_setlocale)
        monkeypatch.setattr(locale, "getlocale", lambda cat=None: ("fr_CA", "UTF-8"))

        suffix = get_period_suffix("2025-01-01", "2025-01-14", _args())

        assert suffix == "14j"
        # Premier appel : requête de la locale courante (sans second argument).
        assert calls[0] == (locale.LC_CTYPE, None)
        # Dernier appel : restauration explicite vers la valeur précédente capturée.
        assert calls[-1] == (locale.LC_CTYPE, "C")
        # Uniquement LC_CTYPE, jamais LC_ALL (pas d'effet de bord sur tout le processus).
        assert all(cat == locale.LC_CTYPE for cat, _ in calls)

    def test_setlocale_error_when_setting_is_handled(self, monkeypatch):
        def fake_setlocale(category, loc=None):
            if loc == "":
                raise locale.Error("simulated failure")
            return "C"

        monkeypatch.setattr(locale, "setlocale", fake_setlocale)

        suffix = get_period_suffix("2025-01-01", "2025-01-14", _args())

        assert suffix == "14d"

    def test_setlocale_restore_error_is_swallowed(self, monkeypatch):
        def fake_setlocale(category, loc=None):
            if loc is None:
                return "C"
            if loc == "":
                return "fr_FR.UTF-8"
            raise locale.Error("simulated restore failure")

        monkeypatch.setattr(locale, "setlocale", fake_setlocale)
        monkeypatch.setattr(locale, "getlocale", lambda cat=None: ("fr_CA", "UTF-8"))

        suffix = get_period_suffix("2025-01-01", "2025-01-14", _args())

        assert suffix == "14j"
