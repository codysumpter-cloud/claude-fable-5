import sqlite3
from typing import List, Tuple

class LocalProjectVault:
    def __init__(self, db_name: str = "vault_storage.db"):
        """
        Initializes the local SQLite database for local-only storage 
        of sessions, history, and workspace structures.
        """
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        """Creates the necessary tables if they do not exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    workspace TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    prompt TEXT NOT NULL,
                    response TEXT NOT NULL
                )
            """)
            conn.commit()

    def save_session(self, workspace: str, prompt: str, response: str):
        """Saves a prompt-response pair tied to a specific local workspace."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sessions (workspace, prompt, response) VALUES (?, ?, ?)",
                (workspace, prompt, response)
            )
            conn.commit()

    def search_vault(self, query: str) -> List[Tuple]:
        """Performs a full-text search across all past local sessions."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT workspace, timestamp, prompt, response FROM sessions WHERE prompt LIKE ? OR response LIKE ?",
                (f"%{query}%", f"%{query}%")
            )
            return cursor.fetchall()
