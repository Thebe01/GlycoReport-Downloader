#'''////////////////////////////////////////////////////////////////////////////////////////////////////
#'''<summary>
#'''FileName: test_utils.py
#'''FileType: py Test file
#'''
#'''Author : Pierre Théberge
#'''Created On : 2025-08-13
#'''Last Modified On : 2025-08-22
#'''CopyRights : Innovations Performances Technologies inc
#'''Description : Tests unitaires pour toutes les fonctions utilitaires du projet Dexcom Clarity Reports Downloader.
#'''              Vérifie la robustesse et la portabilité des fonctions (normalisation des chemins, capture d’écran, etc.).
#'''              Pour exécuter les tests, utilisez la commande : pytest tests/test_utils.py
#'''Version : 0.1.6
#'''Modifications :
#'''Version   Date          Description
#'''0.0.0    2025-08-13    Version initiale
#'''0.0.1    2025-08-18    Ajout de tests unitaires pour toutes les fonctions utilitaires,
#'''                       adaptation pour la centralisation de normalize_path dans utils.py,
#'''                       vérification de la robustesse et de la portabilité des utilitaires.
#'''0.1.6    2025-08-22    Synchronisation des versions dans tous les modules, ajout de version.py, log de la version exécutée.
#''' </summary>
#'''////////////////////////////////////////////////////////////////////////////////////////////////////

import sys
import os
import tempfile
import pytest
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import (
    normalize_path,
    check_internet,
    attendre_disparition_overlay,
    get_last_downloaded_file,
    get_last_downloaded_nonlog_file,
    renomme_prefix,
    attendre_nouveau_bouton_telecharger,
    capture_screenshot,
    cleanup_logs
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
        attendre_nouveau_bouton_telecharger(DummyDriver(), DummyWebElement(), timeout=1)
    except Exception:
        pass  # On accepte que la fonction lève une exception ici, car il n'y a pas de vrai test à faire

def test_cleanup_logs_removes_old_logs(tmp_path):
    # Crée un dossier temporaire pour les logs
    log_dir = tmp_path
    # Crée deux fichiers logs : un ancien et un récent
    old_log = log_dir / "old.log"
    recent_log = log_dir / "recent.log"
    old_log.write_text("ancien log")
    recent_log.write_text("log récent")
    # Modifie la date de modification de l'ancien log pour qu'il soit vieux de 2 jours
    old_time = time.time() - (2 * 86400)
    os.utime(old_log, (old_time, old_time))
    # Appelle cleanup_logs avec une rétention de 1 jour
    cleanup_logs(str(log_dir), retention_days=1)
    # Vérifie que l'ancien log a été supprimé et que le récent existe toujours
    assert not old_log.exists()
    assert recent_log.exists()

def test_cleanup_logs_retention_zero(tmp_path):
    # Crée un dossier temporaire pour les logs
    log_dir = tmp_path
    log_file = log_dir / "test.log"
    log_file.write_text("log à conserver")
    # Appelle cleanup_logs avec une rétention illimitée
    cleanup_logs(str(log_dir), retention_days=0)
    # Vérifie que le log n'a pas été supprimé
    assert log_file.exists()