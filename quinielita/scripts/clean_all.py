import sqlite3
from models.db import DB_PATH

DB_PATH = "../data/quinielita.db"

def borrar_todos_los_temas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ⚠️ Borrar primero las dependencias
    cursor.execute("DELETE FROM apuestas")
    cursor.execute("DELETE FROM opciones_apuesta")
    cursor.execute("DELETE FROM temas")

    conn.commit()
    conn.close()
    print("✅ Todos los temas, apuestas y opciones han sido eliminados.")

if __name__ == "__main__":
    borrar_todos_los_temas()
