
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from modules.config import *
from modules.widgets import PageHeader, ActionButton, SectionLabel
from modules.database import load_contacts, save_contacts, get_next_id


CATEGORIES = ["Family", "Friend", "Colleague", "Client", "Other"]


class ContactsPage(tk.Frame):
    """Contacts manager with table view and search."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app      = app
        self.contacts = load_contacts()
        self._build()

    # ── UI Build ───────────────────────────────────────────────
    def _build(self):
        # Header
        hdr = PageHeader(self, "👤 Contacts", "+ Add Contact", self._open_add_dialog, GREEN)
        hdr.pack(fill="x", padx=35, pady=(28, 8))

        # Filter / Search bar
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=35, pady=(0, 8))

        tk.Label(bar, text="Category:", font=FONT_BODY, bg=BG, fg=SUBTEXT).pack(side="left")
        self.cat_var = tk.StringVar(value="All")
        for cat in ["All"] + CATEGORIES:
            tk.Radiobutton(bar, text=cat, variable=self.cat_var, value=cat,
                           font=FONT_SMALL, bg=BG, fg=TEXT,
                           selectcolor=BG, activebackground=BG,
                           command=self._refresh).pack(side="left", padx=4)

        tk.Label(bar, text="  🔍", font=FONT_BODY, bg=BG, fg=SUBTEXT).pack(side="left", padx=(16, 4))
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *_: self._refresh())
        tk.Entry(bar, textvariable=self.search_var, font=FONT_BODY,
                 bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat", width=22
                 ).pack(side="left", ipady=5)

        # Treeview
        cols = ("Name", "Email", "Phone", "Category", "Address", "Added")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=16)
        widths    = [180, 220, 130, 100, 200, 120]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w,
                             anchor="w" if col in ("Name","Email","Address") else "center")
        self.tree.pack(padx=35, fill="both", expand=True)
        self.tree.bind("<Double-1>", lambda _: self._open_edit_dialog())

        # Action buttons
        btn_row = tk.Frame(self, bg=BG)
        btn_row.pack(padx=35, pady=10, fill="x")
        for text, color, cmd in [
            ("✏️  Edit Contact",   BLUE,   self._open_edit_dialog),
            ("🗑️  Delete Contact", RED,    self._delete_contact),
            ("📋 Copy Email",       ACCENT, self._copy_email),
        ]:
            ActionButton(btn_row, text, color, cmd).pack(side="left", padx=5)

        # Status bar
        self.status_lbl = tk.Label(self, text="", font=FONT_SMALL, bg=BG, fg=SUBTEXT)
        self.status_lbl.pack(anchor="w", padx=35, pady=(0, 6))

        self._refresh()

    # ── Data / Refresh ─────────────────────────────────────────
    def _refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        cat   = self.cat_var.get()
        query = self.search_var.get().lower()
        shown = 0

        for c in self.contacts:
            if cat != "All" and c.get("category", "") != cat:
                continue
            if query and query not in c["name"].lower() \
               and query not in c.get("email","").lower() \
               and query not in c.get("phone","").lower():
                continue
            self.tree.insert("", "end", iid=str(c["id"]),
                             values=(c["name"],
                                     c.get("email",""),
                                     c.get("phone",""),
                                     c.get("category",""),
                                     c.get("address",""),
                                     c.get("added","")))
            shown += 1

        self.status_lbl.config(text=f"Showing {shown} of {len(self.contacts)} contacts")

    # ── Selection Helper ───────────────────────────────────────
    def _get_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select a contact first.")
            return None
        cid = sel[0]
        return next((c for c in self.contacts if str(c["id"]) == str(cid)), None)

    # ── CRUD Actions ───────────────────────────────────────────
    def _open_add_dialog(self):
        ContactDialog(self, "➕ Add Contact", None, self._save_new)

    def _save_new(self, data):
        data["id"]    = get_next_id(self.contacts)
        data["added"] = datetime.now().strftime("%Y-%m-%d")
        self.contacts.append(data)
        save_contacts(self.contacts)
        self._refresh()

    def _open_edit_dialog(self):
        c = self._get_selected()
        if c:
            ContactDialog(self, "✏️ Edit Contact", c,
                          lambda d: self._save_edit(c, d))

    def _save_edit(self, contact, data):
        contact.update(data)
        save_contacts(self.contacts)
        self._refresh()

    def _delete_contact(self):
        c = self._get_selected()
        if c and messagebox.askyesno("Confirm Delete",
                                      f'Delete contact:\n"{c["name"]}"?'):
            self.contacts.remove(c)
            save_contacts(self.contacts)
            self._refresh()

    def _copy_email(self):
        c = self._get_selected()
        if c:
            email = c.get("email","")
            if email:
                self.clipboard_clear()
                self.clipboard_append(email)
                messagebox.showinfo("Copied", f"Email copied:\n{email}")
            else:
                messagebox.showinfo("No Email", "This contact has no email.")


# ── Contact Add/Edit Dialog ────────────────────────────────────
class ContactDialog(tk.Toplevel):
    """Modal dialog for adding or editing a contact."""

    def __init__(self, parent, title, contact, on_save):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=BG)
        self.geometry("450x480")
        self.resizable(False, False)
        self.on_save = on_save
        self._build(contact)
        self.grab_set()
        self.focus_force()

    def _build(self, c):
        tk.Label(self, text=self.title(), font=FONT_HEAD,
                 bg=BG, fg=ACCENT).pack(pady=(18, 12))

        form = tk.Frame(self, bg=BG)
        form.pack(fill="x", padx=30)

        # Fields
        self.entries = {}
        fields = [
            ("Full Name *",   "name"),
            ("Email Address", "email"),
            ("Phone Number",  "phone"),
            ("Address",       "address"),
            ("Company",       "company"),
        ]
        for label, key in fields:
            tk.Label(form, text=label, font=FONT_BODY, bg=BG, fg=TEXT).pack(anchor="w")
            e = tk.Entry(form, font=FONT_BODY, bg=CARD, fg=TEXT,
                         insertbackground=TEXT, relief="flat")
            e.pack(fill="x", ipady=6, pady=(2, 8))
            if c: e.insert(0, c.get(key, ""))
            self.entries[key] = e

        # Category
        tk.Label(form, text="Category", font=FONT_BODY, bg=BG, fg=TEXT).pack(anchor="w")
        self.cat_var = tk.StringVar(value=c.get("category","Other") if c else "Other")
        cat_frame = tk.Frame(form, bg=BG)
        cat_frame.pack(anchor="w", pady=(2, 10))
        colors = {"Family": BLUE, "Friend": GREEN, "Colleague": YELLOW,
                  "Client": ACCENT, "Other": SUBTEXT}
        for cat in CATEGORIES:
            tk.Radiobutton(cat_frame, text=cat, variable=self.cat_var, value=cat,
                           font=FONT_SMALL, bg=BG, fg=colors.get(cat, TEXT),
                           selectcolor=BG, activebackground=BG).pack(side="left", padx=6)

        ActionButton(self, "💾 Save Contact", ACCENT, self._save).pack(pady=12, ipadx=20, ipady=4)

    def _save(self):
        name = self.entries["name"].get().strip()
        if not name:
            messagebox.showwarning("Required", "Full name is required.", parent=self)
            return
        data = {k: e.get().strip() for k, e in self.entries.items()}
        data["category"] = self.cat_var.get()
        self.on_save(data)
        self.destroy()
