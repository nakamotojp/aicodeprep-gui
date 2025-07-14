import os
import sys
import platform
import logging
import uuid
import json
from datetime import datetime, date
from PySide6 import QtWidgets, QtCore, QtGui, QtNetwork
from aicodeprep_gui import __version__
from aicodeprep_gui import update_checker
from PySide6 import QtWidgets, QtCore, QtGui, QtNetwork
from importlib import resources
from aicodeprep_gui.apptheme import system_pref_is_dark, apply_dark_palette, apply_light_palette, get_checkbox_style_dark, get_checkbox_style_light
from typing import List, Tuple
from aicodeprep_gui import smart_logic
from aicodeprep_gui.file_processor import process_files
from aicodeprep_gui import __version__

class FlowLayout(QtWidgets.QLayout):
    def __init__(self, parent=None, margin=-1, hspacing=-1, vspacing=-1):
        super(FlowLayout, self).__init__(parent)
        self._items = []
        self.setContentsMargins(margin, margin, margin, margin)
        self._hspacing = hspacing
        self._vspacing = vspacing

    def __del__(self):
        del self._items[:]

    def addItem(self, item):
        self._items.append(item)
        self.invalidate()

    def horizontalSpacing(self):
        if self._hspacing >= 0:
            return self._hspacing
        return self.smartSpacing(QtWidgets.QStyle.PM_LayoutHorizontalSpacing)

    def verticalSpacing(self):
        if self._vspacing >= 0:
            return self._vspacing
        return self.smartSpacing(QtWidgets.QStyle.PM_LayoutVerticalSpacing)

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self._items):
            item = self._items.pop(index)
            self.invalidate()
            return item
        return None
        
    def insertWidget(self, index, widget):
        self.insertItem(index, QtWidgets.QWidgetItem(widget))

    def insertItem(self, index, item):
        self._items.insert(index, item)
        self.invalidate()

    def removeWidget(self, widget):
        for i, item in enumerate(self._items):
            if item.widget() is widget:
                self.takeAt(i)
                # Do not delete the widget, the caller is responsible
                break
    
    def expandingDirections(self):
        return QtCore.Qt.Orientation(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self.doLayout(QtCore.QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        margins = self.contentsMargins()
        size += QtCore.QSize(margins.left() + margins.right(), margins.top() + margins.bottom())
        return size

    def doLayout(self, rect, testOnly):
        m = self.contentsMargins()
        x = rect.x() + m.left()
        y = rect.y() + m.top()
        lineHeight = 0

        spaceX = self.horizontalSpacing()
        spaceY = self.verticalSpacing()

        for item in self._items:
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() - m.right() and lineHeight > 0:
                x = rect.x() + m.left()
                y = y + lineHeight + spaceY
                lineHeight = 0
            
            if not testOnly:
                item.setGeometry(QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))

            x = x + item.sizeHint().width() + spaceX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight + m.bottom()

    def smartSpacing(self, pm):
        parent = self.parent()
        if not parent:
            return -1
        if parent.isWidgetType():
            return parent.style().pixelMetric(pm, None, parent)
        else:
            return parent.spacing()

# Version for .aicodeprep-gui file format
AICODEPREP_GUI_VERSION = "1.0"

# Default presets for button prompts (label, text)
DEFAULT_PRESETS = [
    ("Debug", "Can you help me debug this code?"),
    ("Security check", "Can you analyze this code for any security issues?"),
    ("Best Practices", "Please analyze this code for: Error handling, Edge cases, Performance optimization, Best practices, Please do not unnecessarily remove any comments or code. Generate the code with clear comments explaining the logic."),
    ("Please review for", "Code quality and adherence to best practices, Potential bugs or edge cases, Performance optimizations, Readability and maintainability, Security concerns. Suggest improvements and explain your reasoning for each suggestion"),
    ("Cline, Roo Code Prompt", "Write a prompt for Cline, an AI coding agent, to make the necessary changes. Enclose the entire Cline prompt in one single code tag for easy copy and paste.")
]

class GlobalPresetManager:
    PRESET_SCHEMA_VERSION = 1

    def __init__(self):
        try:
            self.settings = QtCore.QSettings("aicodeprep-gui", "ButtonPresets")
            self._ensure_default_presets()
        except Exception as e:
            logging.error(f"Failed to initialize global preset manager: {e}")
            self.settings = None

    def _ensure_default_presets(self):
        """
        Ensure default presets are present and up-to-date.
        If the preset schema version is outdated, update only the default presets.
        Custom user presets are preserved.
        """
        try:
            if not self.settings:
                return

            # Read last schema version from QSettings (internal group)
            self.settings.beginGroup("internal")
            last_version = self.settings.value("preset_version", 0, type=int)
            self.settings.endGroup()

            if last_version >= self.PRESET_SCHEMA_VERSION:
                return  # No update needed

            logging.info(f"Updating default button presets (schema version {last_version} -> {self.PRESET_SCHEMA_VERSION})")

            # Overwrite only the default presets in the "presets" group
            self.settings.beginGroup("presets")
            for label, text in DEFAULT_PRESETS:
                self.settings.setValue(label, text)
            self.settings.endGroup()

            # Update the stored schema version
            self.settings.beginGroup("internal")
            self.settings.setValue("preset_version", self.PRESET_SCHEMA_VERSION)
            self.settings.endGroup()

            logging.info("Default button presets updated successfully.")
        except Exception as e:
            logging.error(f"Failed to update default presets: {e}")

    def get_all_presets(self):
        """Get all saved presets as list of (label, text) tuples"""
        try:
            if not self.settings: return []
            presets = []
            self.settings.beginGroup("presets")
            for key in self.settings.childKeys():
                presets.append((key, self.settings.value(key, "")))
            self.settings.endGroup()
            return presets
        except Exception as e:
            logging.error(f"Failed to get presets: {e}")
            return []
    
    def add_preset(self, label, text):
        try:
            if not self.settings or not label.strip() or not text.strip(): return False
            self.settings.beginGroup("presets")
            self.settings.setValue(label.strip(), text.strip())
            self.settings.endGroup()
            return True
        except Exception as e:
            logging.error(f"Failed to add preset '{label}': {e}")
            return False
    
    def delete_preset(self, label):
        try:
            if not self.settings or not label.strip(): return False
            self.settings.beginGroup("presets")
            self.settings.remove(label.strip())
            self.settings.endGroup()
            return True
        except Exception as e:
            logging.error(f"Failed to delete preset '{label}': {e}")
            return False

global_preset_manager = GlobalPresetManager()

class FileSelectionGUI(QtWidgets.QMainWindow):
    def open_settings_folder(self):
        """Open the folder containing the .aicodeprep-gui settings file in the system file explorer."""
        folder_path = os.getcwd()
        if sys.platform.startswith("win"):
            os.startfile(folder_path)
        elif sys.platform.startswith("darwin"):
            import subprocess
            subprocess.Popen(["open", folder_path])
        else:
            import subprocess
            subprocess.Popen(["xdg-open", folder_path])

    def __init__(self, files, force_update=False):
        super().__init__()
        self.force_update = force_update
        self.initial_show_event = True
        # Set application icon
        try:
            with resources.path('aicodeprep_gui.images', 'favicon.ico') as icon_path:
                app_icon = QtGui.QIcon(str(icon_path))
            self.setWindowIcon(app_icon)
            # Add system tray icon with context menu
            from PySide6.QtWidgets import QSystemTrayIcon, QMenu
            from PySide6.QtGui import QAction
            tray = QSystemTrayIcon(app_icon, parent=self)
            # build a minimal context menu
            menu = QMenu()
            show_act = QAction("Show", self)
            quit_act = QAction("Quit", self)
            show_act.triggered.connect(self.show)
            quit_act.triggered.connect(self.quit_without_processing)
            menu.addAction(show_act)
            menu.addSeparator()
            menu.addAction(quit_act)
            tray.setContextMenu(menu)
            tray.show()
            self.tray_icon = tray  # keep a reference so it doesn't get garbage‐collected
        except FileNotFoundError:
            logging.warning("Application icon 'favicon.ico' not found in package resources.")

        self.presets = [] # This local 'presets' list is not used for global presets, but for local ones (which are not saved to the .aicodeprep-gui file, but managed by global_preset_manager through QSettings)
        self.setAcceptDrops(True)
        self.files = files
        self.latest_pypi_version = None

        # Network manager should be initialized early as it's used by multiple components
        self.network_manager = QtNetwork.QNetworkAccessManager(self)

        # Get or create anonymous user UUID
        settings = QtCore.QSettings("aicodeprep-gui", "UserIdentity")
        self.user_uuid = settings.value("user_uuid")
        if not self.user_uuid:
            import uuid
            self.user_uuid = str(uuid.uuid4())
            settings.setValue("user_uuid", self.user_uuid)
            logging.info(f"Generated new anonymous user UUID: {self.user_uuid}")

        # --- Persistent app open counter ---
        app_open_count = settings.value("app_open_count", 0, type=int)
        try:
            app_open_count = int(app_open_count)
        except Exception:
            app_open_count = 0
        app_open_count += 1
        settings.setValue("app_open_count", app_open_count)
        self.app_open_count = app_open_count

        # Send metrics "open" event
        self._send_metric_event("open")

        # --- Store install date if first run ---
        install_date_str = settings.value("install_date")
        if not install_date_str:
            # store ISO date on first launch
            today_iso = date.today().isoformat()
            settings.setValue("install_date", today_iso)
            install_date_str = today_iso
        logging.debug(f"Stored install_date: {install_date_str}")

        from datetime import datetime
        now = datetime.now()
        time_str = f"{now.strftime('%I').lstrip('0') or '12'}{now.strftime('%M')}{now.strftime('%p').lower()}"
        request = QtNetwork.QNetworkRequest(QtCore.QUrl(f"https://wuu73.org/dixels/newaicp.html?t={time_str}&user={self.user_uuid}"))
        self.network_manager.get(request)

        # --- Schedule update checker (non-blocking, after telemetry) ---
        self.update_thread = None

        self.setWindowTitle("aicodeprep-gui - File Selection")
        self.app = QtWidgets.QApplication.instance()
        if self.app is None:
            self.app = QtWidgets.QApplication([])
        self.action = 'quit'

        self.prefs_filename = ".aicodeprep-gui"
        self.remember_checkbox = None 
        self.checked_files_from_prefs = set()
        self.prefs_loaded = False
        self.window_size_from_prefs = None
        self.splitter_state_from_prefs = None # Initialize this attribute
        self.load_prefs_if_exists()

        if platform.system() == 'Windows':
            scale_factor = self.app.primaryScreen().logicalDotsPerInch() / 96.0
        else:
            scale_factor = self.app.primaryScreen().devicePixelRatio()

        default_font_size = 9
        font_stack = '"Segoe UI", "Ubuntu", "Helvetica Neue", Arial, sans-serif'
        default_font_size = int(default_font_size * scale_factor)
        self.default_font = QtGui.QFont("Segoe UI", default_font_size)
        self.setFont(self.default_font)
        self.setStyleSheet(f"font-family: {font_stack};")
        style = self.style()
        self.folder_icon = style.standardIcon(QtWidgets.QStyle.SP_DirIcon)
        self.file_icon = style.standardIcon(QtWidgets.QStyle.SP_FileIcon)

        if self.window_size_from_prefs:
            w, h = self.window_size_from_prefs
            self.setGeometry(100, 100, w, h)
        else:
            self.setGeometry(100, 100, int(600 * scale_factor), int(400 * scale_factor))

        self.is_dark_mode = self._load_dark_mode_setting()
        if self.is_dark_mode: apply_dark_palette(self.app)

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        main_layout = QtWidgets.QVBoxLayout(central)
        main_layout.setContentsMargins(20, 10, 20, 10)

        mb = self.menuBar()
        file_menu = mb.addMenu("&File")

        # Add this new block for the Windows-only menu item
        if platform.system() == "Windows":
            from aicodeprep_gui import windows_registry
            class RegistryManagerDialog(QtWidgets.QDialog):
                def __init__(self, parent=None):
                    super().__init__(parent)
                    self.setWindowTitle("Windows Context Menu Manager")
                    self.setMinimumWidth(450)
                    
                    self.layout = QtWidgets.QVBoxLayout(self)
                    
                    info_text = (
                        "This tool can add or remove a right-click context menu item in "
                        "Windows Explorer to open `aicodeprep-gui` in any folder.<br><br>"
                        "<b>Note:</b> This operation requires administrator privileges. "
                        "A UAC prompt will appear."
                    )
                    self.info_label = QtWidgets.QLabel(info_text)
                    self.info_label.setWordWrap(True)
                    self.layout.addWidget(self.info_label)

                    # Add custom menu text input
                    menu_text_label = QtWidgets.QLabel("Custom menu text:")
                    self.layout.addWidget(menu_text_label)
                    
                    self.menu_text_input = QtWidgets.QLineEdit()
                    self.menu_text_input.setPlaceholderText("Open with aicodeprep-gui")
                    self.menu_text_input.setText("Open with aicodeprep-gui")
                    self.menu_text_input.setToolTip("Enter the text that will appear in the right-click context menu")
                    self.layout.addWidget(self.menu_text_input)
                    
                    # Add some spacing
                    self.layout.addSpacing(10)

                    # Classic menu checkbox and help icon
                    self.classic_menu_checkbox = QtWidgets.QCheckBox("Enable Classic Right-Click Menu (for Windows 11)")
                    self.classic_menu_checkbox.setChecked(True)
                    classic_help = QtWidgets.QLabel("<b style='color:#0078D4; font-size:14px; cursor:help;'>?</b>")
                    classic_help.setToolTip("Restores the full right-click menu in Windows 11, so you don't have to click 'Show more options' to see this app's menu item.")
                    classic_help.setAlignment(QtCore.Qt.AlignVCenter)
                    classic_layout = QtWidgets.QHBoxLayout()
                    classic_layout.setContentsMargins(0,0,0,0)
                    classic_layout.addWidget(self.classic_menu_checkbox)
                    classic_layout.addWidget(classic_help)
                    classic_layout.addStretch()
                    self.layout.addLayout(classic_layout)

                    self.status_label = QtWidgets.QLabel("Ready.")
                    self.status_label.setStyleSheet("font-style: italic;")
                    
                    self.install_button = QtWidgets.QPushButton("Install Right-Click Menu")
                    self.install_button.clicked.connect(self.run_install)
                    
                    self.uninstall_button = QtWidgets.QPushButton("Uninstall Right-Click Menu")
                    self.uninstall_button.clicked.connect(self.run_uninstall)

                    button_layout = QtWidgets.QHBoxLayout()
                    button_layout.addWidget(self.install_button)
                    button_layout.addWidget(self.uninstall_button)
                    
                    self.layout.addLayout(button_layout)
                    self.layout.addWidget(self.status_label)

                def _run_action(self, action_name):
                    enable_classic = self.classic_menu_checkbox.isChecked()
                    if windows_registry.is_admin():
                        # Already running as admin, just do the action
                        if action_name == 'install':
                            custom_text = self.menu_text_input.text().strip()
                            success, message = windows_registry.install_context_menu(
                                custom_text if custom_text else None,
                                enable_classic_menu=enable_classic
                            )
                        else:
                            success, message = windows_registry.remove_context_menu()
                        
                        self.status_label.setText(message)
                        if success:
                            QtWidgets.QMessageBox.information(self, "Success", message)
                        else:
                            QtWidgets.QMessageBox.warning(self, "Error", message)
                    else:
                        # Not admin, need to elevate
                        if action_name == 'install':
                            custom_text = self.menu_text_input.text().strip()
                            success, message = windows_registry.run_as_admin(
                                action_name,
                                custom_text if custom_text else None,
                                enable_classic_menu=enable_classic
                            )
                        else:
                            success, message = windows_registry.run_as_admin(action_name)
                        self.status_label.setText(message)
                        if success:
                            # Close the main app window as a new elevated process will take over
                            self.parent().close()
                
                def run_install(self):
                    self._run_action('install')

                def run_uninstall(self):
                    self._run_action('remove')

            def open_registry_manager(self):
                dialog = RegistryManagerDialog(self)
                dialog.exec()

            install_menu_act = QtGui.QAction("Install Right-Click Menu...", self)
            install_menu_act.triggered.connect(lambda: open_registry_manager(self))
            file_menu.addAction(install_menu_act)
            file_menu.addSeparator() # Optional, for visual separation

        # Add macOS-only menu item
        if platform.system() == "Darwin":
            from aicodeprep_gui import macos_installer

            class MacInstallerDialog(QtWidgets.QDialog):
                def __init__(self, parent=None):
                    super().__init__(parent)
                    self.setWindowTitle("macOS Quick Action Manager")
                    self.setMinimumWidth(450)
                    self.layout = QtWidgets.QVBoxLayout(self)

                    info_text = (
                        "This tool installs or removes a <b>Quick Action</b> to open `aicodeprep-gui` "
                        "from the right-click menu in Finder (under Quick Actions or Services).<br><br>"
                        "The action is installed in your user's Library folder, so no administrator "
                        "privileges are required."
                    )
                    self.info_label = QtWidgets.QLabel(info_text)
                    self.info_label.setWordWrap(True)
                    self.layout.addWidget(self.info_label)
                    self.layout.addSpacing(10)

                    self.install_button = QtWidgets.QPushButton("Install Quick Action")
                    self.install_button.clicked.connect(self.run_install)
                    
                    self.uninstall_button = QtWidgets.QPushButton("Uninstall Quick Action")
                    self.uninstall_button.clicked.connect(self.run_uninstall)

                    button_layout = QtWidgets.QHBoxLayout()
                    button_layout.addWidget(self.install_button)
                    button_layout.addWidget(self.uninstall_button)
                    self.layout.addLayout(button_layout)

                def run_install(self):
                    success, message = macos_installer.install_quick_action()
                    if success:
                        QtWidgets.QMessageBox.information(self, "Success", message)
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", message)

                def run_uninstall(self):
                    success, message = macos_installer.uninstall_quick_action()
                    if success:
                        QtWidgets.QMessageBox.information(self, "Success", message)
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", message)

            def open_mac_installer(self):
                dialog = MacInstallerDialog(self)
                dialog.exec()

            install_menu_act = QtGui.QAction("Install Finder Quick Action...", self)
            install_menu_act.triggered.connect(lambda: open_mac_installer(self))
            file_menu.addAction(install_menu_act)
            file_menu.addSeparator()

        # Add Linux-only menu item
        if platform.system() == "Linux":
            from aicodeprep_gui import linux_installer

            class LinuxInstallerDialog(QtWidgets.QDialog):
                def __init__(self, parent=None):
                    super().__init__(parent)
                    self.setWindowTitle("Linux File Manager Integration")
                    self.setMinimumWidth(500)
                    self.layout = QtWidgets.QVBoxLayout(self)

                    self.tabs = QtWidgets.QTabWidget()
                    
                    # Automated Installer Tab
                    automated_tab = QtWidgets.QWidget()
                    automated_layout = QtWidgets.QVBoxLayout(automated_tab)
                    self.tabs.addTab(automated_tab, "Automated Setup")

                    info_text = QtWidgets.QLabel(
                        "This tool can attempt to install a context menu script for your file manager."
                    )
                    info_text.setWordWrap(True)
                    automated_layout.addWidget(info_text)
                    automated_layout.addSpacing(10)

                    self.nautilus_group = QtWidgets.QGroupBox("Nautilus (GNOME, Cinnamon, etc.)")
                    nautilus_layout = QtWidgets.QVBoxLayout(self.nautilus_group)
                    
                    self.install_nautilus_btn = QtWidgets.QPushButton("Install Nautilus Script")
                    self.install_nautilus_btn.clicked.connect(self.run_install_nautilus)
                    self.uninstall_nautilus_btn = QtWidgets.QPushButton("Uninstall Nautilus Script")
                    self.uninstall_nautilus_btn.clicked.connect(self.run_uninstall_nautilus)
                    
                    nautilus_layout.addWidget(self.install_nautilus_btn)
                    nautilus_layout.addWidget(self.uninstall_nautilus_btn)
                    
                    automated_layout.addWidget(self.nautilus_group)
                    automated_layout.addStretch()

                    # Disable if Nautilus is not detected
                    if not linux_installer.is_nautilus_installed():
                        self.nautilus_group.setDisabled(True)
                        self.nautilus_group.setToolTip("Nautilus file manager not detected in your system's PATH.")

                    # Manual Instructions Tab
                    manual_tab = QtWidgets.QWidget()
                    manual_layout = QtWidgets.QVBoxLayout(manual_tab)
                    self.tabs.addTab(manual_tab, "Manual Instructions")
                    
                    manual_text = QtWidgets.QLabel(
                        "If your file manager is not listed above, you can likely add a custom action manually. "
                        "Create a new executable script with the content below and add it to your file manager's "
                        "scripting or custom actions feature. The selected folder path will be passed as the first argument ($1)."
                    )
                    manual_text.setWordWrap(True)
                    manual_layout.addWidget(manual_text)

                    script_box = QtWidgets.QPlainTextEdit()
                    script_box.setPlainText(linux_installer.NAUTILUS_SCRIPT_CONTENT)
                    script_box.setReadOnly(True)
                    script_box.setFont(QtGui.QFont("Monospace"))
                    manual_layout.addWidget(script_box)
                    
                    self.layout.addWidget(self.tabs)

                def run_install_nautilus(self):
                    success, message = linux_installer.install_nautilus_script()
                    if success:
                        QtWidgets.QMessageBox.information(self, "Success", message)
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", message)

                def run_uninstall_nautilus(self):
                    success, message = linux_installer.uninstall_nautilus_script()
                    if success:
                        QtWidgets.QMessageBox.information(self, "Success", message)
                    else:
                        QtWidgets.QMessageBox.warning(self, "Error", message)

            def open_linux_installer(self):
                dialog = LinuxInstallerDialog(self)
                dialog.exec()

            install_menu_act = QtGui.QAction("Install File Manager Action...", self)
            install_menu_act.triggered.connect(lambda: open_linux_installer(self))
            file_menu.addAction(install_menu_act)
            file_menu.addSeparator()

        quit_act = QtGui.QAction("&Quit", self); quit_act.triggered.connect(self.quit_without_processing); file_menu.addAction(quit_act)
        edit_menu = mb.addMenu("&Edit")
        new_preset_act = QtGui.QAction("&New Preset…", self); new_preset_act.triggered.connect(self.add_new_preset_dialog); edit_menu.addAction(new_preset_act)
        open_settings_folder_act = QtGui.QAction("Open Settings Folder…", self)
        open_settings_folder_act.triggered.connect(self.open_settings_folder)
        edit_menu.addAction(open_settings_folder_act)

        # --- New Help / About menu ---
        help_menu = mb.addMenu("&Help")

        links_act = QtGui.QAction("Help / Links and Guides", self)
        links_act.triggered.connect(self.open_links_dialog)
        help_menu.addAction(links_act)
        help_menu.addSeparator()

        about_act = QtGui.QAction("&About", self)
        about_act.triggered.connect(self.open_about_dialog)
        help_menu.addAction(about_act)
        
        complain_act = QtGui.QAction("Send Ideas, bugs, thoughts!", self)
        complain_act.triggered.connect(self.open_complain_dialog)
        help_menu.addAction(complain_act)

        self.format_combo = QtWidgets.QComboBox()
        self.format_combo.addItems(["XML <code>", "Markdown ###"])
        self.format_combo.setFixedWidth(130)
        self.format_combo.setItemData(0, 'xml')
        self.format_combo.setItemData(1, 'markdown')
        output_label = QtWidgets.QLabel("&Output format:")
        output_label.setBuddy(self.format_combo)
        self.dark_mode_box = QtWidgets.QCheckBox("Dark mode")
        self.dark_mode_box.setChecked(self.is_dark_mode)
        self.dark_mode_box.stateChanged.connect(self.toggle_dark_mode)
        self.token_label = QtWidgets.QLabel("Estimated tokens: 0")
        main_layout.addWidget(self.token_label)
        main_layout.addSpacing(8)

        self.vibe_label = QtWidgets.QLabel("AI Code Prep GUI")
        vibe_font = QtGui.QFont(self.default_font)
        vibe_font.setBold(True)
        vibe_font.setPointSize(self.default_font.pointSize() + 8)
        self.vibe_label.setFont(vibe_font)
        self.vibe_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.vibe_label.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #40203f, stop:1 #1f103f); "
            "color: white; padding: 0px 0px 0px 0px; border-radius: 8px;"
        )
        self.vibe_label.setFixedHeight(44)
        banner_wrap = QtWidgets.QWidget()
        banner_layout = QtWidgets.QHBoxLayout(banner_wrap)
        banner_layout.setContentsMargins(14, 0, 14, 0)
        banner_layout.addWidget(self.vibe_label)
        main_layout.addWidget(banner_wrap)
        main_layout.addSpacing(8)

        # --- Update available label (hidden by default) ---
        self.update_label = QtWidgets.QLabel()
        self.update_label.setTextFormat(QtCore.Qt.RichText)
        self.update_label.setAlignment(QtCore.Qt.AlignCenter)
        self.update_label.setVisible(False)
        main_layout.addWidget(self.update_label)
        main_layout.addSpacing(8)

        self.info_label = QtWidgets.QLabel("The selected files will be added to the LLM Context Block along with your prompt, written to fullcode.txt and copied to clipboard, ready to paste into Gemini in AI studio, Deepseek, ChatGPT, etc.")
        self.info_label.setWordWrap(True)  # Add this line to enable word wrapping
        self.info_label.setAlignment(QtCore.Qt.AlignHCenter)
        main_layout.addWidget(self.info_label)

        self.text_label = QtWidgets.QLabel("")
        self.text_label.setWordWrap(True)
        main_layout.addWidget(self.text_label)

        # Add "Prompt Preset Buttons:" label above presets section
        prompt_header_label = QtWidgets.QLabel("Prompt Preset Buttons:")
        main_layout.addWidget(prompt_header_label)
        
        # Create scrollable preset area
        presets_wrapper = QtWidgets.QHBoxLayout()
        
        # Scrollable area for preset buttons
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setFixedHeight(52)  # Enough height for 22px buttons + padding
        
        scroll_widget = QtWidgets.QWidget()
        self.preset_strip = QtWidgets.QHBoxLayout(scroll_widget)
        self.preset_strip.setContentsMargins(0, 0, 0, 0)
        
        add_preset_btn = QtWidgets.QPushButton("✚")
        add_preset_btn.setFixedSize(24, 24)
        add_preset_btn.setToolTip("New Preset…")
        add_preset_btn.clicked.connect(self.add_new_preset_dialog)
        self.preset_strip.addWidget(add_preset_btn)

        delete_preset_btn = QtWidgets.QPushButton("🗑️")
        delete_preset_btn.setFixedSize(24, 24)
        delete_preset_btn.setToolTip("Delete a preset…")
        delete_preset_btn.clicked.connect(self.delete_preset_dialog)
        self.preset_strip.addWidget(delete_preset_btn)
        
        self.preset_strip.addStretch()
        
        scroll_area.setWidget(scroll_widget)
        presets_wrapper.addWidget(scroll_area)
        
        main_layout.addLayout(presets_wrapper)
        
        # Add explanation text below presets
        preset_explanation = QtWidgets.QLabel("Presets help you save more time and will be saved for later use")
        preset_explanation.setObjectName("preset_explanation")
        preset_explanation.setStyleSheet(
            f"font-size: 10px; color: {'#bbbbbb' if self.is_dark_mode else '#444444'};"
        )
        main_layout.addWidget(preset_explanation)
        
        main_layout.addSpacing(8)

        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.tree_widget = QtWidgets.QTreeWidget()
        self.tree_widget.setHeaderLabels(["File/Folder"])
        self.tree_widget.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        # Apply initial checkbox styling along with other styles
        base_style = """
            QTreeView, QTreeWidget {
                outline: 2; /* Remove focus rectangle */
            }
        """
        checkbox_style = get_checkbox_style_dark() if self.is_dark_mode else get_checkbox_style_light()
        self.tree_widget.setStyleSheet(base_style + checkbox_style)
        
        self.splitter.addWidget(self.tree_widget)
        prompt_widget = QtWidgets.QWidget(); prompt_layout = QtWidgets.QVBoxLayout(prompt_widget); prompt_layout.setContentsMargins(0,0,0,0)
        prompt_layout.addWidget(QtWidgets.QLabel("Optional prompt/question for LLM (will be appended to the end):")); prompt_layout.addSpacing(8)
        self.prompt_textbox = QtWidgets.QPlainTextEdit()
        self.prompt_textbox.setPlaceholderText("Type your question or prompt here (optional)…")
        prompt_layout.addWidget(self.prompt_textbox)

        # Add Clear button below the prompt box
        self.clear_prompt_btn = QtWidgets.QPushButton("Clear")
        self.clear_prompt_btn.setToolTip("Clear the prompt box")
        self.clear_prompt_btn.clicked.connect(self.prompt_textbox.clear)
        prompt_layout.addWidget(self.clear_prompt_btn)
        self.splitter.addWidget(prompt_widget)
        self.splitter.setStretchFactor(0, 4); self.splitter.setStretchFactor(1, 1)
        main_layout.addWidget(self.splitter)

        # Apply saved splitter state if available
        if self.splitter_state_from_prefs: 
            try:
                self.splitter.restoreState(self.splitter_state_from_prefs)
                logging.info("Restored splitter state from preferences")
            except Exception as e:
                logging.warning(f"Failed to restore splitter state: {e}")

        # --- NEW TREE BUILDING LOGIC ---
        self.path_to_item = {}  # Maps relative_path to QTreeWidgetItem
        root_node = self.tree_widget.invisibleRootItem()
        for abs_path, rel_path, is_checked in files:
            parts = rel_path.split(os.sep)
            parent_node = root_node
            path_so_far = ""
            for part in parts[:-1]:
                path_so_far = os.path.join(path_so_far, part) if path_so_far else part
                if path_so_far in self.path_to_item:
                    parent_node = self.path_to_item[path_so_far]
                else:
                    # This case implies a directory was not in the `files` list, create it
                    new_parent = QtWidgets.QTreeWidgetItem(parent_node, [part])
                    new_parent.setIcon(0, self.folder_icon)
                    new_parent.setFlags(new_parent.flags() | QtCore.Qt.ItemIsUserCheckable)
                    new_parent.setCheckState(0, QtCore.Qt.Unchecked)
                    self.path_to_item[path_so_far] = new_parent
                    parent_node = new_parent

            # Create the final item
            item_text = parts[-1]
            item = QtWidgets.QTreeWidgetItem(parent_node, [item_text])
            item.setData(0, QtCore.Qt.UserRole, abs_path) # Store absolute path
            self.path_to_item[rel_path] = item

            if self.prefs_loaded:
                is_checked = rel_path in self.checked_files_from_prefs
            
            if os.path.isdir(abs_path):
                item.setIcon(0, self.folder_icon)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                # For directories, default to unchecked during initial population.
                # Their checked state will reflect children or be set explicitly by load_prefs_if_exists
                item.setCheckState(0, QtCore.Qt.Unchecked) 
            else: # It's a file
                item.setIcon(0, self.file_icon)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                # Don't block binary files, just leave them unchecked by default
                if smart_logic.is_binary_file(abs_path):
                    is_checked = False
            
            item.setCheckState(0, QtCore.Qt.Checked if is_checked else QtCore.Qt.Unchecked)

        # Connect signals for lazy loading and item changes
        self.tree_widget.itemExpanded.connect(self.on_item_expanded)
        self.tree_widget.itemChanged.connect(self.handle_item_changed)
        
        # Auto-expand folders containing checked files
        if self.prefs_loaded and self.checked_files_from_prefs:
            self._expand_folders_for_paths(self.checked_files_from_prefs)
        else:
            # On first load (no prefs), expand based on smart-selected files
            initial_checked_paths = {rel_path for _, rel_path, is_checked in files if is_checked}
            self._expand_folders_for_paths(initial_checked_paths)
        
        # --- Remember checked files checkbox with tooltip and ? icon ---
        self.remember_checkbox = QtWidgets.QCheckBox("Remember checked files for this folder, window size information")
        self.remember_checkbox.setChecked(True)
        self.remember_checkbox.setToolTip("Saves which files are included in the context for this folder, so you don't have to keep doing it over and over")
        remember_help = QtWidgets.QLabel("<b style='color:#0078D4; font-size:14px; cursor:help;'>?</b>")
        remember_help.setToolTip("Saves which files are included in the context for this folder, so you don't have to keep doing it over and over")
        remember_help.setAlignment(QtCore.Qt.AlignVCenter)
        remember_layout = QtWidgets.QHBoxLayout()
        remember_layout.setContentsMargins(0,0,0,0)
        remember_layout.addWidget(self.remember_checkbox)
        remember_layout.addWidget(remember_help)
        remember_layout.addStretch()

        # --- Prompt/question to top checkbox with tooltip and ? icon ---
        self.prompt_top_checkbox = QtWidgets.QCheckBox("Add prompt/question to top")
        self.prompt_top_checkbox.setToolTip("Research shows that asking your question before AND after the code context, can improve quality and ability of the AI responses! Highly recommended to check both of these")
        prompt_top_help = QtWidgets.QLabel("<b style='color:#0078D4; font-size:14px; cursor:help;'>?</b>")
        prompt_top_help.setToolTip("Research shows that asking your question before AND after the code context, can improve quality and ability of the AI responses! Highly recommended to check both of these")
        prompt_top_help.setAlignment(QtCore.Qt.AlignVCenter)
        prompt_top_layout = QtWidgets.QHBoxLayout()
        prompt_top_layout.setContentsMargins(0,0,0,0)
        prompt_top_layout.addWidget(self.prompt_top_checkbox)
        prompt_top_layout.addWidget(prompt_top_help)
        prompt_top_layout.addStretch()

        # --- Prompt/question to bottom checkbox with tooltip and ? icon ---
        self.prompt_bottom_checkbox = QtWidgets.QCheckBox("Add prompt/question to bottom")
        self.prompt_bottom_checkbox.setToolTip("Research shows that asking your question before AND after the code context, can improve quality and ability of the AI responses! Highly recommended to check both of these")
        prompt_bottom_help = QtWidgets.QLabel("<b style='color:#0078D4; font-size:14px; cursor:help;'>?</b>")
        prompt_bottom_help.setToolTip("Research shows that asking your question before AND after the code context, can improve quality and ability of the AI responses! Highly recommended to check both of these")
        prompt_bottom_help.setAlignment(QtCore.Qt.AlignVCenter)
        prompt_bottom_layout = QtWidgets.QHBoxLayout()
        prompt_bottom_layout.setContentsMargins(0,0,0,0)
        prompt_bottom_layout.addWidget(self.prompt_bottom_checkbox)
        prompt_bottom_layout.addWidget(prompt_bottom_help)
        prompt_bottom_layout.addStretch()

        # Load global prompt option settings
        self._load_prompt_options()

        # Save settings when toggled
        self.prompt_top_checkbox.stateChanged.connect(self._save_prompt_options)
        self.prompt_bottom_checkbox.stateChanged.connect(self._save_prompt_options)

