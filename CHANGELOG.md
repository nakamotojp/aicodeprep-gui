# 📦 Changelog

---

## [0.9.8] - 2025-06-18

### 🚀 Major Refactoring: TOML Configuration & Lazy Loading

#### ✨ New Features

- **TOML Configuration System:**

  - Replaced custom Markdown configuration with industry-standard TOML format
  - New `default_config.toml` file with comprehensive configuration options
  - Support for user-specific configuration via `aicodeprep.toml` in working directory
  - `.gitignore`-style pattern matching using `pathspec` library for robust file exclusion

- **Lazy Loading File Tree:**

  - Implemented lazy loading for excluded directories (like `node_modules`, `venv`, etc.)
  - Extremely fast initial startup by avoiding scanning large excluded directories
  - On-demand expansion of any directory for fine-grained file selection
  - Users can now manually expand and select specific files from previously excluded directories

- **Enhanced Pattern Matching:**
  - All file and directory exclusion now uses `.gitignore`-style patterns
  - More powerful and standardized exclusion rules
  - Unified inclusion/exclusion lists for better organization

#### 🔄 Changed

- **Dependencies:**

  - Added `toml` for configuration parsing
  - Added `pathspec` for `.gitignore`-style pattern matching
  - Removed `tiktoken` dependency (no longer used)

- **Configuration Format:**

  - Migrated from `config.md` to `default_config.toml`
  - More structured and maintainable configuration system
  - Better support for complex exclusion patterns

- **Performance Improvements:**
  - Significantly faster startup times due to lazy loading
  - Reduced memory usage during initial file scanning
  - More responsive UI when working with large codebases

#### 🛠️ Technical Improvements

- **Code Architecture:**

  - Complete rewrite of `smart_logic.py` for better performance and maintainability
  - Improved GUI tree building logic with lazy loading support
  - Enhanced checkbox styling using Unicode characters instead of temporary files
  - Better error handling and descriptive error messages for debugging

- **File Processing:**
  - More efficient directory traversal with intelligent pruning
  - Better binary file detection and handling
  - Improved pathspec-based filtering throughout the application

---

## [0.9.9] - 2025-06-10 (Example Date)

### ✨ New Features

- **Output Format Selection:**
  - Added a dropdown menu in the UI to select the output format for `fullcode.txt`.
  - Options: "XML <code>" (uses `<code>...</code>` tags) or "Markdown ###" (uses `### File Path` ... `### END File Path`).
- **Prompt Presets:**
  - Users can now create, save, and quickly apply preset text snippets to the LLM prompt box.
  - Added "Edit" -> "New Preset..." menu option and a "✚" button next to the preset strip for easy creation.
  - Presets are saved per-folder in the `.aicodeprep` preferences file (text is base64 encoded).
- **Enhanced Configuration System:**
  - Default application configuration is now loaded from `aicodeprep_gui_c/data/config.md` (a Markdown file with simple section-based syntax).
  - User-specific overrides can be defined in an `aicodeprep_config.md` file (containing a JSON block) in the application's working directory.
- **UI & UX Improvements:**
  - Implemented a native QMainWindow menu bar ("File" > "Quit", "Edit" > "New Preset...").
  - Binary files are now automatically detected, greyed out, and made unselectable in the file tree view to prevent accidental inclusion.
  - Improved visual style for checkboxes in the file tree view using programmatically generated checkmark images, ensuring better visibility and consistency in both light and dark modes.
  - The state (proportions) of the vertical splitter between the file tree and the prompt input box is now saved and restored via the `.aicodeprep` file.
  - Application style set to "Fusion" for more consistent Qt Quick StyleSheet (QSS) rendering across platforms.
- **File & Directory Handling Enhancements:**
  - Improved logic in `smart_logic.py` to more effectively skip excluded directories (e.g., `.git`, `venv`, `__pycache__`) during the initial file collection phase.
  - Files and folders starting with a dot (e.g., `.vscode`, `.idea`) are now skipped by default.
  - File exclusion patterns (`exclude_patterns` in `config.md`) now support glob-style matching (e.g., `*.log`, `temp_*`) via `fnmatch`.

### 🔄 Changed

