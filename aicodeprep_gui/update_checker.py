import datetime
import sys
import traceback
from typing import Callable, Optional

from PySide6.QtCore import QObject, QThread, Signal, QSettings, QDateTime, Qt, QTimer
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
            self.finished.emit(False, latest if latest else "")
            return
        print(f"[update_checker] Latest version from PyPI: {latest}, Current: {self.current_version}")
        new_available = is_newer_version(self.current_version, latest)
        print(f"[update_checker] Version comparison - New available: {new_available}")
        self.finished.emit(new_available, latest)

class UpdateChecker(QObject):
    """Thread-safe update checker that emits signals."""
    update_finished = Signal(bool, str)  # new_available, latest_version
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.thread = None
        self.worker = None

    def check_for_updates(self, force: bool = False) -> bool:
        """Check for updates. Returns True if check was started, False if skipped.
        Connect to update_finished signal to get results."""
        print(f"[update_checker] Starting update check for version {__version__}")
        settings = QSettings(ORG, GROUP)
        # Reset the prompted flag for new run so we can prompt once per day
        settings.setValue(KEY_PROMPTED_THIS_RUN, False)
        print("[update_checker] Reset prompted_this_run flag to False")
        last_check_str = settings.value(KEY_LAST_CHECK, "")
        # NEW: Store and retrieve last known version
        last_known_version = settings.value("last_known_version", "")
        now = QDateTime.currentDateTimeUtc()
        if last_check_str and not force:
            try:
                last_check = QDateTime.fromString(last_check_str, Qt.ISODate)
                if last_check.isValid() and last_check.secsTo(now) < 86400:
                    print(f"[update_checker] Skipping check - last checked {last_check_str} (< 24h ago)")
                    # Use last known version if available
                    if last_known_version:
                        is_newer = is_newer_version(__version__, last_known_version)
                        # Emit signal on main thread via QTimer
                        QTimer.singleShot(0, lambda: self.update_finished.emit(is_newer, last_known_version))
                    else:
                        QTimer.singleShot(0, lambda: self.update_finished.emit(False, ""))
                    return False
            except Exception as e:
                print(f"[update_checker] Error parsing last_check: {e}", file=sys.stderr)
        
        print("[update_checker] Starting background update check thread")
        # Run fetch in background thread
        self.thread = QThread(self)
        self.worker = _UpdateFetchWorker(__version__)
        self.worker.moveToThread(self.thread)
        
        def on_finish(new_available, latest):
            print(f"[update_checker] Check completed - New available: {new_available}, Latest: {latest}")
            # Schedule ALL operations on the main thread, including QSettings access and signal emission
            def main_thread_operations():
                settings.setValue(KEY_LAST_CHECK, now.toString(Qt.ISODate))
                # NEW: Store the latest version for future use
                if latest:
                    settings.setValue("last_known_version", latest)
                self.update_finished.emit(new_available, latest)
            QTimer.singleShot(0, main_thread_operations)
            self.thread.quit()
            
        self.worker.finished.connect(on_finish)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.started.connect(self.worker.do_work)
        self.thread.start()
        return True

def check_for_updates(callback: Callable[[bool, str], None], parent=None, force: bool = False) -> Optional[QThread]:
    """Legacy function for backwards compatibility. 
    Returns the QThread if one is created, None if check is skipped."""
    print(f"[update_checker] Starting update check for version {__version__}")
    settings = QSettings(ORG, GROUP)
    # Reset the prompted flag for new run so we can prompt once per day
    settings.setValue(KEY_PROMPTED_THIS_RUN, False)
    print("[update_checker] Reset prompted_this_run flag to False")
    last_check_str = settings.value(KEY_LAST_CHECK, "")
    # NEW: Store and retrieve last known version
    last_known_version = settings.value("last_known_version", "")
    now = QDateTime.currentDateTimeUtc()
    if last_check_str and not force:
        try:
            last_check = QDateTime.fromString(last_check_str, Qt.ISODate)
            if last_check.isValid() and last_check.secsTo(now) < 86400:
                print(f"[update_checker] Skipping check - last checked {last_check_str} (< 24h ago)")
                # Use last known version if available
                if last_known_version:
                    is_newer = is_newer_version(__version__, last_known_version)
                    # Schedule callback on main thread via QTimer
                    QTimer.singleShot(0, lambda: callback(is_newer, last_known_version))
                else:
                    QTimer.singleShot(0, lambda: callback(False, ""))
                return None
        except Exception as e:
            print(f"[update_checker] Error parsing last_check: {e}", file=sys.stderr)

    print("[update_checker] Starting background update check thread")
    # Run fetch in background thread - simplified approach
    thread = QThread(parent)
    worker = _UpdateFetchWorker(__version__)
    worker.moveToThread(thread)
    
    def on_finish(new_available, latest):
        print(f"[update_checker] Check completed - New available: {new_available}, Latest: {latest}")
        # CRITICAL: Schedule everything on main thread and quit thread immediately
        def main_thread_callback():
            try:
                settings.setValue(KEY_LAST_CHECK, now.toString(Qt.ISODate))
                if latest:
                    settings.setValue("last_known_version", latest)
                callback(new_available, latest)
            except Exception as e:
                print(f"[update_checker] Error in main thread callback: {e}")
            finally:
                # Clean up thread
                if thread.isRunning():
                    thread.quit()
                    thread.wait(1000)  # Wait up to 1 second
        
        QTimer.singleShot(0, main_thread_callback)
    
    worker.finished.connect(on_finish)
    thread.started.connect(worker.do_work)
    thread.finished.connect(thread.deleteLater)
    thread.start()
    return thread
