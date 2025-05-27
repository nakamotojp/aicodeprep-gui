# AI Code Prep GUI  
*Streamline code sharing with AI chatbots (macOS & Windows)*  

**New in v0.9.5**  
✓ Added macOS installation & support  
✓ Improved file selection logic  
✓ Context menu integration for both platforms  

---
Pictures of how to use it are here:
[wuu73.org/aicp](https://wuu73.org/aicp)

## Installation

### macOS
1. Download and unzip the macOS package
2. Drag `AICodePrepGUI.app` to your Applications folder
3. Double-click `AICodePrepGUI.workflow`, follow instructions to add the menu
4. You may need to restart Finder to activate menu (but often not)
5. **To use:** Select one folder with project/code, Right-click → Quick Actions → AICodePrepGUI
6. Select and unselect any files you want to be added to the context
7. Click Process Selected which will copy it all to clipboard and save it to fullcode.txt. Paste into LLM chat

*Tested on macOS Ventura 13.4 - report issues to wuu73@yahoo.com*

### Windows
1. Run `windows-easy-installer-dist.exe`
2. Follow installation wizard (default: `Program Files\AICodePrep-GUI`)
3. **To use:** Right-click in any folder's blank space in windows file explorer → `AI Code Prep GUI`
     (you might have to click show more options if you don't have 'classic menu' enabled)
4. You may need to restart Windows to activate menu (if it doesn't work right away)
5. Select and unselect any files you want to be added to the context
6. Click Process Selected which will copy it all to clipboard and save it to fullcode.txt. Paste into LLM chat

---

## Features
- **Cross-platform GUI** - Visual file selection beats command line
- **Smart Preselection** - Auto-detects likely code files
- **Context-Aware** - Maintains folder structure in output, uses <> tags that LLMs understand
- **Clipboard & File** - Copies to clipboard AND creates `fullcode.txt`
- **LLM Optimized** - Filters non-essential files for better AI responses

---

## Usage
1. Right-click in project folder blank space (Windows) or use Quick Actions (in macOS, you have to select one folder before right clicking for the menu)
2. Review preselected files:
   - Check/Uncheck individual files
   - Expand/collapse directory trees
3. Click **Process Selected** to:
   - Generate structured code overview
   - Copy sanitized content to clipboard
   - Create `fullcode.txt` in project root


## Support & Development
Found this useful? Support future development:

₿ **Bitcoin:** `bc1qkuwhujaxhzk7e3g4f3vekpzjad2rwlh9usagy6`  
Ł **Litecoin:** `ltc1q3z327a3ea22mlhtawmdjxmwn69n65a32fek2s4`  
ɱ **Monero:** `46FzbFckBy9bbExzwAifMPBheYFb37k8ghGWSHqc6wE1BiEz6rQc2f665JmqUdtv1baRmuUEcDoJ2dpqY6Msa3uCKArszQZ`  
💵 **CashApp:** `$lightweb73`

*Report issues/ideas:* wuu73@yahoo.com  
*Linux version coming soon!*