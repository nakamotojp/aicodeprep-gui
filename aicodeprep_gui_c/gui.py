import os
import sys
import platform
import logging
from PyQt5 import QtWidgets, QtCore, QtGui
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
        self.tree_widget.setHeaderLabels(["", "File Path"])
        self.tree_widget.setColumnCount(2)
        self.tree_widget.setColumnWidth(0, int(30 * scale_factor))
        self.tree_widget.setColumnWidth(1, int(550 * scale_factor))
        self.tree_widget.header().setStretchLastSection(True)
        main_layout.addWidget(self.tree_widget)

        # Add Files to Treeview
        for file_path, relative_path, is_included in files:
            try:
                item = QtWidgets.QTreeWidgetItem(self.tree_widget)
                item.setText(1, relative_path)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState(0, QtCore.Qt.Checked if is_included else QtCore.Qt.Unchecked)
                item.setData(1, QtCore.Qt.UserRole, file_path)
                logging.debug(f"Added file to tree: {relative_path}")
            except Exception as e:
                logging.error(f"Failed to add file to tree: {relative_path}, Error: {str(e)}")

        self.tree_widget.itemChanged.connect(self.handle_item_changed)

        # Button Layout
        button_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(button_layout)

        # Buttons
        website_label = QtWidgets.QLabel("wuu73.org/aicp")
        button_layout.addWidget(website_label)
        button_layout.addStretch()

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

    def handle_item_changed(self, item, column):
        if column == 0:
            file_path = item.data(1, QtCore.Qt.UserRole)
            if item.checkState(0) == QtCore.Qt.Checked:
                if file_path not in self.selected_files:
                    self.selected_files.append(file_path)
            else:
                if file_path in self.selected_files:
                    self.selected_files.remove(file_path)

    def select_all(self):
        for i in range(self.tree_widget.topLevelItemCount()):
            item = self.tree_widget.topLevelItem(i)
            item.setCheckState(0, QtCore.Qt.Checked)

    def deselect_all(self):
        for i in range(self.tree_widget.topLevelItemCount()):
            item = self.tree_widget.topLevelItem(i)
            item.setCheckState(0, QtCore.Qt.Unchecked)

    def get_selected_files(self):
        self.selected_files = []
        for i in range(self.tree_widget.topLevelItemCount()):
            item = self.tree_widget.topLevelItem(i)
            if item.checkState(0) == QtCore.Qt.Checked:
                file_path = item.data(1, QtCore.Qt.UserRole)
                self.selected_files.append(file_path)
        return self.selected_files

    def process_selected(self):
        self.get_selected_files()
        self.close()

def show_file_selection_gui(files):
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])

    gui = FileSelectionGUI(files)
    gui.show()
    app.exec_()
    return gui.selected_files
