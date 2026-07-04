from pathlib import Path
import sqlite3
DB_PATH=Path("database/local_rag.db")
def get_connection():
    conn=sqlite3.connect(DB_PATH)
    conn.row_factory=sqlite3.Row
    return conn
def initialize_database():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""
        Create table if not exists chats(
            id TEXT PRIMARY KEY,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
    cursor.execute("""
        Create table if not exists messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT,
            role TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    cursor.execute("""Create table if not exists documents(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   chat_id TEXT,
                   document_id TEXT,
                   filename TEXT)""")
    conn.commit()
    conn.close()