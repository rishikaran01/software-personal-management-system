
import json
import os
from modules.config import TASKS_FILE, NOTES_FILE, CONTACTS_FILE


def load_json(filepath: str) -> list:
    """Load data from a JSON file. Returns empty list if file doesn't exist."""
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_json(filepath: str, data: list) -> bool:
    """Save data to a JSON file. Returns True on success."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"[ERROR] Could not save to {filepath}: {e}")
        return False


def load_tasks()    -> list: return load_json(TASKS_FILE)
def load_notes()    -> list: return load_json(NOTES_FILE)
def load_contacts() -> list: return load_json(CONTACTS_FILE)

def save_tasks(data)    -> bool: return save_json(TASKS_FILE, data)
def save_notes(data)    -> bool: return save_json(NOTES_FILE, data)
def save_contacts(data) -> bool: return save_json(CONTACTS_FILE, data)


def get_next_id(items: list) -> int:
    """Generate the next available integer ID."""
    return max((item.get("id", 0) for item in items), default=0) + 1


def get_summary() -> dict:
    """Return summary stats for the dashboard."""
    tasks    = load_tasks()
    notes    = load_notes()
    contacts = load_contacts()
    done     = sum(1 for t in tasks if t.get("done"))
    high     = sum(1 for t in tasks if t.get("priority") == "High" and not t.get("done"))
    return {
        "total_tasks":    len(tasks),
        "completed":      done,
        "pending":        len(tasks) - done,
        "high_priority":  high,
        "total_notes":    len(notes),
        "total_contacts": len(contacts),
        "tasks":          tasks,
    }
