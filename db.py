import sqlite3
from datetime import datetime

DB = "olx.db"

def connect():
    return sqlite3.connect(DB)

def init_db():
    with connect() as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS offers (
            id TEXT PRIMARY KEY,
            title TEXT,
            price INTEGER,
            url TEXT,
            last_seen TEXT
        )
        """)

def upsert_offer(offer):
    now = datetime.now().isoformat()

    with connect() as con:
        cur = con.execute(
            "SELECT price FROM offers WHERE id = ?",
            (offer["id"],)
        )
        row = cur.fetchone()

        if row is None:
            # Oferta nie istnieje – wstaw nową
            con.execute(
                "INSERT INTO offers VALUES (?, ?, ?, ?, ?)",
                (offer["id"], offer["title"], offer["price"], offer["url"], now)
            )
        else:
            old_price = row[0]
            if old_price != offer["price"]:
                # Cena się zmieniła – nadpisujemy
                con.execute(
                    "UPDATE offers SET title=?, price=?, last_seen=? WHERE id=?",
                    (offer["title"], offer["price"], now, offer["id"])
                )
            else:
                # Cena taka sama – aktualizujemy tylko last_seen
                con.execute(
                    "UPDATE offers SET last_seen=? WHERE id=?",
                    (now, offer["id"])
                )
