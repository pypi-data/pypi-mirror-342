import sqlite3
import json
from typing import Optional, Any, Dict
from pathlib import Path

class CommandDB:
    def __init__(self, db_path: str = "commands.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database and create tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create commands table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS commands (
            command_id TEXT PRIMARY KEY,
            command_name TEXT NOT NULL,
            command_payload TEXT NOT NULL,
            result TEXT,
            error TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()

    def save_command(self, command_id: str, command_name: str, 
                    command_payload: Dict[str, Any], 
                    result: Optional[Dict[str, Any]] = None,
                    error: Optional[str] = None):
        """Save a command execution record to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT OR REPLACE INTO commands 
        (command_id, command_name, command_payload, result, error)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            command_id,
            command_name,
            json.dumps(command_payload),
            json.dumps(result) if result else None,
            error
        ))
        
        conn.commit()
        conn.close()

    def get_command(self, command_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a command execution record from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT command_name, command_payload, result, error
        FROM commands
        WHERE command_id = ?
        ''', (command_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            command_name, command_payload, result, error = row
            return {
                "command_name": command_name,
                "command_payload": json.loads(command_payload),
                "result": json.loads(result) if result else None,
                "error": error
            }
        return None 