# --- New Collapsible Options Group ---
        # The QGroupBox is checkable, which allows it to function as an accordion.
        options_group_box = QtWidgets.QGroupBox("Options")
        options_group_box.setCheckable(True)
        options_group_box.setChecked(True)  # Default to visible/expanded

        # This container widget holds all the options. We show/hide this container.
        options_container = QtWidgets.QWidget()

        # The layout for the container's content.
        options_content_layout = QtWidgets.QVBoxLayout(options_container)
        options_content_layout.setContentsMargins(0, 5, 0, 5) # Clean inner margins

        # First row: Output format and Dark mode
        options_top_row = QtWidgets.QHBoxLayout()
        options_top_row.addWidget(output_label)
        options_top_row.addWidget(self.format_combo)
        options_top_row.addStretch()
        options_top_row.addWidget(self.dark_mode_box)
        options_content_layout.addLayout(options_top_row)

        # Add the three checkbox layouts (which were created just above this block)
        options_content_layout.addLayout(remember_layout)
        options_content_layout.addLayout(prompt_top_layout)
        options_content_layout.addLayout(prompt_bottom_layout)

        # The main layout for the QGroupBox itself. It will contain the collapsible widget.
        group_box_main_layout = QtWidgets.QVBoxLayout(options_group_box)
        # Margins for the groupbox, so the content doesn't touch the borders
        group_box_main_layout.setContentsMargins(10, 5, 10, 10)
        group_box_main_layout.addWidget(options_container)

        # Connect the group box's toggled signal to the container's setVisible method.
        # This is what makes the content expand and collapse.
        options_group_box.toggled.connect(options_container.setVisible)

        main_layout.addWidget(options_group_box)
        
        # Button layouts
        button_layout1 = QtWidgets.QHBoxLayout()
        button_layout2 = QtWidgets.QHBoxLayout()

        button_layout1.addStretch()
        process_button = QtWidgets.QPushButton("GENERATE CONTEXT!")
        process_button.clicked.connect(self.process_selected)
        button_layout1.addWidget(process_button)
        select_all_button = QtWidgets.QPushButton("Select All")
        select_all_button.clicked.connect(self.select_all)
        button_layout1.addWidget(select_all_button)
        deselect_all_button = QtWidgets.QPushButton("Deselect All")
        deselect_all_button.clicked.connect(self.deselect_all)
        button_layout1.addWidget(deselect_all_button)

        button_layout2.addStretch()
        load_prefs_button = QtWidgets.QPushButton("Load preferences")
        load_prefs_button.clicked.connect(self.load_from_prefs_button_clicked)
        button_layout2.addWidget(load_prefs_button)
        quit_button = QtWidgets.QPushButton("Quit")
        quit_button.clicked.connect(self.quit_without_processing)
        button_layout2.addWidget(quit_button)

        main_layout.addLayout(button_layout1)
        main_layout.addLayout(button_layout2)

        # --- Footer Layout ---
        footer_layout = QtWidgets.QHBoxLayout()
        
        # Email link on the left
        email_text = '<a href="mailto:tom@wuu73.org">tom@wuu73.org</a>'
        email_label = QtWidgets.QLabel(email_text)
        email_label.setOpenExternalLinks(True)
        footer_layout.addWidget(email_label)
        
        footer_layout.addStretch()
        
        # Website link on the right
        website_label = QtWidgets.QLabel('<a href="https://wuu73.org/aicp">aicodeprep-gui</a>')
        website_label.setOpenExternalLinks(True)
        footer_layout.addWidget(website_label)
        
        main_layout.addLayout(footer_layout)

        self.selected_files = []
        self.file_token_counts = {}
        self.update_token_counter()
        self._load_global_presets()

    def on_item_expanded(self, item):
        """Handler for when a tree item is expanded, used for lazy loading."""
        dir_path = item.data(0, QtCore.Qt.UserRole)
        if not dir_path or not os.path.isdir(dir_path): 
            return
            
        # Check if children have already been loaded by verifying if first child is a real item.
        # If it has children and the first one has a UserRole data, it implies content has been loaded.
        if item.childCount() > 0 and item.child(0).data(0, QtCore.Qt.UserRole) is not None:
            return
            
        try:
            # Clear any existing children (e.g., a dummy placeholder item)
            item.takeChildren()
        
            for name in sorted(os.listdir(dir_path)):
                abs_path = os.path.join(dir_path, name)
                
                try:
                    rel_path = os.path.relpath(abs_path, os.getcwd())
                except ValueError: # Path is on a different drive on Windows
                    logging.warning(f"Skipping {abs_path}: not on current drive.")
                    continue
                
                # If an item for this relative path already exists in the dictionary, skip
                # This can happen if some subdirectories were part of the initial 'files' list
                if rel_path in self.path_to_item:
                    continue

                new_item = QtWidgets.QTreeWidgetItem(item, [name])
                new_item.setData(0, QtCore.Qt.UserRole, abs_path)
                new_item.setFlags(new_item.flags() | QtCore.Qt.ItemIsUserCheckable)
                self.path_to_item[rel_path] = new_item
                
                is_excluded = smart_logic.exclude_spec.match_file(rel_path) or smart_logic.exclude_spec.match_file(rel_path + '/')
                
                if os.path.isdir(abs_path):
                    new_item.setIcon(0, self.folder_icon)
                    # For newly loaded directories, inherit check state from parent if not excluded
                    if is_excluded:
                        new_item.setCheckState(0, QtCore.Qt.Unchecked)
                    else:
                        new_item.setCheckState(0, item.checkState(0)) # Inherit from parent
                else: # File
                    new_item.setIcon(0, self.file_icon)
                    # Treat binary files as implicitly excluded
                    if smart_logic.is_binary_file(abs_path):
                        is_excluded = True

                    # Set check state based on parent, unless it's excluded or was specifically unchecked in prefs
                    if is_excluded:
                        new_item.setCheckState(0, QtCore.Qt.Unchecked)
                    elif self.prefs_loaded and rel_path in self.checked_files_from_prefs:
                        new_item.setCheckState(0, QtCore.Qt.Checked)
                    else:
                        # Inherit from parent if not specifically in prefs and not excluded
                        new_item.setCheckState(0, item.checkState(0))

        except OSError as e:
            logging.error(f"Error scanning directory {dir_path}: {e}")

    def handle_item_changed(self, item, column):
        if column == 0:
            self.tree_widget.blockSignals(True)
            try:
                new_state = item.checkState(0)
                # Apply check state to children
                def apply_to_children(parent_item, state):
                    for i in range(parent_item.childCount()):
                        child = parent_item.child(i)
                        if child.flags() & QtCore.Qt.ItemIsUserCheckable and child.flags() & QtCore.Qt.ItemIsEnabled:
                            abs_path = child.data(0, QtCore.Qt.UserRole)
                            
                            # Prevent checking excluded binary files if state is QtCore.Qt.Checked
                            if state == QtCore.Qt.Checked and abs_path and os.path.isfile(abs_path) and smart_logic.is_binary_file(abs_path):
                                child.setCheckState(0, QtCore.Qt.Unchecked)
                            else:
                                child.setCheckState(0, state)
                            
                            # Recursively apply to children of directories
                            if os.path.isdir(abs_path):
                                apply_to_children(child, state)
                                
                apply_to_children(item, new_state)

                # Update parent state based on children (if all children are checked/unchecked)
                parent = item.parent()
                while parent:
                    all_children_checked = True
                    all_children_unchecked = True
                    has_checkable_children = False
                    
                    for i in range(parent.childCount()):
                        child = parent.child(i)
                        if child.flags() & QtCore.Qt.ItemIsUserCheckable and child.flags() & QtCore.Qt.ItemIsEnabled:
                            has_checkable_children = True
                            if child.checkState(0) == QtCore.Qt.Checked:
                                all_children_unchecked = False
                            elif child.checkState(0) == QtCore.Qt.Unchecked:
                                all_children_checked = False
                            else: # Partially checked
                                all_children_checked = False
                                all_children_unchecked = False
                    
                    if has_checkable_children:
                        if all_children_checked:
                            parent.setCheckState(0, QtCore.Qt.Checked)
                        elif all_children_unchecked:
                            parent.setCheckState(0, QtCore.Qt.Unchecked)
                        else:
                            parent.setCheckState(0, QtCore.Qt.PartiallyChecked)
                    else: # No checkable children, or directory that has no files/folders to check
                        parent.setCheckState(0, QtCore.Qt.Unchecked) # Explicitly set to unchecked
                    parent = parent.parent()

            finally:
                self.tree_widget.blockSignals(False)

            # Auto-expand parent folders if a file is checked (using QTimer to avoid timing issues)
            if item.checkState(0) == QtCore.Qt.Checked:
                file_path = item.data(0, QtCore.Qt.UserRole)
                if file_path and os.path.isfile(file_path):
                    # Use QTimer to ensure expansion happens after signal processing
                    QtCore.QTimer.singleShot(0, lambda: self.expand_parents_of_item(item))

            self.update_token_counter()
            # Only save preferences when explicitly requested by the user, or on window close.

    def expand_parents_of_item(self, item):
        """Expand all parent folders of the given item."""
        parent = item.parent()
        while parent is not None:
            self.tree_widget.expandItem(parent)
            parent = parent.parent()
    
    def _load_global_presets(self):
        try:
            presets = global_preset_manager.get_all_presets()
            for label, text in presets:
                self._add_preset_button(label, text, from_global=True)
        except Exception as e: 
            logging.error(f"Failed to load global presets: {e}")
            
    def _add_preset_button(self, label: str, text: str, from_local=False, from_global=False):
        btn = QtWidgets.QPushButton(label)
        btn.setFixedHeight(22)
        btn.clicked.connect(lambda _=None, t=text: self._apply_preset(t))
        
        if from_global:
            btn.setToolTip(f"Global preset: {label}")
        else:
            btn.setToolTip(f"Preset: {label}")
            
        # Insert before the stretch. The add/delete buttons are at the start.
        # Layout: [add_btn, delete_btn, ..., stretch]
        # We want to insert before 'stretch'.
        insert_index = self.preset_strip.count() - 1 
        self.preset_strip.insertWidget(insert_index, btn)

    def _delete_preset(self, label, button, from_global):
        reply = QtWidgets.QMessageBox.question(self, "Delete Preset", f"Are you sure you want to delete the preset '{label}'?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            if from_global:
                if not global_preset_manager.delete_preset(label): 
                    QtWidgets.QMessageBox.warning(self, "Error", f"Failed to delete global preset '{label}'")
                    return
            else: 
                # This branch for 'local' presets is currently not used, as all presets are global.
                # It's kept for logical completeness but would require a local preset saving mechanism.
                self.presets = [(l, t) for l, t in self.presets if l != label]
            self.preset_strip.removeWidget(button)
            button.deleteLater()
            logging.info(f"Deleted preset: {label}")
    
    def _apply_preset(self, preset_text: str):
        current = self.prompt_textbox.toPlainText(); self.prompt_textbox.setPlainText((current.rstrip() + "\n\n" if current else "") + preset_text)

    def delete_preset_dialog(self):
        presets = global_preset_manager.get_all_presets()
        if not presets:
            QtWidgets.QMessageBox.information(self, "No Presets", "There are no presets to delete.")
            return

        preset_labels = [p[0] for p in presets]
        label_to_delete, ok = QtWidgets.QInputDialog.getItem(self, "Delete Preset", 
                                                             "Select a preset to delete:", preset_labels, 0, False)

        if ok and label_to_delete:
            # Find the button widget corresponding to the label
            button_to_remove = None
            for i in range(self.preset_strip.count()):
                item = self.preset_strip.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    if isinstance(widget, QtWidgets.QPushButton) and widget.text() == label_to_delete:
                        button_to_remove = widget
                        break
            
            if button_to_remove:
                # Call the existing delete logic, which includes the confirmation dialog.
                # All presets managed this way are considered global.
                self._delete_preset(label_to_delete, button_to_remove, from_global=True)
            else:
                # This is a descriptive error for debugging, in case the UI and data get out of sync.
                QtWidgets.QMessageBox.warning(self, "Error", "Could not find the corresponding button to delete. The UI might be out of sync.")
                
    def add_new_preset_dialog(self):
        lbl, ok = QtWidgets.QInputDialog.getText(self, "New preset", "Button label:");
        if not ok or not lbl.strip(): return
        dlg = QtWidgets.QDialog(self); dlg.setWindowTitle("Preset text"); dlg.setMinimumSize(400, 300); v = QtWidgets.QVBoxLayout(dlg)
        v.addWidget(QtWidgets.QLabel("Enter the preset text:")); text_edit = QtWidgets.QPlainTextEdit(); v.addWidget(text_edit)
        bb = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel); v.addWidget(bb); bb.accepted.connect(dlg.accept); bb.rejected.connect(dlg.reject)
        if dlg.exec() != QtWidgets.QDialog.Accepted: return
        txt = text_edit.toPlainText().strip()
        if txt and global_preset_manager.add_preset(lbl.strip(), txt): self._add_preset_button(lbl.strip(), txt, from_global=True)
        else: QtWidgets.QMessageBox.warning(self, "Error", "Failed to save preset.")
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() and event.mimeData().urls()[0].isLocalFile() and os.path.isdir(event.mimeData().urls()[0].toLocalFile()):
            event.acceptProposedAction()
    def dropEvent(self, event):
        folder_path = event.mimeData().urls()[0].toLocalFile()
        os.chdir(folder_path); from aicodeprep_gui.smart_logic import collect_all_files
        self.new_gui = FileSelectionGUI(collect_all_files()); self.new_gui.show(); self.close()
        
    def select_all(self):
        def check_all(item):
            # Only check if it's a file or a non-excluded folder
            abs_path = item.data(0, QtCore.Qt.UserRole)
            rel_path = os.path.relpath(abs_path, os.getcwd()) if abs_path else None
            is_excluded = False
            if rel_path:
                is_excluded = smart_logic.exclude_spec.match_file(rel_path) or smart_logic.exclude_spec.match_file(rel_path + '/')
                if os.path.isfile(abs_path) and smart_logic.is_binary_file(abs_path):
                    is_excluded = True # Treat binary files as implicitly excluded from 'select all'
            
            if item.flags() & QtCore.Qt.ItemIsUserCheckable and item.flags() & QtCore.Qt.ItemIsEnabled and not is_excluded:
                item.setCheckState(0, QtCore.Qt.Checked)
            else: # If it's excluded, uncheck it or keep unchecked
                 item.setCheckState(0, QtCore.Qt.Unchecked)

            for i in range(item.childCount()): 
                # Ensure children are loaded before processing, if it's a directory
                if os.path.isdir(abs_path):
                    self.on_item_expanded(item) # Ensures children are present for checking
                check_all(item.child(i))
        
        # Block signals temporarily to prevent recursive updates during mass selection
        self.tree_widget.blockSignals(True)
        try:
            for i in range(self.tree_widget.topLevelItemCount()): 
                check_all(self.tree_widget.topLevelItem(i))
        finally:
            self.tree_widget.blockSignals(False)
        self.update_token_counter()
        
    def deselect_all(self):
        iterator = QtWidgets.QTreeWidgetItemIterator(self.tree_widget)
        self.tree_widget.blockSignals(True) # Block signals during mass deselect
        try:
            while iterator.value():
                item = iterator.value()
                if item.flags() & QtCore.Qt.ItemIsUserCheckable: item.setCheckState(0, QtCore.Qt.Unchecked)
                iterator += 1
        finally:
            self.tree_widget.blockSignals(False)
        self.update_token_counter()

    def get_selected_files(self):
        selected = []; iterator = QtWidgets.QTreeWidgetItemIterator(self.tree_widget)
        while iterator.value():
            item = iterator.value()
            # Only consider files that are checked and not directories
            file_path = item.data(0, QtCore.Qt.UserRole)
            if file_path and os.path.isfile(file_path) and item.checkState(0) == QtCore.Qt.Checked:
                selected.append(file_path)
            iterator += 1
        return selected

    def process_selected(self):
        self._send_metric_event("generate_start", token_count=self.total_tokens)
        self.action = 'process'
        selected_files = self.get_selected_files()
        chosen_fmt = self.format_combo.currentData()
        prompt = self.prompt_textbox.toPlainText().strip()

        if process_files(
            selected_files,
            "fullcode.txt",
            fmt=chosen_fmt,
            prompt=prompt,
            prompt_to_top=self.prompt_top_checkbox.isChecked(),
            prompt_to_bottom=self.prompt_bottom_checkbox.isChecked()
        ) > 0:
            output_path = os.path.join(os.getcwd(), "fullcode.txt")
            # Now, just read the final content for the clipboard
            with open(output_path, "r", encoding="utf-8") as f:
                content = f.read()
            QtWidgets.QApplication.clipboard().setText(content)
            logging.info(f"Copied {len(content)} chars to clipboard.")
            self.text_label.setStyleSheet(
                f"font-size: 20px; color: {'#00c3ff' if self.is_dark_mode else '#0078d4'}; font-weight: bold;"
            )
            self.text_label.setText("Copied to clipboard and fullcode.txt")
            self.save_prefs()
            QtCore.QTimer.singleShot(1500, self.close)
        else:
            self.close()
            
    def quit_without_processing(self): self.action = 'quit'; self.close()
    
    def update_token_counter(self):
        total_tokens = 0
        for file_path in self.get_selected_files():
            if file_path not in self.file_token_counts:
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f: text = f.read()
                    self.file_token_counts[file_path] = len(text) // 4
                except Exception: self.file_token_counts[file_path] = 0
            total_tokens += self.file_token_counts[file_path]
        self.total_tokens = total_tokens; self.token_label.setText(f"Estimated tokens: {total_tokens:,}")
        
    def _expand_folders_for_paths(self, checked_paths: set):
        """Auto-expand folders that contain files from the given paths."""
        folders_to_expand = set()
        
        # Find all folders that should be expanded (containing checked files)
        for checked_path in checked_paths:
            # Get all parent directories of checked files
            path_parts = checked_path.split(os.sep)
            # Iterate up the path hierarchy to find parent directories
            current_path = ""
            for i, part in enumerate(path_parts):
                if i == 0:
                    current_path = part
                else:
                    current_path = os.path.join(current_path, part)
                
                # If it's a directory (and not the file itself)
                if current_path in self.path_to_item and os.path.isdir(self.path_to_item[current_path].data(0, QtCore.Qt.UserRole)):
                    folders_to_expand.add(self.path_to_item[current_path])
        
        # Expand the folders
        for item in folders_to_expand:
            self.tree_widget.expandItem(item)

    def auto_expand_common_folders(self):
        """Auto-expand common project folders on first load. (Currently not called from __init__)"""
        common_folders = ['src', 'lib', 'app', 'components', 'utils', 'helpers', 'models', 'views', 'controllers']
        
        for folder_name in common_folders:
            if folder_name in self.path_to_item:
                item = self.path_to_item[folder_name]
                self.tree_widget.expandItem(item)

    def load_from_prefs_button_clicked(self):
        prefs_path = _prefs_path()
        if os.path.exists(prefs_path):
            self.load_prefs_if_exists() # This re-populates self.checked_files_from_prefs etc.
            self.tree_widget.blockSignals(True)
            try:
                # First, deselect all files to provide a clean slate.
                # Directory states will be updated by handle_item_changed based on their children.
                iterator = QtWidgets.QTreeWidgetItemIterator(self.tree_widget)
                while iterator.value():
                    item = iterator.value()
                    # Only affect files here directly, directories will update based on children
                    if item.flags() & QtCore.Qt.ItemIsUserCheckable and os.path.isfile(item.data(0, QtCore.Qt.UserRole)):
                        item.setCheckState(0, QtCore.Qt.Unchecked) # Deselect all files first
                    iterator += 1

                # Then, check files based on preferences
                for rel_path in self.checked_files_from_prefs:
                    if rel_path in self.path_to_item:
                        item = self.path_to_item[rel_path]
                        if os.path.isfile(item.data(0, QtCore.Qt.UserRole)): # Only check files here
                            item.setCheckState(0, QtCore.Qt.Checked)
                            # Manually trigger parent updates for checked files, if not handled by setCheckState
                            parent = item.parent()
                            while parent:
                                if parent.checkState(0) != QtCore.Qt.PartiallyChecked and parent.checkState(0) != QtCore.Qt.Checked:
                                    # Set to partially checked if it was unchecked. Full check requires all children to be checked.
                                    parent.setCheckState(0, QtCore.Qt.PartiallyChecked) 
                                parent = parent.parent()

            finally:
                self.tree_widget.blockSignals(False)
            # Auto-expand folders after loading preferences
            self._expand_folders_for_paths(self.checked_files_from_prefs)
            file_type = ".auicp" if prefs_path.endswith(".auicp") else ".aicodeprep-gui"
            self.text_label.setText(f"Loaded selection from {file_type}")
            self.update_token_counter()
        else: 
            self.text_label.setText("No preferences file found (.aicodeprep-gui)")

    def closeEvent(self, event):
        # --- Feature Vote Dialog Trigger ---
        try:
            settings = QtCore.QSettings("aicodeprep-gui", "UserIdentity")
            has_voted = settings.value("has_voted_on_features_v1", False, type=bool)
            if getattr(self, "app_open_count", 0) >= 5 and not has_voted:
                dlg = VoteDialog(self.user_uuid, self.network_manager, parent=self)
                dlg.exec()
                settings.setValue("has_voted_on_features_v1", True)
        except Exception as e:
            logging.error(f"Error showing VoteDialog: {e}")

        # Clean up update thread if it's still running
        if self.update_thread and self.update_thread.isRunning():
            print("[gui] Stopping update check thread before closing...")
            self.update_thread.quit()
            if not self.update_thread.wait(3000):  # Wait up to 3 seconds
                print("[gui] Force terminating update check thread...")
                self.update_thread.terminate()
                self.update_thread.wait()
        
        if self.remember_checkbox and self.remember_checkbox.isChecked():
            self.save_prefs() # Save prefs only if 'remember' is checked
        if self.action != 'process': 
            self.action = 'quit'
            self._send_metric_event("quit")
        super(FileSelectionGUI, self).closeEvent(event)

    def load_prefs_if_exists(self):
        checked, window_size, splitter_state = _read_prefs_file()
        self.checked_files_from_prefs = checked
        self.window_size_from_prefs = window_size
        self.splitter_state_from_prefs = splitter_state
        self.prefs_loaded = True

    def save_prefs(self):
        checked_relpaths = []
        # Iterate through path_to_item to get only the checked files (not directories)
        for rel_path, item in self.path_to_item.items():
            if item.checkState(0) == QtCore.Qt.Checked:
                file_path_abs = item.data(0, QtCore.Qt.UserRole)
                if file_path_abs and os.path.isfile(file_path_abs): # Only save files, not directories
                    checked_relpaths.append(rel_path)
        
        size = self.size()
        splitter_state = self.splitter.saveState()
        _write_prefs_file(checked_relpaths, window_size=(size.width(), size.height()), splitter_state=splitter_state)
        self._save_prompt_options()

    def _load_prompt_options(self):
        """Load global prompt/question placement options from QSettings."""
        settings = QtCore.QSettings("aicodeprep-gui", "PromptOptions")
        self.prompt_top_checkbox.setChecked(settings.value("prompt_to_top", True, type=bool))
        self.prompt_bottom_checkbox.setChecked(settings.value("prompt_to_bottom", True, type=bool))

    def _save_prompt_options(self):
        """Save global prompt/question placement options to QSettings."""
        settings = QtCore.QSettings("aicodeprep-gui", "PromptOptions")
        settings.setValue("prompt_to_top", self.prompt_top_checkbox.isChecked())
        settings.setValue("prompt_to_bottom", self.prompt_bottom_checkbox.isChecked())

    def _load_dark_mode_setting(self) -> bool:
        """Load dark mode preference from QSettings, or use system preference if not set."""
        try:
            settings = QtCore.QSettings("aicodeprep-gui", "Appearance")
            if settings.contains("dark_mode"):
                return settings.value("dark_mode", type=bool)
            else:
                # Use system preference as default, save it for next time
                dark = system_pref_is_dark()
                settings.setValue("dark_mode", dark)
                return dark
        except Exception as e:
            logging.error(f"Failed to load dark mode setting: {e}")
            # Fallback to system preference
            return system_pref_is_dark()

    def _save_dark_mode_setting(self):
        """Save current dark mode state to QSettings."""
        try:
            settings = QtCore.QSettings("aicodeprep-gui", "Appearance")
            settings.setValue("dark_mode", self.is_dark_mode)
        except Exception as e:
            logging.error(f"Failed to save dark mode setting: {e}")

    def toggle_dark_mode(self, state):
        self.is_dark_mode = bool(state)
        # 1. Apply the correct palette for the entire application
        if self.is_dark_mode:
            apply_dark_palette(self.app)
        else:
            apply_light_palette(self.app)

        # 2. Re-apply the main window's font stylesheet to force style refresh
        font_stack = '"Segoe UI", "Ubuntu", "Helvetica Neue", Arial, sans-serif'
        self.setStyleSheet(f"font-family: {font_stack};")

        # 3. Now, apply the more specific widget styles as before
        base_style = """
            QTreeView, QTreeWidget {
                outline: 2; /* Remove focus rectangle */
            }
        """
        checkbox_style = get_checkbox_style_dark() if self.is_dark_mode else get_checkbox_style_light()
        self.tree_widget.setStyleSheet(base_style + checkbox_style)
        
        # Update theme-aware styles for other widgets
        self.vibe_label.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #40203f, stop:1 #1f103f); "
            "color: white; padding: 0px 0px 0px 0px; border-radius: 8px;"
        )
        # Find preset_explanation and text_label by attribute
        for child in self.findChildren(QtWidgets.QLabel):
            if getattr(child, "objectName", lambda: "")() == "preset_explanation":
                child.setStyleSheet(
                    f"font-size: 10px; color: {'#bbbbbb' if self.is_dark_mode else '#444444'};"
                )
        # Update the status label's style if it has text
        if self.text_label.text():
            self.text_label.setStyleSheet(
                f"font-size: 20px; color: {'#00c3ff' if self.is_dark_mode else '#0078d4'}; font-weight: bold;"
            )

        # Save the user's dark mode preference
        self._save_dark_mode_setting()

    def _start_update_check(self):
        """Start the update check and store the thread reference."""
        print("[gui] Starting update check...")
        self.update_thread = update_checker.check_for_updates(self._on_update_checked, parent=self, force=self.force_update)
        if self.update_thread:
            print("[gui] Update check thread started")
        else:
            print("[gui] Update check skipped (already checked recently)")

    def _on_update_checked(self, new_available: bool, latest: str):
        """Slot called when update check completes."""

        # --- Update label logic ---
        if hasattr(self, "update_label"):
            if new_available:
                self.update_label.setText('Update available! Open a terminal and type:<br><b>pipx upgrade aicodeprep-gui</b>')
                self.update_label.setStyleSheet("color: #28a745; font-weight: bold;")
                self.update_label.setVisible(True)
            else:
                self.update_label.setVisible(False)

        self.latest_pypi_version = latest
        print(f"[gui] Update check callback received - New available: {new_available}, Latest: {latest}")
        from PySide6.QtCore import QSettings, QDate, QDateTime, Qt
        from PySide6.QtWidgets import QMessageBox, QPushButton
        import subprocess

        ORG = "aicodeprep-gui"
        GROUP = "UpdateChecker"
        KEY_LAST_PROMPT = "last_prompt"
        KEY_PROMPTED_THIS_RUN = "prompted_this_run"

        settings = QSettings(ORG, GROUP)
        today = QDate.currentDate().toString(Qt.ISODate)
        prompted_this_run = settings.value(KEY_PROMPTED_THIS_RUN, False, type=bool)
        last_prompt = settings.value(KEY_LAST_PROMPT, "")

        print(f"[gui] Prompt check - prompted_this_run: {prompted_this_run}, last_prompt: {last_prompt}, today: {today}")

        # Only prompt if new version, not already prompted today, and not this run
        if not new_available or prompted_this_run or last_prompt == today:
            print("[gui] Not showing update dialog (conditions not met)")
            return

        print("[gui] Showing update available dialog")

        # Mark as prompted for this run and today
        settings.setValue(KEY_PROMPTED_THIS_RUN, True)
        settings.setValue(KEY_LAST_PROMPT, today)

        msg = QMessageBox(self)
        msg.setWindowTitle("Update Available")
        msg.setIcon(QMessageBox.Information)
        msg.setText(
            f"A new version of aicodeprep-gui is available: {latest}. You are on {__version__}.\n"
            "Would you like to upgrade now?"
        )
        upgrade_btn = msg.addButton("Upgrade", QMessageBox.AcceptRole)
        later_btn = msg.addButton("Later", QMessageBox.RejectRole)
        msg.setStandardButtons(QMessageBox.NoButton)
        msg.setModal(False)
        msg.show()

        def on_button_clicked(btn):
            if btn == upgrade_btn:
                # Run pipx upgrade in subprocess, show result
                try:
                    proc = subprocess.Popen(
                        ["pipx", "install", "--upgrade", "aicodeprep-gui"],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                    )
                    out, err = proc.communicate(timeout=120)
                    if proc.returncode == 0:
                        QMessageBox.information(self, "Upgrade Complete", "aicodeprep-gui was upgraded successfully.\nPlease restart the application.")
                    else:
                        QMessageBox.warning(self, "Upgrade Failed", f"Upgrade failed:\n{err or out}")
                except Exception as e:
                    QMessageBox.critical(self, "Upgrade Error", f"Could not run upgrade:\n{e}")
            msg.close()

        msg.buttonClicked.connect(on_button_clicked)

    def showEvent(self, event):
        super(FileSelectionGUI, self).showEvent(event)
        if getattr(self, "initial_show_event", False):
            QtCore.QTimer.singleShot(0, self._start_update_check)
            self.initial_show_event = False

    def open_links_dialog(self):
        """Shows a dialog with helpful links."""
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Help / Links and Guides")
        dialog.setMinimumWidth(450)
        
        layout = QtWidgets.QVBoxLayout(dialog)
        
        title_label = QtWidgets.QLabel("Helpful Links & Guides")
        title_font = QtGui.QFont()
        title_font.setBold(True)
        title_font.setPointSize(self.default_font.pointSize() + 2)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        layout.addSpacing(10)

        links_group = QtWidgets.QGroupBox("Click a link to open in your browser")
        links_layout = QtWidgets.QVBoxLayout(links_group)

        link1 = QtWidgets.QLabel('<a href="https://wuu73.org/blog/aiguide1.html">AI Coding on a Budget</a>')
        link1.setOpenExternalLinks(True)
        links_layout.addWidget(link1)

        link2 = QtWidgets.QLabel('<a href="https://wuu73.org/aicp">App Home Page</a>')
        link2.setOpenExternalLinks(True)
        links_layout.addWidget(link2)

        link3 = QtWidgets.QLabel('<a href="https://wuu73.org/blog/index.html">Quick Links to many AI web chats</a>')
        link3.setOpenExternalLinks(True)
        links_layout.addWidget(link3)
        
        layout.addWidget(links_group)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)
        
        dialog.exec()

    def open_complain_dialog(self):
        """Open the feedback/complain dialog."""
        import requests

        class FeedbackDialog(QtWidgets.QDialog):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.setWindowTitle("Send Ideas, bugs, thoughts!")
                self.setMinimumWidth(400)
                layout = QtWidgets.QVBoxLayout(self)

                layout.addWidget(QtWidgets.QLabel("Your Email (optional):"))
                self.email_input = QtWidgets.QLineEdit()
                self.email_input.setPlaceholderText("you@example.com")
                layout.addWidget(self.email_input)

                layout.addWidget(QtWidgets.QLabel("Message:"))
                self.msg_input = QtWidgets.QPlainTextEdit()
                self.msg_input.setPlaceholderText("Describe your idea, bug, or thought here...")
                layout.addWidget(self.msg_input)

                self.status_label = QtWidgets.QLabel("")
                self.status_label.setStyleSheet("color: #d43c2c;")
                layout.addWidget(self.status_label)

                btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
                btns.accepted.connect(self.accept)
                btns.rejected.connect(self.reject)
                layout.addWidget(btns)

            def get_data(self):
                return self.email_input.text().strip(), self.msg_input.toPlainText().strip()

        dlg = FeedbackDialog(self)
        if dlg.exec() != QtWidgets.QDialog.Accepted:
            return

        email, message = dlg.get_data()
        if not email and not message:
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter at least an email or a message.")
            return

        try:
            if message:
                # Submit bug report
                user_uuid = QtCore.QSettings("aicodeprep-gui", "UserIdentity").value("user_uuid", "")
                payload = {
                    "data": {
                        "summary": message.splitlines()[0][:80] if message else "No summary",
                        "details": message
                    },
                    "source_identifier": "aicodeprep-gui"
                }
                headers = {"Content-Type": "application/json"}
                if user_uuid:
                    headers["X-Client-ID"] = user_uuid
                resp = requests.post("https://wuu73.org/idea/collect/bug-report", json=payload, headers=headers, timeout=10)
                if resp.status_code == 200:
                    QtWidgets.QMessageBox.information(self, "Thank you", "Your feedback/complaint was submitted successfully.")
                else:
                    QtWidgets.QMessageBox.critical(self, "Error", f"Submission failed: {resp.status_code} {resp.text}")
            else:
                # Only email provided
                resp = requests.post("https://wuu73.org/idea/collect/submit", json={"email": email}, timeout=10)
                if resp.status_code == 200:
                    QtWidgets.QMessageBox.information(self, "Thank you", "Your email was submitted successfully.")
                else:
                    QtWidgets.QMessageBox.critical(self, "Error", f"Submission failed: {resp.status_code} {resp.text}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Could not submit feedback: {e}")

    def open_about_dialog(self):
        """Show About dialog with version, install age, and links."""
        # read install_date from user settings
        settings = QtCore.QSettings("aicodeprep-gui", "UserIdentity")
        install_date_str = settings.value("install_date", "")
        try:
            dt = datetime.fromisoformat(install_date_str)
            days_installed = (datetime.now() - dt).days
        except Exception:
            days_installed = 0

        # build HTML content
        version_str = __version__

        pypi_version_info = ""
        if self.latest_pypi_version:
            is_newer = update_checker.is_newer_version(__version__, self.latest_pypi_version)
            if is_newer:
                status_text = '<span style="color: #28a745; font-weight: bold;">(Update available)</span>'
            else:
                status_text = '<span style="color: grey;">(Up to date)</span>'
            pypi_version_info = f'<p>Latest version: {self.latest_pypi_version} {status_text}</p>'
        else:
            pypi_version_info = '<p>Latest version: <span style="color: grey;">Checking PyPI...</span></p>'

        html = (
            f"<h2>aicodeprep-gui</h2>"
            f"<p>Installed version: {version_str}</p>"
            f"{pypi_version_info}"
            f"<p>Installed {days_installed} days ago.</p>"
            "<p>"
            '<br><a href="https://github.com/sponsors/detroittommy879">GitHub Sponsors</a><br>'
            '<a href="https://wuu73.org/aicp">AI Code Prep Homepage</a>'
            "</p>"
        )
        # show in rich-text message box
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle("About aicodeprep-gui")
        dlg.setTextFormat(QtCore.Qt.RichText)
        dlg.setText(html)
        dlg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        dlg.exec()

    def _send_metric_event(self, event_type: str, token_count: int = None):
        """Sends an application event to the metrics endpoint in a non-blocking way."""
        try:
            if not hasattr(self, 'user_uuid') or not self.user_uuid:
                logging.warning("Metrics: user_uuid not found, skipping event.")
                return

            endpoint_url = "https://wuu73.org/idea/aicp-metrics/event"
            request = QtNetwork.QNetworkRequest(QtCore.QUrl(endpoint_url))
            request.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, "application/json")

            payload = {
                "user_id": self.user_uuid,
                "event_type": event_type,
                "local_time": datetime.now().isoformat()
            }
            if token_count is not None:
                payload["token_count"] = token_count

            json_data = QtCore.QByteArray(json.dumps(payload).encode('utf-8'))

            # Use the existing network manager to send a fire-and-forget request
            self.network_manager.post(request, json_data)
            logging.info(f"Sent metric event: {event_type}")

        except Exception as e:
            logging.error(f"Error creating metric request for event '{event_type}': {e}")

