"""
Database setup script for Athena AI Assistant
Run this script once to create the database and tables
"""

import mysql.connector
from config import DB_CONFIG

def create_database():
    """Creates the athenadb database if it doesn't exist"""
    try:
        # Connect without specifying database
        connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
        cursor = connection.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS athenadb")
        print("✅ Database 'athenadb' created successfully!")
        
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as err:
        print(f"❌ Error creating database: {err}")

def create_tables():
    """Creates all required tables"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
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
        print("✅ All tables created successfully!")
        
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as err:
        print(f"❌ Error creating tables: {err}")

if __name__ == "__main__":
    print("Setting up Athena database...")
    create_database()
    create_tables()
    print("✅ Database setup complete!")