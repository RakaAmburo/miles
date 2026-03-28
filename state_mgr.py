import sqlite3

DB = "state.db"

def set_state(key: str, value: str):
    with sqlite3.connect(DB) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS state (key TEXT PRIMARY KEY, value TEXT)")
        conn.execute("INSERT OR REPLACE INTO state VALUES (?, ?)", (key, value))

def get_state(key: str) -> str:
    with sqlite3.connect(DB) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS state (key TEXT PRIMARY KEY, value TEXT)")
        row = conn.execute("SELECT value FROM state WHERE key = ?", (key,)).fetchone()
        return row[0] if row else None

# uso
set_state("alarm", "ON")
print(get_state("alarm"))  # ON