def show_file_selection_gui(files, force_update=False):
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    gui = FileSelectionGUI(files, force_update=force_update)
    gui.show()
    app.exec()
    return gui.action, gui.get_selected_files()

def _prefs_path():
    """Get the path to the preferences file, preferring .aicodeprep-gui, with .auicp as legacy for migration"""
    new_path = os.path.join(os.getcwd(), ".aicodeprep-gui")
    legacy_path = os.path.join(os.getcwd(), ".auicp")
    # Prefer new file
    if os.path.exists(new_path):
        return new_path
    # Fallback to legacy for migration
    elif os.path.exists(legacy_path):
        return legacy_path
    # Default to new file for new saves
    else:
        return new_path

def _write_prefs_file(checked_relpaths, window_size=None, splitter_state=None):
    """Write preferences to .aicodeprep-gui file"""
    new_path = os.path.join(os.getcwd(), ".aicodeprep-gui")
    try:
        with open(new_path, "w", encoding="utf-8") as f:
            header = (
                f"# .aicodeprep-gui LLM/AI context helper settings file\n"
                f"# This file stores your preferences (checked code files, window size) for this folder.\n"
                f"# Generated by aicodeprep-gui.\n"
                f"# Homepage: https://wuu73.org/aicp\n"
                f"# GitHub: https://github.com/detroittommy879/aicodeprep-gui\n"
                f"# ----------------------------------------------------------\n"
                f"# aicodeprep-gui preferences file version {AICODEPREP_GUI_VERSION}\n"
            )
            f.write(header)
            f.write(f"version={AICODEPREP_GUI_VERSION}\n\n")
            if window_size:
                f.write(f"[window]\nwidth={window_size[0]}\nheight={window_size[1]}\n")
                if splitter_state is not None:
                    # Convert QByteArray to base64 string for storage
                    import base64
                    splitter_data = base64.b64encode(splitter_state).decode('utf-8')
                    f.write(f"splitter_state={splitter_data}\n")
                f.write("\n")
            if checked_relpaths: f.write("[files]\n" + "\n".join(checked_relpaths) + "\n")
        logging.info(f"Saved preferences to {new_path}")
    except Exception as e: 
        logging.warning(f"Could not write .aicodeprep-gui: {e}")

