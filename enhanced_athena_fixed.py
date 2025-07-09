"""
Enhanced Athena AI Assistant - Fixed Version
Updated to handle both MySQL and SQLite databases
"""

import random
import string
import smtplib
import datetime
import speech_recognition as sr
from email.message import EmailMessage
import pyautogui
import webbrowser as wb 
from time import sleep
import wikipedia
import pywhatkit as kit
import requests
from newsapi import NewsApiClient
import clipboard
import os
import pyjokes
import spacy
from Athenavoice import speak
import openai
import sqlite3

# Try to import MySQL, fall back to SQLite if not available
try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

# Import enhanced utilities
from utils.logger import athena_logger
from utils.connectivity import connectivity_manager, require_internet
from utils.error_handler import safe_execute, retry_on_failure, error_handler
from utils.system_utils import system_manager
from enhanced_config import config_manager

# Global database connection variables
mydb = None
mycursor = None
db_type = "sqlite"  # Default to SQLite

class AthenaCore:
    def __init__(self):
        """Initialize Athena with enhanced utilities"""
        self.config = config_manager
        self.logger = athena_logger
        self.connectivity = connectivity_manager
        self.system = system_manager
        
        # Initialize components
        self._setup_openai()
        self._setup_spacy()
        self._setup_directories()
        
        athena_logger.log_info("Athena AI Assistant initialized", "startup")
    
    def _setup_openai(self):
        """Setup OpenAI with configuration"""
        api_key = self.config.get_secure("api_keys.openai")
        if api_key:
            openai.api_key = api_key
            athena_logger.log_info("OpenAI API configured", "setup")
        else:
            athena_logger.log_error("OpenAI API key not configured", category="setup")
    
    def _setup_spacy(self):
        """Setup spaCy with error handling"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
            athena_logger.log_info("spaCy model loaded successfully", "setup")
        except OSError:
            self.nlp = None
            athena_logger.log_error(
                "spaCy model 'en_core_web_sm' not found. Please run: python -m spacy download en_core_web_sm",
                category="setup"
            )
    
    def _setup_directories(self):
        """Setup required directories"""
        directories = [
            self.config.get("paths.screenshot_folder"),
            self.config.get("paths.logs_folder"),
            self.config.get("paths.data_folder")
        ]
        
        for directory in directories:
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                athena_logger.log_info(f"Created directory: {directory}", "setup")
    
    @safe_execute("database", "Database connection failed")
    def connect_to_database(self):
        """Enhanced database connection with MySQL/SQLite fallback"""
        global mydb, mycursor, db_type
        
        # Try MySQL first if available
        if MYSQL_AVAILABLE:
            try:
                db_config = {
                    "host": "localhost",
                    "user": "root",
                    "password": "",
                    "database": "athenadb"
                }
                mydb = mysql.connector.connect(**db_config, autocommit=True)
                mycursor = mydb.cursor()
                db_type = "mysql"
                
                athena_logger.log_info("Connected to MySQL successfully", "database")
                return True
                
            except mysql.connector.Error as err:
                athena_logger.log_error(
                    f"MySQL Connection Error: {err}. Falling back to SQLite.",
                    exception=err,
                    category="database"
                )
        
        # Fallback to SQLite
        try:
            # Create data directory if it doesn't exist
            data_dir = "data"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            
            db_path = os.path.join(data_dir, "athena_fallback.db")
            mydb = sqlite3.connect(db_path, check_same_thread=False)
            mycursor = mydb.cursor()
            db_type = "sqlite"
            
            # Enable autocommit for SQLite
            mydb.isolation_level = None
            
            athena_logger.log_info(f"Connected to SQLite database: {db_path}", "database")
            return True
            
        except Exception as e:
            athena_logger.log_error(
                f"Database connection failed: {e}",
                exception=e,
                category="database"
            )
            mydb = None
            mycursor = None
            return False
    
    def ensure_db_connection(self):
        """Ensure database connection is active with retry logic"""
        global mydb, mycursor
        
        if mydb is None:
            return self.connect_to_database()
        
        # Check connection based on database type
        try:
            if db_type == "mysql" and hasattr(mydb, 'is_connected'):
                if not mydb.is_connected():
                    return self.connect_to_database()
            elif db_type == "sqlite":
                # Test SQLite connection
                mycursor.execute("SELECT 1")
                
            return True
        except Exception:
            return self.connect_to_database()
    
    def execute_db_query(self, query, params=None):
        """Execute database query with proper syntax for both MySQL and SQLite"""
        if not self.ensure_db_connection():
            return False
        
        try:
            if db_type == "sqlite":
                # Convert MySQL syntax to SQLite if needed
                query = query.replace("AUTO_INCREMENT", "AUTOINCREMENT")
                query = query.replace("INT AUTO_INCREMENT", "INTEGER PRIMARY KEY AUTOINCREMENT")
            
            if params:
                mycursor.execute(query, params)
            else:
                mycursor.execute(query)
            
            if db_type == "mysql":
                # MySQL handles autocommit
                pass
            else:
                # SQLite commit
                mydb.commit()
            
            return True
        except Exception as e:
            athena_logger.log_error(f"Database query error: {e}", category="database")
            return False
    
    @safe_execute("voice_recognition", "I didn't catch that. Could you please repeat?")
    def takeCommandMIC(self):
        """Enhanced voice recognition with better error handling"""
        r = sr.Recognizer()
        
        with sr.Microphone() as source:
            athena_logger.log_info("Listening for voice input", "voice")
            r.adjust_for_ambient_noise(source, duration=1)
            r.pause_threshold = 1
            
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
                athena_logger.log_info("Processing voice input", "voice")
                
                query = r.recognize_google(audio, language='en-in')
                athena_logger.log_activity(query, "voice_input")
                
                print(f"User said: {query}")
                return query.lower()
                
            except sr.UnknownValueError:
                athena_logger.log_info("Could not understand audio", "voice")
                return None
            except sr.RequestError as e:
                athena_logger.log_error(f"Speech recognition service error: {e}", category="voice")
                return None
            except Exception as e:
                athena_logger.log_error(f"Voice recognition error: {e}", category="voice")
                return None
    
    def process_query(self, query):
        """Enhanced query processing with spaCy"""
        if self.nlp is None:
            return query.lower().split()  # Fallback to simple split
        
        try:
            doc = self.nlp(query.lower())
            tokens = [token.text for token in doc if not token.is_punct]
            athena_logger.log_info(f"Processed query tokens: {tokens}", "nlp")
            return tokens
        except Exception as e:
            athena_logger.log_error(f"Query processing error: {e}", category="nlp")
            return query.lower().split()
    
    @safe_execute("time", "Sorry, I couldn't get the current time")
    def get_time(self):
        """Enhanced time function with logging"""
        current_time = datetime.datetime.now()
        hour = current_time.strftime("%I")
        minute = current_time.strftime("%M")
        period = current_time.strftime("%p")
        
        time_str = f"The current time is {hour}:{minute} {period}"
        speak(time_str)
        
        athena_logger.log_activity("time request", "get_time", time_str)
        
        # Database logging
        if self.ensure_db_connection():
            try:
                formatted_time = current_time.strftime("%I:%M %p")
                timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
                
                query = "INSERT INTO time_logs (current_time, timestamp) VALUES (?, ?)"
                self.execute_db_query(query, (formatted_time, timestamp))
                
                athena_logger.log_info("Time logged to database", "database")
            except Exception as e:
                athena_logger.log_error(f"Database logging error: {e}", category="database")
    
    @safe_execute("date", "Sorry, I couldn't get the current date")
    def get_date(self):
        """Enhanced date function with logging"""
        current_date = datetime.datetime.now()
        year = current_date.year
        month = current_date.strftime("%B")
        day = current_date.day
        
        date_str = f"Today is {month} {day}, {year}"
        speak(date_str)
        
        athena_logger.log_activity("date request", "get_date", date_str)
        
        # Database logging
        if self.ensure_db_connection():
            try:
                log_date = current_date.strftime("%Y-%m-%d")
                timestamp = current_date.strftime("%Y-%m-%d %H:%M:%S")
                
                query = "INSERT INTO date_logs (log_date, timestamp) VALUES (?, ?)"
                self.execute_db_query(query, (log_date, timestamp))
                
                athena_logger.log_info("Date logged to database", "database")
            except Exception as e:
                athena_logger.log_error(f"Database logging error: {e}", category="database")
    
    def greeting(self):
        """Enhanced greeting with system info"""
        hour = datetime.datetime.now().hour
        
        if 6 <= hour < 12:
            greeting_msg = "Good Morning Sir!"
        elif 12 <= hour < 18:
            greeting_msg = "Good Afternoon Sir!"
        elif 18 <= hour < 24:
            greeting_msg = "Good Evening Sir!"
        else:
            greeting_msg = "Good Night Sir!"
        
        speak(greeting_msg)
        athena_logger.log_activity("greeting", "greeting", greeting_msg)
    
    def wishme(self):
        """Enhanced welcome message with connectivity status"""
        speak("Welcome back Sir!")
        self.greeting()
        
        # Check connectivity and inform user
        connection_status = self.connectivity.get_connection_status()
        if connection_status['connected']:
            speak("Athena at your service. All systems online. Please tell me how can I help you?")
        else:
            speak("Athena at your service. Note: Some features may be limited due to no internet connection. Please tell me how can I help you?")
        
        athena_logger.log_info(f"Athena started - Connection: {connection_status['status_message']}", "startup")
    
    @require_internet("Wikipedia search requires an internet connection")
    @safe_execute("wikipedia", "Sorry, I couldn't search Wikipedia right now")
    def search_wikipedia(self):
        """Enhanced Wikipedia search with connectivity check"""
        speak("What topic would you like to search on Wikipedia?")
        topic = self.takeCommandMIC()
        
        if not topic:
            return
        
        try:
            athena_logger.log_info(f"Searching Wikipedia for: {topic}", "wikipedia")
            summary = wikipedia.summary(topic, sentences=2)
            
            speak(f"According to Wikipedia: {summary}")
            athena_logger.log_activity(f"wikipedia search: {topic}", "search_wikipedia", summary)
            
            # Database logging
            if self.ensure_db_connection():
                query = "INSERT INTO searches (query, result) VALUES (?, ?)"
                self.execute_db_query(query, (topic, summary))
                
        except wikipedia.exceptions.DisambiguationError as e:
            options = e.options[:3]
            message = f"The search term '{topic}' has multiple meanings. Here are some options: {', '.join(options)}"
            speak(message)
            athena_logger.log_info(f"Wikipedia disambiguation for {topic}: {options}", "wikipedia")
            
        except wikipedia.exceptions.PageError:
            message = "Sorry, I couldn't find a Wikipedia page for that topic."
            speak(message)
            athena_logger.log_info(f"Wikipedia page not found for: {topic}", "wikipedia")
    
    @require_internet("ChatGPT requires an internet connection")
    @retry_on_failure(max_retries=2, context="openai")
    @safe_execute("openai", "Sorry, I encountered an error while processing your request")
    def chat_with_gpt(self, user_input):
        """Enhanced ChatGPT integration with retry logic"""
        api_key = self.config.get_secure("api_keys.openai")
        if not api_key:
            speak("OpenAI API key is not configured. Please add your API key to the configuration.")
            return
        
        athena_logger.log_info(f"ChatGPT request: {user_input}", "openai")
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Athena, a helpful AI assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        
        reply = response["choices"][0]["message"]["content"]
        speak(reply)
        
        # Log API usage
        tokens_used = response.get("usage", {}).get("total_tokens", 0)
        athena_logger.log_api_usage("openai", "chat", tokens_used)
        athena_logger.log_activity(f"chatgpt: {user_input}", "chat_with_gpt", reply)
        
        return reply
    
    @safe_execute("screenshot", "Sorry, I couldn't take the screenshot")
    def take_screenshot(self):
        """Enhanced screenshot function with better file management"""
        screenshot_folder = self.config.get("paths.screenshot_folder")
        
        if not os.path.exists(screenshot_folder):
            os.makedirs(screenshot_folder)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filepath = os.path.join(screenshot_folder, f"screenshot_{timestamp}.png")
        
        img = pyautogui.screenshot()
        img.save(filepath)
        
        speak("Screenshot taken and saved.")
        athena_logger.log_activity("screenshot", "take_screenshot", filepath)
        
        # Database logging
        if self.ensure_db_connection():
            query = "INSERT INTO screenshots (filepath, timestamp) VALUES (?, ?)"
            self.execute_db_query(query, (filepath, timestamp))
    
    @safe_execute("system", "Sorry, I couldn't open that resource")
    def open_resource(self, query):
        """Enhanced resource opening with cross-platform support"""
        query_words = query.lower().split()
        user_dirs = self.system.get_user_directories()
        
        resource_mapping = {
            'documents': user_dirs['documents'],
            'music': user_dirs['music'],
            'pictures': user_dirs['pictures'],
            'videos': user_dirs['videos'],
            'downloads': user_dirs['downloads'],
            'desktop': user_dirs['desktop']
        }
        
        for resource in resource_mapping.keys():
            if resource in query_words:
                resource_path = resource_mapping[resource]
                
                try:
                    self.system.open_file_or_folder(resource_path)
                    speak(f"Opening {resource}")
                    athena_logger.log_activity(f"open {resource}", "open_resource", str(resource_path))
                    
                    # Database logging
                    if self.ensure_db_connection():
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        query = "INSERT INTO resource_actions (resource_type, timestamp) VALUES (?, ?)"
                        self.execute_db_query(query, (resource, timestamp))
                    
                    return
                    
                except Exception as e:
                    athena_logger.log_error(f"Failed to open {resource}: {e}", category="system")
                    speak(f"Sorry, I couldn't open the {resource} folder.")
                    return
        
        speak("I couldn't identify the resource you want to open.")
    
    def show_system_status(self):
        """Show system status and statistics"""
        connection_status = self.connectivity.get_connection_status()
        system_info = self.system.get_system_info()
        error_stats = error_handler.get_error_stats()
        
        status_message = f"""
        System Status:
        - Connection: {connection_status['status_message']}
        - Database: {db_type.upper()} {'Connected' if mydb else 'Disconnected'}
        - OS: {system_info['os']} {system_info['architecture']}
        - Python: {system_info['python_version']}
        - Errors logged: {len(error_stats)}
        """
        
        print(status_message)
        speak("System status displayed. Check the console for details.")
        athena_logger.log_activity("system status", "show_system_status", "displayed")

def main():
    """Main entry point"""
    try:
        athena = AthenaCore()
        
        # Initialize database connection
        if not athena.connect_to_database():
            print("❌ Database connection failed. Some features may not work properly.")
            speak("Warning: Database connection failed. Some features may not work properly.")
        
        athena.wishme()
        
        # Simple command loop for testing
        wake_word = athena.config.get("features.wake_word", "athena")
        
        while True:
            try:
                query = athena.takeCommandMIC()
                if not query:
                    continue
                
                query_tokens = athena.process_query(query)
                print(f"Processing command: {query}")
                
                if wake_word in query_tokens:
                    if 'time' in query_tokens:
                        athena.get_time()
                    elif 'date' in query_tokens:
                        athena.get_date()
                    elif "search" in query_tokens and "wikipedia" in query_tokens:
                        athena.search_wikipedia()
                    elif "chat" in query_tokens or "talk" in query_tokens:
                        speak("What would you like to talk about?")
                        user_input = athena.takeCommandMIC()
                        if user_input:
                            athena.chat_with_gpt(user_input)
                    elif "screenshot" in query_tokens:
                        athena.take_screenshot()
                    elif "open" in query_tokens:
                        athena.open_resource(query)
                    elif "status" in query_tokens:
                        athena.show_system_status()
                    elif "quit" in query_tokens or "exit" in query_tokens or "goodbye" in query_tokens:
                        speak("Goodbye! Have a great day!")
                        break
                    else:
                        speak("I didn't understand that command. Please try again.")
                
            except KeyboardInterrupt:
                speak("Goodbye!")
                break
            except Exception as e:
                error_handler.handle_error(e, "main_loop", "Sorry, something went wrong. Please try again.")
        
        # Cleanup
        if mydb:
            if db_type == "mysql" and hasattr(mydb, 'is_connected') and mydb.is_connected():
                mycursor.close()
                mydb.close()
            elif db_type == "sqlite":
                mydb.close()
            print("✅ Database connection closed")
            
    except Exception as e:
        print(f"❌ Critical error starting Athena: {e}")
        if 'athena_logger' in globals():
            athena_logger.log_error(f"Critical startup error: {e}", category="critical")

if __name__ == "__main__":
    main()