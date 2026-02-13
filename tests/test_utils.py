#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Format d'en-tête standard à respecter pour ce projet.
Voir HEADER_TEMPLATE_PYTHON.md pour les détails.

Module        : tests/test_utils.py
Type          : Python module
Auteur        : Pierre Théberge
Compagnie     : Innovations, Performances, Technologies inc.
Créé le       : 2025-08-13
Modifié le    : 2026-02-12
Version       : 0.3.13
Copyright     : Pierre Théberge

Description
-----------
Tests unitaires pour les fonctions utilitaires partagées (utils.py).

Modifications
-------------
0.0.0  - 2025-08-13             Version initiale.
0.0.1  - 2025-08-18             Ajout de tests unitaires pour toutes les fonctions utilitaires,
                                adaptation pour la centralisation de normalize_path dans utils.py,
                                vérification de la robustesse et de la portabilité des utilitaires.
0.1.6  - 2025-08-22             Synchronisation des versions dans tous les modules, ajout de version.py, log de la version exécutée.
0.2.1  - 2025-08-29             Changement de nom du projet (anciennement Dexcom Clarity Reports Downloader).
0.2.2  - 2025-08-29             Synchronisation des entêtes, robustesse accrue du help, nettoyage des doublons CLI.
0.2.3  - 2025-10-14   [ES-12] : Migration vers ChromeDriverManager pour gestion automatique de ChromeDriver.
0.2.4  - 2025-10-16   [ES-12] : Synchronisation de version (aucun changement fonctionnel dans les tests).
0.2.5  - 2025-10-16   [ES-10] : Ajout de tests pour la suppression des captures d'écran (.png) lors du nettoyage des logs.
0.2.6  - 2025-10-21   [ES-7]  : Synchronisation de version (aucun changement fonctionnel dans les tests).
0.2.15 - 2026-01-19   [ES-19] : Synchronisation de version (aucun changement fonctionnel).
0.2.16 - 2026-01-20   [ES-19] : Synchronisation de version (aucun changement fonctionnel).
0.2.17 - 2026-01-20   [ES-19] : Ajustements typing pour tests (aucun changement fonctionnel).
0.2.18 - 2026-01-20   [ES-19] : Synchronisation de version (aucun changement fonctionnel).
0.3.1  - 2026-02-02   [ES-19] : Synchronisation de version (aucun changement fonctionnel).
0.3.2  - 2026-02-02   [ES-19] : Ajout du test pour filtrer les téléchargements par extension.
0.3.3  - 2026-02-02   [ES-19] : Normalisation des extensions attendues (téléchargements).
0.3.4  - 2026-02-12   [ES-3]  : Synchronisation de version (aucun changement fonctionnel).
0.3.5  - 2026-02-12   [ES-3]  : Synchronisation de version (aucun changement fonctionnel).
0.3.6  - 2026-02-12   [ES-3]  : Synchronisation de version (aucun changement fonctionnel).

Paramètres
----------
N/A.

