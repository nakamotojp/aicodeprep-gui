import os
import sys
import json
import logging
import requests
from datetime import datetime
from PySide6 import QtWidgets, QtCore, QtGui
from aicodeprep_gui import __version__

class VoteDialog(QtWidgets.QDialog):
    FEATURE_IDEAS = [
      "Idea 1: Add an optional preview pane to quickly view file contents.",
      "Idea 2: Allow users to add additional folders to the same context block from any location.",
      "Idea 3: Optional Caching so only the files/folders that have changed are scanned and/or processed.",
      "Idea 4: Introduce partial or skeleton context for files, where only key details (e.g., file paths, function/class names) are included. This provides lightweight context without full file content, helping the AI recognize the file's existence with minimal data.",
      "Idea 5: Context7",
      "Idea 6: Create a 'Super Problem Solver' mode that leverages 3-4 AIs to collaboratively solve complex problems. This would send the context and prompt to multiple APIs, automatically compare outputs, and consolidate results for enhanced problem-solving.",
      "Idea 7: Auto Block Secrets - Automatically block sensitive information like API keys and secrets from being included in the context, ensuring user privacy and security.",
      "Idea 8: Add a command line option to immediately create context, skip UI"
    ]
    
    VOTE_OPTIONS = ["High Priority", "Medium Priority", "Low Priority", "No Interest"]

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

class DialogManager:
    def __init__(self, parent_window):
        self.parent = parent_window

    def open_links_dialog(self):
        """Shows a dialog with helpful links."""
        dialog = QtWidgets.QDialog(self.parent)
        dialog.setWindowTitle("Help / Links and Guides")
        dialog.setMinimumWidth(450)
        
        layout = QtWidgets.QVBoxLayout(dialog)
        
        title_label = QtWidgets.QLabel("Helpful Links & Guides")
        title_font = QtGui.QFont()
        title_font.setBold(True)
        title_font.setPointSize(self.parent.default_font.pointSize() + 2)
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

        dlg = FeedbackDialog(self.parent)
        if dlg.exec() != QtWidgets.QDialog.Accepted:
            return

        email, message = dlg.get_data()
        if not email and not message:
            QtWidgets.QMessageBox.warning(self.parent, "Error", "Please enter at least an email or a message.")
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
                    QtWidgets.QMessageBox.information(self.parent, "Thank you", "Your feedback/complaint was submitted successfully.")
                else:
                    QtWidgets.QMessageBox.critical(self.parent, "Error", f"Submission failed: {resp.status_code} {resp.text}")
            else:
                # Only email provided
                resp = requests.post("https://wuu73.org/idea/collect/submit", json={"email": email}, timeout=10)
                if resp.status_code == 200:
                    QtWidgets.QMessageBox.information(self.parent, "Thank you", "Your email was submitted successfully.")
                else:
                    QtWidgets.QMessageBox.critical(self.parent, "Error", f"Submission failed: {resp.status_code} {resp.text}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.parent, "Error", f"Could not submit feedback: {e}")

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

        version_str = __version__

        html = (
            f"<h2>aicodeprep-gui</h2>"
            f"<p>Installed version: {version_str}</p>"
            f"<p>Installed {days_installed} days ago.</p>"
            "<p>"
            '<br><a href="https://github.com/sponsors/detroittommy879">GitHub Sponsors</a><br>'
            '<a href="https://wuu73.org/aicp">AI Code Prep Homepage</a>'
            "</p>"
        )
        # show in rich-text message box
        dlg = QtWidgets.QMessageBox(self.parent)
        dlg.setWindowTitle("About aicodeprep-gui")
        dlg.setTextFormat(QtCore.Qt.RichText)
        dlg.setText(html)
        dlg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        dlg.exec()

    def add_new_preset_dialog(self):
        from ..settings.presets import global_preset_manager
        
        lbl, ok = QtWidgets.QInputDialog.getText(self.parent, "New preset", "Button label:")
        if not ok or not lbl.strip(): 
            return
        
        dlg = QtWidgets.QDialog(self.parent)
        dlg.setWindowTitle("Preset text")
        dlg.setMinimumSize(400, 300)
        v = QtWidgets.QVBoxLayout(dlg)
        v.addWidget(QtWidgets.QLabel("Enter the preset text:"))
        text_edit = QtWidgets.QPlainTextEdit()
        v.addWidget(text_edit)
        bb = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        v.addWidget(bb)
        bb.accepted.connect(dlg.accept)
        bb.rejected.connect(dlg.reject)
        
        if dlg.exec() != QtWidgets.QDialog.Accepted: 
            return
        
        txt = text_edit.toPlainText().strip()
        if txt and global_preset_manager.add_preset(lbl.strip(), txt): 
            self.parent.preset_manager._add_preset_button(lbl.strip(), txt, from_global=True)
        else: 
            QtWidgets.QMessageBox.warning(self.parent, "Error", "Failed to save preset.")

    def delete_preset_dialog(self):
        from ..settings.presets import global_preset_manager
        
        presets = global_preset_manager.get_all_presets()
        if not presets:
            QtWidgets.QMessageBox.information(self.parent, "No Presets", "There are no presets to delete.")
            return

        preset_labels = [p[0] for p in presets]
        label_to_delete, ok = QtWidgets.QInputDialog.getItem(self.parent, "Delete Preset", 
                                                             "Select a preset to delete:", preset_labels, 0, False)

        if ok and label_to_delete:
            # Find the button widget corresponding to the label
            button_to_remove = None
            for i in range(self.parent.preset_strip.count()):
                item = self.parent.preset_strip.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    if isinstance(widget, QtWidgets.QPushButton) and widget.text() == label_to_delete:
                        button_to_remove = widget
                        break
            
            if button_to_remove:
                # Call the existing delete logic, which includes the confirmation dialog.
                self.parent.preset_manager._delete_preset(label_to_delete, button_to_remove, from_global=True)
            else:
                QtWidgets.QMessageBox.warning(self.parent, "Error", "Could not find the corresponding button to delete. The UI might be out of sync.")
