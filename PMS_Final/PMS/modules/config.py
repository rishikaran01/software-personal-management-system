
import os

# ─── DATA PATHS ────────────────────────────────────────────────
DATA_DIR      = os.path.join(os.path.dirname(__file__), "..", "data")
TASKS_FILE    = os.path.join(DATA_DIR, "tasks.json")
NOTES_FILE    = os.path.join(DATA_DIR, "notes.json")
CONTACTS_FILE = os.path.join(DATA_DIR, "contacts.json")

os.makedirs(DATA_DIR, exist_ok=True)

# ─── COLOR PALETTE (Catppuccin Mocha) ─────────────────────────
# ─── COLOR PALETTE ─────────────────────────────────────────────
BG      = "#F7F8FC"   # main background
SIDEBAR = "#E8ECF4"   # light sidebar
CARD    = "#FFFFFF"   # cards / panels
ACCENT  = "#6C5CE7"   # modern violet
GREEN   = "#2E9B68"   # success
RED     = "#E05260"   # delete / high priority
YELLOW  = "#D89B24"   # pending / medium priority
BLUE    = "#3978D4"   # info / edit
CYAN    = "#269FA8"   # contacts
TEXT    = "#182033"   # dark main text
SUBTEXT = "#5F6B7A"   # readable secondary text
# ─── FONTS ────────────────────────────────────────────────────
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_HEAD  = ("Segoe UI", 12, "bold")
FONT_BODY  = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)
FONT_MONO  = ("Consolas", 10)

# ─── APP META ─────────────────────────────────────────────────
APP_NAME    = "Personal Management System"
APP_VERSION = "1.0.0"
WINDOW_SIZE = "1150x700"
