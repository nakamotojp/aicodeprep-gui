aicodeprep-gui Documentation
🚀 Getting Started
Installation Guide
The easiest way to get started is using our installer scripts - they handle all the technical stuff for you. If you're comfortable with terminals, feel free to skip to the manual instructions.

Windows Installation
Easy Way (Recommended)

Download and run the Python installer from python.org
⚠️ Important: Check "Add Python to PATH" during installation
Double-click INSTALLER_Windows.bat from your download
Wait for it to finish, then close and reopen any terminal windows
Manual Way (if you know your way around terminals)

py -m pip install --user pipx
py -m pipx ensurepath

# Close terminal, open a fresh one

pipx install aicodeprep-gui
[Screenshot suggestion: Windows installer dialog with "Add to PATH" checkbox highlighted]

macOS Installation
Easy Way (Recommended)

Double-click INSTALLER_MacOS.sh
Follow any prompts for Homebrew installation if needed
Manual Way

brew install pipx
pipx ensurepath

# Close terminal, open a fresh one

pipx install aicodeprep-gui
Linux Installation
Easy Way (Recommended)

chmod +x INSTALLER_Linux.sh
./INSTALLER_Linux.sh
Manual Way

sudo apt install python3-pip # or your distro's equivalent
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Close terminal, open a fresh one

pipx install aicodeprep-gui
First Launch
After installation, you can run the app two ways:

From any terminal: Type aicp and press Enter
With a specific folder: Type aicp /path/to/your/project
[Screenshot suggestion: Terminal showing the aicp command and the app launching]

Quick Start Tutorial
Let's get you making your first AI context in under 2 minutes:

Open your project: Navigate to any coding project folder and type aicp
Review the selection: The app automatically selects relevant files (_.py, _.js, README.md, etc.)
Add a question: Click any preset button or type in the prompt box
Generate: Click the big "GENERATE CONTEXT!" button
Paste: Your code + question is now copied to clipboard - paste it into any AI chat!
[Screenshot suggestion: Main interface with numbered callouts showing these 5 steps]

📖 User Guide
Understanding the Interface
The main window has several key areas:

File Tree (Top Half)

Shows all files and folders in your project
✅ Checked files will be included in your context
Smart defaults: excludes node_modules, venv, binary files, etc.
Click folder triangles to expand and see more files
[Screenshot suggestion: Main interface with labeled sections]

Prompt Section (Bottom Half)

Preset Buttons: Quick-access to saved prompts
Text Box: Write custom questions for the AI
Clear Button: Empties the prompt box
Options Panel

Output Format: Choose between XML tags or Markdown formatting
Dark Mode: Toggle light/dark theme
Prompt Position: Add your question to top, bottom, or both
File Selection & Management
Smart Defaults
The app starts with intelligent file selection:

✅ Code files (.py, .js, .ts, .html, etc.)
✅ Documentation (README.md, CHANGELOG.md)
✅ Config files (package.json, pyproject.toml)
❌ Dependencies (node_modules/, venv/)
❌ Build artifacts (dist/, build/)
❌ Binary files (images, executables)
Manual Selection
Individual Files: Check/uncheck any file
Folders: Checking a folder includes all files inside
Select All: Includes all non-excluded files
Deselect All: Clears all selections
[Screenshot suggestion: File tree showing checked/unchecked files and folders]

Token Counter
to help you stay within AI context limits:

Working with Prompts & Presets
Built-in Presets
The app comes with useful presets:

Debug: "Can you help me debug this code?"
Security Check: Analyzes for security issues
Best Practices: Reviews code quality and patterns
Cline Prompt: Formats requests for AI coding agents
[Screenshot suggestion: Preset buttons highlighted]

Creating Custom Presets
New Preset: Click the ✚ button or go to Edit → New Preset
Enter Label: Short name for your button
Add Text: The prompt text that gets inserted
Save: Available across all your projects!
Managing Presets
Delete: Click the 🗑️ button to remove presets
Global: All presets are saved globally and work in any project
Prompt Positioning
Research shows asking questions before AND after code context improves AI responses:

Add to Top: ✅ Question appears before your code
Add to Bottom: ✅ Question appears after your code (default)
Both: ✅✅ Maximum effectiveness (recommended!)
[Screenshot suggestion: Options panel showing the checkbox options]

Output Formats & Options
Format Choice
XML <code>: Wraps each file in <code> tags - great for most AIs
Markdown ###: Uses ### START OF FILE headers - cleaner for reading
Dark Mode
Auto-detect: Matches your system theme
Manual Toggle: Override with the checkbox
Persistent: Remembers your choice
Project Memory (.aicodeprep-gui files)
The app remembers your preferences per project:

File Selections: Which files you included/excluded
Window Size: Your preferred app dimensions
Panel Layout: Splitter position between file tree and prompt
The "Remember" Checkbox
✅ Checked (default): Saves your choices to .aicodeprep-gui file
❌ Unchecked: Uses defaults each time (temporary session)
[Screenshot suggestion: Remember checkbox highlighted with tooltip visible]

🔧 Integration & Workflows
Right-Click Context Menu Setup
For the ultimate workflow, add aicodeprep-gui to your file manager's right-click menu:

