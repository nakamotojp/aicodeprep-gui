import datetime
import sys
import traceback
from typing import Callable, Optional

from PySide6.QtCore import QObject, QThread, Signal, QSettings, QDateTime, Qt
from packaging.version import parse as parse_version

try:
    import requests
except ImportError:
    requests = None

from . import __version__

PYPI_URL = "https://pypi.org/pypi/aicodeprep-gui/json"
ORG = "aicodeprep-gui"
GROUP = "UpdateChecker"
KEY_LAST_CHECK = "last_check"
KEY_LAST_PROMPT = "last_prompt"
KEY_PROMPTED_THIS_RUN = "prompted_this_run"

def get_latest_pypi_version() -> Optional[str]:
    """Fetch latest version string from PyPI. Returns None on error."""
    if not requests:
        return None
    try:
        resp = requests.get(PYPI_URL, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return data["info"]["version"]
    except Exception as e:
        print(f"[update_checker] Error fetching PyPI version: {e}", file=sys.stderr)
        traceback.print_exc()
        return None

def is_newer_version(current: str, latest: str) -> bool:
    """Return True if latest > current (semantic version compare)."""
    try:
        return parse_version(latest) > parse_version(current)
    except Exception as e:
        print(f"[update_checker] Version compare error: {e}", file=sys.stderr)
        return False

class _UpdateFetchWorker(QObject):
    finished = Signal(bool, str)
    def __init__(self, current_version: str):
        QObject.__init__(self)
        self.current_version = current_version

    def do_work(self):
        print(f"[update_checker] Worker running - fetching latest version from PyPI...")
        latest = get_latest_pypi_version()
        if latest is None:
            print(f"[update_checker] Failed to fetch latest version from PyPI")
            self.finished.emit(False, "")
            return
        print(f"[update_checker] Latest version from PyPI: {latest}, Current: {self.current_version}")
        new_available = is_newer_version(self.current_version, latest)
        print(f"[update_checker] Version comparison - New available: {new_available}")
        self.finished.emit(new_available, latest if new_available else "")

def check_for_updates(callback: Callable[[bool, str], None], parent=None) -> Optional[QThread]:
    """Check for updates, calling callback(new_available, latest_version) when done.
    Returns the QThread if one is created, None if check is skipped."""
    print(f"[update_checker] Starting update check for version {__version__}")
    settings = QSettings(ORG, GROUP)
    # Reset the prompted flag for new run so we can prompt once per day
    settings.setValue(KEY_PROMPTED_THIS_RUN, False)
    print("[update_checker] Reset prompted_this_run flag to False")
    last_check_str = settings.value(KEY_LAST_CHECK, "")
    now = QDateTime.currentDateTimeUtc()
    if last_check_str:
        try:
            last_check = QDateTime.fromString(last_check_str, Qt.ISODate)
            if last_check.isValid() and last_check.secsTo(now) < 86400:
                print(f"[update_checker] Skipping check - last checked {last_check_str} (< 24h ago)")
                callback(False, "")
                return None
        except Exception as e:
            print(f"[update_checker] Error parsing last_check: {e}", file=sys.stderr)
    print("[update_checker] Starting background update check thread")
    # Run fetch in background thread
    thread = QThread(parent)
    worker = _UpdateFetchWorker(__version__)
    thread.worker = worker
    worker.moveToThread(thread)
    def on_finish(new_available, latest):
        print(f"[update_checker] Check completed - New available: {new_available}, Latest: {latest}")
        settings.setValue(KEY_LAST_CHECK, now.toString(Qt.ISODate))
        callback(new_available, latest)
        thread.quit()
    worker.finished.connect(on_finish)
    thread.finished.connect(thread.deleteLater)
    thread.started.connect(worker.do_work)
    thread.start()
    return thread
