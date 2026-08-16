
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from modules.config import *
from modules.widgets import PageHeader, ActionButton, SectionLabel
from modules.database import load_notes, save_notes, get_next_id


class NotesPage(tk.Frame):
    """Notes manager with a sidebar list and rich editor pane."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app          = app
        self.notes        = load_notes()
        self.selected_idx = None
        self._build()

    # ── UI Build ───────────────────────────────────────────────
    def _build(self):
        # Header
        hdr = PageHeader(self, "📝 Notes", "+ New Note", self._new_note, GREEN)
        hdr.pack(fill="x", padx=35, pady=(28, 10))

        # Body: left list + right editor
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=35, pady=(0, 15))

        # ── Left Pane ──────────────────────────────────────
        left = tk.Frame(body, bg=SIDEBAR, width=230)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        tk.Label(left, text="My Notes", font=FONT_HEAD, bg=SIDEBAR, fg=ACCENT).pack(pady=(12, 4))

        # Search
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *_: self._refresh_list())
        se = tk.Entry(left, textvariable=self.search_var, font=FONT_SMALL,
                      bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat")
        se.pack(fill="x", padx=8, ipady=5, pady=(0, 6))
        tk.Label(left, text="🔍 Search notes...", font=FONT_SMALL,
                 bg=SIDEBAR, fg=SUBTEXT).place(in_=se, x=6, y=5)

        # Listbox
        self.listbox = tk.Listbox(left, font=FONT_BODY, bg=CARD, fg=TEXT,
                                   selectbackground=ACCENT, selectforeground=BG,
                                   relief="flat", bd=0, activestyle="none",
                                   highlightthickness=0)
        self.listbox.pack(fill="both", expand=True, padx=6, pady=4)
        self.listbox.bind("<<ListboxSelect>>", self._on_note_select)

        # Delete button in left pane
        ActionButton(left, "🗑️ Delete Note", RED, self._delete_note).pack(
            fill="x", padx=6, pady=(4, 10), ipady=3)

        # ── Right Pane (Editor) ────────────────────────────
        right = tk.Frame(body, bg=BG)
        right.pack(side="right", fill="both", expand=True, padx=(12, 0))

        # Note title entry
        self.e_title = tk.Entry(right, font=("Segoe UI", 15, "bold"),
                                 bg=CARD, fg=ACCENT,
                                 insertbackground=ACCENT, relief="flat")
        self.e_title.pack(fill="x", ipady=8, pady=(0, 6))
        self.e_title.insert(0, "Note Title")

        # Category / Tag row
        cat_row = tk.Frame(right, bg=BG)
        cat_row.pack(fill="x", pady=(0, 6))
        tk.Label(cat_row, text="Category:", font=FONT_SMALL, bg=BG, fg=SUBTEXT).pack(side="left")
        self.e_category = tk.Entry(cat_row, font=FONT_SMALL, bg=CARD, fg=TEXT,
                                    insertbackground=TEXT, relief="flat", width=20)
        self.e_category.pack(side="left", padx=6, ipady=4)

        # Metadata label
        self.meta_lbl = tk.Label(right, text="", font=FONT_SMALL, bg=BG, fg=SUBTEXT, anchor="e")
        self.meta_lbl.pack(fill="x")

        # Text editor
        self.e_body = tk.Text(right, font=FONT_BODY, bg=CARD, fg=TEXT,
                               insertbackground=TEXT, relief="flat",
                               wrap="word", padx=12, pady=10,
                               undo=True, maxundo=50)
        self.e_body.pack(fill="both", expand=True, pady=(4, 0))

        # Toolbar
        tools = tk.Frame(right, bg=BG)
        tools.pack(fill="x", pady=8)
        ActionButton(tools, "💾 Save Note", BLUE, self._save_note).pack(side="left", padx=(0, 8))
        ActionButton(tools, "📋 Clear Editor", CARD, self._new_note).pack(side="left")

        self.char_lbl = tk.Label(tools, text="", font=FONT_SMALL, bg=BG, fg=SUBTEXT)
        self.char_lbl.pack(side="right")
        self.e_body.bind("<KeyRelease>", self._update_char_count)

        self._refresh_list()

    # ── List Management ────────────────────────────────────────
    def _refresh_list(self):
        self.listbox.delete(0, "end")
        query = self.search_var.get().lower()
        for note in self.notes:
            if query and query not in note["title"].lower() \
               and query not in note.get("content","").lower():
                continue
            self.listbox.insert("end", f"  {note['title']}")

    def _on_note_select(self, _event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        # Map listbox index to note index (accounting for search filter)
        query = self.search_var.get().lower()
        matched = [i for i, n in enumerate(self.notes)
                   if not query or query in n["title"].lower() or query in n.get("content","").lower()]
        if idx >= len(matched):
            return
        self.selected_idx = matched[idx]
        note = self.notes[self.selected_idx]

        self.e_title.delete(0, "end")
        self.e_title.insert(0, note["title"])
        self.e_category.delete(0, "end")
        self.e_category.insert(0, note.get("category", ""))
        self.e_body.delete("1.0", "end")
        self.e_body.insert("1.0", note.get("content", ""))
        created = note.get("created", "")
        updated = note.get("updated", "")
        self.meta_lbl.config(text=f"Created: {created}   Updated: {updated}")
        self._update_char_count()

    def _update_char_count(self, _=None):
        chars = len(self.e_body.get("1.0", "end").strip())
        self.char_lbl.config(text=f"{chars} chars")

    # ── CRUD Actions ───────────────────────────────────────────
    def _new_note(self):
        self.selected_idx = None
        self.e_title.delete(0, "end")
        self.e_title.insert(0, "Untitled Note")
        self.e_category.delete(0, "end")
        self.e_body.delete("1.0", "end")
        self.meta_lbl.config(text="New note — not yet saved")
        self.listbox.selection_clear(0, "end")

    def _save_note(self):
        title   = self.e_title.get().strip()
        content = self.e_body.get("1.0", "end").strip()
        category = self.e_category.get().strip()

        if not title:
            messagebox.showwarning("Required", "Note title cannot be empty.")
            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        if self.selected_idx is not None and self.selected_idx < len(self.notes):
            # Update existing
            self.notes[self.selected_idx].update({
                "title":    title,
                "content":  content,
                "category": category,
                "updated":  now,
            })
            msg = "Note updated!"
        else:
            # Create new
            self.notes.append({
                "id":       get_next_id(self.notes),
                "title":    title,
                "content":  content,
                "category": category,
                "created":  now,
                "updated":  now,
            })
            self.selected_idx = len(self.notes) - 1
            msg = "Note saved!"

        save_notes(self.notes)
        self._refresh_list()
        self.meta_lbl.config(text=f"Saved at {now}")
        messagebox.showinfo("✅ Saved", msg)

    def _delete_note(self):
        if self.selected_idx is None:
            messagebox.showwarning("No Selection", "Please select a note to delete.")
            return
        note = self.notes[self.selected_idx]
        if messagebox.askyesno("Confirm Delete", f'Delete note:\n"{note["title"]}"?'):
            self.notes.pop(self.selected_idx)
            save_notes(self.notes)
            self.selected_idx = None
            self._new_note()
            self._refresh_list()
