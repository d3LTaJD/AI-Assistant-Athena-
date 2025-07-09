"""
Database handler for AI Assistant
"""
import os
import json
from datetime import datetime
from pathlib import Path

class DatabaseManager:
    def __init__(self):
        self.db_dir = Path.home() / ".ai_assistant" / "database"
        self.db_dir.mkdir(parents=True, exist_ok=True)
        self.chat_history_file = self.db_dir / "chat_history.json"
        self.users_file = self.db_dir / "users.json"
        self.file_aliases_file = self.db_dir / "file_aliases.json"
        
        # Initialize database files
        self.init_database()
    
    def init_database(self):
        """Initialize database files"""
        # Chat history
        if not self.chat_history_file.exists():
            with open(self.chat_history_file, 'w') as f:
                json.dump([], f)
        
        # Users
        if not self.users_file.exists():
            with open(self.users_file, 'w') as f:
                json.dump([], f)
        
        # File aliases
        if not self.file_aliases_file.exists():
            with open(self.file_aliases_file, 'w') as f:
                json.dump({}, f)
    
    def create_user(self, email, password, assistant_name="Assistant", voice_preference="female"):
        """Create a new user"""
        try:
            # Load existing users
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            # Check if user already exists
            for user in users:
                if user.get('email') == email:
                    return None  # User already exists
            
            # Create new user
            user_id = len(users) + 1
            new_user = {
                "id": user_id,
                "email": email,
                "password_hash": password,  # In a real app, this would be hashed
                "assistant_name": assistant_name,
                "voice_preference": voice_preference,
                "created_at": datetime.now().isoformat(),
                "last_login": datetime.now().isoformat()
            }
            
            users.append(new_user)
            
            # Save updated users
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=2)
            
            return user_id
            
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def authenticate_user(self, email, password):
        """Authenticate user login"""
        try:
            # Load users
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            # Find user by email
            for user in users:
                if user.get('email') == email and user.get('password_hash') == password:
                    # Update last login
                    user['last_login'] = datetime.now().isoformat()
                    
                    # Save updated users
                    with open(self.users_file, 'w') as f:
                        json.dump(users, f, indent=2)
                    
                    return {
                        "id": user['id'],
                        "assistant_name": user.get('assistant_name', 'Assistant')
                    }
            
            return None  # Authentication failed
            
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None
    
    def save_chat_history(self, user_id, prompt, response):
        """Save chat interaction to history"""
        try:
            # Load existing history
            with open(self.chat_history_file, 'r') as f:
                history = json.load(f)
            
            # Add new entry
            history.append({
                "user_id": user_id,
                "prompt": prompt,
                "response": response,
                "timestamp": datetime.now().isoformat()
            })
            
            # Keep only last 1000 entries
            if len(history) > 1000:
                history = history[-1000:]
            
            # Save updated history
            with open(self.chat_history_file, 'w') as f:
                json.dump(history, f, indent=2)
                
        except Exception as e:
            print(f"Error saving chat history: {e}")
    
    def get_chat_history(self, user_id, limit=50):
        """Get user's chat history"""
        try:
            # Load history
            with open(self.chat_history_file, 'r') as f:
                history = json.load(f)
            
            # Filter by user_id and get last 'limit' entries
            user_history = [
                (entry['prompt'], entry['response'], entry.get('timestamp', ''))
                for entry in history
                if entry.get('user_id') == user_id
            ]
            
            return user_history[-limit:]
            
        except Exception as e:
            print(f"Error getting chat history: {e}")
            return []
    
    def add_file_alias(self, user_id, alias, path):
        """Add file/folder alias"""
        try:
            # Load existing aliases
            with open(self.file_aliases_file, 'r') as f:
                aliases = json.load(f)
            
            # Initialize user's aliases if not exists
            user_id_str = str(user_id)
            if user_id_str not in aliases:
                aliases[user_id_str] = {}
            
            # Add/update alias
            aliases[user_id_str][alias.lower()] = path
            
            # Save updated aliases
            with open(self.file_aliases_file, 'w') as f:
                json.dump(aliases, f, indent=2)
                
        except Exception as e:
            print(f"Error adding file alias: {e}")
    
    def get_file_aliases(self, user_id):
        """Get user's file aliases"""
        try:
            # Load aliases
            with open(self.file_aliases_file, 'r') as f:
                aliases = json.load(f)
            
            # Get user's aliases
            user_id_str = str(user_id)
            return aliases.get(user_id_str, {})
            
        except Exception as e:
            print(f"Error getting file aliases: {e}")
            return {}

# Global database instance
db = DatabaseManager()