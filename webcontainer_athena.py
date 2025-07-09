#!/usr/bin/env python3
"""
WebContainer Compatible Athena AI Assistant
This version works around WebContainer limitations and missing modules
"""

import sys
import os
import json
import time
import datetime
import random
import math
import sys
from pathlib import Path

# WebContainer-safe imports only
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️ requests not available - some features will be limited")

# Mock missing modules for WebContainer
class MockSpeechRecognition:
    class Recognizer:
        def adjust_for_ambient_noise(self, source, duration=1):
            pass
        
        def listen(self, source, timeout=5, phrase_time_limit=10):
            return "mock audio"
        
        def recognize_google(self, audio, language='en-in'):
            # In WebContainer, we'll simulate voice input
            return input("🎤 Voice input (type your command): ").strip()
    
    class Microphone:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
    
    class UnknownValueError(Exception):
        pass
    
    class RequestError(Exception):
        pass

# Try to import real modules, fall back to mocks
try:
    import speech_recognition as sr
except ImportError:
    sr = MockSpeechRecognition()
    print("⚠️ Using mock speech recognition - type commands instead of speaking")

class WebContainerAthena:
    def __init__(self):
        self.is_running = False
        self.commands_history = []
        self.wake_word = "athena"
        self.notes = []
        self.reminders = []
        self.settings = {
            "wake_word": "athena",
            "voice_enabled": False,
            "tts_enabled": False
        }
        
        # Load saved data if available
        self.load_data()
        
        print("🤖 WebContainer Athena AI Assistant")
        print("=" * 50)
        print("⚠️ Running in WebContainer mode - some features are simulated")
        print("✅ Core functionality available")
        
    def speak(self, text):
        """Text-to-speech simulation for WebContainer"""
        print(f"🔊 Athena: {text}")
        self.log_activity("response", text)
        
    def takeCommandMIC(self):
        """Voice input simulation for WebContainer"""
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("🎤 Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
                query = r.recognize_google(audio, language='en-in')
                print(f"👤 You said: {query}")
                return query.lower()
        except Exception:
            # Fallback to text input in WebContainer
            query = input("💬 Type your command (or 'quit' to exit): ").strip()
            if query:
                print(f"👤 You typed: {query}")
                self.log_activity("text_input", query)
                return query.lower()
            return None
    
    def get_time(self):
        """Get current time"""
        try:
            current_time = datetime.datetime.now()
            time_str = current_time.strftime("The current time is %I:%M %p")
            self.speak(time_str)
            self.log_activity("time_request", time_str)
        except Exception as e:
            self.speak("Sorry, I couldn't get the current time")
            print(f"Error: {e}")
    
    def save_data(self):
        """Save data to JSON file"""
        try:
            data = {
                "notes": self.notes,
                "reminders": self.reminders,
                "settings": self.settings,
                "history": self.commands_history[-50:]  # Save only recent history
            }
            
            with open("athena_data.json", "w") as f:
                json.dump(data, f, indent=2)
                
            print("✅ Data saved successfully")
        except Exception as e:
            print(f"❌ Error saving data: {e}")
    
    def load_data(self):
        """Load data from JSON file"""
        try:
            if os.path.exists("athena_data.json"):
                with open("athena_data.json", "r") as f:
                    data = json.load(f)
                    self.notes = data.get("notes", [])
                    self.reminders = data.get("reminders", [])
                    self.settings = data.get("settings", self.settings)
                    self.commands_history = data.get("history", [])
                print("✅ Data loaded successfully")
        except Exception as e:
            print(f"❌ Error loading data: {e}")
    
    def get_date(self):
        """Get current date"""
        try:
            current_date = datetime.datetime.now()
            date_str = current_date.strftime("Today is %A, %B %d, %Y")
            self.speak(date_str)
            self.log_activity("date_request", date_str)
        except Exception as e:
            self.speak("Sorry, I couldn't get the current date")
            print(f"Error: {e}")
    
    def calculate(self, expression):
        """Safe calculator"""
        try:
            # Remove dangerous functions and only allow safe math
            allowed_names = {
                k: v for k, v in math.__dict__.items() if not k.startswith("__")
            }
            allowed_names.update({"abs": abs, "round": round, "min": min, "max": max})
            
            # Clean the expression
            expression = expression.replace("calculate", "").strip()
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            result_str = f"The result is {result}"
            self.speak(result_str)
            self.log_activity("calculation", f"{expression} = {result}")
            
        except Exception as e:
            self.speak("Sorry, I couldn't calculate that. Please check your expression.")
            print(f"Calculation error: {e}")
    
    def create_note(self, command):
        """Create a note"""
        try:
            note_content = command
            for word in ["athena", "create", "note", "remember", "save"]:
                note_content = note_content.replace(word, "")
            note_content = note_content.strip()
            
            if not note_content:
                self.speak("What would you like me to note?")
                note_content = input("💬 Note content: ").strip()
            
            if note_content:
                note = {
                    "id": len(self.notes) + 1,
                    "content": note_content,
                    "timestamp": datetime.datetime.now().isoformat()
                }
                self.notes.append(note)
                self.save_data()
                self.speak(f"Note saved: {note_content}")
                self.log_activity("create_note", note_content)
        except Exception as e:
            self.speak("Sorry, I couldn't save that note.")
            print(f"Note error: {e}")
    
    def show_notes(self):
        """Show all notes"""
        if not self.notes:
            self.speak("You have no saved notes.")
            return
        
        print("\n📝 YOUR NOTES:")
        print("=" * 30)
        for note in self.notes:
            timestamp = note["timestamp"][:19].replace("T", " ")
            print(f"{note['id']}. [{timestamp}] {note['content']}")
        
        self.speak(f"You have {len(self.notes)} saved notes. Check above for details.")
        self.log_activity("show_notes", f"{len(self.notes)} notes")
    
    def create_reminder(self, command):
        """Create a reminder"""
        try:
            # Extract reminder content
            reminder_content = command
            for word in ["athena", "remind", "me", "to", "reminder", "create"]:
                reminder_content = reminder_content.replace(word, "")
            reminder_content = reminder_content.strip()
            
            if not reminder_content:
                self.speak("What would you like me to remind you about?")
                reminder_content = input("💬 Reminder content: ").strip()
            
            if reminder_content:
                reminder = {
                    "id": len(self.reminders) + 1,
                    "content": reminder_content,
                    "created": datetime.datetime.now().isoformat(),
                    "completed": False
                }
                self.reminders.append(reminder)
                self.save_data()
                self.speak(f"Reminder created: {reminder_content}")
                self.log_activity("create_reminder", reminder_content)
        except Exception as e:
            self.speak("Sorry, I couldn't create that reminder.")
            print(f"Reminder error: {e}")
    
    def show_reminders(self):
        """Show all reminders"""
        active_reminders = [r for r in self.reminders if not r["completed"]]
        
        if not active_reminders:
            self.speak("You have no active reminders.")
            return
        
        print("\n⏰ YOUR REMINDERS:")
        print("=" * 30)
        for reminder in active_reminders:
            timestamp = reminder["created"][:19].replace("T", " ")
            print(f"{reminder['id']}. [{timestamp}] {reminder['content']}")
        
        self.speak(f"You have {len(active_reminders)} active reminders. Check above for details.")
        self.log_activity("show_reminders", f"{len(active_reminders)} reminders")
    
    def tell_joke(self):
        """Tell a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the math book look so sad? Because it had too many problems!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why don't programmers like nature? It has too many bugs!",
            "What's the best thing about Switzerland? I don't know, but the flag is a big plus!"
        ]
        
        joke = random.choice(jokes)
        self.speak(joke)
        self.log_activity("tell_joke", joke)
    
    def flip_coin(self):
        """Flip a virtual coin"""
        result = random.choice(["Heads", "Tails"])
        result_str = f"The coin landed on {result}"
        self.speak(result_str)
        self.log_activity("coin_flip", result)
    
    def roll_dice(self, command=None):
        """Roll dice with optional parameters"""
        try:
            # Parse command for number of dice and sides
            num_dice = 1
            sides = 6
            
            if command:
                words = command.split()
                for word in words:
                    if word.isdigit():
                        num_dice = min(int(word), 10)  # Limit to 10 dice
                        break
                
                if "sided" in command:
                    for i, word in enumerate(words):
                        if word.isdigit() and i+1 < len(words) and "sided" in words[i+1]:
                            sides = min(int(word), 100)  # Limit to 100 sides
            
            # Roll the dice
            results = [random.randint(1, sides) for _ in range(num_dice)]
            
            if num_dice == 1:
                self.speak(f"🎲 The dice rolled {results[0]}!")
            else:
                total = sum(results)
                self.speak(f"🎲 {num_dice} dice rolled: {results} (Total: {total})")
            
            self.log_activity("roll_dice", f"{num_dice}d{sides}: {results}")
            
        except Exception as e:
            self.speak("Sorry, I couldn't roll the dice.")
            print(f"Dice error: {e}")
    
    def get_random_fact(self):
        """Share a random fact"""
        facts = [
            "The Earth is approximately 4.54 billion years old.",
            "Water boils at 100 degrees Celsius at sea level.",
            "The speed of light is approximately 299,792,458 meters per second.",
            "There are 7 continents on Earth.",
            "The human body has 206 bones in adults.",
            "DNA stands for Deoxyribonucleic Acid.",
            "The periodic table has 118 known elements.",
            "Photosynthesis is the process by which plants make food using sunlight.",
            "The smallest unit of matter is an atom.",
            "Gravity is a fundamental force of nature."
        ]
        
        fact = random.choice(facts)
        self.speak(f"Here's an interesting fact: {fact}")
        self.log_activity("get_random_fact", fact)
    
    def search_simulation(self, query):
        """Simulate search functionality"""
        search_term = query.replace("search", "").replace("for", "").strip()
        result = f"I would search for '{search_term}' but search functionality is limited in WebContainer mode. You can manually search for this topic online."
        self.speak(result)
        self.log_activity("search_simulation", search_term)
    
    def weather_simulation(self):
        """Simulate weather functionality"""
        self.speak("Weather functionality requires internet access and API keys. In WebContainer mode, this feature is simulated. Please check your local weather service for current conditions.")
        self.log_activity("weather_simulation", "requested")
    
    def news_simulation(self):
        """Simulate news functionality"""
        self.speak("News functionality requires internet access and API keys. In WebContainer mode, this feature is simulated. Please check your preferred news source for current updates.")
        self.log_activity("news_simulation", "requested")
    
    def simulate_image_generation(self, prompt):
        """Simulate image generation"""
        self.speak(f"Generating an image of: {prompt}")
        print("🎨 Image generation simulation:")
        print(f"Prompt: {prompt}")
        print("In a full installation with API keys, this would generate a real image.")
        self.log_activity("image_generation", prompt)
        
        return f"""🎨 Image Generation Simulated!

Prompt: "{prompt}"

In a full installation with API keys configured, 
a real image would be generated based on your prompt.

To enable actual image generation:
1. Install the OpenAI package
2. Configure your API key
3. Run on a regular Python environment"""
    
    def simulate_code_generation(self, request):
        """Simulate code generation"""
        language = "python"  # Default
        
        # Try to detect language
        if "python" in request.lower():
            language = "python"
        elif "javascript" in request.lower() or "js" in request.lower():
            language = "javascript"
        elif "html" in request.lower():
            language = "html"
        elif "css" in request.lower():
            language = "css"
        
        self.speak(f"Generating {language} code based on your request")
        print(f"💻 Code generation simulation for {language}")
        print(f"Request: {request}")
        print("In a full installation, this would generate actual code.")
        self.log_activity("code_generation", request)
        
        return f"""💻 Code Generation Simulated!

Request: "{request}"
Language: {language}

In a full installation with API keys configured,
actual code would be generated based on your request.

To enable code generation:
1. Install the OpenAI package
2. Configure your API key
3. Run on a regular Python environment"""
    
    def log_activity(self, action, details):
        """Log user activities"""
        timestamp = datetime.datetime.now().isoformat()
        activity = {
            "timestamp": timestamp,
            "action": action,
            "details": details
        }
        self.commands_history.append(activity)
        
        # Keep only last 50 activities
        if len(self.commands_history) > 50:
            self.commands_history = self.commands_history[-50:]
    
    def show_history(self):
        """Show command history"""
        if not self.commands_history:
            self.speak("No command history available.")
            return
        
        self.speak("Here are your recent activities:")
        print("\n📊 COMMAND HISTORY:")
        print("=" * 40)
        
        for i, activity in enumerate(self.commands_history[-10:], 1):
            timestamp = activity["timestamp"][:19]  # Remove microseconds
            action = activity["action"]
            details = activity["details"]
            print(f"{i}. [{timestamp}] {action}: {details}")
    
    def show_help(self):
        """Show available commands"""
        help_text = """
🤖 ATHENA AI ASSISTANT - WEBCONTAINER MODE
{'='*50}

Available commands (say "athena" followed by):

⏰ TIME & DATE:
- "time" - Get current time
- "date" - Get current date

🧮 CALCULATIONS:
- "calculate [expression]" - Perform math calculations
- Example: "athena calculate 2 + 2 * 3"

🎯 UTILITIES:
- "joke" - Tell a random joke
- "flip coin" - Flip a virtual coin
- "random fact" - Share an interesting fact

🔍 SIMULATED FEATURES:
- "search [topic]" - Simulate search (limited in WebContainer)
- "weather" - Weather info (simulated)
- "news" - News updates (simulated)

📊 SYSTEM:
- "history" - Show recent command history
- "help" - Show this help message
- "quit" or "exit" - Stop Athena

💡 EXAMPLES:
- "athena time"
- "athena calculate 15 * 7"
- "athena tell me a joke"
- "athena flip coin"
- "athena help"

⚠️ NOTE: This is WebContainer mode with limited functionality.
For full features, run on a regular Python environment.
"""
        print(help_text)
        self.speak("Help information displayed. Check the console for details.")
    
    def process_command(self, query):
        """Process user commands with enhanced features"""
        if not query:
            return
        
        tokens = query.lower().split()
        
        # Check for wake word
        if self.wake_word not in tokens:
            self.speak("Please start your command with 'athena'")
            return
            # For better UX, we'll still process some commands without wake word
            if query in ["help", "quit", "exit"]:
                pass
            else:
                self.speak("Please start your command with 'athena'")
                return
        
        # Process commands
        if "time" in tokens:
            self.get_time()
        
        elif "date" in tokens:
            self.get_date()
        
        elif "calculate" in tokens or "math" in tokens:
        elif "calculate" in tokens or "math" in tokens or any(op in query for op in ["+", "-", "*", "/", "="]):
            self.calculate(query)
        
        elif "joke" in tokens:
            self.tell_joke()
        
        elif "flip" in tokens and "coin" in tokens:
            self.flip_coin()
        
        elif "roll" in tokens and "dice" in tokens:
            self.roll_dice(query)
        
        elif "fact" in tokens or "random" in tokens:
            self.get_random_fact()
        
        elif "note" in tokens or "remember" in tokens:
            self.create_note(query)
        
        elif "show" in tokens and "notes" in tokens:
            self.show_notes()
        
        elif "remind" in tokens:
            self.create_reminder(query)
        
        elif "show" in tokens and "reminders" in tokens:
            self.show_reminders()
        
        elif any(phrase in query for phrase in ["generate image", "create image", "make image", "draw"]):
            prompt = query.replace("generate image of", "").replace("create image of", "").replace("make image of", "").replace("draw", "").strip()
            response = self.simulate_image_generation(prompt)
            self.speak(response)
        
        elif any(phrase in query for phrase in ["write code", "generate code", "create function", "write program"]):
            response = self.simulate_code_generation(query)
            self.speak(response)
        
        elif "search" in tokens:
            self.search_simulation(query)
        
        elif "weather" in tokens:
            self.weather_simulation()
        
        elif "news" in tokens:
            self.news_simulation()
        
        elif "history" in tokens:
            self.show_history()
        
        elif "help" in tokens:
            self.show_help()
        
        elif "quit" in tokens or "exit" in tokens or "goodbye" in tokens or "bye" in tokens:
            self.save_data()
            self.speak("Goodbye! Thank you for using Athena AI Assistant!")
            self.is_running = False
        
        else:
            self.speak("I didn't understand that command. Say 'athena help' for available commands.")
    
    def greeting(self):
        """Initial greeting"""
        hour = datetime.datetime.now().hour
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        
        if 6 <= hour < 12:
            greeting = "Good Morning!"
        elif 12 <= hour < 18:
            greeting = "Good Afternoon!"
        elif 18 <= hour < 24:
            greeting = "Good Evening!"
        else:
            greeting = "Good Night!"
        
        self.speak(f"{greeting} The time is {current_time}. Welcome to Athena AI Assistant!")
        self.speak("I'm running in WebContainer mode with core functionality available.")
        
        # Show stats if we have any
        if self.notes or self.reminders:
            note_count = len(self.notes)
            reminder_count = len([r for r in self.reminders if not r.get("completed", False)])
            self.speak(f"You have {note_count} notes and {reminder_count} active reminders.")
        
        self.speak("Type 'athena help' to see what I can do, or 'quit' to exit.")
    
    def run(self):
        """Main application loop"""
        self.greeting()
        self.is_running = True
        
        while self.is_running:
            try:
                query = self.takeCommandMIC()
                if query:
                    self.process_command(query)
                else:
                    time.sleep(0.1)  # Small delay to prevent high CPU usage
                    
            except KeyboardInterrupt:
                self.save_data()
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                self.speak("Sorry, something went wrong. Please try again.")

def main():
    """Main entry point"""
    try:
        print("🚀 Starting WebContainer Athena AI Assistant...")
        athena = WebContainerAthena()
        athena.run()
    except Exception as e:
        print(f"❌ Critical error: {e}")
        print("Please check your Python environment and try again.")
        
if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()