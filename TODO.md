-- secretlint

potential bugs:

Target directory: .
2025-07-14 13:05:17,263 - INFO - Starting code concatenation...
2025-07-14 13:05:17,263 - INFO - Starting initial fast scan in: C:\2nd\Main\Git-Projects\aicpgui\aicodeprep-gui-c-lazyloadingworks - Copy
2025-07-14 13:05:17,277 - INFO - Initial scan collected 105 items.
2025-07-14 13:05:17,289 - ERROR - Error creating metric request for event 'open': 'FileSelectionGUI' object has no attribute 'network_manager'
2025-07-14 13:05:17,861 - INFO - Restored splitter state from preferences
[gui] Starting update check...
[update_checker] Starting update check for version 1.0.7
[update_checker] Reset prompted_this_run flag to False
[update_checker] Starting background update check thread
[gui] Update check thread started

Windows registry path quoting bug
windows_registry.py:get_registry_command() returns
f'"{pythonw_exe}" "{script_path}" "%V"'
If either path contains spaces, the nested quotes are not escaped, which breaks the registry entry.
→ Fix: use shlex.quote() or raw-string escaping.

Linux Nautilus script name collision
The generated script is always named Open with aicodeprep-gui; if the user already installed an older version, the file will be overwritten silently.
→ Fix: append version or hash to filename, or warn before overwrite.
Update check can block on slow network
\_UpdateFetchWorker uses requests.get() with timeout=5, but on flaky networks the worker thread never returns if DNS stalls.
→ Fix: set timeout=(3, 5) (connect, read) and wrap in try/except.

---

free:
quick how to on how to use it, on first start and put in menu

premium:
Block secrets, api keys, automatically so people don't have to worry which files they include
preview window on right side option
option to enable skeleton context, list folders/files that are not included but just the names/paths added
for that little bit of context
AI powered summary/compression for large codebases, context packer engine
wuu73 api router
gate the preset buttons or limit to 3, no nag screens, maybe right click menu?
offer updated information about saving money, access to free APIs for Cline/etc, access to info
$19.99 up to 10 machines or unlimited
future access to planned features like automatic cut/paste to all the different web chat's,
automatic 'brain' where it sends prompt to several api's, compares answers
info screen in paid, how to use it with Cline with the free api's, how to plan in web chats, create cline prompt, execute with free api's.
web / electron version added as an extra
VS Code extension / right click

all:
add complaint button

0-------
python -m aicodeprep_gui.main
python -m pip install --upgrade build twine
python -m build
twine upload --repository testpypi dist/\*

python -m build
twine upload dist/\*
---------0
Mac finder menu issue
test user config files, write documentation for it.
create docs website

help diagrams:
'is Cline, Roo Code acting dumb? yes --> if yes, type aicp + enter in the VS Code terminal to open the app.
Code files will be already selected. Type your problem into the prompt box, add or subtract any extra files you think it might need, click the Cline/Roo Code prompt preset button (which is "Write a prompt for Cline, an AI coding agent, to make the necessary changes. Enclose the entire Cline prompt in one single code tag for easy copy and paste."), Click GENERATE CONTEXT. --> paste into Gemini in AI studio (or, into Deepseek, or o3 on OpenAI Playground, Claude, Grok, etc) --> if it figures out how to solve your problem, cut and paste it back into cline set on GPT 4.1 to save' - add animated dotted lines and keep it a dark mode theme

make fullcode.txt name editable in ui
add aicp command

add version number for .aicodeprep file type and make a new file for saving other things like button presets but globally (qsettings?)
save any preset buttons in this file, and it should try to read the file when app starts up, but not have an error if file doesn't exist yet
when app starts for first time ever, it should create this file with these preset buttons already programmed (or created): 1. "Debug" which is "Can you help me debug this code?" 2. "Security check" - "Can you analyze this code for any security issues?" 3. "Best Practices" - "Please keep in mind: Error handling, Edge cases, Performance optimization, Best practices, Please do not unnecessarily remove any comments or code. Generate the code with clear comments explaining the logic." 4. "Please review for" - "Code quality and adherence to best practices, Potential bugs or edge cases, Performance optimizations, Readability and maintainability, Any security concerns, Suggest improvements and explain your reasoning for each suggestion"

a way to use a fancy UI to edit a user config file
add ability to edit name of fullcode.txt

there should be a way to delete any of the presets that were created (or put there by the app's defaults). Error catching is a must.

- also, there should be a regular type of menu, File - quit, then Edit - Presets - The presets thing should let them add custom prompt buttons. They can add a button, and type some text for the button - it should add it to the section near the bottom of the window to the left of the other buttons like process selected, select all, etc. they can add text to a new button, and then later when they click on the button, it will add the button saved prompt text to the end of what is in the question llm box (if anything is there, if not, it will put it there).
  It should save these prompts in the .aicodeprep file
  Also can you make the question llm box so it has word wrap? also, so that it only accepts text / markdown (which is text technically) / emoji's etc. but not have it be richtext (it seems to sometimes make text bigger if pasted in)

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
