
import tkinter as tk
from datetime import datetime
from modules.config import *
from modules.widgets import StatCard, SectionLabel, ActionButton
from modules.database import get_summary, load_tasks, save_tasks, get_next_id
from tkinter import messagebox


class DashboardPage(tk.Frame):
    """Main dashboard with stats, recent tasks, and quick-add."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        # ── Page Title ─────────────────────────────────────
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=35, pady=(30, 5))
        tk.Label(header, text="🏠 Dashboard", font=FONT_TITLE, bg=BG, fg=ACCENT).pack(side="left")

        day_str = datetime.now().strftime("%A, %d %B %Y")
        tk.Label(self, text=f"Welcome back!  •  {day_str}",
                 font=FONT_BODY, bg=BG, fg=SUBTEXT).pack(anchor="w", padx=35)

        tk.Frame(self, bg=CARD, height=1).pack(fill="x", padx=35, pady=12)

        # ── Stats Row ──────────────────────────────────────
        summary = get_summary()
        stats = [
            (summary["total_tasks"],    "📋 Total Tasks",    BLUE),
            (summary["completed"],       "✅ Completed",      GREEN),
            (summary["pending"],         "⏳ Pending",        YELLOW),
            (summary["high_priority"],   "🔴 High Priority",  RED),
            (summary["total_notes"],     "📝 Notes",          ACCENT),
            (summary["total_contacts"],  "👤 Contacts",       CYAN),
        ]
        cards_frame = tk.Frame(self, bg=BG)
        cards_frame.pack(fill="x", padx=35, pady=(0, 18))
        for i, (val, lbl, clr) in enumerate(stats):
            card = StatCard(cards_frame, val, lbl, clr)
            card.grid(row=0, column=i, padx=6, sticky="nsew")
            cards_frame.columnconfigure(i, weight=1)

        # ── Two-column lower section ───────────────────────
        lower = tk.Frame(self, bg=BG)
        lower.pack(fill="both", expand=True, padx=35, pady=(0, 20))
        lower.columnconfigure(0, weight=3)
        lower.columnconfigure(1, weight=2)

        # Left: Recent Tasks
        left = tk.Frame(lower, bg=CARD, padx=15, pady=12)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        SectionLabel(left, "🕒 Recent Tasks").pack(anchor="w", pady=(0, 8))

        tasks = summary["tasks"]
        recent = list(reversed(tasks[-6:])) if tasks else []
        if not recent:
            tk.Label(left, text="No tasks yet. Add your first task below!",
                     font=FONT_BODY, bg=CARD, fg=SUBTEXT).pack(pady=10)
        for t in recent:
            row = tk.Frame(left, bg=CARD)
            row.pack(fill="x", pady=3)
            icon  = "✅" if t.get("done") else "⏳"
            color = GREEN if t.get("done") else YELLOW
            p_color = {
                "High": RED, "Medium": YELLOW, "Low": GREEN
            }.get(t.get("priority","Medium"), YELLOW)

            tk.Label(row, text=icon, font=FONT_BODY, bg=CARD, fg=color).pack(side="left")
            tk.Label(row, text=t["title"], font=FONT_BODY, bg=CARD, fg=TEXT,
                     anchor="w").pack(side="left", padx=6, fill="x", expand=True)
            tk.Label(row, text=f"[{t.get('priority','—')}]", font=FONT_SMALL,
                     bg=CARD, fg=p_color).pack(side="right", padx=4)
            tk.Label(row, text=t.get("due",""), font=FONT_SMALL,
                     bg=CARD, fg=SUBTEXT).pack(side="right")

        # Right: Quick Add
        right = tk.Frame(lower, bg=CARD, padx=15, pady=12)
        right.grid(row=0, column=1, sticky="nsew")

        SectionLabel(right, "⚡ Quick Add Task").pack(anchor="w", pady=(0, 8))

        tk.Label(right, text="Title:", font=FONT_SMALL, bg=CARD, fg=SUBTEXT).pack(anchor="w")
        self.q_title = tk.Entry(right, font=FONT_BODY, bg=BG, fg=TEXT,
                                 insertbackground=TEXT, relief="flat")
        self.q_title.pack(fill="x", ipady=6, pady=(2, 8))

        tk.Label(right, text="Priority:", font=FONT_SMALL, bg=CARD, fg=SUBTEXT).pack(anchor="w")
        self.q_prio = tk.StringVar(value="Medium")
        pf = tk.Frame(right, bg=CARD)
        pf.pack(anchor="w", pady=(2, 8))
        for p, c in [("Low", GREEN), ("Medium", YELLOW), ("High", RED)]:
            tk.Radiobutton(pf, text=p, variable=self.q_prio, value=p,
                           font=FONT_SMALL, bg=CARD, fg=c, selectcolor=BG,
                           activebackground=CARD).pack(side="left", padx=4)

        tk.Label(right, text="Due Date (YYYY-MM-DD):", font=FONT_SMALL,
                 bg=CARD, fg=SUBTEXT).pack(anchor="w")
        self.q_due = tk.Entry(right, font=FONT_BODY, bg=BG, fg=TEXT,
                               insertbackground=TEXT, relief="flat")
        self.q_due.pack(fill="x", ipady=6, pady=(2, 12))

        ActionButton(right, "➕ Add Task", GREEN, self._quick_add).pack(fill="x", ipady=4)

        tk.Frame(right, bg=BG, height=8).pack()

        ActionButton(right, "📋 View All Tasks", BLUE,
                     self.app.show_tasks).pack(fill="x", ipady=4)

    def _quick_add(self):
        title = self.q_title.get().strip()
        if not title:
            messagebox.showwarning("Required", "Please enter a task title.")
            return
        tasks = load_tasks()
        tasks.append({
            "id":       get_next_id(tasks),
            "title":    title,
            "due":      self.q_due.get().strip(),
            "priority": self.q_prio.get(),
            "done":     False,
            "notes":    "",
            "created":  datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
        save_tasks(tasks)
        messagebox.showinfo("✅ Added", f'Task "{title}" added successfully!')
        self.app.show_dashboard()   # Refresh
