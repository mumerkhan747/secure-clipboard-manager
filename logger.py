import json
import os
import time
import pyperclip
import subprocess
import keyboard  # For detecting Ctrl+C to stop the logger (for hotkey functionality)
import re  # Regex module to clean up text if needed

# --- SETUP PATHS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Ensure the script runs in its own directory
HISTORY_FILE = os.path.join(BASE_DIR, "clipboard_history.json")
VIEWER_FILE = os.path.join(BASE_DIR, "viewer.py")  # Path to the viewer script

print(f"[Logger Path]: {HISTORY_FILE}")

MAX_HISTORY = 20  # Keeps the last 20 copied texts


# --- SECRET PATTERNS (With proper comments for identification) ---
SECRET_PATTERNS = [
    # Patterns for OpenAI / DeepSeek API keys, which start with 'sk-'
    (r'sk-[a-zA-Z0-9]{20,}', 'OpenAI / DeepSeek API Key'),
    
    # Patterns for xAI (Grok) API keys, which start with 'xai-'
    (r'xai-[a-zA-Z0-9]{20,}', 'Grok (xAI) API Key'),
    
    # Patterns for Google / Gemini API keys, which start with 'AIza'
    # Google aur Gemini ki keys 'AIza' ya 'AQ' se shuru ho sakti hain
    # 'A' se shuru honay wali koi bhi lambi key ya token (without spaces)
    (r'A[0-9A-Za-z\-_.]{20,}', 'Generic API Key / Token (Starts with A)'),
    
    # Patterns for GitHub Classic Personal Access Tokens, which start with 'ghp_'
    (r'ghp_[a-zA-Z0-9]{36}', 'GitHub Personal Access Token'),
    
    # Patterns for GitHub Fine-Grained Tokens, which start with 'github_pat_'
    (r'github_pat_[a-zA-Z0-9_]{22,}', 'GitHub Fine-Grained Token'),
    
    # Patterns for AWS (Amazon Web Services) Access Keys, which start with 'AKIA'
    (r'AKIA[0-9A-Z]{16}', 'AWS Access Key ID'),
    
    # 7. Authorization headers ya API requests mein use hone wale Bearer tokens
    (r'bearer\s+[a-zA-Z0-9_\-\.]{20,}', 'Bearer Token')
]

def sanitize_text(text):
    """Text ke andar sensitive patterns dhoond kar unhein mask karta hai."""
    sanitized = text
    found_sensitive = False
    
    for pattern, name in SECRET_PATTERNS:
        if re.search(pattern, sanitized, re.IGNORECASE):
            found_sensitive = True
            # Asli key ko hata kar [REDACTED ...] likh deta hai
            sanitized = re.sub(pattern, f'[REDACTED {name}]', sanitized, flags=re.IGNORECASE)
            
    return sanitized, found_sensitive
  
  

def load_history():
  """
  Reads the JSON history file and returns it as a Python list.

  If the file doesn't exist yet, it returns an empty list.
  """
  if not os.path.exists(HISTORY_FILE):
    return []
  try:
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  except json.JSONDecodeError:
    return []


def save_history(history):
  """Takes the Python list of history and saves it into the JSON file."""
  with open(HISTORY_FILE, "w", encoding="utf-8") as f:
    json.dump(history, f, indent=4, ensure_ascii=False)


def open_viewer_window():
  """Triggers viewer.py to open in a new command window when hotkey is pressed."""
  print("[Debug] Hotkey detected! Opening viewer.py...")

  try:
    # This command opens a fresh command prompt window running viewer.py
    subprocess.Popen(f'start cmd /k python "{VIEWER_FILE}"', shell=True)
  except Exception as e:
    print(f"[Error] Failed to open viewer.py: {e}")

def main():
  print("Clipboard Logger is active in the background...")
  print("Press [Alt + C] anywhere on your PC to open the history menu.")
  print("Press [Ctrl + C] to stop the Logger.")
  
  # --- REGISTER GLOBAL HOTKEY ---
  # Whenever you press Alt + C, it executes the open_viewer_window function
  keyboard.add_hotkey("alt+c", open_viewer_window)

  last_text = ""

  # Sync with existing history if available
  history = load_history()

  if history:
    last_text = history[0]["text"]

  while True:
    try:
      current_text = pyperclip.paste()

      # Check if text is not empty and is a new copy action
      if current_text and current_text.strip() and current_text != last_text:
        last_text = current_text
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # --- YAHAN SANITIZE KAREIN ---
        processed_text, is_sensitive = sanitize_text(current_text)

        # Remove duplicate if it already exists lower down in history
        history = [item for item in history if item["text"] != processed_text]

        # Add new item to the top of the list
        history.insert(0, {"text": processed_text, "timestamp": timestamp})

        # Trim list if it exceeds the maximum limit
        if len(history) > MAX_HISTORY:
          history = history[:MAX_HISTORY]

        save_history(history)
        
        # --- PRINTING LOGIC (Yahan dhyan dein) ---
        if is_sensitive:
            print(f"[Security] Sensitive API key detected & masked safely!")
            print(f"[Logged] {processed_text[:40]}...")
        else:
            if len(processed_text) > 100:
                print(f"[Logged] {processed_text[:97]}...")
            else:
                print(f"[Logged] {processed_text}")

    except Exception as e:
      print(f"Error: {e}")

    time.sleep(1)  # Wait 1 second before checking the clipboard again


if __name__ == "__main__":
    main()