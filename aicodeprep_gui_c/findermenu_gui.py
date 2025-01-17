import sys
import subprocess
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QMessageBox, QTextBrowser
)
from PyQt5.QtCore import Qt

class FinderMenuGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout()
        
        # Finder Menu Section
        menu_label = QLabel("Finder Context Menu:")
        menu_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(menu_label)
        
        menu_buttons = QHBoxLayout()
        self.add_menu_btn = QPushButton("Add to Finder Menu")
        self.remove_menu_btn = QPushButton("Remove from Finder Menu")
        menu_buttons.addWidget(self.add_menu_btn)
        menu_buttons.addWidget(self.remove_menu_btn)
        main_layout.addLayout(menu_buttons)
        
        # Instructions
        self.instructions = QTextBrowser()
        self.instructions.setOpenExternalLinks(True)
        self.instructions.setHtml("""
            <p><b>Instructions:</b></p>
            <p>1. Click 'Add to Finder Menu' to install the service</p>
            <p>2. Open System Settings</p>
            <p>3. Go to Keyboard > Keyboard Shortcuts > Services</p>
            <p>4. Find and enable 'AI Code Prep' under Files and Folders</p>
            <p>5. Log out and back in for changes to take effect</p>
            <p><i>Note: If menu doesn't appear, try removing and adding again</i></p>
        """)
        main_layout.addWidget(self.instructions)
        
        # Status Section
        self.status_label = QLabel("Status: Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # Connect buttons
        self.add_menu_btn.clicked.connect(self.add_menu)
        self.remove_menu_btn.clicked.connect(self.remove_menu)
        
        # Window settings
        self.setLayout(main_layout)
        self.setWindowTitle("AI Code Prep GUI - Finder Menu Manager")
        self.setFixedSize(400, 400)
        
    def run_command(self, args):
        """Run command in new terminal window from project directory"""
        try:
            # Get the project directory
            project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # Create command string with explicit Python3 path
            command = f"cd '{project_dir}' && /usr/bin/env python3 aicodeprep_gui_c/findermenu-mac.py {args}"
            
            # Open new Terminal window and execute command
            subprocess.Popen(["osascript", "-e", f'tell app "Terminal" to do script "{command}"'])
            
            if args == "--add":
                self.status_label.setText("Status: Installing service... Check Terminal window")
                QMessageBox.information(self, "Adding Service", 
                    "Service installation started in Terminal.\n\n"
                    "1. Wait for the Terminal to finish\n"
                    "2. Follow the instructions to enable the service\n"
                    "3. Log out and back in for changes to take effect")
            else:
                self.status_label.setText("Status: Removing service... Check Terminal window")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to execute command: {str(e)}")
            self.status_label.setText("Status: Error")
        
    def add_menu(self):
        self.run_command("--add")
        
    def remove_menu(self):
        self.run_command("--remove")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinderMenuGUI()
    window.show()
    sys.exit(app.exec_())
