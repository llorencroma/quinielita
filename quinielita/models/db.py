import sqlite3
import os

DB_PATH = "data/quinielita.db"

def get_connection() -> sqlite3.Connection:
    """Provides a thread-safe DB connection for Streamlit."""
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db() -> None:
    """Initializes database schema and applies light migrations."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()

    # --- TEMAS table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            descripcion TEXT,
            bote_total REAL DEFAULT 0,
            correct_answer TEXT,
            modo TEXT DEFAULT 'cerrada'  -- 'cerrada', 'combinacion', or 'abierta'
        )
    """)


    # --- OPCIONES_APUESTA table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS opciones_apuesta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tema_id INTEGER,
            descripcion TEXT,
            monto_total REAL DEFAULT 0
        )
    """)

    # Unique index for upserts (required for combination/text-based themes)
    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_opcion_unica
        ON opciones_apuesta (tema_id, descripcion)
    """)

    # --- APUESTAS table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS apuestas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tema_id INTEGER,
            nombre TEXT,
            telefono TEXT,
            pin TEXT,
            detalle_apuesta TEXT,
            monto REAL,
            estado TEXT DEFAULT 'no validado',
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS winners (
                tema_id INTEGER PRIMARY KEY,
                ganador TEXT,
                FOREIGN KEY (tema_id) REFERENCES temas(id)
            )
    ''')

    conn.commit()
    conn.close()
