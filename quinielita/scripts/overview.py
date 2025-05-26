import sqlite3


DB_PATH = "../data/quinielita.db"

def print_db_overview():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("📋 Tables in the Database:\n")

    # Get table names (excluding SQLite internal tables)
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
    """)
    tables = cursor.fetchall()

    for (table_name,) in tables:
        print(f"🔹 Table: {table_name}")

        # Get row count
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"   Rows: {count}")
        except Exception as e:
            print(f"   Could not count rows: {e}")

        # Get column definitions
        try:
            cursor.execute(f"PRAGMA table_info({table_name})")
            cols = cursor.fetchall()
            print("   Columns:")
            for col in cols:
                print(f"      - {col[1]} ({col[2]})")
        except Exception as e:
            print(f"   Could not fetch columns: {e}")

        print("-" * 40)

    conn.close()

# Run it
if __name__ == "__main__":
    print_db_overview()