- **Token Counting Logic:**
  - The GUI's token estimation for selected files now uses a simplified character-based approximation (`total_chars / 4`).
  - This removes the direct runtime dependency on the `tiktoken` library for the GUI's token counting feature. (Note: `tiktoken` may still be listed as a project dependency for other potential uses).
- **Preferences File:**
  - `.aicodeprep` now stores splitter state and prompt presets in addition to window size and checked files.
- **Default Configuration File:** Path and format changed from `default_config.yaml` (implicitly, from older versions) to `aicodeprep_gui_c/data/config.md`.

### 🐛 Fixed

- Binary files could previously be selected, potentially leading to very large or unusable `fullcode.txt` content. They are now disabled.
- Directory exclusion logic is now more robust, preventing traversal into common unnecessary folders.

---

## [0.9.8] - 2025-05-27

### ✨ New Features

- 🎨 Added automatic dark/light theme detection based on system preferences
- 🌓 New dark mode toggle in the top-right corner for manual theme switching

### 🔄 Changed

- 🚀 Migrated from PyQt5 to PySide6 for improved performance and better Qt6 features
- 📦 Simplified dependencies - primary GUI functionality now relies on PySide6. (`tiktoken` is also a dependency, though its use for GUI token counting was removed in 0.9.9).

---

## [0.9.7] - 2025-04-28

### 🎉 Added

- New `.aicodeprep` file that saves the size of the window, and also which files you had checked last time you processed in that folder. So the next time you use AI Code Prep GUI in that folder, it will be set up with those same files checked (often when bug fixing I need custom files sent to the AI chat over and over, so this helps save time).
- New buttons for **Load from .aicodeprep** (check the files you last had checked when last processed), **Quit** button.
- Expandable and collapsable folders, will auto expand if any files recursively inside are checked.
- Checkbox to disable creation of the `.aicodeprep` file if you for some reason don't want that feature.
- 🧮 Added a token counter: as you check or uncheck files, the token count is now displayed.
- Added a prompt box, where you can optionally add text that will be added to the end of the context/fullcode.txt/clipboard. So you can type a question or describe what you want the LLM to do with the code (instead of having to use some other editor)
- Linux version! Looks and works the same as Windows/Mac versions.
- Added drag n drop folder onto UI to load a different folder. Work around for issues adding context menu to various Linux distros

---

## [0.9.5] - 2025-01-24 _(Mac GUI version seems to work)_

### 🎉 Added

- 🍏 Mac OS app and workflow file that installs a right click menu to Finder.

---

## [0.5.0] - 2024-11-14 _(GUI Release)_

### 🎉 Added

- 🪟 Windows GUI Version
- 🖱️ Right-click context menu integration for Windows
- 📂 Enhanced file selection GUI with granular file inclusion/exclusion
- 🖥️ DPI awareness for better display on high-resolution screens

### ✨ New Features

- 🗂️ Interactive file selection before code preparation
- ☑️ Checkbox-based file inclusion/exclusion
- 🎨 Scalable UI with multiple theme options
- 🗃️ Windows Explorer context menu integration

### 🔄 Changed

- 💸 Moved from free to premium model
- 🏷️ Lifetime license available for $7
- ⚙️ Enhanced configuration options
- 🪲 Improved logging and error handling

---

## [0.2.2] - 2024-11-02

- 🛠️ Minor tweaks

---

## [0.2.2] - 2024-11-02 _(Duplicate entry, keeping one based on date order if different from file)_

- Note: The original changelog had two entries for 0.2.2 with different dates. I'm using the `YYYY-MM-DD` format. The `2024-07-11` entry with `(Nov 2nd 2024)` in description is likely a typo for `2024-11-02`. The `2024-02-11` entry is distinct. I'll assume the `2024-07-11 (Nov 2nd 2024)` was meant to be `2024-11-02` and the other `0.2.2` is `2024-02-11`. For simplicity, I'll list them chronologically if their content was different, or merge if identical. The provided changelog has `[0.2.2] - 2024-02-11` and `[0.2.2] - 2024-07-11 _(Nov 2nd 2024)_`. Let's assume these were distinct fixes/tweaks.

## [0.2.2] - 2024-11-02

- 🛠️ Minor tweaks

---

## [0.2.0] - 2024-02-11

### 🔧 Moved all hard coded options to the `default_config.yaml` file

