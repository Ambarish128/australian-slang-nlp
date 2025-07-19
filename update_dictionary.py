import json
import csv
import os
from datetime import datetime

PENDING_FILE = "slang_data/pending_slangs.json"
SLANG_DICT_FILE = "slang_data/slang_dict.json"
LOG_FILE = "slang_data/slang_logs.csv"

def submit_new_slang(slang: str, meaning: str):
    slang = slang.strip().lower()
    meaning = meaning.strip()
    
    if not slang or not meaning:
        print("❌ Both slang and meaning are required.")
        return

    # Load pending submissions
    if os.path.exists(PENDING_FILE):
        with open(PENDING_FILE, "r", encoding="utf-8") as f:
            pending_slangs = json.load(f)
    else:
        pending_slangs = {}

    if slang in pending_slangs:
        print("⚠️ Slang already submitted and pending approval.")
        return

    pending_slangs[slang] = meaning

    with open(PENDING_FILE, "w", encoding="utf-8") as f:
        json.dump(pending_slangs, f, indent=2)

    print(f"✅ Slang '{slang}' submitted for admin approval.")


def approve_slang(slang: str):
    slang = slang.strip().lower()

    # Load pending slangs
    with open(PENDING_FILE, "r", encoding="utf-8") as f:
        pending_slangs = json.load(f)

    if slang not in pending_slangs:
        print("❌ Slang not found in pending list.")
        return

    # Load main slang dictionary
    if os.path.exists(SLANG_DICT_FILE):
        with open(SLANG_DICT_FILE, "r", encoding="utf-8") as f:
            slang_dict = json.load(f)
    else:
        slang_dict = {}

    if slang in slang_dict:
        print(f"⚠️ Slang '{slang}' already exists in the dictionary.")
        # Still remove it from pending, assuming admin rejects it silently
        del pending_slangs[slang]
        with open(PENDING_FILE, "w", encoding="utf-8") as f:
            json.dump(pending_slangs, f, indent=2)
        return

    meaning = pending_slangs[slang]
    slang_dict[slang] = meaning

    # Save updated dictionary
    with open(SLANG_DICT_FILE, "w", encoding="utf-8") as f:
        json.dump(slang_dict, f, indent=2)

    # Log approval
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([slang, meaning, datetime.now().isoformat()])

    # Remove from pending
    del pending_slangs[slang]
    with open(PENDING_FILE, "w", encoding="utf-8") as f:
        json.dump(pending_slangs, f, indent=2)

    print(f"✅ Slang '{slang}' approved and added to dictionary.")
