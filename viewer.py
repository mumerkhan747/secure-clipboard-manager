import json
import os
import pyperclip
import questionary  # Arrow keys menu library

# --- SETUP PATHS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(BASE_DIR, "clipboard_history.json")



def load_history():
  """Loads the saved clipboard history from the JSON file."""
  if not os.path.exists(HISTORY_FILE):
    print("[Debug] History file does not exist on disk yet.")
    return []

  try:
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  except json.JSONDecodeError:
    print("[Debug] JSON file is empty or corrupted.")
    return []
  except Exception:
    return []
  
  

def clear_history_file():
  """Deletes all saved logs by writing an empty list to the JSON file."""
  with open(HISTORY_FILE, "w", encoding="utf-8") as f:
    json.dump([], f)
    
  print("\n[Security] Clipboard history successfully cleared!")



def main():
  history = load_history()

  if not history:
    print(
        "\n[Result] No clipboard history found yet! Copy some text first while"
        " logger.py is running."
    )
    return

  # Prepare choices list for interactive menu
  choices = []


  # Display up to the last 10 items
  for index, item in enumerate(history[:10], start=1):
    # Flatten newlines so each item looks clean on a single line
    display_text = item["text"].replace("\n", " ")

    # Cut off text if it's too long to display nicely
    if len(display_text) > 100:
      display_text = display_text[:97] + "..."

    # Create a nice label combining number, text, and timestamp
    label = f"[{index}] {display_text}  (Copied at: {item['timestamp']})"

    # Store both the visible label and the actual hidden text value
    choices.append({"name": label, "value": item["text"]})

  # Management option AFTER the loop finishes
  choices.append({"name": "[Clear History Logs]", "value": "CLEAR_LOGS"})
  choices.append({"name": "Cancel / Exit", "value": None})

  print("\nOpening Clipboard History Viewer...")

  # --- Call questionary OUTSIDE the loop ---
  selected_text = questionary.select(
      "Use Up/Down arrows to select a snippet and press Enter:", choices=choices
  ).ask()

  # If user selected a valid text snippet (and didn't click Cancel)
  if selected_text == "CLEAR_LOGS":
    clear_history_file()
  elif selected_text:
    pyperclip.copy(selected_text)
    print(f"\n[Success] Copied back to clipboard:\n{selected_text[:40]}...")
  else:
    print("\n[Info] No selection made. Exiting viewer.")


if __name__ == "__main__":
  main()