### 🎉 Added

- New `exclude_extensions` configuration option to exclude file types globally
- New `exclude_extensions` configuration option to exclude patterns like `.min.js`
- New `include_dirs` configuration option to explicitly include specific directories
- Enhanced priority system for file inclusion/exclusion rules
- Better support for user configuration overrides
- Updated and added some more exclusions that came up later when it would add unnecessary files

### 🔄 Changed

- Improved file processing logic with clearer priority rules:
  1.  Explicitly included files (highest priority)
  2.  Explicitly excluded files
  3.  Excluded extensions
  4.  Code extensions (lowest priority)
- Enhanced directory processing logic:
  1.  Explicitly included directories (highest priority)
  2.  Explicitly excluded directories
  3.  Normal directory processing

---

## [0.9.8] - 2025-27-5

### ✨ New Features

- 🎨 Added automatic dark/light theme detection based on system preferences
- 🌓 New dark mode toggle in the top-right corner for manual theme switching

### 🔄 Changed

- 🚀 Migrated from PyQt5 to PySide6 for improved performance and better Qt6 features
- 📦 Simplified dependencies - now only requires PySide6 for GUI functionality

---

## [0.9.7] - 2025-28-4

### 🎉 Added

- New `.aicodeprep` file that saves the size of the window, and also which files you had checked last time you processed in that folder. So the next time you use AI Code Prep GUI in that folder, it will be set up with those same files checked (often when bug fixing I need custom files sent to the AI chat over and over, so this helps save time).
- New buttons for **Load from .aicodeprep** (check the files you last had checked when last processed), **Quit** button.
- Expandable and collapsable folders, will auto expand if any files recursively inside are checked.
- Checkbox to disable creation of the `.aicodeprep` file if you for some reason don't want that feature.
- 🧮 Added a token counter: as you check or uncheck files, the token count is now displayed.
- Added a prompt box, where you can optionally add text that will be added to the end of the context/fullcode.txt/clipboard. So you can type a question or describe what you want the LLM to do with the code (instead of having to use some other editor)
- Linux version! Looks and works the same as Windows/Mac versions.
- Added drag n drop folder onto UI to load a different folder. Work around for issues adding context menu to various Linux distros

---

## [0.9.5] - 2025-24-1 _(Mac GUI version seems to work)_

### 🎉 Added

- 🍏 Mac OS app and workflow file that installs a right click menu to Finder.

---

## [0.5.0] - 2024-14-11 _(GUI Release)_

### 🎉 Added

- 🪟 Windows GUI Version
- 🖱️ Right-click context menu integration for Windows
- 📂 Enhanced file selection GUI with granular file inclusion/exclusion
- 🖥️ DPI awareness for better display on high-resolution screens

### ✨ New Features

- 🗂️ Interactive file selection before code preparation
- ☑️ Checkbox-based file inclusion/exclusion
- 🎨 Scalable UI with multiple theme options
- 🗃️ Windows Explorer context menu integration

### 🔄 Changed

- 💸 Moved from free to premium model
- 🏷️ Lifetime license available for $7
- ⚙️ Enhanced configuration options
- 🪲 Improved logging and error handling

---

## [0.2.2] - 2024-02-11

- 🛠️ Minor tweaks and improvements

---

## [0.2.2] - 2024-07-11 _(Nov 2nd 2024)_

- 🛠️ Minor tweaks

---

## [0.2.0] - 2024-02-11 _(Nov 2nd 2024)_

### 🔧 Moved all hard coded options to the `default_config.yaml` file

### 🎉 Added

- New `exclude_extensions` configuration option to exclude file types globally
- New `exclude_extensions` configuration option to exclude patterns like `.min.js`
- New `include_dirs` configuration option to explicitly include specific directories
- Enhanced priority system for file inclusion/exclusion rules
- Better support for user configuration overrides
- Updated and added some more exclusions that came up later when it would add unnecessary files

### 🔄 Changed

- Improved file processing logic with clearer priority rules:
  1. Explicitly included files (highest priority)
  2. Explicitly excluded files
  3. Excluded extensions
  4. Code extensions (lowest priority)
- Enhanced directory processing logic:
  1. Explicitly included directories (highest priority)
  2. Explicitly excluded directories
  3. Normal directory processing
