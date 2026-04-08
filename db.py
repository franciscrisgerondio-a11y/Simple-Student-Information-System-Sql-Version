import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "student_directory.db"


# ─────────────────────────────────────────────────────────────────────────────
# Connection
# ─────────────────────────────────────────────────────────────────────────────

def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


# ─────────────────────────────────────────────────────────────────────────────
# Schema
# ─────────────────────────────────────────────────────────────────────────────

def init_db():
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS college (
                code TEXT PRIMARY KEY,
                name TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS program (
                code    TEXT PRIMARY KEY,
                name    TEXT NOT NULL,
                college TEXT REFERENCES college(code) ON DELETE SET NULL ON UPDATE CASCADE
            );

            CREATE TABLE IF NOT EXISTS student (
                id        TEXT PRIMARY KEY,
                firstname TEXT NOT NULL,
                lastname  TEXT NOT NULL,
                course    TEXT REFERENCES program(code) ON DELETE SET NULL ON UPDATE CASCADE,
                year      INTEGER NOT NULL CHECK(year BETWEEN 1 AND 4),
                gender    TEXT NOT NULL CHECK(gender IN ('Male','Female','Other'))
            );
        """)


# ─────────────────────────────────────────────────────────────────────────────
# Stats
# ─────────────────────────────────────────────────────────────────────────────

def get_stats() -> dict:
    with get_connection() as conn:
        return {
            "students":   conn.execute("SELECT COUNT(*) FROM student").fetchone()[0],
            "programs":   conn.execute("SELECT COUNT(*) FROM program").fetchone()[0],
            "colleges":   conn.execute("SELECT COUNT(*) FROM college").fetchone()[0],
            "unassigned": conn.execute(
                "SELECT COUNT(*) FROM student WHERE course IS NULL"
            ).fetchone()[0],
        }


# ─────────────────────────────────────────────────────────────────────────────
# COLLEGE
# ─────────────────────────────────────────────────────────────────────────────

def get_colleges(search="", sort_col="name", sort_asc=True, page=1, per_page=10):
    col_map = {"Code": "code", "Name": "name", "CODE": "code", "NAME": "name"}
    order   = col_map.get(sort_col, "name")
    dir_    = "ASC" if sort_asc else "DESC"
    like    = f"%{search}%"
    offset  = (page - 1) * per_page

    with get_connection() as conn:
        total = conn.execute(
            "SELECT COUNT(*) FROM college WHERE code LIKE ? OR name LIKE ?",
            (like, like)
        ).fetchone()[0]
        rows = conn.execute(
            f"SELECT code, name FROM college WHERE code LIKE ? OR name LIKE ? "
            f"ORDER BY {order} {dir_} LIMIT ? OFFSET ?",
            (like, like, per_page, offset)
        ).fetchall()
    return [dict(r) for r in rows], total


def get_all_colleges() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("SELECT code, name FROM college ORDER BY name").fetchall()
    return [dict(r) for r in rows]


def college_exists(code: str) -> bool:
    with get_connection() as conn:
        return conn.execute(
            "SELECT 1 FROM college WHERE code = ?", (code,)
        ).fetchone() is not None


def add_college(code: str, name: str):
    with get_connection() as conn:
        conn.execute("INSERT INTO college (code, name) VALUES (?, ?)", (code, name))


def update_college(code: str, name: str):
    with get_connection() as conn:
        conn.execute("UPDATE college SET name = ? WHERE code = ?", (name, code))


def delete_college(code: str):
    """Cascade: nullify students whose program belongs to this college, delete programs, delete college."""
    with get_connection() as conn:
        progs = [r["code"] for r in conn.execute(
            "SELECT code FROM program WHERE college = ?", (code,)
        ).fetchall()]
        for pc in progs:
            conn.execute("UPDATE student SET course = NULL WHERE course = ?", (pc,))
        conn.execute("DELETE FROM program WHERE college = ?", (code,))
        conn.execute("DELETE FROM college WHERE code = ?", (code,))


# ─────────────────────────────────────────────────────────────────────────────
# PROGRAM
# ─────────────────────────────────────────────────────────────────────────────

def get_programs(search="", sort_col="name", sort_asc=True, page=1, per_page=10):
    col_map = {"Code": "p.code", "Name": "p.name", "College": "p.college",
               "CODE": "p.code", "NAME": "p.name", "COLLEGE": "p.college"}
    order   = col_map.get(sort_col, "p.name")
    dir_    = "ASC" if sort_asc else "DESC"
    like    = f"%{search}%"
    offset  = (page - 1) * per_page

    with get_connection() as conn:
        total = conn.execute(
            "SELECT COUNT(*) FROM program p WHERE p.code LIKE ? OR p.name LIKE ? OR p.college LIKE ?",
            (like, like, like)
        ).fetchone()[0]
        rows = conn.execute(
            f"SELECT p.code, p.name, p.college FROM program p "
            f"WHERE p.code LIKE ? OR p.name LIKE ? OR p.college LIKE ? "
            f"ORDER BY {order} {dir_} LIMIT ? OFFSET ?",
            (like, like, like, per_page, offset)
        ).fetchall()
    return [dict(r) for r in rows], total


def get_all_programs() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT code, name, college FROM program ORDER BY code"
        ).fetchall()
    return [dict(r) for r in rows]


def get_programs_for_college(college_code: str) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT code, name FROM program WHERE college = ? ORDER BY code",
            (college_code,)
        ).fetchall()
    return [dict(r) for r in rows]


def program_exists(code: str) -> bool:
    with get_connection() as conn:
        return conn.execute(
            "SELECT 1 FROM program WHERE code = ?", (code,)
        ).fetchone() is not None


def add_program(code: str, name: str, college: str):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO program (code, name, college) VALUES (?, ?, ?)",
            (code, name, college)
        )


def update_program(code: str, name: str, college: str):
    with get_connection() as conn:
        conn.execute(
            "UPDATE program SET name = ?, college = ? WHERE code = ?",
            (name, college, code)
        )


def delete_program(code: str):
    with get_connection() as conn:
        conn.execute("UPDATE student SET course = NULL WHERE course = ?", (code,))
        conn.execute("DELETE FROM program WHERE code = ?", (code,))


# ─────────────────────────────────────────────────────────────────────────────
# STUDENT
# ─────────────────────────────────────────────────────────────────────────────

def get_students(search="", sort_col="id", sort_asc=True, page=1, per_page=10,
                 course_filter="", year_filter="", gender_filter=""):
    col_map = {
        # Original keys
        "ID": "s.id", "First Name": "s.firstname", "Last Name": "s.lastname",
        "Course": "s.course", "Year": "s.year", "Gender": "s.gender",
        # Uppercase header keys (EduTrack design)
        "STUDENT ID": "s.id", "FIRST NAME": "s.firstname", "LAST NAME": "s.lastname",
        "COURSE": "s.course", "YEAR": "s.year", "GENDER": "s.gender",
        # Stripped versions
        "id": "s.id", "firstname": "s.firstname", "lastname": "s.lastname",
        "course": "s.course", "year": "s.year", "gender": "s.gender",
    }
    order  = col_map.get(sort_col, "s.id")
    dir_   = "ASC" if sort_asc else "DESC"
    like   = f"%{search}%"
    offset = (page - 1) * per_page

    # Build filter clauses
    filters = [
        "s.id LIKE ? OR s.firstname LIKE ? OR s.lastname LIKE ? "
        "OR s.course LIKE ? OR s.gender LIKE ?"
    ]
    params_base = [like] * 5

    if course_filter:
        filters.append("s.course = ?")
        params_base.append(course_filter)
    if year_filter:
        filters.append("s.year = ?")
        params_base.append(int(year_filter))
    if gender_filter:
        filters.append("s.gender = ?")
        params_base.append(gender_filter)

    where = " AND ".join(f"({f})" for f in filters)

    with get_connection() as conn:
        total = conn.execute(
            f"SELECT COUNT(*) FROM student s WHERE {where}",
            params_base
        ).fetchone()[0]
        rows = conn.execute(
            f"SELECT s.id, s.firstname, s.lastname, "
            f"COALESCE(s.course, 'NULL') AS course, s.year, s.gender "
            f"FROM student s WHERE {where} "
            f"ORDER BY {order} {dir_} LIMIT ? OFFSET ?",
            params_base + [per_page, offset]
        ).fetchall()
    return [dict(r) for r in rows], total


def student_exists(id_: str) -> bool:
    with get_connection() as conn:
        return conn.execute(
            "SELECT 1 FROM student WHERE id = ?", (id_,)
        ).fetchone() is not None


def add_student(id_: str, firstname: str, lastname: str,
                course: str | None, year: int, gender: str):
    val = None if not course or course == "NULL" else course
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO student (id, firstname, lastname, course, year, gender) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (id_, firstname, lastname, val, year, gender)
        )


def update_student(id_: str, firstname: str, lastname: str,
                   course: str | None, year: int, gender: str):
    val = None if not course or course == "NULL" else course
    with get_connection() as conn:
        conn.execute(
            "UPDATE student SET firstname=?, lastname=?, course=?, year=?, gender=? "
            "WHERE id=?",
            (firstname, lastname, val, year, gender, id_)
        )


def delete_student(id_: str):
    with get_connection() as conn:
        conn.execute("DELETE FROM student WHERE id = ?", (id_,))


# ─────────────────────────────────────────────────────────────────────────────
# DASHBOARD ANALYTICS
# ─────────────────────────────────────────────────────────────────────────────

def get_top_courses(limit: int = 8) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT course AS code, COUNT(*) AS n FROM student "
            "WHERE course IS NOT NULL GROUP BY course ORDER BY n DESC LIMIT ?",
            (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


def get_gender_distribution() -> dict:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT gender, COUNT(*) AS n FROM student GROUP BY gender"
        ).fetchall()
    return {r["gender"]: r["n"] for r in rows}


def get_year_distribution() -> dict:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT year, COUNT(*) AS n FROM student GROUP BY year ORDER BY year"
        ).fetchall()
    return {r["year"]: r["n"] for r in rows}


def get_top_colleges(limit: int = 5) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT p.college AS code, COUNT(*) AS n FROM student s "
            "JOIN program p ON s.course = p.code "
            "GROUP BY p.college ORDER BY n DESC LIMIT ?",
            (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


def get_enrollment_trend() -> list[dict]:
    """Count students per enrollment year (first 4 chars of ID)."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT SUBSTR(id,1,4) AS yr, COUNT(*) AS n "
            "FROM student GROUP BY yr ORDER BY yr"
        ).fetchall()
    return [dict(r) for r in rows]


def get_grad_rate() -> float:
    """Year 4 students as percentage of total (proxy for grad rate)."""
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM student").fetchone()[0]
        yr4   = conn.execute(
            "SELECT COUNT(*) FROM student WHERE year=4"
        ).fetchone()[0]
    return round(yr4 / total * 100, 1) if total else 0.0
