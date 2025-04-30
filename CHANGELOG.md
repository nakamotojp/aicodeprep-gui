# 📦 Changelog

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

---

## [0.9.5] - 2025-24-1 _(Mac GUI version seems to work)_

### 🎉 Added

- 🍏 Mac OS app and workflow file that installs a right click menu to Finder.
- Switched to PyQt5.

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
