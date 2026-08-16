

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from modules.config import *
from modules.widgets import PageHeader, ActionButton, SectionLabel
from modules.database import load_tasks, save_tasks, get_next_id


class TasksPage(tk.Frame):
    """Full task management interface."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app   = app
        self.tasks = load_tasks()
        self._build()

    # ── UI Build ───────────────────────────────────────────────
    def _build(self):
        # Header
        hdr = PageHeader(self, "✅ Task Manager", "+ Add Task", self._open_add_dialog, GREEN)
        hdr.pack(fill="x", padx=35, pady=(28, 8))

        # Filter / Search bar
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=35, pady=(0, 8))

        tk.Label(bar, text="Filter:", font=FONT_BODY, bg=BG, fg=SUBTEXT).pack(side="left")
        self.filter_var = tk.StringVar(value="All")
        for f in ["All", "Pending", "Completed", "High Priority"]:
            tk.Radiobutton(bar, text=f, variable=self.filter_var, value=f,
                           font=FONT_SMALL, bg=BG, fg=TEXT,
                           selectcolor=BG, activebackground=BG,
                           command=self._refresh).pack(side="left", padx=6)

        tk.Label(bar, text="  🔍", font=FONT_BODY, bg=BG, fg=SUBTEXT).pack(side="left", padx=(20, 4))
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *_: self._refresh())
        tk.Entry(bar, textvariable=self.search_var, font=FONT_BODY,
                 bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat", width=24
                 ).pack(side="left", ipady=5)

        # Treeview table
        cols = ("ID", "Title", "Priority", "Due Date", "Status", "Created")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=16)
        widths = [45, 320, 90, 110, 110, 130]
        anchors = ["center", "w", "center", "center", "center", "center"]
        for col, w, a in zip(cols, widths, anchors):
            self.tree.heading(col, text=col,
                              command=lambda c=col: self._sort_by(c))
            self.tree.column(col, width=w, anchor=a)
        self.tree.pack(padx=35, fill="both", expand=True)
        self.tree.bind("<Double-1>", lambda e: self._open_edit_dialog())

        # Tag colors
        self.tree.tag_configure("done",   foreground=GREEN)
        self.tree.tag_configure("high",   foreground=RED)
        self.tree.tag_configure("medium", foreground=YELLOW)
        self.tree.tag_configure("low",    foreground=BLUE)

        # Action buttons
        btn_row = tk.Frame(self, bg=BG)
        btn_row.pack(padx=35, pady=10, fill="x")
        for text, color, cmd in [
            ("✅ Mark Done / Undo", GREEN,  self._toggle_done),
            ("✏️  Edit Task",        BLUE,   self._open_edit_dialog),
            ("🗑️  Delete Task",     RED,    self._delete_task),
            ("🔄 Refresh",          SUBTEXT, self._refresh),
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

        filt   = self.filter_var.get()
        query  = self.search_var.get().lower()
        shown  = 0

        for t in self.tasks:
            # Apply filter
            if filt == "Pending"       and t.get("done"):                     continue
            if filt == "Completed"     and not t.get("done"):                 continue
            if filt == "High Priority" and (t.get("priority") != "High" or t.get("done")): continue
            # Apply search
            if query and query not in t["title"].lower():                      continue

            status = "✅ Done" if t.get("done") else "⏳ Pending"
            prio   = t.get("priority", "Medium")

            if t.get("done"):
                tag = "done"
            elif prio == "High":
                tag = "high"
            elif prio == "Low":
                tag = "low"
            else:
                tag = "medium"

            self.tree.insert("", "end", iid=str(t["id"]),
                             values=(t["id"], t["title"], prio,
                                     t.get("due", "—"), status,
                                     t.get("created", "")),
                             tags=(tag,))
            shown += 1

        total = len(self.tasks)
        done  = sum(1 for t in self.tasks if t.get("done"))
        self.status_lbl.config(
            text=f"Showing {shown} of {total} tasks  •  {done} completed  •  {total - done} pending"
        )

    def _sort_by(self, col):
        """Sort tree by column (toggle asc/desc)."""
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        items.sort()
        for idx, (_, k) in enumerate(items):
            self.tree.move(k, "", idx)

    # ── Selection Helper ───────────────────────────────────────
    def _get_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select a task first.")
            return None
        tid = int(sel[0])
        return next((t for t in self.tasks if t["id"] == tid), None)

    # ── CRUD Actions ───────────────────────────────────────────
    def _open_add_dialog(self):
        TaskDialog(self, "➕ Add New Task", task=None, on_save=self._save_new)

    def _save_new(self, data):
        data["id"]      = get_next_id(self.tasks)
        data["done"]    = False
        data["created"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.tasks.append(data)
        save_tasks(self.tasks)
        self._refresh()

    def _open_edit_dialog(self):
        task = self._get_selected()
        if task:
            TaskDialog(self, "✏️ Edit Task", task=task,
                       on_save=lambda d: self._save_edit(task, d))

    def _save_edit(self, task, data):
        task.update(data)
        task["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        save_tasks(self.tasks)
        self._refresh()

    def _toggle_done(self):
        task = self._get_selected()
        if task:
            task["done"] = not task["done"]
            save_tasks(self.tasks)
            self._refresh()

    def _delete_task(self):
        task = self._get_selected()
        if task and messagebox.askyesno("Confirm Delete",
                                         f'Delete task:\n"{task["title"]}"?'):
            self.tasks.remove(task)
            save_tasks(self.tasks)
            self._refresh()


# ── Task Add/Edit Dialog ───────────────────────────────────────
class TaskDialog(tk.Toplevel):
    """Modal dialog for adding or editing a task."""

    def __init__(self, parent, title, task, on_save):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=BG)
        self.geometry("460x380")
        self.resizable(False, False)
        self.on_save = on_save
        self._build(task)
        self.grab_set()
        self.focus_force()

    def _build(self, t):
        tk.Label(self, text=self.title(), font=FONT_HEAD,
                 bg=BG, fg=ACCENT).pack(pady=(20, 12))

        form = tk.Frame(self, bg=BG)
        form.pack(fill="x", padx=30)

        # Title
        tk.Label(form, text="Task Title *", font=FONT_BODY, bg=BG, fg=TEXT).pack(anchor="w")
        self.e_title = tk.Entry(form, font=FONT_BODY, bg=CARD, fg=TEXT,
                                 insertbackground=TEXT, relief="flat")
        self.e_title.pack(fill="x", ipady=6, pady=(3, 10))
        if t: self.e_title.insert(0, t.get("title", ""))

        # Due Date
        tk.Label(form, text="Due Date (YYYY-MM-DD)", font=FONT_BODY, bg=BG, fg=TEXT).pack(anchor="w")
        self.e_due = tk.Entry(form, font=FONT_BODY, bg=CARD, fg=TEXT,
                               insertbackground=TEXT, relief="flat")
        self.e_due.pack(fill="x", ipady=6, pady=(3, 10))
        if t: self.e_due.insert(0, t.get("due", ""))

        # Priority
        tk.Label(form, text="Priority", font=FONT_BODY, bg=BG, fg=TEXT).pack(anchor="w")
        self.prio_var = tk.StringVar(value=t.get("priority", "Medium") if t else "Medium")
        pf = tk.Frame(form, bg=BG)
        pf.pack(anchor="w", pady=(3, 10))
        for p, c in [("Low", GREEN), ("Medium", YELLOW), ("High", RED)]:
            tk.Radiobutton(pf, text=p, variable=self.prio_var, value=p,
                           font=FONT_BODY, bg=BG, fg=c, selectcolor=BG,
                           activebackground=BG).pack(side="left", padx=10)

        # Notes
        tk.Label(form, text="Notes (optional)", font=FONT_BODY, bg=BG, fg=TEXT).pack(anchor="w")
        self.e_notes = tk.Text(form, font=FONT_BODY, bg=CARD, fg=TEXT,
                                insertbackground=TEXT, relief="flat",
                                height=4, wrap="word")
        self.e_notes.pack(fill="x", pady=(3, 10))
        if t: self.e_notes.insert("1.0", t.get("notes", ""))

        # Save button
        ActionButton(self, "💾 Save Task", ACCENT, self._save).pack(pady=10, ipadx=20, ipady=4)

    def _save(self):
        title = self.e_title.get().strip()
        if not title:
            messagebox.showwarning("Required", "Task title is required.", parent=self)
            return
        self.on_save({
            "title":    title,
            "due":      self.e_due.get().strip(),
            "priority": self.prio_var.get(),
            "notes":    self.e_notes.get("1.0", "end").strip(),
        })
        self.destroy()
