

import tkinter as tk
from tkinter import ttk
from modules.config import *


def apply_treeview_style():
    """Apply dark theme to all ttk.Treeview widgets."""
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background=CARD,
                    foreground=TEXT,
                    fieldbackground=CARD,
                    rowheight=30,
                    font=FONT_BODY)
    style.configure("Treeview.Heading",
                    background=SIDEBAR,
                    foreground=ACCENT,
                    font=FONT_HEAD,
                    relief="flat")
    style.map("Treeview",
              background=[("selected", ACCENT)],
              foreground=[("selected", BG)])


class PageHeader(tk.Frame):
    """Standard page header with title and optional action button."""
    def __init__(self, parent, title, btn_text=None, btn_cmd=None, btn_color=None):
        super().__init__(parent, bg=BG)
        tk.Label(self, text=title, font=FONT_TITLE, bg=BG, fg=ACCENT).pack(side="left")
        if btn_text and btn_cmd:
            tk.Button(self, text=btn_text,
                      font=FONT_BODY,
                      bg=btn_color or GREEN,
                      fg=BG,
                      relief="flat",
                      padx=14, pady=4,
                      cursor="hand2",
                      command=btn_cmd).pack(side="right")


class ActionButton(tk.Button):
    """Styled action button."""
    def __init__(self, parent, text, color, command, **kwargs):
        super().__init__(parent,
                         text=text,
                         font=FONT_BODY,
                         bg=color,
                         fg=BG,
                         relief="flat",
                         padx=12, pady=4,
                         cursor="hand2",
                         activebackground=color,
                         activeforeground=BG,
                         command=command,
                         **kwargs)


class LabeledEntry(tk.Frame):
    """A label + entry field combo."""
    def __init__(self, parent, label, width=45, show=None):
        super().__init__(parent, bg=BG)
        tk.Label(self, text=label, font=FONT_BODY, bg=BG, fg=TEXT).pack(anchor="w")
        self.entry = tk.Entry(self, font=FONT_BODY, bg=CARD, fg=TEXT,
                              insertbackground=TEXT, relief="flat",
                              width=width, show=show or "")
        self.entry.pack(fill="x", ipady=6, pady=(2, 8))

    def get(self): return self.entry.get().strip()
    def set(self, val): self.entry.delete(0, "end"); self.entry.insert(0, val)


class SearchBar(tk.Frame):
    """A search bar with a 🔍 icon."""
    def __init__(self, parent, variable):
        super().__init__(parent, bg=BG)
        tk.Label(self, text="🔍 Search:", font=FONT_BODY, bg=BG, fg=SUBTEXT).pack(side="left")
        tk.Entry(self, textvariable=variable,
                 font=FONT_BODY, bg=CARD, fg=TEXT,
                 insertbackground=TEXT, relief="flat",
                 width=30).pack(side="left", ipady=5, padx=(6, 0))


class StatCard(tk.Frame):
    """Dashboard summary stat card."""
    def __init__(self, parent, value, label, color):
        super().__init__(parent, bg=CARD, padx=18, pady=14)
        tk.Label(self, text=str(value),
                 font=("Segoe UI", 28, "bold"),
                 bg=CARD, fg=color).pack()
        tk.Label(self, text=label,
                 font=FONT_SMALL, bg=CARD, fg=SUBTEXT).pack()


class SectionLabel(tk.Label):
    """Section heading label."""
    def __init__(self, parent, text):
        super().__init__(parent, text=text, font=FONT_HEAD, bg=BG, fg=TEXT)


class Separator(tk.Frame):
    """Horizontal separator line."""
    def __init__(self, parent):
        super().__init__(parent, bg=CARD, height=1)
