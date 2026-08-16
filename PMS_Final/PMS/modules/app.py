
import tkinter as tk
from datetime import datetime
from modules.config import *
from modules.widgets import apply_treeview_style


class PersonalManagementSystem(tk.Tk):
    """Root application window with sidebar + content area."""

    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry(WINDOW_SIZE)
        self.minsize(900, 600)
        self.configure(bg=BG)

        apply_treeview_style()

        self.current_frame = None
        self._active_btn   = None

        self._build_sidebar()
        self._build_content_area()

        # Load dashboard by default
        self.show_dashboard()

    # ── Sidebar ────────────────────────────────────────────────
    def _build_sidebar(self):
        self.sidebar = tk.Frame(self, bg=SIDEBAR, width=210)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo / App name
        logo_frame = tk.Frame(self.sidebar, bg=SIDEBAR)
        logo_frame.pack(fill="x", pady=(30, 20))
        tk.Label(logo_frame, text="📋", font=("Segoe UI", 32),
                 bg=SIDEBAR, fg=ACCENT).pack()
        tk.Label(logo_frame, text=APP_NAME, font=("Segoe UI", 11, "bold"),
                 bg=SIDEBAR, fg=TEXT, wraplength=160, justify="center").pack()
        tk.Label(logo_frame, text=f"v{APP_VERSION}", font=FONT_SMALL,
                 bg=SIDEBAR, fg=SUBTEXT).pack()

        # Divider
        tk.Frame(self.sidebar, bg=CARD, height=1).pack(fill="x", padx=15, pady=5)

        # Navigation buttons
        nav_items = [
            ("🏠  Dashboard",  self.show_dashboard),
            ("✅  Tasks",       self.show_tasks),
            ("📝  Notes",       self.show_notes),
            ("👤  Contacts",    self.show_contacts),
        ]
        self._nav_btns = {}
        for label, cmd in nav_items:
            btn = tk.Button(
                self.sidebar, text=label,
                font=FONT_BODY, bg=SIDEBAR, fg=TEXT,
                activebackground=CARD, activeforeground=ACCENT,
                relief="flat", anchor="w", padx=22, pady=8,
                cursor="hand2", command=lambda c=cmd, b=label: self._navigate(c, b)
            )
            btn.pack(fill="x")
            self._nav_btns[label] = btn

        # Clock at bottom
        self.clock_lbl = tk.Label(self.sidebar, text="", font=FONT_SMALL,
                                   bg=SIDEBAR, fg=SUBTEXT, justify="center")
        self.clock_lbl.pack(side="bottom", pady=20)
        self._update_clock()

    def _update_clock(self):
        now = datetime.now()
        self.clock_lbl.config(
            text=f"📅 {now.strftime('%d %b %Y')}\n🕐 {now.strftime('%H:%M:%S')}"
        )
        self.after(1000, self._update_clock)

    def _navigate(self, cmd, label):
        # Highlight active nav button
        for lbl, btn in self._nav_btns.items():
            if lbl == label:
                btn.config(bg=CARD, fg=ACCENT)
            else:
                btn.config(bg=SIDEBAR, fg=TEXT)
        cmd()

    # ── Content Area ───────────────────────────────────────────
    def _build_content_area(self):
        self.content = tk.Frame(self, bg=BG)
        self.content.pack(side="right", fill="both", expand=True)

    def _switch_page(self, FrameClass):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = FrameClass(self.content, self)
        self.current_frame.pack(fill="both", expand=True)

    # ── Page Loaders ───────────────────────────────────────────
    def show_dashboard(self):
        from modules.dashboard import DashboardPage
        self._switch_page(DashboardPage)

    def show_tasks(self):
        from modules.tasks import TasksPage
        self._switch_page(TasksPage)

    def show_notes(self):
        from modules.notes import NotesPage
        self._switch_page(NotesPage)

    def show_contacts(self):
        from modules.contacts import ContactsPage
        self._switch_page(ContactsPage)
