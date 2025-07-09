"""
Enhanced configuration management for Athena AI Assistant
Includes validation, environment variable support, and secure storage
"""

import os
import json
from pathlib import Path
from cryptography.fernet import Fernet
import base64

class ConfigManager:
    def __init__(self, config_dir="config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        self.config_file = self.config_dir / "athena_config.json"
        self.secure_config_file = self.config_dir / "secure_config.enc"
        self.key_file = self.config_dir / ".key"
        
        self._ensure_encryption_key()
        self.config = self._load_config()
        self.secure_config = self._load_secure_config()
    
    def _ensure_encryption_key(self):
        """Ensure encryption key exists"""
        if not self.key_file.exists():
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            # Hide the key file on Windows
            if os.name == 'nt':
                import ctypes
                ctypes.windll.kernel32.SetFileAttributesW(str(self.key_file), 2)
    
    def _get_cipher(self):
        """Get encryption cipher"""
        with open(self.key_file, 'rb') as f:
            key = f.read()
        return Fernet(key)
    
    def _load_config(self):
        """Load regular configuration"""
        default_config = {
            "voice_settings": {
                "voice": "en-US-AvaNeural",
                "speed": "+30%",
                "volume": 0.8
            },
            "ui_settings": {
                "theme": "dark",
                "minimize_to_tray": True,
                "start_minimized": False,
                "show_notifications": True
            },
            "features": {
                "wake_word_enabled": True,
                "wake_word": "athena",
                "auto_screenshot": False,
                "screenshot_interval": 300,
                "data_collection": True
            },
            "paths": {
                "screenshot_folder": "screenshots",
                "logs_folder": "logs",
                "data_folder": "data"
            },
            "database": {
                "host": "localhost",
                "user": "root",
                "database": "athenadb",
                "port": 3306
            }
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                # Merge with defaults
                return self._merge_configs(default_config, loaded_config)
            except Exception:
                return default_config
        
        return default_config
    
    def _load_secure_config(self):
        """Load encrypted configuration"""
        default_secure = {
            "api_keys": {
                "openai": "",
                "news_api": "",
                "weather_api": "21c9fe0d0b585bed0a16677ee079de8b"
            },
            "email": {
                "sender_email": "",
                "app_password": "",
                "default_recipient": ""
            },
            "database": {
                "password": ""
            }
        }
        
        if self.secure_config_file.exists():
            try:
                cipher = self._get_cipher()
                with open(self.secure_config_file, 'rb') as f:
                    encrypted_data = f.read()
                decrypted_data = cipher.decrypt(encrypted_data)
                return json.loads(decrypted_data.decode())
            except Exception:
                return default_secure
        
        return default_secure
    
    def _merge_configs(self, default, loaded):
        """Recursively merge configurations"""
        for key, value in loaded.items():
            if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                default[key] = self._merge_configs(default[key], value)
            else:
                default[key] = value
        return default
    
    def save_config(self):
        """Save regular configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def save_secure_config(self):
        """Save encrypted configuration"""
        cipher = self._get_cipher()
        data = json.dumps(self.secure_config).encode()
        encrypted_data = cipher.encrypt(data)
        with open(self.secure_config_file, 'wb') as f:
            f.write(encrypted_data)
    
    def get(self, key_path, default=None):
        """Get configuration value using dot notation"""
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def get_secure(self, key_path, default=None):
        """Get secure configuration value using dot notation"""
        keys = key_path.split('.')
        value = self.secure_config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path, value):
        """Set configuration value using dot notation"""
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
        self.save_config()
    
    def set_secure(self, key_path, value):
        """Set secure configuration value using dot notation"""
        keys = key_path.split('.')
        config = self.secure_config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
        self.save_secure_config()
    
    def validate_api_keys(self):
        """Validate that required API keys are present"""
        required_keys = {
            'api_keys.openai': 'OpenAI API key for ChatGPT and DALL-E',
            'api_keys.news_api': 'NewsAPI key for news updates',
            'api_keys.weather_api': 'OpenWeatherMap API key for weather'
        }
        
        missing_keys = []
        for key_path, description in required_keys.items():
            if not self.get_secure(key_path):
                missing_keys.append((key_path, description))
        
        return missing_keys
    
    def get_database_config(self):
        """Get complete database configuration"""
        return {
            "host": self.get("database.host"),
            "user": self.get("database.user"),
            "password": self.get_secure("database.password"),
            "database": self.get("database.database"),
            "port": self.get("database.port")
        }

# Global configuration manager
config_manager = ConfigManager()