import os
import sys
import platform
import logging
from PyQt5 import QtWidgets, QtCore, QtGui, QtNetwork
from typing import List, Tuple
try:
    import tiktoken
except ImportError:
    tiktoken = None
from aicodeprep_gui_c.smart_logic import (
    EXCLUDE_DIRS, EXCLUDE_FILES, EXCLUDE_EXTENSIONS, EXCLUDE_PATTERNS, CODE_EXTENSIONS,
    matches_pattern, is_excluded_directory
)
from aicodeprep_gui_c.file_processor import process_files

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

class FileSelectionGUI(QtWidgets.QWidget):
    def __init__(self, files):
        super().__init__()
        self.files = files  # Store files for preferences loading
        self.setWindowTitle("AI Code Prep - File Selection")
        self.app = QtWidgets.QApplication.instance()
        if self.app is None:
            self.app = QtWidgets.QApplication([])
        self.action = 'quit'  # Track user action: 'process' or 'quit'

        # .aicodeprep prefs
        self.prefs_filename = ".aicodeprep"
        self.remember_checkbox = None
        self.checked_files_from_prefs = set()
        self.prefs_loaded = False
        self.window_size_from_prefs = None
        self.load_prefs_if_exists()

        # DPI Awareness and Scaling
        if platform.system() == 'Windows':
            screen = self.app.primaryScreen()
            scale_factor = screen.logicalDotsPerInch() / 96.0
        else:
            scale_factor = self.app.primaryScreen().devicePixelRatio()

        # Font Configuration
        default_font_size = 9
        try:
            if platform.system() == 'Windows':
                system_font = 'Segoe UI'
            else:
                system_font = 'Arial'

            default_font_size = int(default_font_size * scale_factor)
            self.default_font = QtGui.QFont(system_font, default_font_size)
            self.tree_font = QtGui.QFont(system_font, default_font_size + 1)
            self.checkbox_font = QtGui.QFont(system_font, int(default_font_size * 1.2))
            self.setFont(self.default_font)
            logging.info(f"Using system font: {system_font}, Size: {default_font_size}")
        except Exception as e:
            logging.warning(f"Font/scaling error: {e}")
            self.default_font = QtGui.QFont('Arial', default_font_size)
            self.tree_font = QtGui.QFont('Arial', default_font_size + 1)
            self.checkbox_font = QtGui.QFont('Arial', int(default_font_size * 1.2))

        # Geometry
        if self.window_size_from_prefs:
            w, h = self.window_size_from_prefs
            self.setGeometry(100, 100, w, h)
        else:
            self.setGeometry(100, 100, int(600 * scale_factor), int(400 * scale_factor))
        
        # Layout
        main_layout = QtWidgets.QVBoxLayout(self)
        # Token count label
        self.token_label = QtWidgets.QLabel("Estimated tokens: 0")
        main_layout.addWidget(self.token_label)
        # Status label for messages
        self.text_label = QtWidgets.QLabel("")
        self.text_label.setWordWrap(True)
        main_layout.addWidget(self.text_label)

        # --- Splitter for file tree and prompt ---
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        # File tree
        self.tree_widget = QtWidgets.QTreeWidget()
        self.tree_widget.setHeaderLabels(["File/Folder"])
        self.tree_widget.setColumnCount(1)
        self.tree_widget.setColumnWidth(0, int(400 * scale_factor))  # Wider for file paths
        self.tree_widget.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.splitter.addWidget(self.tree_widget)
        # Prompt area (label + textbox in a widget)
        prompt_widget = QtWidgets.QWidget()
        prompt_layout = QtWidgets.QVBoxLayout(prompt_widget)
        prompt_layout.setContentsMargins(0, 0, 0, 0)
        prompt_label = QtWidgets.QLabel("Optional prompt/question for LLM (will be appended to the end):")
        prompt_layout.addWidget(prompt_label)
        self.prompt_textbox = QtWidgets.QTextEdit()
        self.prompt_textbox.setPlaceholderText("Type your question or prompt here (optional)...")
        self.prompt_textbox.setMinimumHeight(50)
        self.prompt_textbox.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        prompt_layout.addWidget(self.prompt_textbox)
        self.splitter.addWidget(prompt_widget)
        self.splitter.setStretchFactor(0, 4)
        self.splitter.setStretchFactor(1, 1)
        main_layout.addWidget(self.splitter)

        # --- Build folder/file tree ---
        self.path_to_item = {}  # Maps folder path to QTreeWidgetItem
        self.checked_paths = set()
        for file_path, relative_path, is_included in files:
            # If prefs loaded, override: only check files in prefs, uncheck all others
            if self.prefs_loaded:
                is_included = relative_path in self.checked_files_from_prefs
            if is_included:
                self.checked_paths.add(relative_path)
            parts = relative_path.split(os.sep)
            parent = self.tree_widget
            parent_path = ""
            for i, part in enumerate(parts):
                curr_path = os.sep.join(parts[:i+1])
                is_file = (i == len(parts) - 1)
                if curr_path not in self.path_to_item:
                    if is_file:
                        item = QtWidgets.QTreeWidgetItem()
                        item.setText(0, part)  # Show filename in column 0
                        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                        item.setCheckState(0, QtCore.Qt.Checked if is_included else QtCore.Qt.Unchecked)
                        item.setData(0, QtCore.Qt.UserRole, file_path)
                        parent.addTopLevelItem(item) if parent is self.tree_widget else parent.addChild(item)
                        self.path_to_item[curr_path] = item
                    else:
                        folder_item = QtWidgets.QTreeWidgetItem()
                        folder_item.setText(0, part)
                        # Make folders checkable
                        folder_item.setFlags(folder_item.flags() | QtCore.Qt.ItemIsUserCheckable)
                        folder_item.setCheckState(0, QtCore.Qt.Checked if is_included else QtCore.Qt.Unchecked)
                        parent.addTopLevelItem(folder_item) if parent is self.tree_widget else parent.addChild(folder_item)
                        self.path_to_item[curr_path] = folder_item
                    parent = self.path_to_item[curr_path]
                else:
                    parent = self.path_to_item[curr_path]

        self.tree_widget.itemChanged.connect(self.handle_item_changed)

        # --- Auto-expand folders to checked files ---
        def expand_to_checked(item):
            expanded = False
            for i in range(item.childCount()):
                child = item.child(i)
                if child.childCount() > 0:
                    if expand_to_checked(child):
                        self.tree_widget.expandItem(child)
                        expanded = True
                else:
                    if child.checkState(0) == QtCore.Qt.Checked:
                        expanded = True
            return expanded

        for i in range(self.tree_widget.topLevelItemCount()):
            top_item = self.tree_widget.topLevelItem(i)
            if expand_to_checked(top_item):
                self.tree_widget.expandItem(top_item)

        # --- Preferences Checkbox ---
        prefs_checkbox_layout = QtWidgets.QHBoxLayout()
        self.remember_checkbox = QtWidgets.QCheckBox("Remember checked files for this folder (.aicodeprep) and window size")
        self.remember_checkbox.setChecked(True)
        prefs_checkbox_layout.addWidget(self.remember_checkbox)
        prefs_checkbox_layout.addStretch()
        main_layout.addLayout(prefs_checkbox_layout)

        # --- Button Layout: two rows, right-aligned ---
        button_layout1 = QtWidgets.QHBoxLayout()
        button_layout2 = QtWidgets.QHBoxLayout()
        main_layout.addLayout(button_layout1)
        main_layout.addLayout(button_layout2)

        # Website link (left side, above buttons)
        website_label = QtWidgets.QLabel("<a href=\"https://wuu73.org/aicp\">wuu73.org/aicp</a>")
        website_label.setOpenExternalLinks(True)
        website_label.setTextFormat(QtCore.Qt.RichText)
        main_layout.insertWidget(main_layout.count() - 2, website_label)  # Place above buttons

        # First row of buttons (right-aligned)
        button_layout1.addStretch()
        process_button = QtWidgets.QPushButton("Process Selected")
        process_button.clicked.connect(self.process_selected)
        button_layout1.addWidget(process_button)

        select_all_button = QtWidgets.QPushButton("Select All")
        select_all_button.clicked.connect(self.select_all)
        button_layout1.addWidget(select_all_button)

        deselect_all_button = QtWidgets.QPushButton("Deselect All")
        deselect_all_button.clicked.connect(self.deselect_all)
        button_layout1.addWidget(deselect_all_button)

        # Second row of buttons (right-aligned)
        button_layout2.addStretch()
        load_prefs_button = QtWidgets.QPushButton("Load from .aicodeprep")
        load_prefs_button.clicked.connect(self.load_from_prefs_button_clicked)
        button_layout2.addWidget(load_prefs_button)

        quit_button = QtWidgets.QPushButton("Quit")
        quit_button.clicked.connect(self.quit_without_processing)
        button_layout2.addWidget(quit_button)

        self.selected_files = []
        self.file_token_counts = {}
        self.update_token_counter()

    def handle_item_changed(self, item, column):
        if column == 0:
            file_path = item.data(0, QtCore.Qt.UserRole)
            # If it's a folder (no file_path), do smart recursive check/uncheck
            if file_path is None:
                def should_skip_folder(folder_item):
                    # Compose full path from tree
                    path_parts = []
                    curr = folder_item
                    while curr is not None and curr.parent() is not None:
                        path_parts.insert(0, curr.text(0))
                        curr = curr.parent()
                    if curr is not None and curr.parent() is None:
                        path_parts.insert(0, curr.text(0))
                    folder_path = os.path.join(*path_parts)
                    return (folder_item.text(0) in EXCLUDE_DIRS or
                            is_excluded_directory(folder_path))
                def smart_check(item, check_state):
                    # Skip blocked folders
                    if should_skip_folder(item):
                        item.setCheckState(0, QtCore.Qt.Unchecked)
                        return
                    for i in range(item.childCount()):
                        child = item.child(i)
                        child_file_path = child.data(0, QtCore.Qt.UserRole)
                        if child_file_path:
                            # It's a file
                            filename = os.path.basename(child_file_path)
                            ext = os.path.splitext(filename)[1].lower()
                            if (filename in EXCLUDE_FILES or
                                ext in EXCLUDE_EXTENSIONS or
                                any(matches_pattern(filename, pat) for pat in EXCLUDE_PATTERNS)):
                                child.setCheckState(0, QtCore.Qt.Unchecked)
                                continue
                            child.setCheckState(0, check_state)
                        else:
                            # It's a folder
                            smart_check(child, check_state)
                    item.setCheckState(0, check_state)
                smart_check(item, item.checkState(0))
            else:
                # File item: update selected_files as before
                if item.checkState(0) == QtCore.Qt.Checked:
                    if file_path and file_path not in self.selected_files:
                        self.selected_files.append(file_path)
                else:
                    if file_path and file_path in self.selected_files:
                        self.selected_files.remove(file_path)
            self.update_token_counter()
            # Save preferences on checkbox change if "Remember" is checked
            if self.remember_checkbox and self.remember_checkbox.isChecked():
                self.save_prefs()

    def select_all(self):
        # Recursively select all file items
        def check_all_items(item):
            if item.flags() & QtCore.Qt.ItemIsUserCheckable:
                item.setCheckState(0, QtCore.Qt.Checked)
            for i in range(item.childCount()):
                check_all_items(item.child(i))

        for i in range(self.tree_widget.topLevelItemCount()):
            check_all_items(self.tree_widget.topLevelItem(i))
        self.update_token_counter()

    def deselect_all(self):
        # Recursively deselect all file items
        def uncheck_all_items(item):
            if item.flags() & QtCore.Qt.ItemIsUserCheckable:
                item.setCheckState(0, QtCore.Qt.Unchecked)
            for i in range(item.childCount()):
                uncheck_all_items(item.child(i))

        for i in range(self.tree_widget.topLevelItemCount()):
            uncheck_all_items(self.tree_widget.topLevelItem(i))
        self.update_token_counter()

    def get_selected_files(self):
        self.selected_files = []

        # Recursively collect all checked files
        def collect_checked_files(item):
            if item.flags() & QtCore.Qt.ItemIsUserCheckable and item.checkState(0) == QtCore.Qt.Checked:
                file_path = item.data(0, QtCore.Qt.UserRole)
                if file_path:
                    self.selected_files.append(file_path)

            for i in range(item.childCount()):
                collect_checked_files(item.child(i))

        for i in range(self.tree_widget.topLevelItemCount()):
            collect_checked_files(self.tree_widget.topLevelItem(i))

        return self.selected_files

    def process_selected(self):
        self.action = 'process'  # Set action first
        logging.info(f"Process Selected clicked - action set to: {self.action}")
        selected_files = self.get_selected_files()
        files_processed_count = process_files(selected_files, "fullcode.txt")
        if files_processed_count > 0:
            output_path = os.path.join(os.getcwd(), "fullcode.txt")
            try:
                with open(output_path, "r", encoding="utf-8") as f:
                    full_code = f.read()
                # Append prompt if present
                prompt = self.prompt_textbox.toPlainText().strip()
                if prompt:
                    full_code += "\n\n" + prompt
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(full_code)
                app = QtWidgets.QApplication.instance()
                if app is None:
                    app = QtWidgets.QApplication([])
                clipboard = app.clipboard()
                clipboard.setText(full_code)
                logging.info(f"Copied {len(full_code)} characters to clipboard from {output_path}")
            except Exception as e:
                logging.error(f"Failed to copy to clipboard: {e}")
            # Save prefs if checkbox is checked
            if self.remember_checkbox and self.remember_checkbox.isChecked():
                self.save_prefs()
        else:
            logging.warning("No files selected or processed; skipping clipboard operation.")
        logging.info(f"Process Selected closing - action is: {self.action}")
        self.close()

    def fetch_text_content(self):
        url = "https://wuu73.org/aicp/display.txt"  # URL to fetch text from
        request = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
        self.network_manager.get(request)

    def handle_network_reply(self, reply):
        if reply.error() == QtNetwork.QNetworkReply.NoError:
            text = reply.readAll().data().decode()
            # Check if the text is not just whitespace
            if text.strip():
                # Convert plain text links to HTML links (basic link handling)
                text_with_links = self.convert_text_links_to_html(text)
                self.text_label.setText(text_with_links)
        # If there's an error or the content is empty, do nothing (silent handling)

    def convert_text_links_to_html(self, text):
        """Converts URLs in plain text to clickable HTML links (very basic)."""
        import re
        url_pattern = re.compile(r'(https?://\S+)')
        return url_pattern.sub(r'<a href="\1">\1</a>', text)

    def load_from_prefs_button_clicked(self):
        import os
        prefs_path = _prefs_path()
        if os.path.exists(prefs_path):
            self.load_prefs_if_exists()
            # Uncheck all first, then check those in prefs
            self.deselect_all()
            for file_path, relative_path, is_included in self.files:
                if relative_path in self.checked_files_from_prefs:
                    parts = relative_path.split(os.sep)
                    curr_path = os.sep.join(parts)
                    item = self.path_to_item.get(curr_path)
                    if item:
                        item.setCheckState(0, QtCore.Qt.Checked)
            # Optionally show a message
            self.text_label.setText("Loaded selection from .aicodeprep")
            self.update_token_counter()
        else:
            self.text_label.setText(".aicodeprep not found")

    def quit_without_processing(self):
        # Immediately close the window and exit the app without processing
        logging.info("Quit button clicked - setting action to quit")
        self.action = 'quit'
        self.close()

    def update_token_counter(self):
        selected_files = self.get_selected_files()
        total_tokens = 0
        for file_path in selected_files:
            if file_path not in self.file_token_counts:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        text = f.read()
                    if tiktoken:
                        enc = tiktoken.get_encoding("cl100k_base")
                        token_count = len(enc.encode(text))
                    else:
                        token_count = len(text) // 4
                    self.file_token_counts[file_path] = token_count
                except Exception as e:
                    self.file_token_counts[file_path] = 0
            total_tokens += self.file_token_counts[file_path]
        self.token_label.setText(f"Estimated tokens: {total_tokens:,}")

