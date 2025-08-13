# aicodeprep-gui: The fast context maker

**Context Engineering basically.. but made effortless! prepare and share project code with any AI model, on any OS, from any editor.**

[![GitHub stars](https://img.shields.io/github/stars/detroittommy879/aicodeprep-gui.svg?style=social&label=Stars)](https://github.com/detroittommy879/aicodeprep-gui/stargazers)
[![PyPI version](https://badge.fury.io/py/aicodeprep-gui.svg)](https://badge.fury.io/py/aicodeprep-gui)

Manually copying and pasting files into AI chatbots is slow, error-prone, and kills your workflow. `aicodeprep-gui` solves this with a sleek, powerful, and blazing-fast desktop application that makes preparing code context a one-click process.

It is **platform-independent** (Windows, macOS, Linux) and **IDE-independent**. Use it alongside VS Code, Cursor, Windsurf, or any other editor. It doesn't replace your agentic workflow; it works along side it, user-curated context every time.

AI models get 'dumbed down' the more irrelevant text that gets sent with your prompt - like when you are trying to fix a bug, agents (like Cursor, Cline, etc) will send huge giant pages of text about MCP servers, how to edit files etc all of that is not related to your bug. When you use the web chat interfaces, it is clean without any tools, no MCP stuff etc and it can 100% focus on your task.

This tool allows you to go from project ---> web chat very fast. It is designed to remove that friction. All the features are to save time and save you from having to do repetitive things.

![Screenshot](scrs/n1.png)

## The aicodeprep-gui Workflow

The core philosophy is simple: **You know your code best.** Instead of letting a "dumber" IDE agent guess which files are relevant, `aicodeprep-gui` puts you in control with a smart, intuitive UI.

1.  **Launch Instantly**:

    - **Right-click** any folder in your File Explorer, Finder, or Nautilus and select "Open with aicodeprep-gui".
    - _or_ Pop open a terminal and type `aicp` and press Enter.

2.  **Review Smart Selection**: The app opens instantly, having already pre-selected the most relevant files based on a `.gitignore`-style configuration.

3.  **Fine-tune & Prompt**: Quickly check/uncheck files, use powerful **prompt presets** (like one for [Cline](https://github.com/stitionai/cline)), or write a custom question.

4.  **Generate & Paste**: Click "GENERATE CONTEXT!". The entire code bundle and your prompt are **instantly copied to your clipboard**, ready to be pasted into ChatGPT, Gemini, Claude, Openrouter, or any other AI model.

![Screenshot](scrs/flowbig.png)

5.  **Smarter AI responses and abilities**: Whenever you rely on IDE extensions or agentic IDEs to do everything, they feed too much crap into the AI which always seems to reduce its intelligence. You end up needing to use Claude for everything even minor bugs, which gets expensive. With this tool, you can use the web chat interfaces for the hard/difficult stuff, bug fixing, planning, and then paste the result back into the agent set to use a cheap unlimited model, to make the actual file changes.

## ✨ Key Features

- 🚀 **Seamless OS Integration**: The only tool of its kind with optional, native right-click context menu integration for **Windows File Explorer**, **macOS Finder**, and **Linux Nautilus**.
- 💻 **Truly Cross-Platform**: A single, consistent experience on Windows, macOS (Intel & Apple Silicon), and major Linux distributions.
- ⌨️ **Simple & Fast Commands**: Launch from anywhere by simply typing `aicp` in your terminal. Pass a directory (`aicp ./my-project`) or run it in the current folder.
- 🧠 **Intelligent File Scanning**:
  - Uses a powerful `.gitignore`-style pattern system (`aicodeprep-gui.toml`) to smartly include/exclude files.
  - Blazing-fast startup thanks to **lazy-loading**, which skips huge directories like `node_modules/` or `venv/` until you need them.
  - Remembers your file selections, window size, and layout on a per-project basis in a local `.aicodeprep-gui` file.
- 🎨 **Unique & Polished UI**:
  - A clean, modern interface built with PySide6.
  - **Automatic Light/Dark mode** detection that syncs with your OS, plus a manual toggle.
  - Satisfying, custom-styled UI components, including an intuitive file tree with hover effects.
  - Real-time **token counter** to help you stay within context limits.
- 🔧 **Powerful Prompt Engineering**:
  - Create, save, and manage **global prompt presets** that are available across all your projects.
  - Comes with useful defaults for debugging, security analysis, or generating prompts for AI agents like **Cline**.
- 🌐 **IDE & Agent Agnostic**:
  - This is **not another IDE plugin**. It's a standalone utility that enhances your workflow with _any_ tool.
  - Perfect for preparing context for agent-based IDEs like **Cursor** or **Windsurf**, or for direct use in web-based chatbots.

---

## Installation

The TL;DR version:
Make sure python is installed on your system, then install pipx. Just google how to do that or ask AI etc. Then open a fresh terminal/cmd window and type:

pipx install aicodeprep-gui

## Mac

```sh
# Install pipx using Homebrew
brew install pipx

# Add pipx to your PATH
pipx ensurepath
```

#### (then close/open a fresh new terminal window)

```sh
pipx install aicodeprep-gui
```

## Windows

Download python from python.org - pick one of the stable versions, 3.13.x is good.

Make sure the button for adding python.exe to path is turned on):

![Python path dialog](scrs/python-path.png)

Then try:

```sh
py -m pip install --user pipx
py -m pipx ensurepath
```

(if py doesn't work, try 'python' or 'python3')

Close that terminal window, and open a fresh new one (very important after installing pipx

```sh
pipx install aicodeprep-gui
```

It should say success or something similar or done.

Now that it is installed, you can type 'aicp' + enter in a terminal to run it, or 'aicp path/to/folder/'

also aicodeprep-gui command works instead of aicp - but aicp is shorter, both do the same thing (open the app window in whichever folder you typed it)

A common thing would be when you are using VS Code or Cursor, and whichever agent / agentic coder is unable to do the task or is acting stupid, go to the VS Code terminal and type 'aicp' to open it for the project you are working on. Adjust which files are going to be included in the context, then press GENERATE CONTEXT!. Paste into AI chat.

## Linux (Debian/Ubuntu instructions here but should work anywhere Python and Qt6 can work)

#### Update package lists and upgrade existing packages

```sh
sudo apt update && sudo apt upgrade -y
```

#### Install pip for Python 3

```sh
sudo apt install python3-pip -y
```

#### Install and Configure pipx

Now, use pip to install pipx. It's best to install it in your user space to avoid needing sudo for Python packages.

```sh
pip3 install --user pipx
```

```sh
pipx ensurepath
```

#### IMPORTANT: After running pipx ensurepath, you must close and reopen your terminal for the PATH changes to take effect.

In a new terminal, type:

```sh
pipx install aicodeprep-gui
```

### File Explorer Integration (Optional, Recommended)

For the ultimate workflow, add the right-click menu item after installing:

1.  Run the application (`aicp`).
2.  Go to the **File** menu in the top-left corner.
3.  Select **"Install Right-Click Menu..."** (or the equivalent for your OS).
4.  Follow the on-screen instructions. A UAC prompt may appear on Windows, as this requires administrator rights.

---

## Usage

### The GUI Way

1.  **Launch**: Right-click a project folder or type `aicp` in a terminal inside the folder.
2.  **Select**: Review the automatically selected files. The app will remember your choices for the next time you open it in this folder.
3.  **Prompt (Optional)**: Click a preset button or type a question in the prompt box.
4.  **Generate**: Click **GENERATE CONTEXT!**.
5.  **Paste**: Your context is now on your clipboard. Paste it into your AI of choice.

### The Command Line

While the GUI is the main feature, you can use these command-line options:

```bash
# Run in the current directory
aicp

# Run in a specific directory
aicodeprep-gui /path/to/your/project

# See all options
aicp --help
```

---

## Configuration

`aicodeprep-gui` is powerful out of the box, but you can customize its behavior by creating an `aicodeprep-gui.toml` file in your project's root directory. This allows you to override the default filters.

**Example `aicodeprep-gui.toml`:**

```toml
# Set a different max file size in bytes
max_file_size = 2000000

# Override the default code extensions to check
code_extensions = [".py", ".js", ".ts", ".html", ".css", ".rs"]

# Add custom exclusion patterns (uses .gitignore syntax)
exclude_patterns = [
    "build/",
    "dist/",
    "*.log",
    "temp_*",
    "cache/"
]

# Add custom patterns for files that should always be checked by default
default_include_patterns = [
    "README.md",
    "main.py",
    "docs/architecture.md"
]
```

For a full list of default settings, see the [default_config.toml](aicodeprep_gui/data/default_config.toml) in the source code.

---

## Contributing

Contributions, bug reports, and feature requests are welcome! Please feel free to open an issue or submit a pull request on GitHub. Or just email me your complaints! Happy to hear from you: tom@wuu73.org

## Github Sponsors

Your github, or your website, name, can get listed somewhere, maybe in the app itself or website, on github, etc. Any amount helps. Can enable Pro mode forever as thanks. Moved to new state, mom is dying from stage 4 adenocarcinoma, been taking care of her and also coding lots of stuff like this app. Bills are high but can't work quite yet (well I am, just not a normal job). Any money would go towards the basics to keep the lights on etc and for anything related to this. Also seeing people send dollars just motivates me to do better and want to make other useful things.

Been setting up Stripe but want to spend time reading all the docs and make sure I do everything correct - seen a lot of people that get banned posting about it and I don't ever want that to happen. I have it on Gumroad, but can take cryptocurrency, cashapp, apple pay, github sponsor button, etc

---

## Support & Donations

If this tool saves you time and makes your life easier, consider supporting its development.

| Method   | Address / Link                                                                                    |
| -------- | ------------------------------------------------------------------------------------------------- |
| Bitcoin  | `bc1qut8nz74hlwztckdghlg0jxan5gnwyqmzkr9c94`                                                      |
| Litecoin | `ltc1q3z327a3ea22mlhtawmdjxmwn69n65a32fek2s4`                                                     |
| Monero   | `46FzbFckBy9bbExzwAifMPBheYFb37k8ghGWSHqc6wE1BiEz6rQc2f665JmqUdtv1baRmuUEcDoJ2dpqY6Msa3uCKArszQZ` |
| CashApp  | `$lightweb73`                                                                                     |
| Website  | [https://wuu73.org/hello.html](https://wuu73.org/hello.html)                                      |

---

Bitcoin QR Code (same address as above):
![alt text](scrs/qrb.png)

---

## License

This software uses a Sustainable License:

- ✅ Free for personal and commercial use
- ✅ Keep and modify source code
- ✅ Use app output commercially without restrictions
- ❌ Cannot sell/redistribute this software
- ❌ Cannot offer this as a hosted service

[Full license details](SUSTAINABLE-LICENSE)

**・[GLM-4.5](https://gigazine.net/news/20250729-glm-4-5/)**  

GLM-4.5は中国に拠点を置くAI企業の**[Z.ai](https://chat.z.ai/)**が公開しているチャットAIです。Tom氏いわく「冗談抜きで、Claude 4と同等性能」とのことで、GLM-4.5のタブを2～3個開きっぱなしにしているそうです。  

**・[Kimi K2](https://gigazine.net/news/20250714-ai-kimi-k2/)**  

Kimi K2も中国製のAIで、**[Moonshot AI](https://www.moonshot.cn/)**によって2025年7月にリリースされました。Tom氏は1～2個のタブで**[kimi.com](https://www.kimi.com/)**を開いており、難しいバグについて1日に何度も質問しているそうです。  

**・[Qwenシリーズ](https://gigazine.net/news/20250728-qwen3-235b-a22b-thinking-2507/)**  

AlibabaのAI研究チームであるQwenが開発するAIシリーズもお気に入りとのこと。  

**・[OpenAI Playground](https://platform.openai.com/playground)**  

OpenAI PlaygroundはGPT-4.5やOpenAI o3といったOpenAI製AIモデルをトークン数に応じて使えるサービスです。Tom氏は使用データをAIの学習に使用することに同意した際にもらえる無料クレジットを活用しています。  

**・[Google AI Studio](https://aistudio.google.com/)**  

Google AI StudioではGemini 2.5 ProやGemini 2.5 Flashを一部無料で使えます。Tom氏は3個のタブでGoogle AI Studioを使っています。  

**・[Poe](https://poe.com/)**  

PoeはClaude 4などのAIサービスを回数制限があるものの無料で使えるサービスです。  

**・[OpenRouter](https://openrouter.ai/)**  

OpenRouterも各種AIサービスを一部無料で使えます。  

**・[LMArena](https://lmarena.ai/)**  

LMArenaもいろんなAIを使えるサービスです。特にClaude Opus 4を無料で使える点がお気に入りとのこと。  

**・[ChatGPT](https://chatgpt.com/)**  

もちろん、ChatGPTも使っています。Tom氏いわく「無料でも便利」とのこと。  

**・[Perplexity](https://gigazine.net/news/20240912-perplexity-dmitry-shevelenko-cbo-interview/)**  

Perplexityのタブを少なくとも1つは開いており、ウェブ上の情報を調査させたいタスクで活用しています。  

**・[DeepSeek](https://gigazine.net/news/20250121-deepseek-r1-open-released/)**  

DeepSeek-R1で一躍有名になったDeepSeekのチャットAIも常用。おもにDeepSeek-R1とDeepSeek-V3を使っているそうです。  

**・[Grok](https://grok.com/)**  

Tom氏はGrokをPerplexityと同様に調査用のツールとして使っているとのこと。Tom氏はGrokに**[政治的な偏り](https://gigazine.net/news/20250709-grok-update-conspiracy-jewish/)**が存在することを認識しつつ、「用途をコーディングに限るか、疑わしい動機で開発されている可能性に注意すれば、ときどき役に立つ」と述べています。  

**・[Phind](https://www.phind.com/)**  

Phindは無料で使えるチャットAIで、フローチャートや図表の作成で威力を発揮します。  
