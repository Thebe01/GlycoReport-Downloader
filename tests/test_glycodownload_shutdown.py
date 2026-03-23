#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Format d'en-tête standard à respecter pour ce projet.
Voir .github/HEADER_TEMPLATE_PYTHON.md pour les détails.

Module        : tests/test_glycodownload_shutdown.py
Type          : Python module
Auteur        : Pierre Théberge
Compagnie     : Innovations, Performances, Technologies inc.
Créé le       : 2026-03-23
Modifié le    : 2026-03-23
Version       : 0.3.17
Copyright     : Pierre Théberge

Description
-----------
Tests unitaires pour la fermeture de session navigateur en fin de traitement.

Modifications
-------------
0.3.17 - 2026-03-23   [ES-14] : Ajout des tests unitaires de fermeture onglet/navigateur (single-tab vs multi-tab).

Paramètres
----------
N/A.

Exemple
-------
>>> pytest -q tests/test_glycodownload_shutdown.py
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from GlycoDownload import close_browser_session  # noqa: E402


class DummyLogger:
    def __init__(self):
        self.messages = []

    def info(self, msg, *args):
        self.messages.append(("info", msg % args if args else msg))

    def debug(self, msg, *args, **kwargs):
        self.messages.append(("debug", msg % args if args else msg))

    def warning(self, msg, *args, **kwargs):
        self.messages.append(("warning", msg % args if args else msg))


class DummyDriver:
    def __init__(self, handles, cdp_raises=False, close_raises=False):
        self.window_handles = handles
        self.cdp_raises = cdp_raises
        self.close_raises = close_raises
        self.cdp_calls = []
        self.close_called = 0
        self.quit_called = 0

    def execute_cdp_cmd(self, cmd, payload):
        self.cdp_calls.append((cmd, payload))
        if self.cdp_raises:
            raise RuntimeError("cdp error")

    def close(self):
        self.close_called += 1
        if self.close_raises:
            raise RuntimeError("close error")

    def quit(self):
        self.quit_called += 1


def test_close_browser_session_single_tab_uses_browser_close():
    logger = DummyLogger()
    driver = DummyDriver(handles=["tab-1"])

    close_browser_session(driver, logger, debug=True)

    assert driver.cdp_calls == [("Browser.close", {})]
    assert driver.close_called == 0
    assert driver.quit_called == 0


def test_close_browser_session_single_tab_fallbacks_to_quit_when_cdp_fails():
    logger = DummyLogger()
    driver = DummyDriver(handles=["tab-1"], cdp_raises=True)

    close_browser_session(driver, logger, debug=True)

    assert driver.cdp_calls == [("Browser.close", {})]
    assert driver.quit_called == 1


def test_close_browser_session_multi_tab_closes_only_current_tab():
    logger = DummyLogger()
    driver = DummyDriver(handles=["tab-1", "tab-2"])

    close_browser_session(driver, logger, debug=True)

    assert driver.cdp_calls == []
    assert driver.close_called == 1
    assert driver.quit_called == 0


def test_close_browser_session_multi_tab_fallbacks_to_quit_if_close_fails():
    logger = DummyLogger()
    driver = DummyDriver(handles=["tab-1", "tab-2"], close_raises=True)

    close_browser_session(driver, logger, debug=True)

    assert driver.close_called == 1
    assert driver.quit_called == 1
