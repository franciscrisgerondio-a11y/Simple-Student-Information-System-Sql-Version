# 📚 Simple Student Information System (SSIS)

A Python PyQt6-based desktop application that manages **Students**, **Programs**, and **Colleges** using a local **SQLite database**.

---

## 🚀 Features

### 👨‍🎓 Student Management
* Add, Edit, Delete students
* Student ID format validation (`YYYY-NNNN`)
* Program selection filtered by selected College
* Pagination (10 records per page)
* Live search with keyword highlighting
* Filter by Course, Year Level, and Gender
* Duplicate ID prevention

### 🏫 College Management
* Add, Edit, Delete colleges
* Duplicate college code prevention
* Cascade delete:
  * Deletes all related programs
  * Sets affected students' course to `NULL`

### 🎓 Program Management
* Add, Edit, Delete programs
* Program selection filtered by College
* Duplicate program code prevention
* Cascade delete:
  * Deleting a program sets affected students' course to `NULL`

---

## 🗂 Data Storage (SQLite)

All data is stored in a single SQLite database file located at:

```
data/student_directory.db
```

### 🗃 Table: `college`
```sql
code  TEXT  PRIMARY KEY
name  TEXT  NOT NULL
```

### 🗃 Table: `program`
```sql
code     TEXT  PRIMARY KEY
name     TEXT  NOT NULL
college  TEXT  REFERENCES college(code) ON DELETE SET NULL ON UPDATE CASCADE
```

### 🗃 Table: `student`
```sql
id         TEXT     PRIMARY KEY
firstname  TEXT     NOT NULL
lastname   TEXT     NOT NULL
course     TEXT     REFERENCES program(code) ON DELETE SET NULL ON UPDATE CASCADE
year       INTEGER  NOT NULL  CHECK(year BETWEEN 1 AND 4)
gender     TEXT     NOT NULL  CHECK(gender IN ('Male', 'Female', 'Other'))
```

---

## 🔗 Data Relationships

The system enforces a relational structure:

* `Student.course` → references `Program.code`
* `Program.college` → references `College.code`

Foreign key enforcement is handled by SQLite with `PRAGMA foreign_keys = ON`.
Write-ahead logging is enabled via `PRAGMA journal_mode = WAL` for reliability.

---

## 📊 Sorting System

* Click any column header to sort
* Click again to toggle direction
* Sort indicators:
  * ▲ Ascending
  * ▼ Descending
* Sorting applies globally across all pages before pagination
* The **Actions** column is excluded from sorting

---

## 📄 Pagination

* 10 rows per page (default)
* Navigation controls:
  * `«` First page
  * `‹ Prev` Previous page
  * `Next ›` Next page
  * `»` Last page
* Record counter shows current range (e.g. `Showing 1–10 of 5,500 records`)
* Sorting and search apply globally before pagination

---

## 🔎 Search

* Real-time filtering as you type
* Case-insensitive
* Searches across: ID, First Name, Last Name, Course, Gender
* Keyword highlighting inside matching table cells

---

## 🛡 Data Integrity Rules

| Rule | Enforcement |
| ---- | ----------- |
| Student ID format `YYYY-NNNN` | Regex validation on save |
| No duplicate Student ID | Checked before insert |
| No duplicate Program Code | Checked before insert |
| No duplicate College Code | Checked before insert |
| Cannot edit primary keys | Fields disabled in edit mode |
| Year level range 1–4 | SQLite `CHECK` constraint |
| Gender restricted values | SQLite `CHECK` constraint |
| Cascade delete (College → Programs → Students) | SQLite FK + manual guard |
| Cascade delete (Program → Students) | SQLite `ON DELETE SET NULL` |

---

## 🎨 UI & Theming

* Custom-painted glassmorphism cards and sidebar
* **Dark mode** and **Light mode** toggle (bottom of sidebar)
* Animated hover effects on table rows and nav buttons
* Stat cards showing live counts: Total Students, Programs, Colleges, No-Course students
* All icons drawn programmatically (no external image assets)

---

## 🧠 Architecture

```
main.py       — Entry point
ui.py         — All PyQt6 widgets, views, and the main window
db.py         — All SQLite queries and database logic
dialogs.py    — Add/Edit dialogs for Students, Programs, and Colleges
theme.py      — QSS stylesheets for dark and light themes
data/
  student_directory.db  — Auto-created SQLite database
```

---

## ▶ How to Run

### Requirements
* Python 3.10+
* PyQt6

### Install dependencies
```bash
pip install PyQt6
```

### Launch
```bash
python main.py
```

The `data/` folder and SQLite database will be created automatically on first run.

---

## 💡 Design Decisions

* **SQLite over CSV** — enables real foreign key constraints, atomic transactions, and efficient paginated queries without loading all records into memory
* **WAL journal mode** — improves write reliability and allows concurrent reads
* **Parameterized queries throughout** — no raw string interpolation in SQL, preventing injection
* **Manual cascade in `delete_college`** — adds an explicit safety net on top of SQLite's FK cascade for the multi-step college → program → student nullification
* **Sorting implemented in SQL** — `ORDER BY` in the database query ensures sort applies globally before pagination, not just on the visible page
* **Programmatic icons** — all icons are drawn with `QPainter` paths, requiring no bundled image files

---

## 📌 Author Notes

This project demonstrates:

* Relational data management with SQLite and Python
* PyQt6 custom widget painting and theming
* Pagination with server-side sorting and search integration
* Dialog-based CRUD with validation and duplicate prevention
* Referential integrity via both SQLite FK constraints and application-level guards

---
