import eel
import sqlite3
import subprocess
import tempfile
import os
import re

eel.init("web")

session_registered = False

def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mobile TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@eel.expose
def is_session_registered():
    global session_registered
    return session_registered

@eel.expose
def save_user(name, mobile):
    global session_registered

    if not name or name.strip() == "":
        return "Name is required"

    if not re.fullmatch(r"[0-9]{10}", mobile):
        return "Mobile number must be exactly 10 digits"

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, mobile) VALUES (?, ?)",
        (name.strip(), mobile)
    )
    conn.commit()
    conn.close()

    session_registered = True
    return "SUCCESS"

@eel.expose
def run_code(code):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp:
        temp.write(code.encode())
        fname = temp.name

    try:
        result = subprocess.run(
            ["python", fname],
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout + result.stderr
    finally:
        os.remove(fname)

    return output

init_db()
eel.start("user.html", size=(900, 600))
