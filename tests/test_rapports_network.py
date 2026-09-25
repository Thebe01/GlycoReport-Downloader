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
Modifié le    : 2026-09-25
Version       : 0.7.0
Copyright     : Pierre Théberge

Description
-----------
Tests unitaires ciblés pour la robustesse réseau pendant le traitement des rapports.

Modifications
-------------
0.3.17 - 2026-03-23   [ES-14] : Ajout des tests de reconnexion (succès puis échec persistant).
0.3.19 - 2026-03-25   [ES-14] : Ajout des tests d'intégration de selection_rapport
                               (retry après NetworkRecoveryRetry et propagation de NetworkRecoveryFailedError).
0.5.23 - 2026-09-23   ES-28   : Ajout des tests de reset TCP distant : _handle_network_loss relance
                                le rapport quand l'hôte coupe malgré un accès internet fonctionnel,
                                et telechargement_rapport convertit une ProtocolError en retry.
0.5.24 - 2026-09-23   CR      : Ajout des tests de relance des erreurs de transport non reconnues
                                et de non-deplacement de fichier dans le flux d'export.
0.7.0  - 2026-09-25   ES-29   : Les tests de retry remplacent l'entrée « Aperçu » de
                                TRAITEMENTS_RAPPORTS ; ajout des tests de couverture du dispatch
                                et du rapport inconnu.
0.5.25 - 2026-09-23   CR      : Ajout du test ciblant le bloc de fermeture de modale d'export :
                                les deux clics precedents reussissent, la coupure survient sur la
                                fermeture, et l'assertion verifie le contexte atteint.

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
import types

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from requests.exceptions import ChunkedEncodingError  # noqa: E402
from urllib3.exceptions import ProtocolError  # noqa: E402
from selenium.common.exceptions import WebDriverException  # noqa: E402

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
    monkeypatch.setitem(rapports.TRAITEMENTS_RAPPORTS, "Aperçu", fake_apercu_handler)

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
    monkeypatch.setitem(rapports.TRAITEMENTS_RAPPORTS, "Aperçu", fake_apercu_handler)

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
    monkeypatch.setitem(rapports.TRAITEMENTS_RAPPORTS, "Aperçu", fake_apercu_handler)

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
    monkeypatch.setitem(rapports.TRAITEMENTS_RAPPORTS, "Aperçu", fake_apercu_handler)

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


