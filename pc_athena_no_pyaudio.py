#!/usr/bin/env python3
"""
PC Athena AI Assistant - No PyAudio Version
This version works without PyAudio dependency for systems where it's difficult to install
"""

import sys
import os
import json
import time
import datetime
import random
import math
from pathlib import Path

# Try to import optional modules with fallbacks
try:
    import pyttsx3
    TEXT_TO_SPEECH_AVAILABLE = True
except ImportError:
    TEXT_TO_SPEECH_AVAILABLE = False
    print("⚠️ Text-to-speech not available. Install with: pip install pyttsx3")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️ Internet features limited. Install with: pip install requests")

class PCAthenaNoVoice:
    def __init__(self):
        self.running = True
        self.wake_word = "athena"
        self.tts_enabled = TEXT_TO_SPEECH_AVAILABLE
        
        # Data storage
        self.notes = []
        self.reminders = []
        self.history = []
        self.settings = {
            "tts_enabled": self.tts_enabled,
            "wake_word": self.wake_word
        }
        
        # Initialize TTS engine
        if self.tts_enabled:
            try:
                self.tts_engine = pyttsx3.init()
                self.setup_tts()
            except Exception as e:
                print(f"TTS initialization failed: {e}")
                self.tts_enabled = False
        
        # Load saved data
        self.load_data()
        
        print("🤖 PC Athena AI Assistant (No Voice Input Version)")
        print("=" * 50)
        print(f"🔊 Text-to-Speech: {'✅ Available' if self.tts_enabled else '❌ Not Available'}")
        print(f"🌐 Internet Features: {'✅ Available' if REQUESTS_AVAILABLE else '❌ Limited'}")
    
    def setup_tts(self):
        """Setup text-to-speech engine"""
        try:
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Try to set a female voice if available
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            
            # Set speech rate and volume
            self.tts_engine.setProperty('rate', 180)  # Speed
            self.tts_engine.setProperty('volume', 0.8)  # Volume
        except Exception as e:
            print(f"TTS setup error: {e}")
    
    def speak(self, text):
        """Text-to-speech with fallback to print"""
        print(f"🤖 Athena: {text}")
        
        if self.tts_enabled:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"TTS error: {e}")
        
        self.log_interaction("response", text)
    
    def get_text_input(self):
        """Get text input from user"""
        try:
            user_input = input("💬 Type your command: ").strip()
            if user_input:
                print(f"👤 You typed: {user_input}")
                self.log_interaction("text_input", user_input)
            return user_input.lower()
        except (EOFError, KeyboardInterrupt):
            return "quit"
    
    def log_interaction(self, type, content):
        """Log interactions for history"""
        timestamp = datetime.datetime.now().isoformat()
        self.history.append({
            "timestamp": timestamp,
            "type": type,
            "content": content
        })
        
        # Keep only last 200 interactions
        if len(self.history) > 200:
            self.history = self.history[-200:]
    
    def save_data(self):
        """Save data to JSON file"""
        try:
            data_dir = Path("athena_data")
            data_dir.mkdir(exist_ok=True)
            
            data = {
                "notes": self.notes,
                "reminders": self.reminders,
                "history": self.history[-100:],  # Save only recent history
                "settings": self.settings
            }
            
            with open(data_dir / "athena_data.json", "w", encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Warning: Could not save data: {e}")
    
    def load_data(self):
        """Load data from JSON file"""
        try:
            data_file = Path("athena_data") / "athena_data.json"
            if data_file.exists():
                with open(data_file, "r", encoding='utf-8') as f:
                    data = json.load(f)
                    self.notes = data.get("notes", [])
                    self.reminders = data.get("reminders", [])
                    self.history = data.get("history", [])
                    saved_settings = data.get("settings", {})
                    self.settings.update(saved_settings)
        except Exception as e:
            print(f"Warning: Could not load data: {e}")
    
    # Time and Date Functions
    def get_time(self):
        """Get current time"""
        current_time = datetime.datetime.now()
        time_str = current_time.strftime("The current time is %I:%M %p")
        self.speak(time_str)
    
    def get_date(self):
        """Get current date"""
        current_date = datetime.datetime.now()
        date_str = current_date.strftime("Today is %A, %B %d, %Y")
        self.speak(date_str)
    
    # Math and Calculation Functions
    def calculate(self, expression):
        """Enhanced calculator with more functions"""
        try:
            # Remove command words
            for word in ["athena", "calculate", "math", "compute", "what", "is", "equals"]:
                expression = expression.replace(word, "")
            expression = expression.strip()
            
            if not expression:
                self.speak("Please provide a mathematical expression to calculate.")
                return
            
            # Enhanced safe evaluation
            allowed_names = {
                k: v for k, v in math.__dict__.items() if not k.startswith("__")
            }
            allowed_names.update({
                "abs": abs, "round": round, "min": min, "max": max,
                "sum": sum, "pow": pow, "len": len, "int": int, "float": float
            })
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            self.speak(f"The result of {expression} is {result}")
            
        except Exception as e:
            self.speak("Sorry, I couldn't calculate that. Please check your expression.")
            print(f"Calculation error: {e}")
    
    # Note and Reminder Functions
    def create_note(self, command):
        """Create a note"""
        try:
            note_content = command
            for word in ["athena", "create", "note", "remember", "save", "write"]:
                note_content = note_content.replace(word, "")
            note_content = note_content.strip()
            
            if not note_content:
                self.speak("What would you like me to note?")
                note_content = self.get_text_input()
            
            if note_content and note_content not in ["quit", "cancel", "nevermind"]:
                note = {
                    "id": len(self.notes) + 1,
                    "content": note_content,
                    "timestamp": datetime.datetime.now().isoformat(),
                    "category": "general"
                }
                self.notes.append(note)
                self.save_data()
                self.speak(f"Note saved: {note_content}")
            
        except Exception as e:
            self.speak("Sorry, I couldn't save that note.")
            print(f"Note error: {e}")
    
    def show_notes(self):
        """Show all notes"""
        if not self.notes:
            self.speak("You have no saved notes.")
            return
        
        print(f"\n📝 YOUR NOTES ({len(self.notes)} total):")
        print("=" * 50)
        for note in self.notes[-20:]:  # Show last 20 notes
            timestamp = note["timestamp"][:19].replace("T", " ")
            print(f"{note['id']}. [{timestamp}] {note['content']}")
        
        if len(self.notes) > 20:
            print(f"... and {len(self.notes) - 20} more notes")
        
        self.speak(f"You have {len(self.notes)} saved notes. Recent ones are displayed above.")
    
    def create_reminder(self, command):
        """Create a reminder"""
        try:
            reminder_content = command
            for word in ["athena", "remind", "me", "to", "reminder", "create", "set"]:
                reminder_content = reminder_content.replace(word, "")
            reminder_content = reminder_content.strip()
            
            if not reminder_content:
                self.speak("What would you like me to remind you about?")
                reminder_content = self.get_text_input()
            
            if reminder_content and reminder_content not in ["quit", "cancel", "nevermind"]:
                reminder = {
                    "id": len(self.reminders) + 1,
                    "content": reminder_content,
                    "created": datetime.datetime.now().isoformat(),
                    "completed": False,
                    "priority": "normal"
                }
                self.reminders.append(reminder)
                self.save_data()
                self.speak(f"Reminder created: {reminder_content}")
            
        except Exception as e:
            self.speak("Sorry, I couldn't create that reminder.")
            print(f"Reminder error: {e}")
    
    def show_reminders(self):
        """Show all active reminders"""
        active_reminders = [r for r in self.reminders if not r["completed"]]
        
        if not active_reminders:
            self.speak("You have no active reminders.")
            return
        
        print(f"\n⏰ YOUR ACTIVE REMINDERS ({len(active_reminders)} total):")
        print("=" * 50)
        for reminder in active_reminders:
            timestamp = reminder["created"][:19].replace("T", " ")
            print(f"{reminder['id']}. [{timestamp}] {reminder['content']}")
        
        self.speak(f"You have {len(active_reminders)} active reminders. Check above for details.")
    
    # Entertainment Functions
    def tell_joke(self):
        """Tell a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the math book look so sad? Because it had too many problems!",
            "What do you call a fake noodle? An impasta!",
            "Why don't programmers like nature? It has too many bugs!",
            "What's the best thing about Switzerland? I don't know, but the flag is a big plus!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a sleeping bull? A bulldozer!",
            "Why did the coffee file a police report? It got mugged!"
        ]
        joke = random.choice(jokes)
        self.speak(joke)
    
    def flip_coin(self):
        """Flip a coin"""
        result = random.choice(["Heads", "Tails"])
        self.speak(f"🪙 The coin landed on {result}!")
    
    def roll_dice(self, command):
        """Roll dice with optional number specification"""
        try:
            words = command.split()
            num_dice = 1
            sides = 6
            
            # Look for number of dice
            for i, word in enumerate(words):
                if word.isdigit():
                    num_dice = int(word)
                    break
            
            # Look for number of sides
            if "sided" in command or "side" in command:
                for i, word in enumerate(words):
                    if word.isdigit() and i > 0 and ("sided" in words[i+1:i+2] or "side" in words[i+1:i+2]):
                        sides = int(word)
                        break
            
            num_dice = max(1, min(10, num_dice))  # Limit 1-10 dice
            sides = max(2, min(100, sides))  # Limit 2-100 sides
            
            results = [random.randint(1, sides) for _ in range(num_dice)]
            
            if num_dice == 1:
                self.speak(f"🎲 The {sides}-sided dice rolled {results[0]}!")
            else:
                total = sum(results)
                results_str = ", ".join(map(str, results))
                self.speak(f"🎲 {num_dice} {sides}-sided dice rolled: {results_str} (Total: {total})")
                
        except Exception:
            result = random.randint(1, 6)
            self.speak(f"🎲 The dice rolled {result}!")
    
    def random_number(self, command):
        """Generate random number with optional range"""
        try:
            words = command.split()
            if "between" in words:
                idx = words.index("between")
                if idx + 3 < len(words) and words[idx + 2] == "and":
                    start = int(words[idx + 1])
                    end = int(words[idx + 3])
                    result = random.randint(start, end)
                    self.speak(f"🔢 Random number between {start} and {end}: {result}")
                    return
            
            # Default random number 1-100
            result = random.randint(1, 100)
            self.speak(f"🔢 Random number: {result}")
            
        except Exception:
            result = random.randint(1, 100)
            self.speak(f"🔢 Random number: {result}")
    
    def get_random_fact(self):
        """Share a random interesting fact"""
        facts = [
            "The Earth is approximately 4.54 billion years old.",
            "Water boils at 100 degrees Celsius at sea level.",
            "The speed of light is approximately 299,792,458 meters per second.",
            "There are 7 continents on Earth.",
            "The human body has 206 bones in adults.",
            "DNA stands for Deoxyribonucleic Acid.",
            "The periodic table has 118 known elements.",
            "Photosynthesis is the process by which plants make food using sunlight.",
            "A group of flamingos is called a 'flamboyance'.",
            "Honey never spoils - archaeologists have found edible honey in ancient Egyptian tombs.",
            "The shortest war in history lasted only 38-45 minutes.",
            "Bananas are berries, but strawberries aren't.",
            "A single cloud can weigh more than a million pounds.",
            "Octopuses have three hearts and blue blood.",
            "The Great Wall of China isn't visible from space with the naked eye.",
            "A group of pandas is called an 'embarrassment'.",
            "The human brain uses about 20% of the body's total energy.",
            "Lightning strikes the Earth about 100 times per second.",
            "The longest recorded flight of a chicken is 13 seconds.",
            "Sharks have been around longer than trees."
        ]
        
        fact = random.choice(facts)
        self.speak(f"🧠 Here's an interesting fact: {fact}")
    
    def show_history(self):
        """Show interaction history"""
        if not self.history:
            self.speak("No interaction history available.")
            return
        
        print(f"\n📊 RECENT INTERACTIONS ({len(self.history)} total):")
        print("=" * 60)
        
        recent_history = self.history[-30:]  # Show last 30 interactions
        for i, interaction in enumerate(recent_history, 1):
            timestamp = interaction["timestamp"][:19].replace("T", " ")
            type_icon = "👤" if "input" in interaction["type"] else "🤖"
            content = interaction["content"][:80] + "..." if len(interaction["content"]) > 80 else interaction["content"]
            print(f"{i}. [{timestamp}] {type_icon} {content}")
        
        self.speak("Recent interaction history displayed above.")
    
    def toggle_tts(self):
        """Toggle text-to-speech on/off"""
        if not TEXT_TO_SPEECH_AVAILABLE:
            print("🔊 Text-to-speech is not available on this system.")
            return
        
        self.tts_enabled = not self.tts_enabled
        self.settings["tts_enabled"] = self.tts_enabled
        self.save_data()
        
        status = "enabled" if self.tts_enabled else "disabled"
        message = f"Text-to-speech {status}."
        
        if self.tts_enabled:
            self.speak(message)
        else:
            print(f"🤖 Athena: {message}")
    
    def show_help(self):
        """Show available commands"""
        help_text = f"""
🤖 PC ATHENA AI ASSISTANT - HELP (NO VOICE INPUT VERSION)
{'='*60}

⏰ TIME & DATE:
• "athena time" - Current time
• "athena date" - Current date  
• "athena datetime" - Detailed date/time info

🧮 MATH & CONVERSIONS:
• "athena calculate 2 + 2" - Basic calculations
• "athena convert 100 celsius to fahrenheit" - Unit conversions
• Supported: temperature, length, weight conversions

📝 NOTES & REMINDERS:
• "athena create note [content]" - Save a note
• "athena show notes" - Display all notes
• "athena remind me to [task]" - Create reminder
• "athena show reminders" - Display active reminders

🎲 ENTERTAINMENT & RANDOM:
• "athena joke" - Tell a joke
• "athena flip coin" - Flip a coin
• "athena roll dice" or "athena roll 3 dice" - Roll dice
• "athena random number" - Random number 1-100
• "athena random number between 1 and 50" - Random in range
• "athena random fact" - Share an interesting fact

📊 SYSTEM FEATURES:
• "athena history" - Show recent interactions
• "athena toggle speech" - Enable/disable text-to-speech {'✅' if TEXT_TO_SPEECH_AVAILABLE else '❌ (not available)'}

🎛️ CONTROL:
• "athena help" - Show this help
• "quit", "exit", "goodbye" - Stop Athena

💡 EXAMPLES:
• athena calculate sqrt(144) + 5
• athena create note Buy groceries tomorrow
• athena remind me to call dentist
• athena roll 2 6-sided dice

🔊 TEXT-TO-SPEECH:
• {'Available - Athena will speak responses' if self.tts_enabled else 'Disabled - Athena will only display text'}
• Toggle with "athena toggle speech"

💾 DATA: Your notes, reminders, and history are automatically saved!
"""
        print(help_text)
        self.speak("Complete help displayed above. What would you like to do?")
    
    def process_command(self, command):
        """Process user command with enhanced parsing"""
        if not command:
            return
        
        original_command = command
        
        # Handle quit commands
        if command in ["quit", "exit", "goodbye", "bye", "stop", "shutdown"]:
            self.save_data()
            self.speak("Goodbye! Thanks for using PC Athena AI Assistant!")
            self.running = False
            return
        
        # Check for wake word (optional)
        if self.wake_word not in command and command not in ["help"]:
            command = f"{self.wake_word} {command}"
        
        # Process commands
        try:
            if "time" in command and "date" not in command:
                self.get_time()
            
            elif "date" in command and "time" not in command:
                self.get_date()
            
            elif "calculate" in command or "math" in command or any(op in command for op in ["+", "-", "*", "/", "sqrt", "pow", "sin", "cos"]):
                self.calculate(command)
            
            elif ("create" in command and "note" in command) or ("remember" in command and "note" not in command):
                self.create_note(original_command)
            
            elif "show" in command and "note" in command:
                self.show_notes()
            
            elif "remind" in command and "me" in command:
                self.create_reminder(original_command)
            
            elif "show" in command and "reminder" in command:
                self.show_reminders()
            
            elif "joke" in command:
                self.tell_joke()
            
            elif "flip" in command and "coin" in command:
                self.flip_coin()
            
            elif "roll" in command and ("dice" in command or "die" in command):
                self.roll_dice(command)
            
            elif "random" in command and "number" in command:
                self.random_number(command)
            
            elif "random" in command and "fact" in command:
                self.get_random_fact()
            
            elif "history" in command:
                self.show_history()
            
            elif "toggle" in command and ("speech" in command or "tts" in command):
                self.toggle_tts()
            
            elif "help" in command:
                self.show_help()
            
            else:
                suggestions = [
                    "Try 'athena help' for available commands",
                    "Say 'athena time' for current time",
                    "Use 'athena calculate' for math",
                    "Try 'athena joke' for entertainment"
                ]
                suggestion = random.choice(suggestions)
                self.speak(f"I didn't understand that command. {suggestion}")
        
        except Exception as e:
            self.speak("Sorry, something went wrong processing that command.")
            print(f"Command processing error: {e}")
    
    def run(self):
        """Main application loop"""
        # Startup greeting
        hour = datetime.datetime.now().hour
        if 6 <= hour < 12:
            greeting = "Good morning!"
        elif 12 <= hour < 18:
            greeting = "Good afternoon!"
        elif 18 <= hour < 24:
            greeting = "Good evening!"
        else:
            greeting = "Good night!"
        
        self.speak(f"{greeting} I'm PC Athena, your AI assistant.")
        
        # Show quick stats
        note_count = len(self.notes)
        reminder_count = len([r for r in self.reminders if not r["completed"]])
        
        if note_count > 0 or reminder_count > 0:
            self.speak(f"You have {note_count} notes and {reminder_count} active reminders.")
        
        self.speak(f"I'm ready for text commands. Type 'athena help' for available commands or 'quit' to exit.")
        
        while self.running:
            try:
                command = self.get_text_input()
                if command:
                    self.process_command(command)
                else:
                    time.sleep(0.1)  # Small delay to prevent high CPU usage
                    
            except KeyboardInterrupt:
                self.save_data()
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"Runtime error: {e}")
                self.speak("Something went wrong. Please try again.")

def main():
    """Main entry point"""
    try:
        print("🚀 Starting PC Athena AI Assistant (No Voice Input Version)...")
        athena = PCAthenaNoVoice()
        athena.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Critical error: {e}")
        print("Please check your Python environment and try again.")

if __name__ == "__main__":
    main()