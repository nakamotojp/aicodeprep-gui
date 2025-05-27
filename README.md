# AI Code Prep GUI

_Streamline code sharing with AI chatbots (macOS & Windows & Linux)_

[![GitHub stars](https://img.shields.io/github/stars/detroittommy879/aicodeprep.svg?style=social&label=Stars)](https://github.com/detroittommy879/aicodeprep/stargazers)

**Latest Version: 0.9.8 (May 27, 2025)**

---

## What is AI Code Prep GUI?

AI Code Prep GUI is a cross-platform desktop application that helps developers quickly gather and share their project code with AI chatbots. Instead of manually copying and pasting multiple files, this tool automatically collects relevant code files into a single text file, copies it to your clipboard, and formats it with AI-friendly `<code>` tags.

It supports **Windows**, **macOS (M1+)**, and **Linux** with context menu/right-click integration.

---

## New Features in v0.9.8

- **Dark Mode Support:**
  - Automatic theme detection based on system preferences
  - Manual dark/light mode toggle in the top-right corner
  - Carefully designed dark theme palette for optimal readability
- **PySide6 Migration:**
  - Upgraded to Qt6 via PySide6 for improved performance
  - Simplified dependencies - only requires PySide6 and tiktoken
  - Better modern Qt features and future-proofing

## Features from v0.9.7

- **Persistent Preferences:** Automatically saves window size and the last selected files in a `.aicodeprep` file per project folder. When you re-open the tool in the same folder, your previous selections and window layout are restored.
  - New checkbox lets you disable creation of the `.aicodeprep` file if you don't want this feature.
- **Folder Tree UI Improvements:**
  - Expandable and collapsable folders for easier navigation
  - Auto-expands folders containing checked files
- **Token Counter:** As you check or uncheck files, the token count is now displayed.
- **Enhanced Smart Auto-Selection:** Smarter file checking logic that respects exclusions and better filters irrelevant files
- **Additional UI Buttons:**
  - **Load from .aicodeprep** button to restore your last saved selection
  - **Quit** button for quick exit without processing
- **Better Visual Styling:** Improved fonts and DPI scaling for crisp display on high-resolution screens

---

## Screenshots & Usage

See screenshots and a quick usage guide here:  
[https://wuu73.org/aicp](https://wuu73.org/aicp)

### New version 0.9.8 available for Windows, macOS, and Linux

---

## Future idea's

MCP Server to automatically attach to a browser, and automatically paste the output context into various AI/LLM chats like Gemini on AI Studio, ChatGPT, Openrouter, Poe, Deepseek, X, etc so even less copying and pasting.

## Installation

### macOS

1. Download and unzip the macOS package.
2. Drag `AICodePrepGUI.app` to your Applications folder.
3. Double-click `AICodePrepGUI.workflow` and follow instructions to add the right-click Quick Actions menu to Finder.
4. Restart Finder if needed to activate the menu.
5. To use: Right-click on a project folder → Quick Actions → AICodePrepGUI.
6. Select/deselect files and folders as needed, then click **Process Selected**.
7. The tool will create a `fullcode.txt` and copy all selected code to your clipboard, ready to paste into your AI chatbot.

_Tested on macOS Ventura 13.4 and newer (M1+)._

### Windows

1. Run `windows-easy-installer-dist.exe` or the newer v0.9.8 installer file.
2. Follow the installation wizard (default directory: `Program Files\AICodePrep-GUI`).
3. To use: Right-click in any folder's blank space in Windows File Explorer → `AI Code Prep GUI`.
4. Restart Windows if the context menu does not appear immediately.
5. Select/deselect files and folders, then click **Process Selected**.
6. Your selected code will be saved to `fullcode.txt` and copied to the clipboard.

### Linux

1. Download the Linux package from the releases page.
2. Follow the installation instructions in the included README.
3. Use via command line or file manager context menu integration.

---

## Features Summary

- **Cross-platform GUI** for easy visual file selection
- **Smart Preselection** of relevant code files based on configured extensions and exclusions
- **Dark/Light Theme Support** with system preference detection and manual toggle
- **Folder Tree View** with collapsible/expandable folders and auto-expansion for selected files
- **Preferences Saving** via `.aicodeprep` per folder to remember your last selected files and window size (with option to disable)
- **Token Counter** displays token count as you check/uncheck files
- **Context Menu Integration** for quick access
- **Clipboard & File Output** for seamless pasting into AI chatbots
- **LLM-Optimized Formatting** with `<code>` tags around file contents
- **Configurable via YAML** to suit various project needs
- **Improved DPI & Font Scaling** for crisp UI on all displays

---

## Usage

1. Open the tool from your project folder's context menu (right-click).
2. Review the preselected files and folders. Expand or collapse folders as needed.
3. Use the **Smart Auto** button to auto-select files based on smart logic.
4. Use **Load from .aicodeprep** to restore your previous session's selection.
5. Check or uncheck files/folders manually.
6. Toggle dark/light mode using the checkbox in the top-right corner if desired.
7. If you want to save your preferences for the folder, ensure the **Remember checked files for this folder (.aicodeprep)** checkbox is ticked.
8. Click **Process Selected** to generate the output file and copy it to your clipboard.

---

## Configuration

You can customize file extensions, directories, and exclusion patterns via a `aicodeprep_config.yaml` file in your project folder. Refer to the [default_config.yaml](aicodeprep_gui_c/data/default_config.yaml) for examples.

---

## Contributing

Contributions and pull requests are welcome! Please submit bug reports and feature requests via GitHub Issues.

---

## Support & Donations

If you find this tool useful, consider supporting future development:

| Method   | Address / Link                                                                                    |
| -------- | ------------------------------------------------------------------------------------------------- |
| Bitcoin  | `bc1qkuwhujaxhzk7e3g4f3vekpzjad2rwlh9usagy6`                                                      |
| Litecoin | `ltc1q3z327a3ea22mlhtawmdjxmwn69n65a32fek2s4`                                                     |
| Monero   | `46FzbFckBy9bbExzwAifMPBheYFb37k8ghGWSHqc6wE1BiEz6rQc2f665JmqUdtv1baRmuUEcDoJ2dpqY6Msa3uCKArszQZ` |
| CashApp  | `$lightweb73`                                                                                     |
| Website  | [https://wuu73.org/hello.html](https://wuu73.org/hello.html)                                      |

---
