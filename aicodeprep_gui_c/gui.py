import os
import sys
import platform
import logging
from PyQt5 import QtWidgets, QtCore, QtGui, QtNetwork
from typing import List, Tuple

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
        self.setWindowTitle("AI Code Prep - File Selection")
        self.app = QtWidgets.QApplication.instance()
        if self.app is None:
            self.app = QtWidgets.QApplication([])

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
        self.setGeometry(100, 100, int(600 * scale_factor), int(400 * scale_factor))
        
        # Layout
        main_layout = QtWidgets.QVBoxLayout(self)
        self.tree_widget = QtWidgets.QTreeWidget()
        self.tree_widget.setHeaderLabels(["File/Folder"])
        self.tree_widget.setColumnCount(1)
        self.tree_widget.setColumnWidth(0, int(400 * scale_factor))  # Wider for file paths
        self.tree_widget.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        main_layout.addWidget(self.tree_widget)
        
        # --- Build folder/file tree ---
        self.path_to_item = {}  # Maps folder path to QTreeWidgetItem
        self.checked_paths = set()
        for file_path, relative_path, is_included in files:
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
                        # Make folders not checkable but keep them enabled
                        folder_item.setFlags(folder_item.flags())
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

        # Button Layout
        button_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(button_layout)

        # Website link
        website_label = QtWidgets.QLabel("<a href=\"https://wuu73.org/aicp\">wuu73.org/aicp</a>")
        website_label.setOpenExternalLinks(True)
        website_label.setTextFormat(QtCore.Qt.RichText)
        button_layout.addWidget(website_label)

        # Create a network manager to handle requests
        self.network_manager = QtNetwork.QNetworkAccessManager()
        self.network_manager.finished.connect(self.handle_network_reply)

        # Use a QLabel to display the text
        self.text_label = QtWidgets.QLabel("")  # Start with an empty label
        self.text_label.setTextFormat(QtCore.Qt.RichText)
        self.text_label.setOpenExternalLinks(True)
        self.text_label.setWordWrap(True)
        # Insert the label into the layout
        main_layout.insertWidget(main_layout.indexOf(website_label) + 1, self.text_label)

        # Fetch content from the URL (silently)
        self.fetch_text_content()

        # Add some vertical space using QSpacerItem with a fixed height
        vertical_spacer = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        main_layout.insertItem(main_layout.indexOf(self.text_label) + 1, vertical_spacer)  # Insert below text_label

        button_layout.addStretch()

        # Buttons
        process_button = QtWidgets.QPushButton("Process Selected")
        process_button.clicked.connect(self.process_selected)
        button_layout.addWidget(process_button)

        select_all_button = QtWidgets.QPushButton("Select All")
        select_all_button.clicked.connect(self.select_all)
        button_layout.addWidget(select_all_button)

        deselect_all_button = QtWidgets.QPushButton("Deselect All")
        deselect_all_button.clicked.connect(self.deselect_all)
        button_layout.addWidget(deselect_all_button)

        self.selected_files = []
        
        # No need for manual column resize handling with the new header settings

    def handle_item_changed(self, item, column):
        if column == 0:
            file_path = item.data(0, QtCore.Qt.UserRole)
            if item.checkState(0) == QtCore.Qt.Checked:
                if file_path and file_path not in self.selected_files:
                    self.selected_files.append(file_path)
            else:
                if file_path and file_path in self.selected_files:
                    self.selected_files.remove(file_path)
                    
    def select_all(self):
        # Recursively select all file items
        def check_all_items(item):
            if item.flags() & QtCore.Qt.ItemIsUserCheckable:
                item.setCheckState(0, QtCore.Qt.Checked)
            for i in range(item.childCount()):
                check_all_items(item.child(i))
                
        for i in range(self.tree_widget.topLevelItemCount()):
            check_all_items(self.tree_widget.topLevelItem(i))

    def deselect_all(self):
        # Recursively deselect all file items
        def uncheck_all_items(item):
            if item.flags() & QtCore.Qt.ItemIsUserCheckable:
                item.setCheckState(0, QtCore.Qt.Unchecked)
            for i in range(item.childCount()):
                uncheck_all_items(item.child(i))                
        for i in range(self.tree_widget.topLevelItemCount()):
            uncheck_all_items(self.tree_widget.topLevelItem(i))
            
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
        self.get_selected_files()
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

def show_file_selection_gui(files):
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])

    gui = FileSelectionGUI(files)
    gui.show()
    app.exec_()
    return gui.selected_files