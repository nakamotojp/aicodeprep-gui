# aicodeprep-gui - AI Code Preparation GUI

_Streamline code sharing with AI chatbots (macOS & Windows & Linux)_

[![GitHub stars](https://img.shields.io/github/stars/detroittommy879/aicodeprep-gui.svg?style=social&label=Stars)](https://github.com/detroittommy879/aicodeprep-gui/stargazers)

**Latest Version: 1.0.0 (June 20, 2025)**

---

## What is aicodeprep-gui?

aicodeprep-gui is a cross-platform desktop application that helps developers quickly gather and share their project code with AI chatbots. Instead of manually copying and pasting multiple files just to ask a question, this tool automatically collects relevant code files into a single 'block' + text file, copies it to your clipboard automatically, and formats it with AI-friendly tags. READY... to paste right into an AI chat, or multiple ones (they are still usually free!).

You can set presets which quickly add on text to what you typed, so you can do things like click the Cline button to tell the AI you want it to reply with a nice prompt you can just paste right into Cline to make fast changes without all the manual copying, pasting, typing over and over..

Basically what this does is get rid of all the little annoying frictions between me asking my question, and giving the AI the code i'm asking about. Without this tool I would have to open each code file, copy, paste it into AI Studio/Gemini/whatever, type the same questions I ask over and over.. I hate the tedious stuff, I want to spend my brain power on better things. That's what this helps with.

ChatGPT, Gemini 2.5 Pro, o3, I have like 15 tabs open of different web chat's like this and most are totally free to use.
(for more info about the workflow, staying free or cheap yet still good: wuu73.org/blog/guide.html)

This helps you "vibe code" faster. Only need to paste one time. It will automatically guess as to which code files you will want for context, but allow you to fine tune it. This might seem pointless ohhh but its not. All of the available agents in IDEs will make the AI dumber by giving it a bunch of information unrelated to your problem.

Or, it won't give it enough information or context from your project.

When you use web chat interfaces, you don't have the giant hidden prompts telling the AI all about how to be an agent, how to edit files, etc. The more of this that is sent with your prompt, the dumber it will be. If you ask a question or give it a task via the web chat interface its almost always going to be smarter. This app gets rid of most of the friction between you giving the AI your code files and questions/tasks.

There are many other similar tools that are command line only, and don't have smart file checking and prefs saving, saving which files you chose for next time (when you check more files or uncheck certain ones, it will remember, for next time - this is what the .aicodepre-gui file is for). It even saves the window size and where you dragged the bar in the UI, so you won't have to do that again. Saving time and being less annoying, makes me happy, and probably makes you happy too.

It supports **Windows**, **macOS (M1+)**, and **Linux** with context menu/right-click integration.

---

## ✨ New Features in v1.0.0

- **Modern TOML Configuration System:**

  - Industry-standard TOML configuration replacing custom formats
  - User-customizable settings via `aicodeprep-gui.toml` in project directories
  - Comprehensive default configuration with smart file filtering
  - `.gitignore`-style pattern matching for robust exclusion rules

- **Lazy Loading Performance:**

  - Lightning-fast startup by avoiding scanning of large excluded directories
  - On-demand expansion of folders like `node_modules`, `venv`, etc.
  - Dramatically improved performance for large codebases
  - Users can still manually expand any directory for fine-grained selection

- **Enhanced Global Preset System:**

  - Create and manage reusable prompt presets globally across projects
  - Presets are automatically saved and synced across all project folders
  - Quick preset buttons with ✚ and 🗑️ controls for easy management
  - Default presets include "Debug", "Security check", "Best Practices", etc.

- **Improved File Tree Experience:**

  - Smart auto-expansion of folders containing checked files
  - Better visual feedback with hover effects on checkboxes
  - Binary file detection and automatic exclusion
  - Cleaner, more intuitive folder navigation

- **Enhanced Output Options:**
  - Choose between XML `<code>` tags or Markdown `###` formatting
  - Optional prompt/question text appended to output
  - Intelligent file processing with better error handling

---

## Previous Features (v0.9.x)

- **Dark Mode Support:**

  - Automatic theme detection based on system preferences
  - Manual dark/light mode toggle in the top-right corner
  - Carefully designed dark theme palette for optimal readability

- **PySide6 Migration:**

  - Upgraded to Qt6 via PySide6 for improved performance
  - Modern Qt features and future-proofing
  - Better cross-platform compatibility

- **Persistent Preferences:**

  - Automatically saves window size and selected files in `.aicodeprep-gui` file per project
  - Remembers splitter position and window layout
  - Optional preference saving (can be disabled)

- **Smart Token Counter:**
  - Real-time token estimation as you select/deselect files
  - Helps optimize context size for AI models

---

## Screenshots & Usage

See screenshots and a quick usage guide here:  
[https://wuu73.org/aicodeprep-gui](https://wuu73.org/aicodeprep-gui)

---

## Installation

### macOS

1. Download and unzip the macOS package from the releases page.
2. Drag `aicodeprep-gui.app` to your Applications folder.
3. Install the Finder integration workflow if provided.
4. To use: Right-click on a project folder → Quick Actions → aicodeprep-gui.
5. Select/deselect files and folders as needed, then click **Process Selected**.
6. The tool will create a `fullcode.txt` and copy all selected code to your clipboard.

_Tested on macOS Ventura 13.4 and newer (M1+)._

### Windows

1. Run the Windows installer from the releases page.
2. Follow the installation wizard.
3. To use: Right-click in any folder's blank space in Windows File Explorer → `aicodeprep-gui`.
4. Restart Windows if the context menu does not appear immediately.
5. Select/deselect files and folders, then click **Process Selected**.
6. Your selected code will be saved to `fullcode.txt` and copied to the clipboard.

### Linux

1. Download the Linux package from the releases page.
2. Follow the installation instructions in the included README.
3. Use via command line: `aicodeprep-gui [directory]`
4. File manager context menu integration may be available depending on your desktop environment.

### Python Installation

```bash
pip install aicodeprep-gui
aicodeprep-gui  # Run in current directory
aicodeprep-gui /path/to/project  # Run in specific directory
```

---

## Features Summary

- **Cross-platform GUI** for easy visual file selection
- **Smart Preselection** of relevant code files based on configured extensions and exclusions
- **Dark/Light Theme Support** with system preference detection and manual toggle
- **Lazy Loading Tree View** with instant startup and on-demand directory expansion
- **Global Preset Management** for reusable prompt templates across projects
- **TOML Configuration** with `.gitignore`-style pattern matching
- **Preferences Saving** via `.aicodeprep-gui` per folder to remember selections and window layout
- **Token Counter** displays estimated token count in real-time
- **Context Menu Integration** for quick access from file managers
- **Clipboard & File Output** for seamless pasting into AI chatbots
- **Flexible Output Formats** (XML `<code>` tags or Markdown `###` sections)
- **High-DPI Support** with crisp UI scaling on all displays

---

## Usage

1. **Launch:** Open the tool from your project folder's context menu (right-click) or command line.
2. **Review Files:** The tool automatically pre-selects relevant code files and expands folders containing them.
3. **Customize Selection:**
   - Expand/collapse folders as needed
   - Check/uncheck files manually
   - Use **Select All** or **Deselect All** for bulk operations
4. **Choose Format:** Select XML `<code>` or Markdown `###` output format from the dropdown.
5. **Add Prompt (Optional):** Use preset buttons or type custom prompts in the text area.
6. **Process:** Click **Process Selected** to generate output and copy to clipboard.
7. **Preferences:** Toggle "Remember checked files..." to save your selection for next time.

---

## Configuration

You can customize file extensions, directories, and exclusion patterns via an `aicodeprep-gui.toml` file in your project folder. This will override the default configuration.

Example `aicodeprep-gui.toml`:

```toml
max_file_size = 2000000

code_extensions = [".py", ".js", ".ts", ".html", ".css"]

exclude_patterns = [
    "build/",
    "dist/",
    "*.log",
    "temp_*"
]

default_include_patterns = [
    "README.md",
    "main.py"
]
```

Refer to `aicodeprep-gui/data/default_config.toml` for all available configuration options.

---

## Command Line Options

```bash
aicodeprep-gui [directory] [options]

Options:
  -h, --help          Show help message
  -n, --no-copy       Don't copy output to clipboard
  -o, --output FILE   Output filename (default: fullcode.txt)
  -d, --debug         Enable debug logging
```

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
