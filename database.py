# database.py
import sqlite3
from datetime import datetime

DB_NAME = "achizitii.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Tabela pentru achiziții
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS achizitii (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nume_produs TEXT NOT NULL,
            pret_produs REAL NOT NULL,
            date_created TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 🔥 Nou: Tabela pentru buget lunar
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buget (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            valoare REAL NOT NULL
        )
    ''')

    # Asigurăm că avem un rând inițial dacă nu există
    cursor.execute('INSERT OR IGNORE INTO buget (id, valoare) VALUES (1, 2000.0)')

    conn.commit()
    conn.close()

def get_buget():
    conn =sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT valoare FROM buget WHERE id = 1')
    valoare = cursor.fetchone()[0]
    conn.close()
    return valoare

def update_buget(nou_buget):
    conn =sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE buget SET valoare = ? WHERE id = 1', (nou_buget,)) #schimbam valoarea 
    conn.commit()
    conn.close()


def get_all_achizitii(limit=5):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nume_produs, pret_produs, date_created
        FROM achizitii
        ORDER BY date_created DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_achizitii_pe_luna(luna: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nume_produs, pret_produs, date_created
        FROM achizitii
        WHERE strftime('%m', date_created) = ?
        ORDER BY date_created DESC
    """, (luna,))
    rows = cursor.fetchall()
    conn.close()
    return rows



def add_achizitie(nume_produs: str, pret_produs: float):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO achizitii (nume_produs, pret_produs, date_created) VALUES (?, ?, datetime('now'))",
                   (nume_produs, pret_produs))
    conn.commit()
    conn.close()

