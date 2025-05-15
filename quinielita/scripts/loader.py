import sqlite3
import os

DB_PATH = "data/quinielita.db"

def cargar_tema_llorara_novio():
    if not os.path.exists(DB_PATH):
        print("❌ La base de datos no existe. Ejecuta primero init_db().")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verificar si el tema ya existe
    cursor.execute("SELECT id FROM temas WHERE nombre = ?", ("¿Llorará el Novio?",))
    existing = cursor.fetchone()
    if existing:
        print("✅ El tema ya existe. No se insertó nada.")
        return

    # Crear tema
    cursor.execute("""
        INSERT INTO temas (nombre, descripcion, bote_total, modo)
        VALUES (?, ?, ?, ?)
    """, (
        "¿Llorará el Novio?",
        "Apuesta si el novio se emocionará hasta llorar durante la ceremonia.",
        0,
        "cerrada"
    ))
    tema_id = cursor.lastrowid

    # Insertar opciones cerradas
    opciones = ["Sí", "No"]
    for opcion in opciones:
        cursor.execute("""
            INSERT INTO opciones_apuesta (tema_id, descripcion, monto_total)
            VALUES (?, ?, 0)
        """, (tema_id, opcion))

    conn.commit()
    conn.close()
    print("✅ Tema '¿Llorará el Novio?' creado con opciones: Sí / No")

if __name__ == "__main__":
    cargar_tema_llorara_novio()
