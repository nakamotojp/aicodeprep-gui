x add token counting, look for libraries to help

track user behavior like how much they use in a day etc,
maybe for errors also

x change yaml format to markdown

------ notes:

python -m aicodeprep_gui_c.main
linux python3
$ pyinstaller --onefile --add-data "aicodeprep_gui_c/data/default_config.md:aicodeprep_gui_c/data" aicodeprep_gui_c/main.py

pyside6

1. High-level goals
   • Drop PyQt5, adopt the latest PySide 6.\* series. Use context7 MCP server, to get the latest docs for pyside6.
   • Detect OS dark / light appearance at start-up and theme the GUI accordingly.  
   • Let the user toggle the theme with a checkbox (top-right corner, always visible).  
   • Keep the rest of the behaviour and file structure intact.  
   • Update packaging / install docs so only PySide6 is required.

2. Main tasks / work breakdown

   1. Packaging  
      a. pyproject.toml → replace  
       dependencies = [ "PySide6>=6.7", "tiktoken" ]  
      b. requirements.txt → delete all Qt5 lines, add `PySide6==<latest>` (look up exact version).

   2. Code-base migration (PyQt5 → PySide6)  
      a. In every `.py` file import Qt classes via  
       from PySide6 import QtCore, QtGui, QtWidgets, QtNetwork  
      b. Replace any `exec_()` with `exec()` (PySide keeps the alias but linting will complain).  
      c. Replace `QtWidgets.QApplication.desktop()` (deprecated) with `QApplication.primaryScreen()` if still present.  
      d. Remove `pyqtSignal`, `pyqtSlot` etc.; rename to `Signal`, `Slot` if used.  
      e. Search-and-replace `QtCore.Qt` enums that changed (`AlignHCenter` → `AlignmentFlag.AlignHCenter`, etc.).  
       (Most kept backward compat – verify with `dir(QtCore.Qt)`).

   3. Dark-/Light-mode detection utility  
      a. Create utils/apptheme.py with

      ```
      def system_pref_is_dark() -> bool:
          import platform, subprocess, ctypes, json, os, sys
          ...
      ```

      – On macOS: `defaults read -g AppleInterfaceStyle` == 'Dark'  
       – On Windows 10+: read registry `HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize\AppsUseLightTheme`  
       – Else: fall back to palette heuristic:  
       `return QtWidgets.QApplication.palette().color(QtGui.QPalette.Window).lightness() < 128`

   4. Dark palette helper

      ```
      def apply_dark_palette(app: QtWidgets.QApplication):
          dark = QtGui.QPalette()
          dark.setColor(QtGui.QPalette.Window, QtGui.QColor(53,53,53))
          ...
          app.setPalette(dark)
      ```

      Provide symmetrical `apply_light_palette`.

   5. GUI changes (aicodeprep_gui_c/gui.py)  
      a. At the very beginning, decide palette:

      ```
      if system_pref_is_dark():
          apply_dark_palette(self.app)
      ```

      b. Add a `QCheckBox("Dark mode")` into a small horizontal layout that is aligned top-right:

      ```
      title_bar_layout = QtWidgets.QHBoxLayout()
      title_bar_layout.addStretch()
      self.dark_mode_box = QtWidgets.QCheckBox("Dark")
      self.dark_mode_box.setChecked(system_pref_is_dark())
      title_bar_layout.addWidget(self.dark_mode_box)
      main_layout.addLayout(title_bar_layout, 0)
      ```

      Connect `stateChanged` → function that switches palettes on the fly.  
      c. Persist the user’s choice in `.aicodeprep` (optional but easy: add key `theme=dark|light`).

   6. Tests / smoke runs  
      • Run the GUI on Windows, macOS, Linux with both dark / light OS settings.  
      • Run `python -m aicodeprep_gui_c.main .` to ensure no runtime import errors.

3. Deliverables  
   • All modified source files committed.  
   • Updated pyproject.toml, requirements.txt.  
   • CHANGELOG/README sections that mention the move to PySide6 and the new dark-mode support.  
   • If time permits: an opt-in CLI flag `--theme=[auto|dark|light]` that overrides detection (stretch goal).

────────────────────────  
PROMPT FOR CLINE
────────────────────────
You are Cline, an expert Python/Qt engineer upgrading an existing project.  
Repository root contains `aicodeprep_gui_c/` as described below.

Tasks

1. Replace PyQt5 with PySide6 throughout the code-base.  
   – Every `from PyQt5 import ...` → `from PySide6 import ...`.  
   – Audit for API differences (`exec_`, enum names, Signals) and adjust.  
   – Project must run with PySide 6.7 or newer and **no PyQt5 installed**.

2. Add dark / light theme support.  
   a. Implement `aicodeprep_gui_c/apptheme.py` containing
   • `system_pref_is_dark()` – platform detection (macOS, Windows registry; fallback palette heuristic).  
    • `apply_dark_palette(app)` and `apply_light_palette(app)` – use Fusion style palettes.  
   b. In `gui.py`  
    • On init, call the detection and apply palette accordingly.  
    • Insert a `QCheckBox("Dark mode")` in the banner area (top-right corner).  
    • When toggled, switch between the palettes immediately.  
    • (Optional) persist setting in `.aicodeprep` under `[theme]` section.

3. Update packaging
   – `pyproject.toml`: remove `pyqt5`, add `PySide6>=6.7`.  
   – `requirements.txt`: prune PyQt5\* lines, add exact present latest.  
   – Confirm no other dependency still imports Qt5 modules.

4. Confirm all tests / manual smoke runs pass:

   ```
   python -m aicodeprep_gui_c.main .
   ```

   – GUI shows, inherits OS theme, checkbox works, file processing unchanged.

5. Update README “Installation” and “New Features” with:
   • “Switched to PySide6 backend for better licensing and Qt6 features.”  
   • “Automatic dark / light theme with manual override.”

Important constraints
• Do NOT introduce new top-level dependencies besides PySide6.  
• Keep file structure, entry point (`aicodeprep_gui_c.main:main`) intact.  
• All new code must follow the project’s existing logging scheme.  
• Final commit message: `feat: migrate to PySide6 & add dark-mode support`.

Proceed step-by-step, commit frequently if needed, then open a PR named  
“PySide6 migration + dark theme”.

────────────────────────

Send the above prompt (section “PROMPT FOR CLINE”) to Cline.
