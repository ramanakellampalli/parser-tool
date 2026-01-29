<div align="center">

# 🔧 Curl Breakdown Editor

### A modern split-screen GUI tool for parsing and formatting curl commands

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)]()

![Curl Breakdown Editor](https://img.shields.io/badge/Status-Active-success)

</div>

---

## ✨ Overview

**Curl Breakdown Editor** instantly parses and reformats complex curl commands into human-readable sections. Simply paste any curl command (single-line or multi-line with `\` continuations) on the left, and see a beautifully formatted breakdown on the right in real time.

Perfect for developers who work with APIs, need to debug curl requests, or want to understand complex commands at a glance.

---

## 🎯 Features

- ⚡ **Real-time parsing** of curl commands (handles multi-line with `\`)
- 📋 **Clean, sectioned output** (URL, Method, Headers, Body, Auth, Other flags)
- 🎨 **Automatic JSON pretty-printing** for `-d` payloads
- 🌓 **Dark & Light themes** with one-click toggle
- 📎 **Copy to Clipboard** functionality
- 💫 **Smooth status bar feedback**
- 🔤 **Modern monospace font** (JetBrains Mono recommended)

---

## 📋 Requirements

- **Python** 3.8 or higher
- **Tkinter** (usually comes bundled with Python)
- **pyperclip** (for copy-to-clipboard functionality)

---

## 🚀 Installation

### Option 1: Using a Virtual Environment (Recommended)

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/ramanakellampalli/parser-tool.git
cd parser-tool
```

#### 2️⃣ Create and Activate Virtual Environment

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

#### 3️⃣ Install Dependencies

```bash
pip install pyperclip
```

### Option 2: Using Homebrew Python (macOS Only)

```bash
brew install python@3.12
python3.12 -m venv venv
source venv/bin/activate
pip install pyperclip
```

---

## 🎮 Running the Application

With the virtual environment activated:

```bash
python curl_split_editor.py
```

Or using a specific Python version:

```bash
python3.12 curl_split_editor.py
```

The GUI window should open immediately! 🎉

---

## 💡 Usage

### Step-by-Step Guide

1. **Paste** any curl command into the left pane
2. **Watch** the right pane update live with formatted sections
3. **Toggle** between Dark Mode and Light Mode using the theme button
4. **Click** the "Copy" button to copy the formatted breakdown to your clipboard

### 📝 Example

#### Input (Left Pane):
```bash
curl -X POST https://api.example.com/login \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer xyz123" \
  -d '{"username":"admin","password":"secret"}' \
  -u "debug:1234" --verbose
```

#### Output (Right Pane):
```
URL:
  https://api.example.com/login

Method:
  POST

Headers:
  Content-Type: application/json
  Authorization: Bearer xyz123

Body / Data:
  {
    "username": "admin",
    "password": "secret"
  }

Basic Auth (-u):
  debug:1234

Other flags:
  --verbose
```

---

## 🎨 Recommended Font

For the **best visual experience**, install **JetBrains Mono** (free, open-source):

🔗 [Download JetBrains Mono](https://www.jetbrains.com/lp/mono/)

1. Download and install the font files on your system
2. Restart the application

> **Note:** The application automatically falls back to **Consolas** (Windows) or **Menlo** (macOS) if JetBrains Mono is not available.

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Text appears invisible** | Select the text or switch themes (rare macOS Tkinter redraw issue) |
| **Copy button does nothing** | Ensure `pyperclip` is installed in the active virtual environment |
| **Font looks wrong** | Install JetBrains Mono or adjust the font settings in the code |
| **Tkinter errors on macOS** | Use Python from [python.org](https://www.python.org) or Homebrew instead of system Python |

---

## 🤝 Contributing

Contributions are welcome! Feel free to submit **Pull Requests** or open **Issues** for bugs and feature requests.

### 💭 Ideas for Future Improvements

- [ ] Syntax highlighting for curl commands in the input area
- [ ] Line numbers for the input text
- [ ] Save/load curl presets
- [ ] Export to Markdown or JSON
- [ ] Additional animations and visual effects
- [ ] Support for more curl flags and options
- [ ] Command history navigation

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

Feel free to use, modify, and distribute! 🎉

---

## 🙏 Acknowledgments

Built with:
- 🐍 **Python**
- 🖼️ **Tkinter**
- 📋 **pyperclip**

---

<div align="center">

**Made with ❤️ by developers, for developers**

Happy curling! 🚀

[Report Bug](https://github.com/ramanakellampalli/parser-tool/issues) · [Request Feature](https://github.com/ramanakellampalli/parser-tool/issues)

</div>