"""
Command processor for AI Assistant
"""
import os
import webbrowser
import subprocess
import requests
from datetime import datetime
import random
import math
from file_handler import file_handler
from voice_handler import voice_handler
from database import db
from config import config

class CommandProcessor:
    def __init__(self, user_id):
        self.user_id = user_id
        self.last_search_results = None
        self.assistant_name = config.get('assistant_name', 'Assistant')
    
    def process_command(self, command):
        """Process user command and return response"""
        command = command.lower().strip()
        
        try:
            # File/folder operations
            if any(keyword in command for keyword in ['open', 'find', 'search', 'play', 'show']):
                if any(keyword in command for keyword in ['file', 'folder', 'drive', 'downloads', 'documents', 'desktop', 'music', 'videos', 'pictures']):
                    response = self.handle_file_command(command)
                    self.save_interaction(command, str(response))
                    return response
            
            # Handle numbered selections from previous search
            if command.isdigit() and self.last_search_results:
                index = int(command) - 1
                response = file_handler.open_by_index(self.last_search_results, index)
                self.save_interaction(f"Selected option {command}", response)
                return response
            
            # Time and date
            if 'time' in command:
                response = self.get_current_time()
            elif 'date' in command:
                response = self.get_current_date()
            
            # Math calculations
            elif any(op in command for op in ['calculate', 'math', '+', '-', '*', '/', 'equals']):
                response = self.calculate(command)
            
            # System operations
            elif 'shutdown' in command or 'restart' in command:
                response = self.system_control(command)
            
            # Web operations (requires internet)
            elif 'youtube' in command or 'search web' in command:
                response = self.web_search(command)
            elif 'weather' in command:
                response = self.get_weather(command)
            elif 'news' in command:
                response = self.get_news()
            
            # Entertainment
            elif 'joke' in command:
                response = self.tell_joke()
            elif 'flip coin' in command:
                response = self.flip_coin()
            elif 'roll dice' in command:
                response = self.roll_dice()
            
            # Assistant management
            elif 'change name' in command or 'rename' in command:
                response = self.change_assistant_name(command)
            elif 'change voice' in command:
                response = self.change_voice(command)
            
            # Help and information
            elif 'help' in command or 'what can you do' in command:
                response = self.show_help()
            elif 'history' in command:
                response = self.show_history()
            
            # Default response
            else:
                response = self.default_response(command)
            
            # Save interaction to database
            self.save_interaction(command, response)
            return response
            
        except Exception as e:
            error_response = f"Sorry, I encountered an error: {str(e)}"
            self.save_interaction(command, error_response)
            return error_response
    
    def handle_file_command(self, command):
        """Handle file and folder operations"""
        result = file_handler.parse_file_command(command, self.user_id)
        
        if isinstance(result, dict) and result.get('type') == 'multiple_results':
            self.last_search_results = result['results']
            response = result['message'] + "\n"
            for i, path in enumerate(result['results'], 1):
                response += f"{i}. {os.path.basename(path)} ({os.path.dirname(path)})\n"
            response += "\nSay the number to open that file."
            return response
        
        return result
    
    def get_current_time(self):
        """Get current time"""
        now = datetime.now()
        return f"The current time is {now.strftime('%I:%M %p')}"
    
    def get_current_date(self):
        """Get current date"""
        now = datetime.now()
        return f"Today is {now.strftime('%A, %B %d, %Y')}"
    
    def calculate(self, command):
        """Perform mathematical calculations"""
        try:
            # Extract mathematical expression
            expression = command
            for word in ['calculate', 'math', 'what', 'is', 'equals']:
                expression = expression.replace(word, '')
            expression = expression.strip()
            
            # Safe evaluation
            allowed_names = {
                k: v for k, v in math.__dict__.items() if not k.startswith("__")
            }
            allowed_names.update({
                "abs": abs, "round": round, "min": min, "max": max,
                "sum": sum, "pow": pow
            })
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return f"The result is {result}"
            
        except Exception as e:
            return "Sorry, I couldn't calculate that. Please check your expression."
    
    def system_control(self, command):
        """Handle system control commands"""
        if 'shutdown' in command:
            return "I cannot shutdown the system for security reasons. Please do it manually."
        elif 'restart' in command:
            return "I cannot restart the system for security reasons. Please do it manually."
        return "System control command not recognized."
    
    def web_search(self, command):
        """Handle web searches (requires internet)"""
        try:
            if 'youtube' in command:
                search_term = command.replace('youtube', '').replace('search', '').strip()
                url = f"https://www.youtube.com/results?search_query={search_term.replace(' ', '+')}"
                webbrowser.open(url)
                return f"Opened YouTube search for: {search_term}"
            else:
                search_term = command.replace('search web', '').replace('google', '').strip()
                url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}"
                webbrowser.open(url)
                return f"Opened web search for: {search_term}"
        except Exception as e:
            return "Sorry, I couldn't perform the web search. Please check your internet connection."
    
    def get_weather(self, command):
        """Get weather information (requires internet)"""
        return "Weather feature requires internet connection and API setup. This is a placeholder for weather functionality."
    
    def get_news(self):
        """Get news (requires internet)"""
        return "News feature requires internet connection and API setup. This is a placeholder for news functionality."
    
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
        return random.choice(jokes)
    
    def flip_coin(self):
        """Flip a virtual coin"""
        result = random.choice(["Heads", "Tails"])
        return f"The coin landed on {result}!"
    
    def roll_dice(self):
        """Roll a virtual dice"""
        result = random.randint(1, 6)
        return f"The dice rolled {result}!"
    
    def change_assistant_name(self, command):
        """Change assistant name"""
        words = command.split()
        if 'to' in words:
            name_index = words.index('to') + 1
            if name_index < len(words):
                new_name = ' '.join(words[name_index:]).title()
                config.update_assistant_name(new_name)
                self.assistant_name = new_name
                return f"My name has been changed to {new_name}. You can now call me {new_name}!"
        
        return "Please specify the new name. For example: 'change name to Jarvis'"
    
    def change_voice(self, command):
        """Change voice type"""
        if 'male' in command:
            voice_handler.change_voice('male')
            return "Voice changed to male."
        elif 'female' in command:
            voice_handler.change_voice('female')
            return "Voice changed to female."
        else:
            return "Please specify 'male' or 'female' voice."
    
    def show_help(self):
        """Show available commands"""
        help_text = f"""
Hi! I'm {self.assistant_name}. Here's what I can do:

📁 FILE OPERATIONS:
• "Open Downloads folder"
• "Find resume.pdf on C drive"
• "Play music from Music folder"
• "Show pictures from Desktop"

⏰ TIME & DATE:
• "What time is it?"
• "What's today's date?"

🧮 CALCULATIONS:
• "Calculate 15 + 25"
• "What's 2 to the power of 8?"

🌐 WEB (requires internet):
• "Search YouTube for cats"
• "Search web for Python tutorials"
• "Get weather"
• "Show news"

🎮 ENTERTAINMENT:
• "Tell me a joke"
• "Flip a coin"
• "Roll a dice"

⚙️ SETTINGS:
• "Change name to [new name]"
• "Change voice to male/female"
• "Show history"

Just speak naturally or type your commands!
        """
        return help_text.strip()
    
    def show_history(self):
        """Show recent chat history"""
        history = db.get_chat_history(self.user_id, limit=10)
        if not history:
            return "No chat history found."
        
        response = "Recent conversations:\n"
        for prompt, resp, timestamp in history:
            response += f"• {prompt} → {resp[:50]}...\n"
        
        return response
    
    def default_response(self, command):
        """Default response for unrecognized commands"""
        responses = [
            f"I'm not sure how to help with that. Try saying 'help' to see what I can do.",
            f"I didn't understand that command. Would you like to see my available features?",
            f"Sorry, I don't know how to handle that request. Type 'help' for assistance.",
        ]
        return random.choice(responses)
    
    def save_interaction(self, prompt, response):
        """Save interaction to database"""
        try:
            db.save_chat_history(self.user_id, prompt, str(response))
        except Exception as e:
            print(f"Error saving interaction: {e}")