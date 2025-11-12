import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "eta.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS eta_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            distance_km REAL NOT NULL,
            actual_days INTEGER NOT NULL,
            priority TEXT NOT NULL CHECK(priority IN ('standard','express','overnight')),
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def list_history():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, distance_km, actual_days, priority, notes, created_at
        FROM eta_history ORDER BY id DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_history(hid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, distance_km, actual_days, priority, notes, created_at FROM eta_history WHERE id = ?", (hid,))
    row = cur.fetchone()
    conn.close()
    return row

def create_history(distance_km: float, actual_days: int, priority: str, notes: str = None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO eta_history (distance_km, actual_days, priority, notes)
        VALUES (?, ?, ?, ?)
    """, (float(distance_km), int(actual_days), priority, notes))
    conn.commit()
    rid = cur.lastrowid
    conn.close()
    return rid

def update_history(hid: int, distance_km: float, actual_days: int, priority: str, notes: str = None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE eta_history SET distance_km = ?, actual_days = ?, priority = ?, notes = ?
        WHERE id = ?
    """, (float(distance_km), int(actual_days), priority, notes, hid))
    conn.commit()
    conn.close()

def delete_history(hid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM eta_history WHERE id = ?", (hid,))
    conn.commit()
    conn.close()