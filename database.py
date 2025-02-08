import sqlite3

# Initialize database
def init_db():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            name TEXT PRIMARY KEY,
            quantity INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()
