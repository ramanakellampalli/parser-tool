# Curl Breakdown Editor

A modern, split-screen GUI tool that instantly parses and reformats complex curl commands into human-readable sections (URL, Method, Headers, Body, Auth, etc.).

Paste any curl command (single-line or multi-line with \ continuations) on the left → see a nicely formatted breakdown on the right in real time.

## Features

- Real-time parsing of curl commands (handles multi-line with \)
- Clean, sectioned output (URL, Method, Headers, Body, Auth, Other flags)
- Automatic JSON pretty-printing for -d payloads
- Dark & Light themes with one-click toggle
- "Copy to Clipboard" button
- Smooth status bar feedback
- Modern monospace font (JetBrains Mono recommended)

## Requirements

- Python 3.8+
- Tkinter (usually comes with Python)
- pyperclip (for copy-to-clipboard functionality)

## Installation

### Recommended: Using a virtual environment

1. Clone or download the project:
   git clone https://github.com/yourusername/parser-tool.git
   cd parser-tool

2. Create and activate a virtual environment:
   python3 -m venv venv
   source venv/bin/activate          # On Windows: venv\Scripts\activate

3. Install the required package:
   pip install pyperclip

### Alternative: Using Homebrew Python (macOS)

brew install python@3.12
python3.12 -m venv venv
source venv/bin/activate
pip install pyperclip

## Running the Application

With the virtual environment activated:

python curl_split_editor.py

Or directly using a specific Python version:

python3.12 curl_split_editor.py

The GUI window should open immediately.

## Setup & Running

1. Clone the repository
2. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
3. Install dependencies:
    ```bash
    pip install pyperclip
4. Run the app:
    ```bash
    python curl_split_editor.py

## Usage

1. Paste any curl command into the left pane
2. Watch the right pane update live with formatted sections
3. Use the Dark Mode / Light Mode button to switch themes
4. Click Copy to copy the formatted breakdown to your clipboard

### Example Input

curl -X POST https://api.example.com/login \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer xyz123" \
  -d '{"username":"admin","password":"secret"}' \
  -u "debug:1234" --verbose

### Example Output (formatted)

URL:
  https://api.example.com/login

Method:
  POST

Headers:
  Content-Type: application/json
  Authorization: Bearer xyz123

Body / Data:
  (JSON pretty-printed)
  {
    "username": "admin",
    "password": "secret"
  }

Basic Auth (-u):
  debug:1234

Other flags:
  --verbose

## Recommended Font

For the best visual experience, install JetBrains Mono (free):

https://www.jetbrains.com/lp/mono/

Install the font files on your system and restart the application.

The application falls back to Consolas or Menlo if the font is not available.

## Troubleshooting

- Text appears invisible → Select the text or switch themes (rare macOS Tkinter redraw issue)
- Copy button does nothing → Ensure pyperclip is installed in the active environment
- Font looks wrong → Install JetBrains Mono or adjust the font in the code
- Tkinter errors on macOS → Try using Python from python.org or Homebrew instead of the system Python

## Contributing

Pull requests are welcome!

Possible improvements:

- Basic syntax highlighting for curl commands in the input area
- Line numbers for the input text
- Save/load curl presets
- Export to Markdown or JSON
- Additional animations or visual effects

## License

MIT License

Feel free to use, modify, and distribute.

---

Made with Python + Tkinter
Happy curling!