import sqlite3

DB_NAME = "shipment.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shipments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            receiver TEXT NOT NULL,
            source TEXT NOT NULL,
            destination TEXT NOT NULL,
            weight REAL NOT NULL,
            eta TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_user(name, email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users(name, email, password) VALUES (?, ?, ?)", 
                   (name, email, password))
    conn.commit()
    conn.close()

def get_user(email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", 
                   (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

def add_shipment(sender, receiver, source, destination, weight, eta):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO shipments(sender, receiver, source, destination, weight, eta)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (sender, receiver, source, destination, weight, eta))
    conn.commit()
    conn.close()

def get_all_shipments():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shipments")
    shipments = cursor.fetchall()
    conn.close()
    return shipments

def get_shipment_by_id(shipment_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shipments WHERE id = ?", (shipment_id,))
    shipment = cursor.fetchone()
    conn.close()
    return shipment

def update_shipment(shipment_id, sender, receiver, source, destination, weight):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE shipments
        SET sender = ?, receiver = ?, source = ?, destination = ?, weight = ?
        WHERE id = ?
    """, (sender, receiver, source, destination, weight, shipment_id))
    conn.commit()
    conn.close()

def delete_shipment(shipment_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM shipments WHERE id = ?", (shipment_id,))
    conn.commit()
    conn.close()