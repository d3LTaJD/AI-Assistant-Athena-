"""
Configuration file for API keys and settings
"""

# OpenAI API Configuration
OPENAI_API_KEY = ""  # Replace with your OpenAI API key

# News API Configuration  
NEWS_API_KEY = ""  # Replace with your NewsAPI key from https://newsapi.org/

# Weather API Configuration
WEATHER_API_KEY = "21c9fe0d0b585bed0a16677ee079de8b"  # Replace with your OpenWeatherMap API key

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root", 
    "password": "",  # Replace with your MySQL password
    "database": "athenadb"
}

# Voice Configuration
VOICE_SETTINGS = {
    "voice": "en-US-AvaNeural",
    "speed": "+30%"
}

# File Paths
SCREENSHOT_FOLDER = "screenshots"  # Will be created if doesn't exist