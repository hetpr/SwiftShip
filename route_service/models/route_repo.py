import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "routes.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            destination TEXT NOT NULL,
            distance_km INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def list_routes():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, source, destination, distance_km FROM routes ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_route(route_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, source, destination, distance_km FROM routes WHERE id = ?", (route_id,))
    row = cur.fetchone()
    conn.close()
    return row

def create_route(source: str, destination: str, distance_km: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO routes (source, destination, distance_km) VALUES (?, ?, ?)",
        (source.title(), destination.title(), int(distance_km))
    )
    conn.commit()
    rid = cur.lastrowid
    conn.close()
    return rid

def update_route(route_id: int, source: str, destination: str, distance_km: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE routes SET source = ?, destination = ?, distance_km = ? WHERE id = ?",
        (source.title(), destination.title(), int(distance_km), route_id)
    )
    conn.commit()
    conn.close()

def delete_route(route_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM routes WHERE id = ?", (route_id,))
    conn.commit()
    conn.close()

def load_graph_from_db():
    """
    Returns an undirected adjacency map: { city: {neighbor: distance, ...}, ... }
    """
    graph = {}
    for _, src, dst, dist in list_routes():
        dist = int(dist)
        graph.setdefault(src, {})[dst] = dist
        graph.setdefault(dst, {})[src] = dist
    return graph