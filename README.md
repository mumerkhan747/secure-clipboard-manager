# 📋 Secure Lightweight Clipboard Manager for Windows

A lightweight, terminal-based clipboard manager built with Python. It runs quietly in the background, logs your copied snippets, features an interactive arrow-key menu, and **automatically masks/redacts sensitive API keys and tokens** for your privacy!

---

## ✨ Features

- **Background Logging:** Automatically tracks and saves your copied text history (up to the last 20 items) using `pyperclip`.
- **Global Hotkey (`Alt + C`):** Instantly pops up an interactive menu anywhere on your PC without interrupting your workflow.
- **Interactive Viewer:** Use your **Up/Down arrow keys** via `questionary` to select and copy past items right back to your clipboard.
- **🛡️ Built-in Security (Auto-Redaction):** Automatically detects and masks sensitive data (like OpenAI, Grok, Gemini, and GitHub tokens or generic keys starting with 'A') before saving them to disk.
- **Privacy First:** Your raw history is stored locally in a JSON file and is completely ignored by Git.

---

## 🛠️ Requirements & Installation

Make sure you have Python installed on your Windows machine. Then follow these steps:

1. **Clone or download** this repository.
2. Open your terminal inside the project folder and install the required dependencies:
   ```bash
   pip install -r requirements.txt