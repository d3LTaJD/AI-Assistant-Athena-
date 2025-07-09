"""
Database handler for AI Assistant
"""
import sqlite3
import bcrypt
import json
from datetime import datetime
from pathlib import Path
from config import config

class DatabaseManager:
    def __init__(self):
        self.db_path = config.db_dir / "assistant.db"
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                assistant_name TEXT DEFAULT 'Assistant',
                voice_preference TEXT DEFAULT 'female',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Chat history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                prompt TEXT NOT NULL,
                response TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # File aliases table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_aliases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                alias TEXT NOT NULL,
                path TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                setting_key TEXT NOT NULL,
                setting_value TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, email, password, assistant_name="Assistant", voice_preference="female"):
        """Create a new user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Hash password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            cursor.execute('''
                INSERT INTO users (email, password_hash, assistant_name, voice_preference)
                VALUES (?, ?, ?, ?)
            ''', (email, password_hash, assistant_name, voice_preference))
            
            user_id = cursor.lastrowid
            conn.commit()
            return user_id
        except sqlite3.IntegrityError:
            return None  # User already exists
        finally:
            conn.close()
    
    def authenticate_user(self, email, password):
        """Authenticate user login"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, password_hash, assistant_name FROM users WHERE email = ?', (email,))
        result = cursor.fetchone()
        
        if result and bcrypt.checkpw(password.encode('utf-8'), result[1]):
            # Update last login
            cursor.execute('UPDATE users SET last_login = ? WHERE id = ?', 
                         (datetime.now(), result[0]))
            conn.commit()
            conn.close()
            return {"id": result[0], "assistant_name": result[2]}
        
        conn.close()
        return None
    
    def save_chat_history(self, user_id, prompt, response):
        """Save chat interaction to history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO chat_history (user_id, prompt, response)
            VALUES (?, ?, ?)
        ''', (user_id, prompt, response))
        
        conn.commit()
        conn.close()
    
    def get_chat_history(self, user_id, limit=50):
        """Get user's chat history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT prompt, response, timestamp FROM chat_history
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (user_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def add_file_alias(self, user_id, alias, path):
        """Add file/folder alias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO file_aliases (user_id, alias, path)
            VALUES (?, ?, ?)
        ''', (user_id, alias.lower(), path))
        
        conn.commit()
        conn.close()
    
    def get_file_aliases(self, user_id):
        """Get user's file aliases"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT alias, path FROM file_aliases WHERE user_id = ?', (user_id,))
        results = cursor.fetchall()
        conn.close()
        return dict(results)

# Global database instance
db = DatabaseManager()