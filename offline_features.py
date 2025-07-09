"""
Offline Features Implementation for Athena AI Assistant
Provides functionality that works without internet connection
"""

import os
import json
import sqlite3
from datetime import datetime
import random
import math
import calendar
from pathlib import Path

class OfflineManager:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize offline database
        self.db_path = self.data_dir / "offline_data.db"
        self.init_offline_database()
        
        # Load offline data
        self.load_offline_data()
    
    def init_offline_database(self):
        """Initialize SQLite database for offline data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables for offline functionality
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS offline_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS offline_reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reminder TEXT NOT NULL,
                due_date TEXT,
                completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS offline_calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expression TEXT NOT NULL,
                result TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS offline_commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT NOT NULL,
                response TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def load_offline_data(self):
        """Load offline data and knowledge base"""
        # Load basic facts and information
        self.offline_facts = {
            "general": [
                "The Earth is approximately 4.54 billion years old.",
                "Water boils at 100 degrees Celsius at sea level.",
                "The speed of light is approximately 299,792,458 meters per second.",
                "There are 7 continents on Earth.",
                "The human body has 206 bones in adults."
            ],
            "science": [
                "DNA stands for Deoxyribonucleic Acid.",
                "The periodic table has 118 known elements.",
                "Photosynthesis is the process by which plants make food using sunlight.",
                "The smallest unit of matter is an atom.",
                "Gravity is a fundamental force of nature."
            ],
            "history": [
                "World War II ended in 1945.",
                "The Great Wall of China was built over many centuries.",
                "The Renaissance period was from the 14th to 17th century.",
                "The first moon landing was in 1969.",
                "The printing press was invented by Johannes Gutenberg."
            ]
        }
        
        # Load common calculations and conversions
        self.conversions = {
            "temperature": {
                "celsius_to_fahrenheit": lambda c: (c * 9/5) + 32,
                "fahrenheit_to_celsius": lambda f: (f - 32) * 5/9,
                "celsius_to_kelvin": lambda c: c + 273.15,
                "kelvin_to_celsius": lambda k: k - 273.15
            },
            "length": {
                "meters_to_feet": lambda m: m * 3.28084,
                "feet_to_meters": lambda f: f / 3.28084,
                "kilometers_to_miles": lambda km: km * 0.621371,
                "miles_to_kilometers": lambda mi: mi / 0.621371
            },
            "weight": {
                "kg_to_pounds": lambda kg: kg * 2.20462,
                "pounds_to_kg": lambda lb: lb / 2.20462,
                "grams_to_ounces": lambda g: g * 0.035274,
                "ounces_to_grams": lambda oz: oz / 0.035274
            }
        }
    
    def get_offline_fact(self, category=None):
        """Get a random offline fact"""
        if category and category in self.offline_facts:
            facts = self.offline_facts[category]
        else:
            # Get facts from all categories
            facts = []
            for category_facts in self.offline_facts.values():
                facts.extend(category_facts)
        
        return random.choice(facts) if facts else "No facts available."
    
    def calculate_expression(self, expression):
        """Safely evaluate mathematical expressions"""
        try:
            # Remove any potentially dangerous functions
            allowed_names = {
                k: v for k, v in math.__dict__.items() if not k.startswith("__")
            }
            allowed_names.update({"abs": abs, "round": round})
            
            # Evaluate the expression safely
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            
            # Store in offline database
            self.store_calculation(expression, str(result))
            
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    def store_calculation(self, expression, result):
        """Store calculation in offline database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO offline_calculations (expression, result) VALUES (?, ?)",
            (expression, result)
        )
        
        conn.commit()
        conn.close()
    
    def get_calculation_history(self, limit=10):
        """Get recent calculation history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT expression, result, timestamp FROM offline_calculations ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        )
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def create_note(self, title, content):
        """Create an offline note"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO offline_notes (title, content) VALUES (?, ?)",
            (title, content)
        )
        
        conn.commit()
        conn.close()
        
        return "Note created successfully."
    
    def get_notes(self, search_term=None):
        """Get offline notes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if search_term:
            cursor.execute(
                "SELECT id, title, content, created_at FROM offline_notes WHERE title LIKE ? OR content LIKE ? ORDER BY updated_at DESC",
                (f"%{search_term}%", f"%{search_term}%")
            )
        else:
            cursor.execute(
                "SELECT id, title, content, created_at FROM offline_notes ORDER BY updated_at DESC"
            )
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def create_reminder(self, reminder_text, due_date=None):
        """Create an offline reminder"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO offline_reminders (reminder, due_date) VALUES (?, ?)",
            (reminder_text, due_date)
        )
        
        conn.commit()
        conn.close()
        
        return "Reminder created successfully."
    
    def get_reminders(self, include_completed=False):
        """Get offline reminders"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if include_completed:
            cursor.execute(
                "SELECT id, reminder, due_date, completed, created_at FROM offline_reminders ORDER BY created_at DESC"
            )
        else:
            cursor.execute(
                "SELECT id, reminder, due_date, completed, created_at FROM offline_reminders WHERE completed = FALSE ORDER BY created_at DESC"
            )
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def complete_reminder(self, reminder_id):
        """Mark reminder as completed"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE offline_reminders SET completed = TRUE WHERE id = ?",
            (reminder_id,)
        )
        
        conn.commit()
        conn.close()
        
        return "Reminder marked as completed."
    
    def get_calendar_info(self, year=None, month=None):
        """Get calendar information"""
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        try:
            cal = calendar.monthcalendar(year, month)
            month_name = calendar.month_name[month]
            
            calendar_text = f"\n{month_name} {year}\n"
            calendar_text += "Mo Tu We Th Fr Sa Su\n"
            
            for week in cal:
                week_str = ""
                for day in week:
                    if day == 0:
                        week_str += "   "
                    else:
                        week_str += f"{day:2d} "
                calendar_text += week_str + "\n"
            
            return calendar_text
        except Exception as e:
            return f"Error generating calendar: {str(e)}"
    
    def convert_units(self, value, from_unit, to_unit, unit_type):
        """Convert between different units"""
        try:
            if unit_type not in self.conversions:
                return f"Unit type '{unit_type}' not supported."
            
            conversion_key = f"{from_unit}_to_{to_unit}"
            if conversion_key not in self.conversions[unit_type]:
                return f"Conversion from {from_unit} to {to_unit} not available."
            
            converter = self.conversions[unit_type][conversion_key]
            result = converter(float(value))
            
            return f"{value} {from_unit} = {result:.2f} {to_unit}"
        except Exception as e:
            return f"Error in conversion: {str(e)}"
    
    def get_system_time_info(self):
        """Get detailed time information"""
        now = datetime.now()
        
        info = {
            "current_time": now.strftime("%I:%M:%S %p"),
            "current_date": now.strftime("%A, %B %d, %Y"),
            "day_of_year": now.timetuple().tm_yday,
            "week_number": now.isocalendar()[1],
            "timezone": str(now.astimezone().tzinfo),
            "unix_timestamp": int(now.timestamp())
        }
        
        return info
    
    def generate_password(self, length=12, include_symbols=True):
        """Generate a secure password"""
        import string
        
        characters = string.ascii_letters + string.digits
        if include_symbols:
            characters += "!@#$%^&*"
        
        password = ''.join(random.choice(characters) for _ in range(length))
        return password
    
    def get_file_info(self, file_path):
        """Get information about a file"""
        try:
            path = Path(file_path)
            if not path.exists():
                return f"File '{file_path}' does not exist."
            
            stat = path.stat()
            
            info = {
                "name": path.name,
                "size": stat.st_size,
                "size_human": self.format_bytes(stat.st_size),
                "created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "is_file": path.is_file(),
                "is_directory": path.is_dir(),
                "extension": path.suffix
            }
            
            return info
        except Exception as e:
            return f"Error getting file info: {str(e)}"
    
    def format_bytes(self, bytes_value):
        """Format bytes into human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"
    
    def get_offline_help(self):
        """Get help information for offline features"""
        help_text = """
🔌 OFFLINE FEATURES HELP
{'='*50}

Available offline commands:

📝 NOTES:
- "create note [title] [content]" - Create a new note
- "show notes" - Display all notes
- "search notes [term]" - Search notes

⏰ REMINDERS:
- "create reminder [text]" - Create a reminder
- "show reminders" - Display active reminders
- "complete reminder [id]" - Mark reminder as done

🧮 CALCULATIONS:
- "calculate [expression]" - Perform math calculations
- "convert [value] [from] to [to] [type]" - Unit conversions
- "calculation history" - Show recent calculations

📅 TIME & CALENDAR:
- "time info" - Detailed time information
- "calendar" - Show current month calendar
- "calendar [year] [month]" - Show specific month

🔧 UTILITIES:
- "generate password" - Create secure password
- "file info [path]" - Get file information
- "random fact" - Get a random fact
- "offline help" - Show this help

💡 EXAMPLES:
- "calculate 2 + 2 * 3"
- "convert 100 celsius to fahrenheit temperature"
- "create note Shopping buy milk and bread"
- "create reminder Call dentist"
"""
        return help_text

# Global offline manager instance
offline_manager = OfflineManager()