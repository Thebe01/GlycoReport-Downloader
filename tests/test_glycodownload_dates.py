#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Format d'en-tête standard à respecter pour ce projet.
Voir .github/HEADER_TEMPLATE_PYTHON.md pour les détails.

Module        : tests/test_glycodownload_dates.py
Type          : Python module
Auteur        : Pierre Théberge
Compagnie     : Innovations, Performances, Technologies inc.
Créé le       : 2026-04-14
Modifié le    : 2026-04-15
Version       : 0.1.0
Copyright     : Pierre Théberge

Description
-----------
Tests unitaires pour resolve_effective_date_range (GlycoDownload.py).

Couvre la chaîne de priorité :
  1. CLI date_debut + date_fin (les deux fournis)
  2. CLI --days
  3. config.yaml days
  4. config.yaml date_debut / date_fin

Modifications
-------------
0.0.0 - 2026-04-14   [ES-21] : Version initiale.
0.1.0 - 2026-04-15   [ES-25] : Dates CLI partielles : ValueError attendue (garde defensif).
                               Ajout de test_only_date_debut_raises_value_error
                               et de test_only_date_fin_raises_value_error.

Paramètres
----------
N/A.

Exemple
-------
>>> pytest -q tests/test_glycodownload_dates.py
"""

import sys
import os
import pytest
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from GlycoDownload import resolve_effective_date_range

# Date fixe pour rendre les tests déterministes (un mardi quelconque)
TODAY = datetime(2026, 4, 14)

# Valeurs de config par défaut utilisées quand la priorité n'active pas autre chose
CONFIG_DATE_DEBUT = "2025-01-01"
CONFIG_DATE_FIN = "2025-01-31"


class TestResolveDateRange:

    # ------------------------------------------------------------------
    # Priorité 1 — CLI date_debut + date_fin explicites
    # ------------------------------------------------------------------

    def test_cli_explicit_dates_take_priority_over_everything(self):
        """CLI date_debut + date_fin priment sur --days CLI et config days."""
        debut, fin = resolve_effective_date_range(
            args_days=30,
            args_date_debut="2025-06-01",
            args_date_fin="2025-06-30",
            config_days=90,
            config_date_debut=CONFIG_DATE_DEBUT,
            config_date_fin=CONFIG_DATE_FIN,
            today=TODAY,
        )
        assert debut == "2025-06-01"
        assert fin == "2025-06-30"

    def test_cli_explicit_dates_take_priority_over_config_days(self):
        """CLI dates priment sur config days même sans --days CLI."""
        debut, fin = resolve_effective_date_range(
            args_days=None,
            args_date_debut="2025-03-01",
            args_date_fin="2025-03-31",
            config_days=14,
            config_date_debut=CONFIG_DATE_DEBUT,
            config_date_fin=CONFIG_DATE_FIN,
            today=TODAY,
        )
        assert debut == "2025-03-01"
        assert fin == "2025-03-31"

    def test_only_date_debut_raises_value_error(self):
        """Seulement date_debut fournie (sans date_fin) → ValueError (dates partielles refusées)."""
        with pytest.raises(ValueError, match="date_debut"):
            resolve_effective_date_range(
                args_days=7,
                args_date_debut="2025-03-01",
                args_date_fin=None,
                config_days=None,
                config_date_debut=CONFIG_DATE_DEBUT,
                config_date_fin=CONFIG_DATE_FIN,
                today=TODAY,
            )

    def test_only_date_fin_raises_value_error(self):
        """Seulement date_fin fournie (sans date_debut) → ValueError (dates partielles refusées)."""
        with pytest.raises(ValueError, match="date_fin"):
            resolve_effective_date_range(
                args_days=None,
                args_date_debut=None,
                args_date_fin="2025-03-31",
                config_days=None,
                config_date_debut=CONFIG_DATE_DEBUT,
                config_date_fin=CONFIG_DATE_FIN,
                today=TODAY,
            )

    # ------------------------------------------------------------------
    # Priorité 2 — CLI --days
    # ------------------------------------------------------------------

    def test_cli_days_produces_rolling_window(self):
        """--days N depuis CLI calcule la fenêtre glissante à partir d'aujourd'hui."""
        debut, fin = resolve_effective_date_range(
            args_days=7,
            args_date_debut=None,
            args_date_fin=None,
            config_days=None,
            config_date_debut=CONFIG_DATE_DEBUT,
            config_date_fin=CONFIG_DATE_FIN,
            today=TODAY,
        )
        expected_fin = (TODAY - timedelta(days=1)).strftime("%Y-%m-%d")
        expected_debut = (TODAY - timedelta(days=7)).strftime("%Y-%m-%d")
        assert fin == expected_fin
        assert debut == expected_debut

    def test_cli_days_overrides_config_days(self):
        """CLI --days prime sur config.yaml days."""
        debut, fin = resolve_effective_date_range(
            args_days=14,
            args_date_debut=None,
            args_date_fin=None,
            config_days=90,
            config_date_debut=CONFIG_DATE_DEBUT,
            config_date_fin=CONFIG_DATE_FIN,
            today=TODAY,
        )
        expected_fin = (TODAY - timedelta(days=1)).strftime("%Y-%m-%d")
        expected_debut = (TODAY - timedelta(days=14)).strftime("%Y-%m-%d")
        assert fin == expected_fin
        assert debut == expected_debut

    # ------------------------------------------------------------------
    # Priorité 3 — config.yaml days
    # ------------------------------------------------------------------

    def test_config_days_produces_rolling_window(self):
        """config.yaml days calcule la fenêtre glissante quand CLI est vide."""
        debut, fin = resolve_effective_date_range(
            args_days=None,
            args_date_debut=None,
            args_date_fin=None,
            config_days=30,
            config_date_debut=CONFIG_DATE_DEBUT,
            config_date_fin=CONFIG_DATE_FIN,
            today=TODAY,
        )
        expected_fin = (TODAY - timedelta(days=1)).strftime("%Y-%m-%d")
        expected_debut = (TODAY - timedelta(days=30)).strftime("%Y-%m-%d")
        assert fin == expected_fin
        assert debut == expected_debut

    # ------------------------------------------------------------------
    # Priorité 4 — config.yaml date_debut / date_fin
    # ------------------------------------------------------------------

    def test_falls_back_to_config_dates(self):
        """Quand rien n'est fourni, retourne les dates du config.yaml."""
        debut, fin = resolve_effective_date_range(
            args_days=None,
            args_date_debut=None,
            args_date_fin=None,
            config_days=None,
            config_date_debut=CONFIG_DATE_DEBUT,
            config_date_fin=CONFIG_DATE_FIN,
            today=TODAY,
        )
        assert debut == CONFIG_DATE_DEBUT
        assert fin == CONFIG_DATE_FIN

    # ------------------------------------------------------------------
    # Cas limites
    # ------------------------------------------------------------------

    def test_days_1_means_only_yesterday(self):
        """days=1 → date_debut == date_fin == hier."""
        debut, fin = resolve_effective_date_range(
            args_days=1,
            args_date_debut=None,
            args_date_fin=None,
            config_days=None,
            config_date_debut=CONFIG_DATE_DEBUT,
            config_date_fin=CONFIG_DATE_FIN,
            today=TODAY,
        )
        yesterday = (TODAY - timedelta(days=1)).strftime("%Y-%m-%d")
        assert debut == yesterday
        assert fin == yesterday

    def test_today_parameter_is_honoured(self):
        """Le paramètre today= est bien utilisé au lieu de datetime.today()."""
        custom_today = datetime(2025, 12, 25)
        debut, fin = resolve_effective_date_range(
            args_days=7,
            args_date_debut=None,
            args_date_fin=None,
            config_days=None,
            config_date_debut=CONFIG_DATE_DEBUT,
            config_date_fin=CONFIG_DATE_FIN,
            today=custom_today,
        )
        assert fin == "2025-12-24"
        assert debut == "2025-12-18"
