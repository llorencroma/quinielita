import sqlite3
DB_PATH = "../data/quinielita.db"

def display_all_data(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch all from TEMAS
    print("📘 TEMAS:")
    cursor.execute("SELECT * FROM temas")
    temas = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    print(" | ".join(colnames))
    for row in temas:
        print(" | ".join(str(cell) for cell in row))

    print("\n" + "="*60 + "\n")

    # Fetch all from APUESTAS
    print("🎲 APUESTAS:")
    cursor.execute("SELECT * FROM apuestas")
    apuestas = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    print(" | ".join(colnames))
    for row in apuestas:
        print(" | ".join(str(cell) for cell in row))

    print("\n" + "="*60 + "\n")

    print("📘 OPCIONES:")
    cursor.execute("SELECT * FROM opciones_apuesta")
    temas = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    print(" | ".join(colnames))
    for row in temas:
        print(" | ".join(str(cell) for cell in row))

    print("\n" + "="*60 + "\n")

    conn.close()

# 🔧 Usage
if __name__ == "__main__":
    display_all_data(DB_PATH)
