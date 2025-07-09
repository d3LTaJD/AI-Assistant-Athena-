#!/usr/bin/env python3
"""
PC-Compatible Athena AI Assistant
Complete version designed to work on Windows/Mac/Linux with proper error handling
"""

import sys
import os
import json
import time
import datetime
import random
import math
import platform
from pathlib import Path

# Try to import optional modules with fallbacks
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("⚠️ Speech recognition not available. Install with: pip install SpeechRecognition pyaudio")

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

try:
    import pyautogui
    SCREENSHOT_AVAILABLE = True
except ImportError:
    SCREENSHOT_AVAILABLE = False
    print("⚠️ Screenshot feature not available. Install with: pip install pyautogui")

class PCAthena:
    def __init__(self):
        self.running = True
        self.wake_word = "athena"
        self.voice_enabled = SPEECH_RECOGNITION_AVAILABLE
        self.tts_enabled = TEXT_TO_SPEECH_AVAILABLE
        
        # Data storage
        self.notes = []
        self.reminders = []
        self.history = []
        self.settings = {
            "voice_enabled": self.voice_enabled,
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
        
        print("🤖 PC Athena AI Assistant")
        print("=" * 50)
        print(f"🖥️ Platform: {platform.system()} {platform.release()}")
        print(f"🎤 Voice Input: {'✅ Available' if self.voice_enabled else '❌ Not Available'}")
        print(f"🔊 Text-to-Speech: {'✅ Available' if self.tts_enabled else '❌ Not Available'}")
        print(f"🌐 Internet Features: {'✅ Available' if REQUESTS_AVAILABLE else '❌ Limited'}")
        print(f"📸 Screenshot: {'✅ Available' if SCREENSHOT_AVAILABLE else '❌ Not Available'}")
    
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
    
    def get_voice_input(self):
        """Get voice input with fallback to text"""
        if not self.voice_enabled:
            return self.get_text_input()
        
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("🎤 Listening... (or press Ctrl+C for text input)")
                r.adjust_for_ambient_noise(source, duration=1)
                r.pause_threshold = 1
                
                try:
                    audio = r.listen(source, timeout=5, phrase_time_limit=10)
                    print("🔄 Processing...")
                    
                    query = r.recognize_google(audio, language='en-US')
                    print(f"👤 You said: {query}")
                    self.log_interaction("voice_input", query)
                    return query.lower()
                    
                except sr.UnknownValueError:
                    print("❌ Could not understand audio")
                    return self.get_text_input()
                except sr.RequestError as e:
                    print(f"❌ Speech recognition error: {e}")
                    return self.get_text_input()
                    
        except KeyboardInterrupt:
            print("\n💬 Switching to text input...")
            return self.get_text_input()
        except Exception as e:
            print(f"Voice input error: {e}")
            return self.get_text_input()
    
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
    
    def get_input(self):
        """Get input (voice or text based on availability)"""
        if self.voice_enabled:
            return self.get_voice_input()
        else:
            return self.get_text_input()
    
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
    
    def get_datetime_info(self):
        """Get detailed date and time information"""
        now = datetime.datetime.now()
        info = f"""📅 Current Date & Time Information:
• Date: {now.strftime('%A, %B %d, %Y')}
• Time: {now.strftime('%I:%M:%S %p')}
• Day of year: {now.timetuple().tm_yday}
• Week number: {now.isocalendar()[1]}
• Unix timestamp: {int(now.timestamp())}"""
        
        print(info)
        self.speak("Detailed date and time information displayed.")
    
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
    
    def unit_converter(self, command):
        """Convert between different units"""
        try:
            words = command.split()
            
            if "convert" in words and "to" in words:
                convert_idx = words.index("convert")
                to_idx = words.index("to")
                
                if convert_idx + 3 <= to_idx:
                    value = float(words[convert_idx + 1])
                    from_unit = words[convert_idx + 2].lower()
                    to_unit = words[to_idx + 1].lower() if to_idx + 1 < len(words) else ""
                    
                    conversions = {
                        # Temperature
                        ("celsius", "fahrenheit"): lambda x: (x * 9/5) + 32,
                        ("fahrenheit", "celsius"): lambda x: (x - 32) * 5/9,
                        ("celsius", "kelvin"): lambda x: x + 273.15,
                        ("kelvin", "celsius"): lambda x: x - 273.15,
                        
                        # Length
                        ("meters", "feet"): lambda x: x * 3.28084,
                        ("feet", "meters"): lambda x: x / 3.28084,
                        ("kilometers", "miles"): lambda x: x * 0.621371,
                        ("miles", "kilometers"): lambda x: x / 0.621371,
                        ("inches", "centimeters"): lambda x: x * 2.54,
                        ("centimeters", "inches"): lambda x: x / 2.54,
                        
                        # Weight
                        ("kg", "pounds"): lambda x: x * 2.20462,
                        ("pounds", "kg"): lambda x: x / 2.20462,
                        ("grams", "ounces"): lambda x: x * 0.035274,
                        ("ounces", "grams"): lambda x: x / 0.035274,
                    }
                    
                    conversion_key = (from_unit, to_unit)
                    if conversion_key in conversions:
                        result = conversions[conversion_key](value)
                        unit_symbols = {
                            "celsius": "°C", "fahrenheit": "°F", "kelvin": "K",
                            "meters": "m", "feet": "ft", "kilometers": "km", 
                            "miles": "mi", "inches": "in", "centimeters": "cm",
                            "kg": "kg", "pounds": "lbs", "grams": "g", "ounces": "oz"
                        }
                        from_symbol = unit_symbols.get(from_unit, from_unit)
                        to_symbol = unit_symbols.get(to_unit, to_unit)
                        self.speak(f"{value} {from_symbol} equals {result:.2f} {to_symbol}")
                    else:
                        self.speak(f"Sorry, I don't know how to convert {from_unit} to {to_unit}")
                else:
                    self.speak("Please use format: convert [number] [from_unit] to [to_unit]")
            else:
                self.speak("Please use format: convert [number] [from_unit] to [to_unit]")
                
        except Exception as e:
            self.speak("Sorry, I couldn't perform that conversion. Please check your format.")
            print(f"Conversion error: {e}")
    
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
                note_content = self.get_input()
            
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
                reminder_content = self.get_input()
            
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
            "Why did the coffee file a police report? It got mugged!",
            "What do you call a dinosaur that crashes his car? Tyrannosaurus Wrecks!",
            "Why don't skeletons fight each other? They don't have the guts!",
            "What do you call a fish wearing a bowtie? Sofishticated!",
            "Why did the bicycle fall over? Because it was two tired!",
            "What do you call a cow with no legs? Ground beef!"
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
    
    def generate_password(self, command):
        """Generate a secure password"""
        try:
            import string
            
            # Default settings
            length = 12
            include_symbols = True
            
            # Try to extract length from command
            words = command.split()
            for word in words:
                if word.isdigit():
                    length = int(word)
                    break
            
            # Check for no symbols request
            if "no symbols" in command or "without symbols" in command:
                include_symbols = False
            
            # Limit length
            length = max(4, min(50, length))
            
            # Generate password
            characters = string.ascii_letters + string.digits
            if include_symbols:
                characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
            
            password = ''.join(random.choice(characters) for _ in range(length))
            
            print(f"🔐 Generated password ({length} characters): {password}")
            self.speak(f"Generated a {length}-character password. Check the screen for the password.")
            
        except Exception as e:
            self.speak("Sorry, I couldn't generate a password.")
            print(f"Password error: {e}")
    
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
    
    # System Functions
    def take_screenshot(self):
        """Take a screenshot"""
        if not SCREENSHOT_AVAILABLE:
            self.speak("Screenshot feature is not available. Please install pyautogui.")
            return
        
        try:
            screenshots_dir = Path("athena_data") / "screenshots"
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = screenshots_dir / f"screenshot_{timestamp}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            
            self.speak(f"Screenshot saved as {filename.name}")
            print(f"📸 Screenshot saved: {filename}")
            
        except Exception as e:
            self.speak("Sorry, I couldn't take a screenshot.")
            print(f"Screenshot error: {e}")
    
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
    
    def show_system_info(self):
        """Show system information"""
        info = f"""
🖥️ SYSTEM INFORMATION:
{'='*40}
• Operating System: {platform.system()} {platform.release()}
• Architecture: {platform.architecture()[0]}
• Processor: {platform.processor() or 'Unknown'}
• Python Version: {platform.python_version()}
• Hostname: {platform.node()}
• Current Directory: {os.getcwd()}

📊 ATHENA STATUS:
{'='*40}
• Voice Input: {'✅ Available' if self.voice_enabled else '❌ Not Available'}
• Text-to-Speech: {'✅ Available' if self.tts_enabled else '❌ Not Available'}
• Internet Features: {'✅ Available' if REQUESTS_AVAILABLE else '❌ Limited'}
• Screenshot: {'✅ Available' if SCREENSHOT_AVAILABLE else '❌ Not Available'}
• Notes: {len(self.notes)} saved
• Reminders: {len([r for r in self.reminders if not r['completed']])} active
• History: {len(self.history)} interactions
"""
        print(info)
        self.speak("System information displayed above.")
    
    def toggle_voice(self):
        """Toggle voice input on/off"""
        if not SPEECH_RECOGNITION_AVAILABLE:
            self.speak("Voice recognition is not available on this system.")
            return
        
        self.voice_enabled = not self.voice_enabled
        self.settings["voice_enabled"] = self.voice_enabled
        self.save_data()
        
        status = "enabled" if self.voice_enabled else "disabled"
        self.speak(f"Voice input {status}.")
    
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
🤖 PC ATHENA AI ASSISTANT - HELP
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
• "athena generate password" - Create secure password

📸 SYSTEM FEATURES:
• "athena screenshot" - Take a screenshot {'✅' if SCREENSHOT_AVAILABLE else '❌ (not available)'}
• "athena system info" - Show system information
• "athena history" - Show recent interactions
• "athena toggle voice" - Enable/disable voice input {'✅' if SPEECH_RECOGNITION_AVAILABLE else '❌ (not available)'}
• "athena toggle speech" - Enable/disable text-to-speech {'✅' if TEXT_TO_SPEECH_AVAILABLE else '❌ (not available)'}

🎛️ CONTROL:
• "athena help" - Show this help
• "quit", "exit", "goodbye" - Stop Athena

💡 EXAMPLES:
• athena calculate sqrt(144) + 5
• athena convert 5 feet to meters
• athena create note Buy groceries tomorrow
• athena remind me to call dentist
• athena generate password 20
• athena roll 2 6-sided dice
• athena screenshot

🎤 INPUT MODES:
• Voice: {'Available - speak your commands' if self.voice_enabled else 'Not available - use text input'}
• Text: Always available - type your commands

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
            
            elif "datetime" in command or ("date" in command and "time" in command):
                self.get_datetime_info()
            
            elif "calculate" in command or "math" in command or any(op in command for op in ["+", "-", "*", "/", "sqrt", "pow", "sin", "cos"]):
                self.calculate(command)
            
            elif "convert" in command and "to" in command:
                self.unit_converter(command)
            
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
            
            elif "generate" in command and "password" in command:
                self.generate_password(command)
            
            elif "screenshot" in command or "screen shot" in command:
                self.take_screenshot()
            
            elif "system" in command and "info" in command:
                self.show_system_info()
            
            elif "history" in command:
                self.show_history()
            
            elif "toggle" in command and "voice" in command:
                self.toggle_voice()
            
            elif "toggle" in command and ("speech" in command or "tts" in command):
                self.toggle_tts()
            
            elif "help" in command:
                self.show_help()
            
            else:
                suggestions = [
                    "Try 'athena help' for available commands",
                    "Say 'athena time' for current time",
                    "Use 'athena calculate' for math",
                    "Try 'athena joke' for entertainment",
                    "Say 'athena screenshot' to capture your screen"
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
        
        input_method = "voice or text" if self.voice_enabled else "text"
        self.speak(f"I'm ready for {input_method} commands. Say 'athena help' for available commands or 'quit' to exit.")
        
        while self.running:
            try:
                command = self.get_input()
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
        print("🚀 Starting PC Athena AI Assistant...")
        athena = PCAthena()
        athena.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Critical error: {e}")
        print("Please check your Python environment and try again.")

if __name__ == "__main__":
    main()