def _read_prefs_file():
    """Read preferences file with backwards compatibility for legacy .auicp files (migrates to .aicodeprep-gui)"""
    checked, window_size, splitter_state = set(), None, None
    width_val, height_val = None, None 

    legacy_path = os.path.join(os.getcwd(), ".auicp")
    new_path = os.path.join(os.getcwd(), ".aicodeprep-gui")

    prefs_path = _prefs_path()

    try:
        with open(prefs_path, "r", encoding="utf-8") as f:
            section = None
            for line in f.read().splitlines():
                if line.strip().startswith('[') and line.strip().endswith(']'):
                    section = line.strip()[1:-1]
                    continue
                if not section: continue

                if section == "files":
                    if line.strip(): checked.add(line.strip())
                elif section == "window":
                    if line.startswith('width='):
                        try: width_val = int(line.split('=')[1])
                        except (ValueError, IndexError): pass
                    elif line.startswith('height='):
                        try: height_val = int(line.split('=')[1])
                        except (ValueError, IndexError): pass
                    elif line.startswith('splitter_state='):
                        try:
                            import base64
                            splitter_data = line.split('=', 1)[1]
                            splitter_state = base64.b64decode(splitter_data.encode('utf-8'))
                        except Exception as e:
                            logging.warning(f"Failed to decode splitter state: {e}")

            if width_val is not None and height_val is not None:
                window_size = (width_val, height_val)

        # Migration logic: if we read from .auicp, migrate to .aicodeprep-gui
        if prefs_path == legacy_path and not os.path.exists(new_path):
            logging.info("Migrating preferences from .auicp to .aicodeprep-gui")
            try:
                # Write the data to the new .aicodeprep-gui file
                _write_prefs_file(list(checked), window_size, splitter_state) 
                logging.info("Successfully migrated preferences to .aicodeprep-gui")
            except Exception as e:
                logging.error(f"Failed to migrate preferences: {e}")

    except FileNotFoundError:
        file_type = ".auicp" if prefs_path.endswith(".auicp") else ".aicodeprep-gui"
        logging.info(f"{file_type} file not found, will create on save.")
    except Exception as e:
        logging.error(f"Error reading preferences file: {e}")

    return checked, window_size, splitter_state

