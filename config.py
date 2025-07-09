"""
Configuration file for AI Assistant
"""
import os
import json
from pathlib import Path

class Config:
    def __init__(self):
        self.config_dir = Path.home() / ".ai_assistant"
        self.config_file = self.config_dir / "config.json"
        self.db_dir = self.config_dir / "database"
        
        # Create directories if they don't exist
        self.config_dir.mkdir(exist_ok=True)
        self.db_dir.mkdir(exist_ok=True)
        
        # Default configuration
        self.default_config = {
            "assistant_name": "Assistant",
            "wake_word": "assistant",
            "voice_type": "female",
            "voice_speed": 180,
            "voice_volume": 0.8,
            "theme": "dark",
            "auto_listen": True,
            "offline_mode": True,
            "file_search_depth": 3,
            "common_folders": {
                "downloads": str(Path.home() / "Downloads"),
                "documents": str(Path.home() / "Documents"),
                "desktop": str(Path.home() / "Desktop"),
                "music": str(Path.home() / "Music"),
                "videos": str(Path.home() / "Videos"),
                "pictures": str(Path.home() / "Pictures")
            }
        }
        
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
                # Merge with defaults for any missing keys
                for key, value in self.default_config.items():
                    if key not in self.config:
                        self.config[key] = value
            except Exception as e:
                print(f"Error loading config: {e}")
                self.config = self.default_config.copy()
        else:
            self.config = self.default_config.copy()
            self.save_config()
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set configuration value"""
        self.config[key] = value
        self.save_config()
    
    def update_assistant_name(self, name):
        """Update assistant name and wake word"""
        self.set("assistant_name", name)
        self.set("wake_word", name.lower())

# Global config instance
config = Config()