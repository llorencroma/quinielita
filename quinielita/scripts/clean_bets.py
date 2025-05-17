import sqlite3
import os

DB_PATH = "../data/quinielita.db"

def borrar_apuestas():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM apuestas")
        cursor.execute("UPDATE temas SET bote_total = 0")
        conn.commit()
        conn.close()

if __name__ == "__main__":
    borrar_apuestas()