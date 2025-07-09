#!/usr/bin/env python3
"""
Enhanced Simple Athena AI Assistant for WebContainer
More features while maintaining WebContainer compatibility
"""

import sys
import os
import time
import datetime
import random
import math
import json
from pathlib import Path

class EnhancedSimpleAthena:
    def __init__(self):
        self.running = True
        self.wake_word = "athena"
        self.notes = []
        self.reminders = []
        self.history = []
        self.load_data()
        
        print("🤖 Enhanced Simple Athena AI Assistant")
        print("=" * 50)
        print("✅ Enhanced functionality available")
        print("💾 Data persistence enabled")
        print("💬 Type your commands (no voice recognition needed)")
        
    def speak(self, text):
        """Print response (simulated speech)"""
        print(f"🤖 Athena: {text}")
        self.log_interaction("response", text)
    
    def get_input(self):
        """Get user input"""
        try:
            user_input = input("👤 You: ").strip()
            if user_input:
                self.log_interaction("input", user_input)
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
        
        # Keep only last 100 interactions
        if len(self.history) > 100:
            self.history = self.history[-100:]
    
    def save_data(self):
        """Save data to JSON file"""
        try:
            data = {
                "notes": self.notes,
                "reminders": self.reminders,
                "history": self.history[-50:]  # Save only recent history
            }
            with open("athena_data.json", "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save data: {e}")
    
    def load_data(self):
        """Load data from JSON file"""
        try:
            if os.path.exists("athena_data.json"):
                with open("athena_data.json", "r") as f:
                    data = json.load(f)
                    self.notes = data.get("notes", [])
                    self.reminders = data.get("reminders", [])
                    self.history = data.get("history", [])
        except Exception as e:
            print(f"Warning: Could not load data: {e}")
    
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
        info = f"""Current date and time information:
- Date: {now.strftime('%A, %B %d, %Y')}
- Time: {now.strftime('%I:%M:%S %p')}
- Day of year: {now.timetuple().tm_yday}
- Week number: {now.isocalendar()[1]}
- Timezone: {now.astimezone().tzinfo}"""
        
        print(info)
        self.speak("Detailed date and time information displayed above.")
    
    def calculate(self, expression):
        """Enhanced calculator with more functions"""
        try:
            # Remove command words
            for word in ["athena", "calculate", "math", "compute", "what", "is"]:
                expression = expression.replace(word, "")
            expression = expression.strip()
            
            if not expression:
                self.speak("Please provide a mathematical expression to calculate.")
                return
            
            # Enhanced safe evaluation with more math functions
            allowed_names = {
                k: v for k, v in math.__dict__.items() if not k.startswith("__")
            }
            allowed_names.update({
                "abs": abs, "round": round, "min": min, "max": max,
                "sum": sum, "pow": pow, "len": len
            })
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            self.speak(f"The result of {expression} is {result}")
            
            # Save calculation to history
            calc_record = {
                "expression": expression,
                "result": result,
                "timestamp": datetime.datetime.now().isoformat()
            }
            
        except Exception as e:
            self.speak("Sorry, I couldn't calculate that. Please check your expression.")
            print(f"Calculation error: {e}")
    
    def unit_converter(self, command):
        """Convert between different units"""
        try:
            words = command.split()
            
            # Find conversion pattern: "convert X Y to Z"
            if "convert" in words and "to" in words:
                convert_idx = words.index("convert")
                to_idx = words.index("to")
                
                if convert_idx + 3 <= to_idx:
                    value = float(words[convert_idx + 1])
                    from_unit = words[convert_idx + 2]
                    to_unit = words[to_idx + 1] if to_idx + 1 < len(words) else ""
                    
                    # Temperature conversions
                    if from_unit == "celsius" and to_unit == "fahrenheit":
                        result = (value * 9/5) + 32
                        self.speak(f"{value}°C = {result:.2f}°F")
                    elif from_unit == "fahrenheit" and to_unit == "celsius":
                        result = (value - 32) * 5/9
                        self.speak(f"{value}°F = {result:.2f}°C")
                    
                    # Length conversions
                    elif from_unit == "meters" and to_unit == "feet":
                        result = value * 3.28084
                        self.speak(f"{value} meters = {result:.2f} feet")
                    elif from_unit == "feet" and to_unit == "meters":
                        result = value / 3.28084
                        self.speak(f"{value} feet = {result:.2f} meters")
                    elif from_unit == "kilometers" and to_unit == "miles":
                        result = value * 0.621371
                        self.speak(f"{value} km = {result:.2f} miles")
                    elif from_unit == "miles" and to_unit == "kilometers":
                        result = value / 0.621371
                        self.speak(f"{value} miles = {result:.2f} km")
                    
                    # Weight conversions
                    elif from_unit == "kg" and to_unit == "pounds":
                        result = value * 2.20462
                        self.speak(f"{value} kg = {result:.2f} pounds")
                    elif from_unit == "pounds" and to_unit == "kg":
                        result = value / 2.20462
                        self.speak(f"{value} pounds = {result:.2f} kg")
                    
                    else:
                        self.speak(f"Sorry, I don't know how to convert {from_unit} to {to_unit}")
                else:
                    self.speak("Please use format: convert [number] [from_unit] to [to_unit]")
            else:
                self.speak("Please use format: convert [number] [from_unit] to [to_unit]")
                
        except Exception as e:
            self.speak("Sorry, I couldn't perform that conversion. Please check your format.")
            print(f"Conversion error: {e}")
    
    def create_note(self, command):
        """Create a note"""
        try:
            # Extract note content after "note" or "remember"
            note_content = command
            for word in ["athena", "create", "note", "remember", "save"]:
                note_content = note_content.replace(word, "")
            note_content = note_content.strip()
            
            if not note_content:
                self.speak("What would you like me to note?")
                note_content = self.get_input()
            
            if note_content and note_content != "quit":
                note = {
                    "id": len(self.notes) + 1,
                    "content": note_content,
                    "timestamp": datetime.datetime.now().isoformat()
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
        
        print("\n📝 YOUR NOTES:")
        print("=" * 30)
        for note in self.notes:
            timestamp = note["timestamp"][:19]  # Remove microseconds
            print(f"{note['id']}. [{timestamp}] {note['content']}")
        
        self.speak(f"You have {len(self.notes)} saved notes. Check above for details.")
    
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
                reminder_content = self.get_input()
            
            if reminder_content and reminder_content != "quit":
                reminder = {
                    "id": len(self.reminders) + 1,
                    "content": reminder_content,
                    "created": datetime.datetime.now().isoformat(),
                    "completed": False
                }
                self.reminders.append(reminder)
                self.save_data()
                self.speak(f"Reminder created: {reminder_content}")
            
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
            timestamp = reminder["created"][:19]
            print(f"{reminder['id']}. [{timestamp}] {reminder['content']}")
        
        self.speak(f"You have {len(active_reminders)} active reminders. Check above for details.")
    
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
            # Check for number of dice
            words = command.split()
            num_dice = 1
            
            for i, word in enumerate(words):
                if word.isdigit():
                    num_dice = int(word)
                    break
            
            if num_dice > 10:
                num_dice = 10  # Limit to prevent spam
            
            results = [random.randint(1, 6) for _ in range(num_dice)]
            
            if num_dice == 1:
                self.speak(f"🎲 The dice rolled {results[0]}!")
            else:
                total = sum(results)
                results_str = ", ".join(map(str, results))
                self.speak(f"🎲 {num_dice} dice rolled: {results_str} (Total: {total})")
                
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
            
            # Default length
            length = 12
            
            # Try to extract length from command
            words = command.split()
            for word in words:
                if word.isdigit():
                    length = int(word)
                    break
            
            # Limit length
            length = max(4, min(50, length))
            
            # Generate password
            characters = string.ascii_letters + string.digits + "!@#$%^&*"
            password = ''.join(random.choice(characters) for _ in range(length))
            
            print(f"🔐 Generated password ({length} characters): {password}")
            self.speak(f"Generated a {length}-character password. Check above for the password.")
            
        except Exception as e:
            self.speak("Sorry, I couldn't generate a password.")
            print(f"Password error: {e}")
    
    def show_history(self):
        """Show interaction history"""
        if not self.history:
            self.speak("No interaction history available.")
            return
        
        print("\n📊 RECENT INTERACTIONS:")
        print("=" * 40)
        
        recent_history = self.history[-20:]  # Show last 20 interactions
        for i, interaction in enumerate(recent_history, 1):
            timestamp = interaction["timestamp"][:19]
            type_icon = "👤" if interaction["type"] == "input" else "🤖"
            content = interaction["content"][:60] + "..." if len(interaction["content"]) > 60 else interaction["content"]
            print(f"{i}. [{timestamp}] {type_icon} {content}")
        
        self.speak("Recent interaction history displayed above.")
    
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
            "The smallest unit of matter is an atom.",
            "Gravity is a fundamental force of nature.",
            "A group of flamingos is called a 'flamboyance'.",
            "Honey never spoils - archaeologists have found edible honey in ancient Egyptian tombs.",
            "The shortest war in history lasted only 38-45 minutes.",
            "Bananas are berries, but strawberries aren't.",
            "A single cloud can weigh more than a million pounds."
        ]
        
        fact = random.choice(facts)
        self.speak(f"🧠 Here's an interesting fact: {fact}")
    
    def show_help(self):
        """Show available commands"""
        help_text = """
🤖 ENHANCED SIMPLE ATHENA COMMANDS:

⏰ TIME & DATE:
- "athena time" - Current time
- "athena date" - Current date  
- "athena datetime" - Detailed date/time info

🧮 MATH & CONVERSIONS:
- "athena calculate 2 + 2" - Basic calculations
- "athena convert 100 celsius to fahrenheit" - Unit conversions
- Supported conversions: temperature, length, weight

📝 NOTES & REMINDERS:
- "athena create note [content]" - Save a note
- "athena show notes" - Display all notes
- "athena remind me to [task]" - Create reminder
- "athena show reminders" - Display active reminders

🎲 RANDOM & FUN:
- "athena joke" - Tell a joke
- "athena flip coin" - Flip a coin
- "athena roll dice" or "athena roll 3 dice" - Roll dice
- "athena random number" - Random number 1-100
- "athena random number between 1 and 50" - Random in range
- "athena random fact" - Share an interesting fact
- "athena generate password" or "athena generate password 16" - Create password

📊 SYSTEM:
- "athena history" - Show recent interactions
- "athena help" - Show this help
- "quit" or "exit" - Stop Athena

💡 EXAMPLES:
- athena calculate sqrt(144) + 5
- athena convert 5 feet to meters
- athena create note Buy groceries tomorrow
- athena remind me to call dentist
- athena generate password 20
- athena roll 2 dice

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
        if command in ["quit", "exit", "goodbye", "bye", "stop"]:
            self.save_data()
            self.speak("Goodbye! Thanks for using Enhanced Simple Athena!")
            self.running = False
            return
        
        # Check for wake word (optional for simple version)
        if self.wake_word not in command and command not in ["help"]:
            command = f"{self.wake_word} {command}"
        
        # Process commands with enhanced matching
        if "time" in command and "date" not in command:
            self.get_time()
        
        elif "date" in command and "time" not in command:
            self.get_date()
        
        elif "datetime" in command or ("date" in command and "time" in command):
            self.get_datetime_info()
        
        elif "calculate" in command or "math" in command or any(op in command for op in ["+", "-", "*", "/", "sqrt", "pow"]):
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
        
        elif "roll" in command and "dice" in command:
            self.roll_dice(command)
        
        elif "random" in command and "number" in command:
            self.random_number(command)
        
        elif "random" in command and "fact" in command:
            self.get_random_fact()
        
        elif "generate" in command and "password" in command:
            self.generate_password(command)
        
        elif "history" in command:
            self.show_history()
        
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
            self.speak(f"I didn't understand that. {suggestion}")
    
    def run(self):
        """Main loop with enhanced startup"""
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
        
        self.speak(f"{greeting} I'm Enhanced Simple Athena.")
        
        # Show quick stats
        note_count = len(self.notes)
        reminder_count = len([r for r in self.reminders if not r["completed"]])
        
        if note_count > 0 or reminder_count > 0:
            self.speak(f"You have {note_count} notes and {reminder_count} active reminders.")
        
        self.speak("Type 'help' for commands or 'quit' to exit. What can I help you with?")
        
        while self.running:
            try:
                command = self.get_input()
                self.process_command(command)
            except KeyboardInterrupt:
                self.save_data()
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                self.speak("Something went wrong. Please try again.")

def main():
    """Main entry point"""
    try:
        athena = EnhancedSimpleAthena()
        athena.run()
    except Exception as e:
        print(f"❌ Critical error: {e}")
        print("Please check your Python environment and try again.")

if __name__ == "__main__":
    main()