def show_file_selection_gui(files):
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])

    gui = FileSelectionGUI(files)
    gui.show()
    app.exec_()
    logging.info(f"GUI event loop finished - final action value: {gui.action}")
    return gui.action, gui.selected_files

# --- Preferences Save/Load Methods ---

def _prefs_path():
    # Always save/load in current working directory
    return os.path.join(os.getcwd(), ".aicodeprep")

def _write_prefs_file(checked_relpaths, window_size=None, splitter_state=None):
    try:
        with open(_prefs_path(), "w", encoding="utf-8") as f:
            if window_size or splitter_state:
                f.write("[window]\n")
                if window_size:
                    f.write(f"width={window_size[0]}\n")
                    f.write(f"height={window_size[1]}\n")
                if splitter_state:
                    # Convert splitter_state (QByteArray) to bytes, then hex string
                    f.write(f"splitter={bytes(splitter_state).hex()}\n")
                f.write("\n")
            for relpath in checked_relpaths:
                f.write(relpath + "\n")
    except Exception as e:
        logging.warning(f"Could not write .aicodeprep: {e}")


def _read_prefs_file():
    checked = set()
    window_size = None
    splitter_state = None
    try:
        with open(_prefs_path(), "r", encoding="utf-8") as f:
            lines = f.readlines()
        i = 0
        if lines and lines[0].strip() == '[window]':
            width = height = None
            for j in range(1, len(lines)):
                line = lines[j].strip()
                if line.startswith('width='):
                    width = int(line.split('=', 1)[1])
                elif line.startswith('height='):
                    height = int(line.split('=', 1)[1])
                elif line.startswith('splitter='):
                    splitter_state = bytes.fromhex(line.split('=', 1)[1])
                elif line == '':
                    i = j + 1
                    break
            if width and height:
                window_size = (width, height)
        for line in lines[i:]:
            line = line.strip()
            if line and not line.startswith('#'):
                checked.add(line)
    except Exception:
        pass
    return checked, window_size, splitter_state

