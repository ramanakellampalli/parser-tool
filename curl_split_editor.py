import tkinter as tk
from tkinter import ttk, scrolledtext
import shlex
from typing import Dict, Any
import json
import pyperclip

import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'

# ────────────────────────────────────────────────
#  Parsing logic (unchanged)
# ────────────────────────────────────────────────

def parse_curl_command(curl_cmd: str) -> Dict[str, Any]:
    curl_cmd = curl_cmd.strip()
    if not curl_cmd.startswith('curl'):
        raise ValueError("Command should start with 'curl'")

    lines = []
    for line in curl_cmd.splitlines():
        line = line.strip()
        if line.endswith('\\'):
            line = line[:-1].rstrip()
        lines.append(line)

    curl_cmd = ' '.join(lines)
    curl_cmd = ' '.join(curl_cmd.split())

    try:
        tokens = shlex.split(curl_cmd)
    except Exception as e:
        raise ValueError(f"Shell parsing error: {e}")

    if tokens[0] != 'curl':
        raise ValueError("Not a valid curl command")

    result = {
        'url': None,
        'method': 'GET',
        'headers': {},
        'body': [],
        'user': None,
        'other_flags': []
    }

    i = 1
    while i < len(tokens):
        token = tokens[i]
        if token in ('-X', '--request'):
            i += 1
            if i < len(tokens): result['method'] = tokens[i]
        elif token in ('-H', '--header'):
            i += 1
            if i < len(tokens):
                header = tokens[i]
                if ':' in header:
                    k, v = header.split(':', 1)
                    result['headers'][k.strip()] = v.strip()
                else:
                    result['headers'][header] = None
        elif token in ('-d', '--data', '--data-raw', '--data-binary', '--data-urlencode'):
            i += 1
            if i < len(tokens): result['body'].append(tokens[i])
        elif token in ('-u', '--user'):
            i += 1
            if i < len(tokens): result['user'] = tokens[i]
        elif not token.startswith('-'):
            if result['url'] is not None:
                raise ValueError("Multiple URLs not supported")
            result['url'] = token
        else:
            other = token
            i += 1
            if i < len(tokens) and not tokens[i].startswith('-'):
                other += f" {tokens[i]}"
            result['other_flags'].append(other)
        i += 1

    if result['url'] is None:
        raise ValueError("No URL found")

    return result


def format_parsed(parsed: Dict[str, Any]) -> str:
    lines = []
    lines.append("URL:")
    lines.append(f"  {parsed['url'] or '(not found)'}")
    lines.append("")
    lines.append("Method:")
    lines.append(f"  {parsed['method']}")
    lines.append("")
    if parsed['headers']:
        lines.append("Headers:")
        for k, v in sorted(parsed['headers'].items()):
            lines.append(f"  {k}: {v}")
        lines.append("")
    if parsed['body']:
        lines.append("Body / Data:")
        body_str = parsed['body'][0] if parsed['body'] else ""
        try:
            json_data = json.loads(body_str)
            pretty_body = json.dumps(json_data, indent=2)
            lines.append(f"{pretty_body}")
        except json.JSONDecodeError:
            lines.append(f"  {body_str}")
        lines.append("")
    if parsed['user']:
        lines.append("Basic Auth (-u):")
        lines.append(f"  {parsed['user']}")
        lines.append("")
    if parsed['other_flags']:
        lines.append("Other flags:")
        for flag in parsed['other_flags']:
            lines.append(f"  {flag}")
        lines.append("")
    return "\n".join(lines)


class CurlEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Curl Breakdown Editor")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)

        self.dark_mode = tk.BooleanVar(value=False)

        style = ttk.Style()
        style.theme_use('clam')

        # Modern sash style (thicker divider, modern grip)
        style.configure("Sash", background="#888888" if self.dark_mode.get() else "#cccccc",
                        gripcount=20, sashthickness=8, sashrelief="flat")

        main_pane = ttk.PanedWindow(root, orient=tk.HORIZONTAL)  # Removed invalid options
        main_pane.pack(fill=tk.BOTH, expand=True)

        # Left: Input
        left_frame = ttk.Frame(main_pane)
        main_pane.add(left_frame, weight=1)

        ttk.Label(left_frame, text="CURL COMMAND", font=("Helvetica", 16, "bold")).pack(pady=(25, 10))

        self.input_text = scrolledtext.ScrolledText(
            left_frame,
            wrap=tk.WORD,
            font=("JetBrains Mono", 13),
            undo=True,
            relief="flat",
            borderwidth=0
        )
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Right: Output
        right_frame = ttk.Frame(main_pane)
        main_pane.add(right_frame, weight=1)

        header_frame = ttk.Frame(right_frame)
        header_frame.pack(fill=tk.X, pady=(25, 10), padx=20)

        ttk.Label(header_frame, text="READABLE BREAKDOWN", font=("Helvetica", 16, "bold")).pack(side=tk.LEFT)

        btn_frame = ttk.Frame(header_frame)
        btn_frame.pack(side=tk.RIGHT)

        self.theme_btn = ttk.Button(btn_frame, text="Dark Mode", width=12, command=self.toggle_theme)
        self.theme_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.copy_btn = ttk.Button(btn_frame, text="Copy", width=8, command=self.copy_to_clipboard)
        self.copy_btn.pack(side=tk.LEFT)

        self.output_text = scrolledtext.ScrolledText(
            right_frame,
            wrap=tk.WORD,
            font=("JetBrains Mono", 13),
            state='disabled',
            relief="flat",
            borderwidth=0
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        self.output_text.bind("<Key>", lambda e: "break")
        self.output_text.bind("<Button-1>", lambda e: "break")
        self.output_text.bind("<B1-Motion>", lambda e: "break")

        self.status_var = tk.StringVar(value="Ready - Paste your curl command")
        self.status = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        self.apply_theme()

        self.input_text.bind("<KeyRelease>", self.on_key_release)
        self.root.after(300, self.update_preview)
        self.input_text.focus_set()

    def apply_theme(self):
        if self.dark_mode.get():
            self.root.configure(bg="#121212")
            self.input_text.configure(bg="#1e1e1e", fg="#e0e0e0", insertbackground="white")
            self.output_text.configure(bg="#1e1e1e", fg="#e0e0e0")
            self.theme_btn.configure(text="Light Mode")
            # Update sash for dark
            ttk.Style().configure("Sash", background="#888888", gripcount=20, sashthickness=8, sashrelief="flat")
        else:
            self.root.configure(bg="#fafafa")
            self.input_text.configure(bg="#ffffff", fg="#212121", insertbackground="black")
            self.output_text.configure(bg="#ffffff", fg="#212121")
            self.theme_btn.configure(text="Dark Mode")
            ttk.Style().configure("Sash", background="#cccccc", gripcount=20, sashthickness=8, sashrelief="flat")

    def toggle_theme(self):
        self.dark_mode.set(not self.dark_mode.get())
        self.apply_theme()
        self.update_preview()

    def copy_to_clipboard(self):
        text = self.output_text.get("1.0", tk.END).strip()
        if text and text != "Waiting for curl command...":
            pyperclip.copy(text)
            self.animate_status("Copied to clipboard! ✓", "green")
            self.root.after(2500, lambda: self.animate_status("Parsed successfully", "green"))
        else:
            self.animate_status("Nothing to copy", "orange")

    def animate_status(self, message: str, color: str):
        self.status_var.set(message)
        self.status.configure(foreground=color)
        self.status.configure(font=("Helvetica", 11, "bold"))
        self.root.after(100, lambda: self.status.configure(font=("Helvetica", 11)))

    def on_key_release(self, event=None):
        if hasattr(self, 'after_id'):
            self.root.after_cancel(self.after_id)
        self.after_id = self.root.after(400, self.update_preview)

    def update_preview(self):
        curl_text = self.input_text.get("1.0", tk.END).strip()

        if not curl_text:
            self._set_output("Waiting for curl command...")
            self.animate_status("Ready - Paste your curl command", "gray")
            return

        try:
            parsed = parse_curl_command(curl_text)
            formatted = format_parsed(parsed)
            self._set_output(formatted)
            self.animate_status("Parsed successfully ✓", "green")
        except ValueError as e:
            self._set_output(f"Error:\n\n{str(e)}")
            self.animate_status(f"Error: {str(e)}", "red")
        except Exception as e:
            self._set_output(f"Unexpected error:\n\n{str(e)}")
            self.animate_status("Unexpected error", "red")

    def _set_output(self, text: str):
        self.output_text.configure(state='normal')
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.configure(state='disabled')
        self.output_text.see("1.0")
        self.output_text.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = CurlEditorApp(root)
    root.mainloop()