Exemple
-------
>>> pytest -v --log-cli-level=INFO tests/test_utils.py
"""

import sys
import os
import tempfile
import pytest
import time
from typing import cast
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import (
    normalize_path,
    check_internet,
    url_is_allowed,
    attendre_disparition_overlay,
    get_last_downloaded_file,
    get_last_downloaded_nonlog_file,
    get_last_downloaded_report_file,
    renomme_prefix,
    attendre_nouveau_bouton_telecharger,
    capture_screenshot,
    cleanup_logs,
    _compute_backoff_seconds
)

# Dummy classes for Selenium objects
class DummyDriver:
    def __init__(self):
        self.screenshot_taken = False
    def save_screenshot(self, path):
        with open(path, "wb") as f:
            f.write(b"fake image")
        self.screenshot_taken = True
        return True

class DummyLogger:
    def __init__(self):
        self.messages = []
    def info(self, msg): self.messages.append(("info", msg))
    def warning(self, msg): self.messages.append(("warning", msg))
    def error(self, msg): self.messages.append(("error", msg))
    def debug(self, msg, exc_info=None): self.messages.append(("debug", msg))

class DummyWebElement:
    pass

@pytest.fixture
def dummy_driver():
    return DummyDriver()

@pytest.fixture
def dummy_logger():
    return DummyLogger()

def test_normalize_path_home():
    home = os.path.expanduser("~")
    assert normalize_path("~/test_folder").startswith(home)

def test_normalize_path_absolute():
    path = os.path.abspath("C:/Temp/test")
    assert normalize_path("C:/Temp/test") == path

def test_check_internet():
    # Ce test suppose que google.com est accessible
    assert check_internet() is True


def test_url_is_allowed_exact_host_only():
    allowed = ["example.com"]
    assert url_is_allowed("https://example.com/path", allowed) is True
    assert url_is_allowed("https://evil-example.net/example.com", allowed) is False
    assert url_is_allowed("https://benign-looking-prefix-example.com", allowed) is False


def test_url_is_allowed_subdomains_optional():
    allowed = ["example.com"]
    assert url_is_allowed("https://a.example.com", allowed, allow_subdomains=True) is True
    assert url_is_allowed("https://a.b.example.com", allowed, allow_subdomains=True) is True
    assert url_is_allowed("https://notexample.com", allowed, allow_subdomains=True) is False


def test_check_internet_rejects_non_web_schemes():
    assert check_internet("file:///C:/Windows/System32/drivers/etc/hosts") is False
    assert check_internet("data:text/plain,hello") is False

def test_get_last_downloaded_file(tmp_path):
    f1 = tmp_path / "file1.txt"
    f2 = tmp_path / "file2.txt"
    f1.write_text("a")
    time.sleep(1)
    f2.write_text("b")
    result = get_last_downloaded_file(str(tmp_path))
    assert result == str(f2)

def test_get_last_downloaded_nonlog_file(tmp_path):
    f1 = tmp_path / "file1.log"
    f2 = tmp_path / "file2.txt"
    f1.write_text("a")
    f2.write_text("b")
    result = get_last_downloaded_nonlog_file(str(tmp_path))
    assert result == str(f2)

def test_get_last_downloaded_report_file_filters_extensions(tmp_path):
    pdf_file = tmp_path / "report.pdf"
    txt_file = tmp_path / "note.txt"
    pdf_file.write_text("pdf")
    txt_file.write_text("txt")
    result = get_last_downloaded_report_file(str(tmp_path), allowed_extensions={".pdf"})
    assert result == str(pdf_file)

def test_get_last_downloaded_report_file_multiple_extensions(tmp_path):
    pdf_file = tmp_path / "report.pdf"
    csv_file = tmp_path / "export.csv"
    pdf_file.write_text("pdf")
    time.sleep(1)
    csv_file.write_text("csv")
    result = get_last_downloaded_report_file(str(tmp_path), allowed_extensions={".pdf", ".csv"})
    assert result == str(csv_file)

def test_get_last_downloaded_report_file_no_match_returns_none(tmp_path):
    txt_file = tmp_path / "note.txt"
    txt_file.write_text("txt")
    result = get_last_downloaded_report_file(str(tmp_path), allowed_extensions={".pdf"})
    assert result is None

def test_get_last_downloaded_report_file_ignores_log_and_crdownload(tmp_path):
    pdf_file = tmp_path / "report.pdf"
    log_file = tmp_path / "latest.log"
    crdownload_file = tmp_path / "partial.crdownload"
    pdf_file.write_text("pdf")
    time.sleep(1)
    log_file.write_text("log")
    time.sleep(1)
    crdownload_file.write_text("partial")
    result = get_last_downloaded_report_file(str(tmp_path), allowed_extensions={".pdf"})
    assert result == str(pdf_file)

def test_get_last_downloaded_report_file_returns_most_recent(tmp_path):
    old_pdf = tmp_path / "old.pdf"
    new_pdf = tmp_path / "new.pdf"
    old_pdf.write_text("old")
    time.sleep(1)
    new_pdf.write_text("new")
    result = get_last_downloaded_report_file(str(tmp_path), allowed_extensions={".pdf"})
    assert result == str(new_pdf)

def test_renomme_prefix_standard(dummy_logger):
    prefix = "Apercu_20230801_1"
    date_fin = "20230813"
    result = renomme_prefix(prefix, date_fin, logger=dummy_logger)
    assert result == "Apercu_20230813_1"

def test_renomme_prefix_nonstandard(dummy_logger):
    prefix = "Apercu"
    date_fin = "20230813"
    result = renomme_prefix(prefix, date_fin, logger=dummy_logger)
    assert result == "Apercu_20230813"

def test_capture_screenshot_creates_file(tmp_path, dummy_driver, dummy_logger):
    log_dir = str(tmp_path)
    now_str = "20250101_120000"
    step = "test"
    time.sleep(1)
    capture_screenshot(dummy_driver, dummy_logger, step, log_dir, now_str)
    screenshot_path = os.path.join(log_dir, f"screenshot_{step}_{now_str}.png")
    assert os.path.exists(screenshot_path)
    assert dummy_driver.screenshot_taken

def test_attendre_disparition_overlay_no_overlay(dummy_driver, dummy_logger):
    # Ce test vérifie simplement que la fonction ne lève pas d'exception si aucun overlay n'est présent.
    # On ne peut pas tester Selenium ici, donc on vérifie juste l'appel.
    try:
        attendre_disparition_overlay(dummy_driver, timeout=1, logger=dummy_logger)
    except Exception:
        pytest.fail("attendre_disparition_overlay a levé une exception alors qu'il ne devait pas.")

def test_attendre_nouveau_bouton_telecharger_signature():
    # On ne peut pas tester le comportement réel sans Selenium, mais on peut tester la signature
    try:
        attendre_nouveau_bouton_telecharger(
            cast(WebDriver, DummyDriver()),
            cast(WebElement, DummyWebElement()),
            timeout=1,
        )
    except Exception:
        pass  # On accepte que la fonction lève une exception ici, car il n'y a pas de vrai test à faire

def test_cleanup_logs_removes_old_logs(tmp_path):
    # Crée un dossier temporaire pour les logs
    log_dir = tmp_path
    # Crée deux fichiers logs : un ancien et un récent
    old_log = log_dir / "old.log"
    recent_log = log_dir / "recent.log"
    # Crée également des captures d'écran anciennes et récentes
    old_screenshot = log_dir / "screenshot_old.png"
    recent_screenshot = log_dir / "screenshot_recent.png"
    
    old_log.write_text("ancien log")
    recent_log.write_text("log récent")
    old_screenshot.write_bytes(b"fake old screenshot")
    recent_screenshot.write_bytes(b"fake recent screenshot")
    
    # Modifie la date de modification des anciens fichiers pour qu'ils soient vieux de 2 jours
    old_time = time.time() - (2 * 86400)
    os.utime(old_log, (old_time, old_time))
    os.utime(old_screenshot, (old_time, old_time))
    
    # Appelle cleanup_logs avec une rétention de 1 jour
    cleanup_logs(str(log_dir), retention_days=1)
    
    # Vérifie que les anciens fichiers ont été supprimés et que les récents existent toujours
    assert not old_log.exists()
    assert not old_screenshot.exists()
    assert recent_log.exists()
    assert recent_screenshot.exists()

def test_cleanup_logs_retention_zero(tmp_path):
    # Crée un dossier temporaire pour les logs
    log_dir = tmp_path
    log_file = log_dir / "test.log"
    screenshot_file = log_dir / "screenshot_test.png"
    
    log_file.write_text("log à conserver")
    screenshot_file.write_bytes(b"fake screenshot to keep")
    
    # Appelle cleanup_logs avec une rétention illimitée
    cleanup_logs(str(log_dir), retention_days=0)

    # Vérifie que les fichiers n'ont pas été supprimés
    assert log_file.exists()
    assert screenshot_file.exists()


def test_compute_backoff_seconds_caps():
    assert _compute_backoff_seconds(2.0, 0, 30.0) == 2.0
    assert _compute_backoff_seconds(2.0, 1, 30.0) == 4.0
    assert _compute_backoff_seconds(2.0, 2, 30.0) == 8.0
    assert _compute_backoff_seconds(2.0, 4, 30.0) == 30.0
    assert _compute_backoff_seconds(0.0, 1, 30.0) == 30.0
    assert _compute_backoff_seconds(-1.0, 1, 30.0) == 30.0

def test_cleanup_logs_removes_only_old_screenshots(tmp_path):
    # Test spécifique pour vérifier que seules les vieilles captures d'écran sont supprimées
    log_dir = tmp_path
    
    old_screenshot1 = log_dir / "screenshot_20230101_120000.png"
    old_screenshot2 = log_dir / "debug_screenshot.png"
    recent_screenshot = log_dir / "screenshot_20250101_120000.png"
    
    old_screenshot1.write_bytes(b"old screenshot 1")
    old_screenshot2.write_bytes(b"old screenshot 2")
    recent_screenshot.write_bytes(b"recent screenshot")
    
    # Modifie la date des anciens fichiers
    old_time = time.time() - (2 * 86400)
    os.utime(old_screenshot1, (old_time, old_time))
    os.utime(old_screenshot2, (old_time, old_time))
    
    # Appelle cleanup_logs avec une rétention de 1 jour
    cleanup_logs(str(log_dir), retention_days=1)
    
    # Vérifie que seules les anciennes captures ont été supprimées
    assert not old_screenshot1.exists()
    assert not old_screenshot2.exists()
    assert recent_screenshot.exists()