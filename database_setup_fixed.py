"""
Fixed Database setup script for Athena AI Assistant
This version includes better error handling and fallback options
"""

import mysql.connector
import sqlite3
import os
from pathlib import Path

def check_mysql_availability():
    """Check if MySQL server is available and accessible"""
    try:
        # Try to connect to MySQL server without specifying database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""  # Default empty password
        )
        connection.close()
        return True, "MySQL server is available"
    except mysql.connector.Error as err:
        return False, f"MySQL connection failed: {err}"
    except Exception as e:
        return False, f"Unexpected error: {e}"

def create_mysql_database():
    """Creates the athenadb database if MySQL is available"""
    try:
        # Connect without specifying database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = connection.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS athenadb")
        print("✅ MySQL Database 'athenadb' created successfully!")
        
        cursor.close()
        connection.close()
        return True
        
    except mysql.connector.Error as err:
        print(f"❌ Error creating MySQL database: {err}")
        return False

def create_mysql_tables():
    """Creates all required tables in MySQL"""
    try:
        # Database configuration
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "athenadb"
        }
        
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        # Create tables
        tables = [
            """
            CREATE TABLE IF NOT EXISTS time_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                current_time VARCHAR(20),
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS date_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                log_date DATE,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS searches (
                id INT AUTO_INCREMENT PRIMARY KEY,
                query TEXT,
                result TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS emails (
                id INT AUTO_INCREMENT PRIMARY KEY,
                receiver VARCHAR(255),
                subject TEXT,
                content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS whatsapp_messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                phone_no VARCHAR(20),
                message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS news (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title TEXT,
                description TEXT,
                content TEXT,
                category VARCHAR(50),
                country VARCHAR(50),
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS weather (
                id INT AUTO_INCREMENT PRIMARY KEY,
                city VARCHAR(100),
                temperature FLOAT,
                humidity INT,
                description TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS clipboard_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                copied_text TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS resource_actions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                resource_type VARCHAR(50),
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS screenshots (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filepath TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                task TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS jokes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                joke TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS coin_flips (
                id INT AUTO_INCREMENT PRIMARY KEY,
                result VARCHAR(10),
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS command_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                command TEXT,
                output TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        ]
        
        for table_sql in tables:
            cursor.execute(table_sql)
            
        connection.commit()
        print("✅ All MySQL tables created successfully!")
        
        cursor.close()
        connection.close()
        return True
        
    except mysql.connector.Error as err:
        print(f"❌ Error creating MySQL tables: {err}")
        return False

def create_sqlite_fallback():
    """Create SQLite database as fallback when MySQL is not available"""
    try:
        # Create data directory if it doesn't exist
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # SQLite database path
        db_path = data_dir / "athena_fallback.db"
        
        connection = sqlite3.connect(str(db_path))
        cursor = connection.cursor()
        
        # Create tables (SQLite syntax)
        tables = [
            """
            CREATE TABLE IF NOT EXISTS time_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                current_time TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS date_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_date DATE,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT,
                result TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receiver TEXT,
                subject TEXT,
                content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS whatsapp_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_no TEXT,
                message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                content TEXT,
                category TEXT,
                country TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS weather (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT,
                temperature REAL,
                humidity INTEGER,
                description TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS clipboard_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                copied_text TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS resource_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resource_type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS screenshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filepath TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS jokes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                joke TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS coin_flips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                result TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS command_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT,
                output TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        ]
        
        for table_sql in tables:
            cursor.execute(table_sql)
            
        connection.commit()
        connection.close()
        
        print(f"✅ SQLite fallback database created at: {db_path}")
        return True, str(db_path)
        
    except Exception as e:
        print(f"❌ Error creating SQLite fallback: {e}")
        return False, None

def update_config_for_sqlite(db_path):
    """Update configuration to use SQLite instead of MySQL"""
    try:
        config_content = f'''"""
Configuration file for API keys and settings
Updated to use SQLite fallback database
"""

# OpenAI API Configuration
OPENAI_API_KEY = ""  # Replace with your OpenAI API key

# News API Configuration  
NEWS_API_KEY = ""  # Replace with your NewsAPI key from https://newsapi.org/

# Weather API Configuration
WEATHER_API_KEY = "21c9fe0d0b585bed0a16677ee079de8b"  # Replace with your OpenWeatherMap API key

# Database Configuration - Using SQLite fallback
DB_CONFIG = {{
    "type": "sqlite",
    "database": "{db_path}"
}}

# MySQL Configuration (commented out - not available)
# DB_CONFIG = {{
#     "host": "localhost",
#     "user": "root", 
#     "password": "",
#     "database": "athenadb"
# }}

# Voice Configuration
VOICE_SETTINGS = {{
    "voice": "en-US-AvaNeural",
    "speed": "+30%"
}}

# File Paths
SCREENSHOT_FOLDER = "screenshots"  # Will be created if doesn't exist
'''
        
        with open("config_sqlite.py", "w") as f:
            f.write(config_content)
        
        print("✅ Created config_sqlite.py with SQLite configuration")
        return True
        
    except Exception as e:
        print(f"❌ Error updating config: {e}")
        return False

def main():
    """Main setup function with fallback options"""
    print("🚀 Setting up Athena database...")
    print("=" * 50)
    
    # Check MySQL availability
    mysql_available, mysql_message = check_mysql_availability()
    print(f"MySQL Status: {mysql_message}")
    
    if mysql_available:
        print("\n🔄 Setting up MySQL database...")
        
        # Try to create MySQL database and tables
        if create_mysql_database() and create_mysql_tables():
            print("\n✅ MySQL database setup completed successfully!")
            print("\n📋 Next steps:")
            print("1. Configure your API keys in config.py")
            print("2. Set up your email credentials in secrets_1.py")
            print("3. Run python phase2_implementation.py to start the GUI")
        else:
            print("\n⚠️ MySQL setup failed, falling back to SQLite...")
            setup_sqlite_fallback()
    else:
        print("\n⚠️ MySQL not available, using SQLite fallback...")
        setup_sqlite_fallback()

def setup_sqlite_fallback():
    """Setup SQLite as fallback database"""
    success, db_path = create_sqlite_fallback()
    
    if success:
        update_config_for_sqlite(db_path)
        print("\n✅ SQLite fallback database setup completed!")
        print("\n📋 Next steps:")
        print("1. Use config_sqlite.py instead of config.py")
        print("2. Configure your API keys in the new config file")
        print("3. Set up your email credentials in secrets_1.py")
        print("4. Run python phase2_implementation.py to start the GUI")
        print("\n💡 Note: SQLite provides the same functionality as MySQL")
        print("   but stores data in a local file instead of a server.")
    else:
        print("\n❌ Both MySQL and SQLite setup failed!")
        print("Please check your Python installation and try again.")

if __name__ == "__main__":
    main()