import sqlite3
import json

DB_PATH = "chat_memory.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS history (
                sender_id TEXT PRIMARY KEY,
                messages TEXT
            )
        """)
    conn.close()

def get_chat_history(sender_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT messages FROM history WHERE sender_id = ?", (sender_id,))
        row = cursor.fetchone()
        if row:
            return json.loads(row[0])
    return []

def save_chat_history(sender_id, messages):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO history (sender_id, messages) VALUES (?, ?)
            ON CONFLICT(sender_id) DO UPDATE SET messages = excluded.messages
        """, (sender_id, json.dumps(messages)))