# --- Feature Voting Dialog ---
class VoteDialog(QtWidgets.QDialog):
    FEATURE_IDEAS = [
      "Idea 1: Add an optional preview pane to quickly view file contents.",
      "Idea 2: Allow users to add additional folders to the same context block from any location.",
      "Idea 3: Enable drag-and-drop functionality for adding files and folders directly into the app.",
      "Idea 4: Introduce partial or skeleton context for files, where only key details (e.g., file paths, function/class names) are included. This provides lightweight context without full file content, helping the AI recognize the file's existence with minimal data.",
      "Idea 5: Add an MCP Server feature to paste directly into the browser chat and emulate an API for seamless interaction.",
      "Idea 6: Create a 'Super Problem Solver' mode that leverages 3-4 AIs to collaboratively solve complex problems. This would send the context and prompt to multiple APIs, automatically compare outputs, and consolidate results for enhanced problem-solving.",
      "Idea 7: Auto Block Secrets - Automatically block sensitive information like API keys and secrets from being included in the context, ensuring user privacy and security.",
      "Idea 8: Add a command line option"
    ]

    def __init__(self, user_uuid, network_manager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Vote on New Features")
        self.setMinimumWidth(600)
        self.votes = {}
        self.user_uuid = user_uuid
        self.network_manager = network_manager

        layout = QtWidgets.QVBoxLayout(self)

        # Title
        title = QtWidgets.QLabel("Vote Screen!")
        title.setAlignment(QtCore.Qt.AlignHCenter)
        title.setStyleSheet("font-size: 28px; color: #1fa31f; font-weight: bold; margin-bottom: 12px;")
        layout.addWidget(title)

        # Feature voting rows
        self.button_groups = []
        for idx, idea in enumerate(self.FEATURE_IDEAS):
            row = QtWidgets.QHBoxLayout()
            label = QtWidgets.QLabel(idea)
            label.setWordWrap(True)
            label.setMinimumWidth(220)
            row.addWidget(label, 2)
            btns = []
            for opt in self.VOTE_OPTIONS:
                btn = QtWidgets.QPushButton(opt)
                btn.setCheckable(True)
                btn.setMinimumWidth(120)
                btn.clicked.connect(self._make_vote_handler(idx, opt, btn))
                row.addWidget(btn, 1)
                btns.append(btn)
            self.button_groups.append(btns)
            layout.addLayout(row)
            layout.addSpacing(4)

        # Bottom buttons
        btn_row = QtWidgets.QHBoxLayout()
        btn_row.addStretch()
        self.vote_btn = QtWidgets.QPushButton("Vote!")
        self.vote_btn.clicked.connect(self.submit_votes)
        btn_row.addWidget(self.vote_btn)
        self.skip_btn = QtWidgets.QPushButton("Skip")
        self.skip_btn.clicked.connect(self.reject)
        btn_row.addWidget(self.skip_btn)
        layout.addLayout(btn_row)

    def _make_vote_handler(self, idx, opt, btn):
        def handler():
            # Uncheck other buttons in this group
            for b in self.button_groups[idx]:
                if b is not btn:
                    b.setChecked(False)
                    b.setStyleSheet("")
            btn.setChecked(True)
            btn.setStyleSheet("background-color: #1fa31f; color: white;")
            self.votes[self.FEATURE_IDEAS[idx]] = opt
        return handler

    def submit_votes(self):
        # Collect votes for all features (if not voted, skip)
        details = {idea: self.votes.get(idea, None) for idea in self.FEATURE_IDEAS}
        payload = {
            "user_id": self.user_uuid,
            "event_type": "feature_vote",
            "local_time": datetime.now().isoformat(),
            "details": details
        }
        try:
            endpoint_url = "https://wuu73.org/idea/aicp-metrics/event"
            request = QtNetwork.QNetworkRequest(QtCore.QUrl(endpoint_url))
            request.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, "application/json")
            json_data = QtCore.QByteArray(json.dumps(payload).encode('utf-8'))
            self.network_manager.post(request, json_data)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Failed to submit votes: {e}")
        self.accept()