def test_traitement_rapport_comparer_preserves_selected_dates(monkeypatch):
    """Comparer réapplique ?dates et restaure la page d'origine pour les rapports suivants."""
    logger = logging.getLogger("tests.rapports.comparer.dates")

    class DummyElement:
        def __init__(self, driver, locator=None):
            self.driver = driver
            self.locator = locator

        def click(self):
            xpath = ""
            if self.locator and isinstance(self.locator, tuple) and len(self.locator) == 2:
                xpath = self.locator[1]
            if "/compare/trends" in xpath:
                self.driver.current_url = "https://clarity.dexcom.eu/i/#/compare/trends"

    class DummyDriver:
        def __init__(self):
            self.current_url = "https://clarity.dexcom.eu/i/#/data/daily?dates=2026-04-13%2F2026-04-27"
            self.get_calls = []
            self.title = "Dexcom Clarity"

        def execute_script(self, *_args, **_kwargs):
            return None

        def get(self, url):
            self.get_calls.append(url)
            self.current_url = url

    class DummyWait:
        def __init__(self, driver, _timeout):
            self.driver = driver

        def until(self, condition):
            if callable(condition):
                assert condition(self.driver)
                return True
            if isinstance(condition, tuple) and condition and condition[0] == "clickable":
                return DummyElement(self.driver, condition[1])
            return DummyElement(self.driver)

    driver = DummyDriver()
    recorded_download_urls = []

    monkeypatch.setattr(rapports, "_recover_network_or_fail", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(rapports, "attendre_disparition_overlay", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(rapports.time, "sleep", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(rapports, "WebDriverWait", DummyWait)
    monkeypatch.setattr(
        rapports,
        "_find_clickable_with_xpath_candidates",
        lambda d, *_args, **_kwargs: DummyElement(d),
    )
    monkeypatch.setattr(
        rapports.EC,
        "element_to_be_clickable",
        lambda locator: ("clickable", locator),
    )
    monkeypatch.setattr(
        rapports.EC,
        "presence_of_element_located",
        lambda _locator: ("presence", _locator),
    )
    monkeypatch.setattr(
        rapports,
        "telechargement_rapport",
        lambda *_args, **_kwargs: recorded_download_urls.append(driver.current_url),
    )

    args = types.SimpleNamespace(debug=False)
    rapports.traitement_rapport_comparer(
        "Comparer",
        driver,
        logger,
        DOWNLOAD_DIR=".",
        DIR_FINAL_BASE=".",
        DATE_FIN="2026-04-26",
        DATE_DEBUT="2026-04-13",
        args=args,
    )

    assert recorded_download_urls
    assert "dates=2026-04-13%2F2026-04-27" in recorded_download_urls[0]
    assert driver.get_calls[-1] == "https://clarity.dexcom.eu/i/#/data/daily?dates=2026-04-13%2F2026-04-27"


def test_traitement_rapport_comparer_rebuilds_dates_when_entry_url_lost_them(monkeypatch):
    """Comparer reconstruit ?dates depuis DATE_DEBUT/DATE_FIN si l'URL d'entrée ne l'a plus."""
    logger = logging.getLogger("tests.rapports.comparer.dates.fallback")

    class DummyElement:
        def __init__(self, driver, locator=None):
            self.driver = driver
            self.locator = locator

        def click(self):
            xpath = ""
            if self.locator and isinstance(self.locator, tuple) and len(self.locator) == 2:
                xpath = self.locator[1]
            if "/compare/trends" in xpath:
                self.driver.current_url = "https://clarity.dexcom.eu/i/#/compare/trends"

    class DummyDriver:
        def __init__(self):
            self.current_url = "https://clarity.dexcom.eu/i/#/data/daily"
            self.get_calls = []
            self.title = "Dexcom Clarity"

        def execute_script(self, *_args, **_kwargs):
            return None

        def get(self, url):
            self.get_calls.append(url)
            self.current_url = url

    class DummyWait:
        def __init__(self, driver, _timeout):
            self.driver = driver

        def until(self, condition):
            if callable(condition):
                assert condition(self.driver)
                return True
            if isinstance(condition, tuple) and condition and condition[0] == "clickable":
                return DummyElement(self.driver, condition[1])
            return DummyElement(self.driver)

    driver = DummyDriver()
    recorded_download_urls = []

    monkeypatch.setattr(rapports, "_recover_network_or_fail", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(rapports, "attendre_disparition_overlay", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(rapports.time, "sleep", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(rapports, "WebDriverWait", DummyWait)
    monkeypatch.setattr(
        rapports,
        "_find_clickable_with_xpath_candidates",
        lambda d, *_args, **_kwargs: DummyElement(d),
    )
    monkeypatch.setattr(
        rapports.EC,
        "element_to_be_clickable",
        lambda locator: ("clickable", locator),
    )
    monkeypatch.setattr(
        rapports.EC,
        "presence_of_element_located",
        lambda _locator: ("presence", _locator),
    )
    monkeypatch.setattr(
        rapports,
        "telechargement_rapport",
        lambda *_args, **_kwargs: recorded_download_urls.append(driver.current_url),
    )

    args = types.SimpleNamespace(debug=False)
    rapports.traitement_rapport_comparer(
        "Comparer",
        driver,
        logger,
        DOWNLOAD_DIR=".",
        DIR_FINAL_BASE=".",
        DATE_FIN="2026-04-26",
        DATE_DEBUT="2026-04-13",
        args=args,
    )

    assert recorded_download_urls
    assert "dates=2026-04-13%2F2026-04-27" in recorded_download_urls[0]
    assert driver.get_calls[-1] == "https://clarity.dexcom.eu/i/#/data/daily?dates=2026-04-13%2F2026-04-27"


def test_traitement_rapport_comparer_reapplies_dates_if_removed_before_download(monkeypatch):
    """Comparer réapplique les dates si Dexcom les retire après chargement initial."""
    logger = logging.getLogger("tests.rapports.comparer.dates.reapply-before-download")

    class DummyElement:
        def __init__(self, driver, locator=None):
            self.driver = driver
            self.locator = locator

        def click(self):
            xpath = ""
            if self.locator and isinstance(self.locator, tuple) and len(self.locator) == 2:
                xpath = self.locator[1]
            if "/compare/trends" in xpath:
                # Simule un premier état correct (avec dates) juste après clic.
                self.driver.current_url = "https://clarity.dexcom.eu/i/#/compare/trends?dates=2026-04-13%2F2026-04-27"

    class DummyDriver:
        def __init__(self):
            self.current_url = "https://clarity.dexcom.eu/i/#/data/daily?dates=2026-04-13%2F2026-04-27"
            self.get_calls = []
            self.title = "Dexcom Clarity"

        def execute_script(self, *_args, **_kwargs):
            return None

        def get(self, url):
            self.get_calls.append(url)
            self.current_url = url

    class DummyWait:
        def __init__(self, driver, _timeout):
            self.driver = driver

        def until(self, condition):
            if callable(condition):
                assert condition(self.driver)
                return True
            if isinstance(condition, tuple) and condition and condition[0] == "clickable":
                return DummyElement(self.driver, condition[1])
            return DummyElement(self.driver)

    driver = DummyDriver()
    recorded_download_urls = []

    def fake_attendre_disparition_overlay(*_args, **_kwargs):
        # Simule un retrait tardif des dates par Dexcom après le premier chargement.
        if "/compare/trends" in (driver.current_url or ""):
            driver.current_url = "https://clarity.dexcom.eu/i/#/compare/trends"

    monkeypatch.setattr(rapports, "_recover_network_or_fail", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(rapports, "attendre_disparition_overlay", fake_attendre_disparition_overlay)
    monkeypatch.setattr(rapports.time, "sleep", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(rapports, "WebDriverWait", DummyWait)
    monkeypatch.setattr(
        rapports,
        "_find_clickable_with_xpath_candidates",
        lambda d, *_args, **_kwargs: DummyElement(d),
    )
    monkeypatch.setattr(
        rapports.EC,
        "element_to_be_clickable",
        lambda locator: ("clickable", locator),
    )
    monkeypatch.setattr(
        rapports.EC,
        "presence_of_element_located",
        lambda _locator: ("presence", _locator),
    )
    monkeypatch.setattr(
        rapports,
        "telechargement_rapport",
        lambda *_args, **_kwargs: recorded_download_urls.append(driver.current_url),
    )

    args = types.SimpleNamespace(debug=False)
    rapports.traitement_rapport_comparer(
        "Comparer",
        driver,
        logger,
        DOWNLOAD_DIR=".",
        DIR_FINAL_BASE=".",
        DATE_FIN="2026-04-26",
        DATE_DEBUT="2026-04-13",
        args=args,
    )

    assert recorded_download_urls
    assert "dates=2026-04-13%2F2026-04-27" in recorded_download_urls[0]


# --- ES-28 : reset TCP ferme par l'hote distant (incident du 2026-09-15 14:02:12) ---

def _reset_emballe():
    """Reproduit la forme exacte du 10054 journalise : reset emballe par urllib3 puis requests."""
    reset = ConnectionResetError(
        10054, "Une connexion existante a du etre fermee par l'hote distant", None, 10054, None
    )
    return ChunkedEncodingError(ProtocolError(f"Connection broken: {reset!r}", reset))


def test_handle_network_loss_relance_le_rapport_sur_reset_distant(monkeypatch, caplog):
    """L'acces internet repond, mais l'hote a coupe : il faut quand meme reessayer.

    C'est le cas du 2026-09-15 : check_internet renvoyait vrai, donc l'incident
    n'etait pas traite et le rapport etait abandonne en silence.
    """
    monkeypatch.setattr(rapports, "check_internet", lambda *_a, **_k: True)
    logger = logging.getLogger("tests.rapports.network.reset.distant")

    with caplog.at_level(logging.WARNING, logger=logger.name):
        with pytest.raises(rapports.NetworkRecoveryRetry):
            rapports._handle_network_loss(logger, "test reset distant", _reset_emballe())

    assert "hote distant" in caplog.text or "hôte distant" in caplog.text


def test_handle_network_loss_ignore_une_erreur_selenium_avec_internet_ok(monkeypatch):
    """Une vraie erreur Selenium ne doit pas etre transformee en retry reseau."""
    monkeypatch.setattr(rapports, "check_internet", lambda *_a, **_k: True)
    logger = logging.getLogger("tests.rapports.network.selenium.ok")

    assert rapports._handle_network_loss(
        logger, "test erreur selenium", WebDriverException("element introuvable")
    ) is None


def test_telechargement_rapport_convertit_un_reset_en_retry(monkeypatch):
    """Le reset doit etre rattrape par l'except du site de telechargement, pas s'echapper.

    Avant ES-28, ProtocolError n'etant ni WebDriverException ni OSError, elle traversait
    tous les except et remontait jusqu'au gestionnaire principal de GlycoDownload.
    """
    monkeypatch.setattr(rapports, "_recover_network_or_fail", lambda *_a, **_k: None)
    monkeypatch.setattr(rapports, "check_internet", lambda *_a, **_k: True)
    monkeypatch.setattr(rapports.time, "sleep", lambda *_a, **_k: None)

    def overlay_coupe(*_args, **_kwargs):
        raise _reset_emballe()

    monkeypatch.setattr(rapports, "attendre_disparition_overlay", overlay_coupe)

    logger = logging.getLogger("tests.rapports.network.telechargement.reset")
    with pytest.raises(rapports.NetworkRecoveryRetry):
        rapports.telechargement_rapport(
            "Aperçu",
            driver=object(),
            logger=logger,
            DOWNLOAD_DIR=".",
            DIR_FINAL_BASE=".",
            DATE_FIN="2026-09-13",
            DATE_DEBUT="2026-08-31",
            args=types.SimpleNamespace(debug=False),
        )


# --- CR : une erreur de transport non reconnue ne doit pas etre avalee ---

def test_handle_network_loss_relance_une_erreur_de_transport_non_reset(monkeypatch):
    """Ni reset, ni perte d'acces : l'exception doit remonter, pas disparaitre.

    Sans cette relance, _handle_network_loss retournait None et l'appelant se contentait
    de journaliser puis de sortir : le rapport etait abandonne sans erreur visible.
    """
    monkeypatch.setattr(rapports, "check_internet", lambda *_a, **_k: True)
    logger = logging.getLogger("tests.rapports.network.transport.inconnu")
    transport = ChunkedEncodingError("reponse tronquee sans reset")

    with pytest.raises(ChunkedEncodingError):
        rapports._handle_network_loss(logger, "test transport inconnu", transport)


def test_export_csv_ne_poursuit_pas_apres_une_erreur_de_transport(monkeypatch):
    """Une erreur de transport dans le flux d'export ne doit pas mener au deplacement.

    Le flux d'export est le plus expose : son bloc de fermeture de modale journalise en
    warning sans return, donc il poursuit vers wait_for_csv_download puis le deplacement
    du fichier. Tant que _handle_network_loss avalait l'exception, le traitement se
    terminait comme si le rapport etait valide. Ce test verrouille l'invariant du flux :
    une erreur de transport remonte, et aucun fichier n'est deplace.
    """
    monkeypatch.setattr(rapports, "_recover_network_or_fail", lambda *_a, **_k: None)
    monkeypatch.setattr(rapports, "check_internet", lambda *_a, **_k: True)
    monkeypatch.setattr(rapports.time, "sleep", lambda *_a, **_k: None)

    deplacements = []
    monkeypatch.setattr(
        rapports,
        "deplace_et_renomme_rapport",
        lambda *_a, **_k: deplacements.append(True),
    )
    monkeypatch.setattr(rapports, "wait_for_csv_download", lambda *_a, **_k: True)

    def clic_qui_coupe(*_args, **_kwargs):
        raise ChunkedEncodingError("reponse tronquee sans reset")

    monkeypatch.setattr(rapports, "attendre_disparition_overlay", clic_qui_coupe)

    logger = logging.getLogger("tests.rapports.network.export.transport")
    with pytest.raises(ChunkedEncodingError):
        rapports.traitement_export_csv(
            "Export",
            driver=object(),
            logger=logger,
            DOWNLOAD_DIR=".",
            DIR_FINAL_BASE=".",
            DATE_FIN="2026-09-13",
            DATE_DEBUT="2026-08-31",
            args=types.SimpleNamespace(debug=False),
        )

    assert deplacements == [], "aucun fichier ne doit etre deplace apres une erreur de transport"


def test_export_csv_ne_deplace_rien_si_la_fermeture_de_modale_coupe(monkeypatch):
    """Cible le bloc de fermeture de modale, le seul sans return apres le handler.

    Les deux clics precedents reussissent, la coupure survient sur la fermeture. C'est le
    chemin le plus dangereux : sans return, le traitement poursuivait jusqu'au deplacement
    du fichier, donc une erreur de transport y produisait un rapport d'apparence valide.
    """

    class DummyElement:
        def click(self):
            return None

    class DummyDriver:
        def execute_script(self, *_args, **_kwargs):
            return None

    class DummyWait:
        """Laisse passer les deux premiers until, coupe sur le troisieme."""

        appels = {"n": 0}

        def __init__(self, _driver, _timeout):
            pass

        def until(self, _condition):
            DummyWait.appels["n"] += 1
            if DummyWait.appels["n"] >= 3:
                raise ChunkedEncodingError("reponse tronquee sans reset")
            return DummyElement()

    monkeypatch.setattr(rapports, "_recover_network_or_fail", lambda *_a, **_k: None)
    monkeypatch.setattr(rapports, "check_internet", lambda *_a, **_k: True)
    monkeypatch.setattr(rapports.time, "sleep", lambda *_a, **_k: None)
    monkeypatch.setattr(rapports, "attendre_disparition_overlay", lambda *_a, **_k: None)
    monkeypatch.setattr(rapports, "WebDriverWait", DummyWait)
    monkeypatch.setattr(
        rapports.EC, "element_to_be_clickable", lambda locator: ("clickable", locator)
    )

    contextes = []
    vrai_handler = rapports._handle_network_loss
    monkeypatch.setattr(
        rapports,
        "_handle_network_loss",
        lambda logger, contexte, exc: (
            contextes.append(contexte), vrai_handler(logger, contexte, exc)
        )[1],
    )

    deplacements = []
    monkeypatch.setattr(rapports, "wait_for_csv_download", lambda *_a, **_k: True)
    monkeypatch.setattr(
        rapports,
        "deplace_et_renomme_rapport",
        lambda *_a, **_k: deplacements.append(True),
    )

    logger = logging.getLogger("tests.rapports.network.export.fermeture")
    with pytest.raises(ChunkedEncodingError):
        rapports.traitement_export_csv(
            "Export",
            driver=DummyDriver(),
            logger=logger,
            DOWNLOAD_DIR=".",
            DIR_FINAL_BASE=".",
            DATE_FIN="2026-09-13",
            DATE_DEBUT="2026-08-31",
            args=types.SimpleNamespace(debug=False),
        )

    assert contextes == ["fermeture de la fenêtre modale d'export"], (
        f"le test doit atteindre le bloc de fermeture de modale, pas {contextes}"
    )
    assert deplacements == [], "aucun fichier ne doit etre deplace"


def test_traitements_rapports_couvre_tous_les_rapports():
    """Chaque rapport de --list-rapports a un traitement dans le dispatch."""
    assert set(rapports.TRAITEMENTS_RAPPORTS) == {
        "Aperçu", "Modèles", "Superposition", "Quotidien",
        "Comparer", "Statistiques", "AGP", "Export",
    }


def test_selection_rapport_rapport_inconnu_journalise_sans_planter(monkeypatch, caplog):
    """Un nom de rapport absent du dispatch est journalisé en erreur, sans exception."""
    monkeypatch.setattr(rapports, "_recover_network_or_fail", lambda _logger, _contexte: None)

    logger = logging.getLogger("tests.rapports.network.selection.inconnu")
    with caplog.at_level(logging.ERROR, logger=logger.name):
        rapports.selection_rapport(
            ["Inexistant"],
            driver=object(),
            logger=logger,
            DOWNLOAD_DIR=".",
            DIR_FINAL_BASE=".",
            DATE_FIN="2026-03-25",
            DATE_DEBUT="2026-03-01",
            args=object(),
        )

    assert "Rapport inconnu : Inexistant" in caplog.text
