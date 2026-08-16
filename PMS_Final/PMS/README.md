# 📋 Software Personal Management System
**Python Desktop Application | Tkinter GUI**

---

## 🗂️ Project Structure

```
PMS/
│
├── main.py                  ← Entry point — run this file
│
├── modules/
│   ├── __init__.py          ← Package marker
│   ├── config.py            ← Colors, fonts, file paths, constants
│   ├── database.py          ← JSON read/write utility functions
│   ├── widgets.py           ← Reusable custom UI components
│   ├── app.py               ← Main window + sidebar navigation
│   ├── dashboard.py         ← Dashboard page (stats + quick-add)
│   ├── tasks.py             ← Task Manager page (full CRUD)
│   ├── notes.py             ← Notes Manager page (full CRUD)
│   └── contacts.py          ← Contacts Manager page (full CRUD)
│
├── data/                    ← Auto-created on first run
│   ├── tasks.json
│   ├── notes.json
│   └── contacts.json
│
└── README.md
```

---

## 🚀 How to Run in VSCode

### Prerequisites
- Python 3.8 or higher
- No external libraries needed (uses built-in `tkinter`, `json`, `os`)

### Steps
1. Open the `PMS` folder in VSCode: `File → Open Folder`
2. Open the integrated terminal: `Ctrl + ~`
3. Run:
   ```bash
   python main.py
   ```

---

## ✨ Features

### 🏠 Dashboard
- Summary statistics cards (tasks, notes, contacts)
- Recent 6 tasks with status and priority
- Quick-add task widget

### ✅ Task Manager
- Add, Edit, Delete tasks
- Mark tasks as Done / Undo
- Priority levels: Low / Medium / High (color-coded)
- Filter: All / Pending / Completed / High Priority
- Search by title
- Sort by any column (click header)
- Due date tracking
- Per-task notes field
- Double-click to edit

### 📝 Notes Manager
- Split-pane: note list + rich text editor
- Create, Edit, Delete notes
- Category tagging
- Search by title or content
- Character count
- Undo/Redo in editor

### 👤 Contacts Manager
- Add, Edit, Delete contacts
- Fields: Name, Email, Phone, Address, Company, Category
- Categories: Family / Friend / Colleague / Client / Other
- Search by name, email, or phone
- Filter by category
- One-click copy email to clipboard
- Double-click to edit

---

## 💾 Data Storage
All data is saved automatically as JSON files in the `data/` folder.
Data persists between sessions. No database setup required.

---

## 🎨 Design
- Dark theme (Catppuccin Mocha color palette)
- Responsive sidebar navigation
- Color-coded priority and status indicators
- Real-time clock in sidebar