Windows Explorer
Launch aicp
Go to File → Install Right-Click Menu
Customize text (optional): "Open with aicodeprep-gui"
✅ Enable classic menu (recommended for Windows 11)
Click Install - UAC prompt will appear
Right-click any folder → "Open with aicodeprep-gui"!
[Screenshot suggestion: Windows right-click menu showing the option]

macOS Finder
Find the AICodePrep.workflow file in your download
Double-click it
Click "Install" when prompted
Right-click any folder in Finder → Quick Actions → "AICodePrep"
Linux (Nautilus/GNOME)
Launch aicp
Go to File → Install File Manager Action
Click "Install Nautilus Script"
Restart Nautilus: nautilus -q in terminal
Right-click any folder → Scripts → "Open with aicodeprep-gui"
IDE Integration Tips
VS Code / Cursor / Windsurf

# Open terminal in VS Code (Ctrl+`)

aicp

# When the agent is being difficult, use this for clean context!

Any IDE with Terminal
The beauty of aicodeprep-gui is it works alongside ANY editor:

Keep your IDE open
Open terminal in your project
Type aicp when you need clean AI context
Paste result into web-based AI for best results
AI Platform Workflows
Gemini 2.0 Flash / Pro (AI Studio) - Recommended
Why: Excellent with code, very fast, generous free tier
Paste: Direct paste works perfectly
Context: Handles large contexts well (2M+ tokens)
[Screenshot suggestion: AI Studio interface with pasted code context]

Deepseek Chat
Why: Amazing at coding tasks, very affordable
Best For: Complex debugging, architecture questions
Tip: Use "Best Practices" preset for code reviews
OpenRouter (Claude, GPT-4, etc.)
Why: Access to ALL models in one place, lots of free options
Models: Claude 3.5 Sonnet, GPT-4o, and dozens more
Perfect For: Comparing different AI responses
OpenAI Playground
Why: Latest models (o1, o3), free playground credits
Best For: Complex reasoning tasks
Tip: Use XML format for better parsing
The Two-Step Workflow
For complex projects, try this powerful pattern:

Web AI (Step 1): Use aicodeprep-gui → paste into Gemini/Claude

Get the smart solution/architecture/debug info
Clean context = better AI responses
IDE Agent (Step 2): Copy the solution → paste into Cursor/Windsurf

Let the agent make the actual file changes
Use cheaper models for implementation
This gives you the best of both: smart problem-solving + efficient implementation!

❓ Help & Troubleshooting
Common Issues
"Command not found: aicp"
Solution: You need to open a fresh terminal after installation

Close all terminal/command windows
Open a new one
The PATH changes take effect in new sessions only
"No module named 'aicodeprep_gui'"
Solution: pipx installation issue

pipx reinstall aicodeprep-gui
App won't start / crashes immediately
Solutions:

Update to latest version: pipx upgrade aicodeprep-gui
Try debug mode: aicp --debug
Delete settings: aicp --delset (removes all saved preferences)
Right-click menu not appearing (Windows)
Solutions:

Run installer as Administrator
Restart Windows Explorer: Ctrl+Shift+Esc → Find "Windows Explorer" → Restart
Try the manual registry option in the installer dialog
Binary files showing as selected
Solution: This shouldn't happen, but if it does:

Click "Deselect All"
Click "Select All" - binary files will stay unselected
Or manually uncheck them
FAQ
Q: Do I need to install this in every project? A: No! Install once globally with pipx, then use aicp in any folder.

Q: What's the difference between aicp and aicodeprep-gui? A: Same program, aicp is just shorter to type.

Q: Can I use this with proprietary/private code? A: Yes! Everything runs locally, nothing is sent anywhere except when you paste into an AI.

Q: How do I update to the newest version? A: The app checks for updates automatically, or run: pipx upgrade aicodeprep-gui

Q: Can I exclude specific files permanently? A: Create an aicodeprep-gui.toml config file (see Configuration section), or just uncheck them - the app remembers per-project.

Getting Help
Email: tom@wuu73.org
GitHub Issues: Report bugs or request features
Built-in Feedback: Help → Send Feedback (in the app)
📚 Reference
Command Line Options

# Basic usage

aicp # Current directory
aicp /path/to/project # Specific directory
aicodeprep-gui # Same as aicp

# Options

aicp --debug # Enable debug logging
aicp --no-copy # Don't copy to clipboard
aicp --output myfile.txt # Custom output filename
aicp --force-update-check # Check for updates now
aicp --delset # Reset all settings

# Help

aicp --help # Show all options
Keyboard Shortcuts
Shortcut Action
Ctrl+A Select All files
Ctrl+D Deselect All files
Ctrl+Q Quit application
F1 Open About dialog
Default File Patterns
Always Included (if present):
README.md, CHANGELOG.md, LICENSE
package.json, pyproject.toml, requirements.txt
Dockerfile, docker-compose.yml
Always Excluded:
Dependencies: node_modules/, venv/, vendor/
Build Output: dist/, build/, target/
IDE Files: .vscode/, .idea/
Caches: .cache/, **pycache**/
Logs: \*.log, logs/