# Add closeEvent to set action to 'quit' ONLY if window is closed via 'X'
def closeEvent(self, event):
    logging.info(f"closeEvent triggered - action before: {self.action}")
    # Only set to 'quit' if it wasn't already set to 'process'
    if self.action != 'process':
        self.action = 'quit'
    logging.info(f"closeEvent triggered - action after: {self.action}")
    super(FileSelectionGUI, self).closeEvent(event)

# Patch methods into FileSelectionGUI

def load_prefs_if_exists(self):
    prefs_path = _prefs_path()
    if os.path.exists(prefs_path):
        checked, window_size, splitter_state = _read_prefs_file()
        self.checked_files_from_prefs = checked
        self.window_size_from_prefs = window_size
        self.prefs_loaded = True
        # Restore splitter state if available
        if splitter_state and hasattr(self, "splitter"):
            self.splitter.restoreState(splitter_state)
    else:
        self.checked_files_from_prefs = set()
        self.window_size_from_prefs = None
        self.prefs_loaded = False

def save_prefs(self):
    checked_relpaths = []
    # Collect checked files using relative_path from self.files
    checked_files_set = set()

    def collect_checked_files(item):
        if item.flags() & QtCore.Qt.ItemIsUserCheckable and item.checkState(0) == QtCore.Qt.Checked:
            file_path = item.data(0, QtCore.Qt.UserRole)
            if file_path:
                checked_files_set.add(os.path.abspath(file_path))
        for i in range(item.childCount()):
            collect_checked_files(item.child(i))

    for i in range(self.tree_widget.topLevelItemCount()):
        collect_checked_files(self.tree_widget.topLevelItem(i))

    # Map absolute file paths back to relative_path as in self.files
    for file_path, relative_path, _ in self.files:
        if os.path.abspath(file_path) in checked_files_set:
            checked_relpaths.append(relative_path)

    # Save window size and splitter state
    size = self.size()
    window_size = (size.width(), size.height())
    splitter_state = self.splitter.saveState() if hasattr(self, "splitter") else None
    _write_prefs_file(checked_relpaths, window_size=window_size, splitter_state=splitter_state)

FileSelectionGUI.load_prefs_if_exists = load_prefs_if_exists
FileSelectionGUI.save_prefs = save_prefs
FileSelectionGUI.closeEvent = closeEvent
