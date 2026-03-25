#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Format d'en-tête standard à respecter pour ce projet.
Voir .github/HEADER_TEMPLATE_PYTHON.md pour les détails.

Module        : tests/test_rapports_network.py
Type          : Python module
Auteur        : Pierre Théberge
Compagnie     : Innovations, Performances, Technologies inc.
Créé le       : 2026-03-23
Modifié le    : 2026-03-25
Version       : 0.3.19
Copyright     : Pierre Théberge

Description
-----------
Tests unitaires ciblés pour la robustesse réseau pendant le traitement des rapports.

Modifications
-------------
0.3.17 - 2026-03-23   [ES-14] : Ajout des tests de reconnexion (succès puis échec persistant).
0.3.19 - 2026-03-25   [ES-14] : Ajout des tests d'intégration de selection_rapport
                               (retry après NetworkRecoveryRetry et propagation de NetworkRecoveryFailedError).

Paramètres
----------
N/A.

Exemple
-------
>>> pytest -q tests/test_rapports_network.py
"""

import logging
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import rapports  # noqa: E402


def test_recover_network_or_fail_recovers_after_retry(monkeypatch, caplog):
    """La reconnexion réussit au 3e check (1 initial + 2 retries)."""
    checks = []
    states = iter([False, False, True])

    def fake_check_internet():
        checks.append(1)
        return next(states)

    monkeypatch.setattr(rapports, "check_internet", fake_check_internet)
    monkeypatch.setattr(rapports.time, "sleep", lambda _: None)

    logger = logging.getLogger("tests.rapports.network.success")
    with caplog.at_level(logging.INFO):
        rapports._recover_network_or_fail(
            logger,
            "test reconnexion succes",
            attempts=3,
            delay_seconds=1,
        )

    assert len(checks) == 3
    assert "Connexion internet rétablie" in caplog.text


def test_recover_network_or_fail_raises_when_network_stays_down(monkeypatch):
    """La reconnexion échoue après tous les essais -> exception fatale."""
    checks = []

    def fake_check_internet():
        checks.append(1)
        return False

    monkeypatch.setattr(rapports, "check_internet", fake_check_internet)
    monkeypatch.setattr(rapports.time, "sleep", lambda _: None)

    logger = logging.getLogger("tests.rapports.network.failure")
    with pytest.raises(rapports.NetworkRecoveryFailedError) as exc_info:
        rapports._recover_network_or_fail(
            logger,
            "test reconnexion echec",
            attempts=3,
            delay_seconds=1,
        )

    # 1 check initial + 3 checks après chaque attente de retry.
    assert len(checks) == 4
    assert "Perte de connexion internet persistante" in str(exc_info.value)


def test_selection_rapport_retries_report_once_after_network_recovery(monkeypatch):
    """selection_rapport relance le même rapport après NetworkRecoveryRetry."""
    calls = {"recover": 0, "handler": 0}

    def fake_recover(_logger, _contexte):
        calls["recover"] += 1

    def fake_apercu_handler(*_args, **_kwargs):
        calls["handler"] += 1
        if calls["handler"] == 1:
            raise rapports.NetworkRecoveryRetry("retry demandé")

    monkeypatch.setattr(rapports, "_recover_network_or_fail", fake_recover)
    monkeypatch.setattr(rapports, "traitement_rapport_apercu", fake_apercu_handler)

    logger = logging.getLogger("tests.rapports.network.selection.retry")
    rapports.selection_rapport(
        ["Aperçu"],
        driver=object(),
        logger=logger,
        DOWNLOAD_DIR=".",
        DIR_FINAL_BASE=".",
        DATE_FIN="2026-03-25",
        DATE_DEBUT="2026-03-01",
        args=object(),
    )

    assert calls["handler"] == 2
    assert calls["recover"] == 2


def test_selection_rapport_retries_report_multiple_times_then_succeeds(monkeypatch):
    """selection_rapport supporte plusieurs retries réseau avant succès."""
    calls = {"recover": 0, "handler": 0}

    def fake_recover(_logger, _contexte):
        calls["recover"] += 1

    def fake_apercu_handler(*_args, **_kwargs):
        calls["handler"] += 1
        if calls["handler"] <= 2:
            raise rapports.NetworkRecoveryRetry("retry demandé")

    monkeypatch.setattr(rapports, "_recover_network_or_fail", fake_recover)
    monkeypatch.setattr(rapports, "traitement_rapport_apercu", fake_apercu_handler)

    logger = logging.getLogger("tests.rapports.network.selection.multi-retry")
    rapports.selection_rapport(
        ["Aperçu"],
        driver=object(),
        logger=logger,
        DOWNLOAD_DIR=".",
        DIR_FINAL_BASE=".",
        DATE_FIN="2026-03-25",
        DATE_DEBUT="2026-03-01",
        args=object(),
    )

    assert calls["handler"] == 3
    assert calls["recover"] == 3


def test_selection_rapport_raises_after_max_network_retries(monkeypatch):
    """selection_rapport abandonne proprement après dépassement du max de retries."""
    calls = {"recover": 0, "handler": 0}

    def fake_recover(_logger, _contexte):
        calls["recover"] += 1

    def fake_apercu_handler(*_args, **_kwargs):
        calls["handler"] += 1
        raise rapports.NetworkRecoveryRetry("retry demandé")

    monkeypatch.setattr(rapports, "_recover_network_or_fail", fake_recover)
    monkeypatch.setattr(rapports, "traitement_rapport_apercu", fake_apercu_handler)

    logger = logging.getLogger("tests.rapports.network.selection.max-retries")
    with pytest.raises(rapports.NetworkRecoveryFailedError):
        rapports.selection_rapport(
            ["Aperçu"],
            driver=object(),
            logger=logger,
            DOWNLOAD_DIR=".",
            DIR_FINAL_BASE=".",
            DATE_FIN="2026-03-25",
            DATE_DEBUT="2026-03-01",
            args=object(),
        )

    assert calls["handler"] == 3
    assert calls["recover"] == 3


def test_selection_rapport_propagates_network_recovery_failed(monkeypatch):
    """selection_rapport remonte l'exception fatale si la reconnexion échoue."""
    calls = {"handler": 0}

    def fake_recover(_logger, _contexte):
        raise rapports.NetworkRecoveryFailedError("réseau indisponible")

    def fake_apercu_handler(*_args, **_kwargs):
        calls["handler"] += 1

    monkeypatch.setattr(rapports, "_recover_network_or_fail", fake_recover)
    monkeypatch.setattr(rapports, "traitement_rapport_apercu", fake_apercu_handler)

    logger = logging.getLogger("tests.rapports.network.selection.failed")
    with pytest.raises(rapports.NetworkRecoveryFailedError):
        rapports.selection_rapport(
            ["Aperçu"],
            driver=object(),
            logger=logger,
            DOWNLOAD_DIR=".",
            DIR_FINAL_BASE=".",
            DATE_FIN="2026-03-25",
            DATE_DEBUT="2026-03-01",
            args=object(),
        )

    assert calls["handler"] == 0
