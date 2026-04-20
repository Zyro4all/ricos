import os
import json

# --- FILE PATH CONFIGURATION ---
# This ensures the app finds the JSON file regardless of where it's hosted
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "keys_database.json")

def load_keys():
    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # This matches the error in your screenshot
        print(f"Error: Could not find {DB_PATH}")
        return {"keys": {}}
    except json.JSONDecodeError:
        # This handles the 'line 1 column 1' error
        print("Error: JSON file is empty or corrupted")
        return {"keys": {}}
# -------------------------------
