import sqlite3
from datetime import datetime
from pathlib import Path
from appdirs import user_data_dir
from typing import Optional, List, Dict, Any
import json

def get_db_path(app_name: str = "smai", db_name: str = "smai.db") -> Path:
    """Get the platform-specific database path."""
    data_dir = Path(user_data_dir(app_name))
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / db_name

DB_PATH = str(get_db_path())

def init_db(db_path: str = DB_PATH):
    """Initialize the SQLite database with required tables."""
    with sqlite3.connect(db_path) as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            output_type TEXT NOT NULL DEFAULT 'text',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        # Add index on created_at
        conn.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON conversations(created_at)')
        
        # Create api_keys table
        conn.execute('''
        CREATE TABLE IF NOT EXISTS api_keys (
            key_name TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

def save_conversation(conversation_id: str, data: Dict[str, Any], created_at: str, output_type: str = "text", db_path: str = DB_PATH) -> None:
    """Save a conversation to the database."""
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            'INSERT OR REPLACE INTO conversations (id, data, output_type, created_at) VALUES (?, ?, ?, datetime(?))',
            (conversation_id, json.dumps(data), output_type, created_at)
        )

def load_conversation(conversation_id: str, db_path: str = DB_PATH) -> Optional[Dict[str, Any]]:
    """Load a conversation from the database by ID."""
    with sqlite3.connect(db_path) as conn:
        result = conn.execute(
            'SELECT data FROM conversations WHERE id = ?',
            (conversation_id,)
        ).fetchone()
        
        if result:
            return json.loads(result[0])
        return None

def list_conversations(db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """List all conversations in the database."""
    with sqlite3.connect(db_path) as conn:
        results = conn.execute(
            'SELECT id, data FROM conversations ORDER BY created_at DESC'
        ).fetchall()
        
        return [
            {
                'id': row[0],
                **json.loads(row[1])
            }
            for row in results
        ]

def get_latest_conversation(db_path: str = DB_PATH, output_type: str = None) -> Optional[Dict[str, Any]]:
    """Get the most recent conversation from the database.
    
    Args:
        db_path: Path to the database file
        output_type: Filter by output type (text, image, audio)
    """
    with sqlite3.connect(db_path) as conn:
        query = 'SELECT id, data FROM conversations'
        params = []
        
        if output_type:
            query += ' WHERE output_type = ?'
            params.append(output_type)
            
        query += ' ORDER BY created_at DESC LIMIT 1'
        
        result = conn.execute(query, params).fetchone()
        
        if result:
            return {
                'id': result[0],
                **json.loads(result[1])
            }
        return None

def get_latest_text_conversation(db_path: str = DB_PATH) -> Optional[Dict[str, Any]]:
    """Get the most recent text conversation from the database."""
    return get_latest_conversation(db_path, output_type='text')

def add_api_key(key_name: str, db_path: str = DB_PATH) -> None:
    """Add an API key name to the database."""
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            'INSERT OR REPLACE INTO api_keys (key_name) VALUES (?)',
            (key_name,)
        )

def remove_api_key(key_name: str, db_path: str = DB_PATH) -> None:
    """Remove an API key name from the database."""
    with sqlite3.connect(db_path) as conn:
        conn.execute('DELETE FROM api_keys WHERE key_name = ?', (key_name,))

def get_api_keys(db_path: str = DB_PATH) -> List[str]:
    """Get all stored API key names from the database."""
    with sqlite3.connect(db_path) as conn:
        results = conn.execute('SELECT key_name FROM api_keys').fetchall()
        return [row[0] for row in results]

# Initialize the database when the module is imported
init_db()
