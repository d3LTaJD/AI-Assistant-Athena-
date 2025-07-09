#!/usr/bin/env python3
"""
Simple Athena AI Assistant for WebContainer
Minimal version with basic functionality that works in any Python environment
"""

import sys
import os
import time
import datetime
import random
import math
import json

class SimpleAthena:
    def __init__(self):
        self.running = True
        self.wake_word = "athena"
        print("🤖 Simple Athena AI Assistant")
        print("=" * 40)
        print("✅ Basic functionality available")
        print("💬 Type your commands (no voice recognition)")
        
    def speak(self, text):
        """Print response (simulated speech)"""
        print(f"🤖 Athena: {text}")
    
    def get_input(self):
        """Get user input"""
        try:
            return input("👤 You: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return "quit"
    
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
    
    def calculate(self, expression):
        """Simple calculator"""
        try:
            # Remove command words
            for word in ["athena", "calculate", "math", "compute"]:
                expression = expression.replace(word, "")
            expression = expression.strip()
            
            if not expression:
                self.speak("Please provide a mathematical expression to calculate.")
                return
            
            # Safe evaluation
            allowed_names = {
                k: v for k, v in math.__dict__.items() if not k.startswith("__")
            }
            allowed_names.update({
                "abs": abs, "round": round, "min": min, "max": max,
                "sum": sum, "pow": pow
            })
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            self.speak(f"The result of {expression} is {result}")
            
        except Exception as e:
            self.speak("Sorry, I couldn't calculate that. Please check your expression.")
            print(f"Calculation error: {e}")
    
    def tell_joke(self):
        """Tell a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the math book look so sad? Because it had too many problems!",
            "What do you call a fake noodle? An impasta!",
            "Why don't programmers like nature? It has too many bugs!",
            "What's the best thing about Switzerland? I don't know, but the flag is a big plus!"
        ]
        joke = random.choice(jokes)
        self.speak(joke)
    
    def flip_coin(self):
        """Flip a coin"""
        result = random.choice(["Heads", "Tails"])
        self.speak(f"The coin landed on {result}!")
    
    def roll_dice(self):
        """Roll a dice"""
        result = random.randint(1, 6)
        self.speak(f"The dice rolled {result}!")
    
    def random_number(self, command):
        """Generate random number"""
        try:
            # Try to extract range from command
            words = command.split()
            if "between" in words:
                idx = words.index("between")
                if idx + 3 < len(words) and words[idx + 2] == "and":
                    start = int(words[idx + 1])
                    end = int(words[idx + 3])
                    result = random.randint(start, end)
                    self.speak(f"Random number between {start} and {end}: {result}")
                    return
            
            # Default random number 1-100
            result = random.randint(1, 100)
            self.speak(f"Random number: {result}")
            
        except Exception:
            result = random.randint(1, 100)
            self.speak(f"Random number: {result}")
    
    def show_help(self):
        """Show available commands"""
        help_text = """
🤖 SIMPLE ATHENA COMMANDS:

⏰ TIME & DATE:
- "athena time" - Current time
- "athena date" - Current date

🧮 MATH:
- "athena calculate 2 + 2" - Basic calculations
- "athena math 5 * 7" - Mathematical operations

🎲 RANDOM:
- "athena joke" - Tell a joke
- "athena flip coin" - Flip a coin
- "athena roll dice" - Roll a dice
- "athena random number" - Random number 1-100
- "athena random number between 1 and 50" - Random in range

ℹ️ SYSTEM:
- "athena help" - Show this help
- "quit" or "exit" - Stop Athena

💡 EXAMPLES:
- athena time
- athena calculate 15 + 25
- athena joke
- athena random number between 10 and 20
"""
        print(help_text)
        self.speak("Help displayed above. What would you like to do?")
    
    def process_command(self, command):
        """Process user command"""
        if not command:
            return
        
        # Handle quit commands
        if command in ["quit", "exit", "goodbye", "bye"]:
            self.speak("Goodbye! Thanks for using Simple Athena!")
            self.running = False
            return
        
        # Check for wake word (optional for simple version)
        if self.wake_word not in command and command not in ["help"]:
            # Allow commands without wake word for simplicity
            command = f"{self.wake_word} {command}"
        
        # Process commands
        if "time" in command:
            self.get_time()
        
        elif "date" in command:
            self.get_date()
        
        elif "calculate" in command or "math" in command:
            self.calculate(command)
        
        elif "joke" in command:
            self.tell_joke()
        
        elif "flip" in command and "coin" in command:
            self.flip_coin()
        
        elif "roll" in command and "dice" in command:
            self.roll_dice()
        
        elif "random" in command and "number" in command:
            self.random_number(command)
        
        elif "help" in command:
            self.show_help()
        
        else:
            self.speak("I didn't understand that. Type 'help' for available commands.")
    
    def run(self):
        """Main loop"""
        self.speak("Hello! I'm Simple Athena. Type 'help' for commands or 'quit' to exit.")
        
        while self.running:
            try:
                command = self.get_input()
                self.process_command(command)
            except KeyboardInterrupt:
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                self.speak("Something went wrong. Please try again.")

def main():
    """Main entry point"""
    athena = SimpleAthena()
    athena.run()

if __name__ == "__main__":
    main()