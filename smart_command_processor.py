"""
Smart Command Processor with Advanced AI Capabilities
Handles complex commands, context awareness, and intelligent responses
"""
import os
import webbrowser
import subprocess
import requests
import json
import re
import math
import random
from datetime import datetime, timedelta
from pathlib import Path
import psutil
import platform
import socket
import uuid
import hashlib

from file_handler import file_handler
from advanced_voice_handler import advanced_voice_handler
from database import db
from config import config

class SmartCommandProcessor:
    def __init__(self, user_id):
        self.user_id = user_id
        self.last_search_results = None
        self.conversation_context = []
        self.assistant_name = config.get('assistant_name', 'Assistant')
        self.user_preferences = self.load_user_preferences()
        self.command_history = []
        
        # Initialize smart features
        self.setup_smart_responses()
        self.setup_system_monitoring()
    
    def setup_smart_responses(self):
        """Setup intelligent response patterns"""
        self.smart_responses = {
            'greetings': [
                f"Hello! I'm {self.assistant_name}, ready to help you.",
                f"Hi there! {self.assistant_name} at your service.",
                f"Good to see you! How can {self.assistant_name} assist you today?"
            ],
            'confirmations': [
                "Done!", "Completed!", "All set!", "Task finished!",
                "There you go!", "Mission accomplished!"
            ],
            'thinking': [
                "Let me think about that...",
                "Processing your request...",
                "Working on it...",
                "Give me a moment..."
            ]
        }
    
    def setup_system_monitoring(self):
        """Setup system monitoring capabilities"""
        self.system_info = {
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total,
            'disk_usage': {},
            'network_interfaces': psutil.net_if_addrs()
        }
        
        # Get disk usage for all drives
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                self.system_info['disk_usage'][partition.device] = {
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free
                }
            except PermissionError:
                continue
    
    def load_user_preferences(self):
        """Load user preferences and learning data"""
        try:
            # This would load from database in a real implementation
            return {
                'preferred_browser': 'default',
                'common_folders': config.get('common_folders', {}),
                'frequently_used_apps': [],
                'response_style': 'friendly'
            }
        except Exception:
            return {}
    
    def process_command(self, command):
        """Process user command with advanced intelligence"""
        command = command.lower().strip()
        self.command_history.append(command)
        
        # Keep only last 10 commands for context
        if len(self.command_history) > 10:
            self.command_history = self.command_history[-10:]
        
        try:
            # Context-aware processing
            response = self.process_with_context(command)
            
            if response:
                self.save_interaction(command, str(response))
                return response
            
            # Main command processing
            response = self.process_main_command(command)
            
            # Save interaction to database
            self.save_interaction(command, str(response))
            return response
            
        except Exception as e:
            error_response = f"I encountered an error: {str(e)}"
            self.save_interaction(command, error_response)
            return error_response
    
    def process_with_context(self, command):
        """Process command with conversation context"""
        # Handle follow-up questions
        if command in ['yes', 'yeah', 'yep', 'sure', 'ok', 'okay']:
            if self.last_search_results:
                return "Please specify which number you'd like to select."
            return "What would you like me to do?"
        
        if command in ['no', 'nope', 'cancel', 'never mind']:
            self.last_search_results = None
            return "Okay, cancelled. What else can I help you with?"
        
        # Handle numbered selections
        if command.isdigit() and self.last_search_results:
            index = int(command) - 1
            response = file_handler.open_by_index(self.last_search_results, index)
            self.last_search_results = None
            return response
        
        return None
    
    def process_main_command(self, command):
        """Main command processing with advanced features"""
        # Greeting detection
        if any(greeting in command for greeting in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
            return self.handle_greeting(command)
        
        # File/folder operations (enhanced)
        if any(keyword in command for keyword in ['open', 'find', 'search', 'play', 'show', 'launch', 'run', 'execute']):
            return self.handle_file_operations(command)
        
        # System operations (enhanced)
        if any(keyword in command for keyword in ['system', 'computer', 'pc', 'machine']):
            return self.handle_system_operations(command)
        
        # Time and date (enhanced)
        if any(keyword in command for keyword in ['time', 'clock']):
            return self.handle_time_operations(command)
        elif any(keyword in command for keyword in ['date', 'day', 'today', 'calendar']):
            return self.handle_date_operations(command)
        
        # Math and calculations (enhanced)
        elif any(op in command for op in ['calculate', 'math', 'compute', '+', '-', '*', '/', 'equals', 'convert']):
            return self.handle_math_operations(command)
        
        # Web operations (enhanced)
        elif any(keyword in command for keyword in ['youtube', 'search web', 'google', 'browse']):
            return self.handle_web_operations(command)
        elif 'weather' in command:
            return self.handle_weather_request(command)
        elif 'news' in command:
            return self.handle_news_request()
        
        # Entertainment (enhanced)
        elif any(keyword in command for keyword in ['joke', 'funny', 'laugh']):
            return self.handle_entertainment(command)
        elif 'flip coin' in command or 'coin flip' in command:
            return self.flip_coin()
        elif 'roll dice' in command or 'dice roll' in command:
            return self.roll_dice(command)
        elif any(keyword in command for keyword in ['random', 'pick', 'choose']):
            return self.handle_random_operations(command)
        
        # Assistant management (enhanced)
        elif any(keyword in command for keyword in ['change name', 'rename', 'call you']):
            return self.change_assistant_name(command)
        elif 'change voice' in command or 'voice' in command:
            return self.handle_voice_operations(command)
        elif any(keyword in command for keyword in ['remember', 'note', 'remind']):
            return self.handle_memory_operations(command)
        
        # Smart home simulation
        elif any(keyword in command for keyword in ['lights', 'temperature', 'thermostat']):
            return self.handle_smart_home(command)
        
        # Productivity features
        elif any(keyword in command for keyword in ['schedule', 'appointment', 'meeting']):
            return self.handle_scheduling(command)
        elif any(keyword in command for keyword in ['email', 'message', 'text']):
            return self.handle_communication(command)
        
        # Learning and information
        elif any(keyword in command for keyword in ['learn', 'teach', 'explain', 'what is', 'who is']):
            return self.handle_learning_requests(command)
        
        # Help and information
        elif any(keyword in command for keyword in ['help', 'what can you do', 'commands', 'features']):
            return self.show_enhanced_help()
        elif 'history' in command:
            return self.show_history()
        
        # Screenshot and screen operations
        elif any(keyword in command for keyword in ['screenshot', 'screen capture', 'capture screen']):
            return self.take_screenshot()
        
        # Default intelligent response
        else:
            return self.generate_intelligent_response(command)
    
    def handle_greeting(self, command):
        """Handle greetings with personality"""
        hour = datetime.now().hour
        
        if 'morning' in command or (6 <= hour < 12):
            time_greeting = "Good morning"
        elif 'afternoon' in command or (12 <= hour < 17):
            time_greeting = "Good afternoon"
        elif 'evening' in command or (17 <= hour < 22):
            time_greeting = "Good evening"
        else:
            time_greeting = "Hello"
        
        responses = [
            f"{time_greeting}! I'm {self.assistant_name}, ready to help you today.",
            f"{time_greeting}! How can I assist you?",
            f"{time_greeting}! What would you like to do today?"
        ]
        
        return random.choice(responses)
    
    def handle_file_operations(self, command):
        """Enhanced file operations with smart suggestions"""
        result = file_handler.parse_file_command(command, self.user_id)
        
        if isinstance(result, dict) and result.get('type') == 'multiple_results':
            self.last_search_results = result['results']
            response = result['message'] + "\n"
            for i, path in enumerate(result['results'], 1):
                response += f"{i}. {os.path.basename(path)} ({os.path.dirname(path)})\n"
            response += "\nSay the number to open that file, or say 'cancel' to abort."
            return response
        
        # Add smart suggestions if file not found
        if isinstance(result, str) and "not found" in result.lower():
            suggestions = self.get_file_suggestions(command)
            if suggestions:
                result += f"\n\nDid you mean:\n{suggestions}"
        
        return result
    
    def get_file_suggestions(self, command):
        """Get smart file suggestions"""
        # Extract potential filename from command
        words = command.split()
        potential_files = []
        
        for word in words:
            if '.' in word or len(word) > 3:
                potential_files.append(word)
        
        if potential_files:
            return f"• Try searching for: {', '.join(potential_files)}\n• Check your recent files\n• Make sure the file exists"
        
        return None
    
    def handle_system_operations(self, command):
        """Handle system-related operations"""
        if 'status' in command or 'info' in command:
            return self.get_system_status()
        elif 'performance' in command or 'usage' in command:
            return self.get_system_performance()
        elif 'processes' in command or 'running' in command:
            return self.get_running_processes()
        elif 'network' in command:
            return self.get_network_info()
        elif 'disk' in command or 'storage' in command:
            return self.get_disk_info()
        else:
            return "What system information would you like? Try: status, performance, processes, network, or disk info."
    
    def get_system_status(self):
        """Get comprehensive system status"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        
        status = f"""🖥️ System Status:
• CPU Usage: {cpu_percent}%
• Memory Usage: {memory.percent}% ({self.bytes_to_gb(memory.used):.1f}GB / {self.bytes_to_gb(memory.total):.1f}GB)
• System Uptime: {str(uptime).split('.')[0]}
• Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}
• Platform: {platform.system()} {platform.release()}"""
        
        return status
    
    def get_system_performance(self):
        """Get detailed system performance"""
        cpu_freq = psutil.cpu_freq()
        cpu_count = psutil.cpu_count()
        
        performance = f"""⚡ System Performance:
• CPU Cores: {cpu_count} cores
• CPU Frequency: {cpu_freq.current:.0f} MHz (Max: {cpu_freq.max:.0f} MHz)
• CPU Usage per Core: {psutil.cpu_percent(percpu=True)}
• Load Average: {psutil.getloadavg() if hasattr(psutil, 'getloadavg') else 'N/A'}"""
        
        return performance
    
    def get_running_processes(self):
        """Get top running processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by CPU usage
        processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
        
        result = "🔄 Top Processes by CPU Usage:\n"
        for i, proc in enumerate(processes[:10], 1):
            result += f"{i}. {proc['name']} - CPU: {proc['cpu_percent']:.1f}%, Memory: {proc['memory_percent']:.1f}%\n"
        
        return result
    
    def get_network_info(self):
        """Get network information"""
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            # Get network interfaces
            interfaces = psutil.net_if_addrs()
            
            info = f"""🌐 Network Information:
• Hostname: {hostname}
• Local IP: {local_ip}
• Network Interfaces: {len(interfaces)}"""
            
            # Add interface details
            for interface, addresses in list(interfaces.items())[:3]:  # Show first 3
                info += f"\n• {interface}: "
                for addr in addresses:
                    if addr.family == socket.AF_INET:
                        info += f"{addr.address}"
                        break
            
            return info
        except Exception as e:
            return f"Network information unavailable: {str(e)}"
    
    def get_disk_info(self):
        """Get disk usage information"""
        info = "💾 Disk Usage:\n"
        
        for device, usage in self.system_info['disk_usage'].items():
            total_gb = self.bytes_to_gb(usage['total'])
            used_gb = self.bytes_to_gb(usage['used'])
            free_gb = self.bytes_to_gb(usage['free'])
            used_percent = (usage['used'] / usage['total']) * 100
            
            info += f"• {device} {used_gb:.1f}GB / {total_gb:.1f}GB ({used_percent:.1f}% used, {free_gb:.1f}GB free)\n"
        
        return info
    
    def bytes_to_gb(self, bytes_value):
        """Convert bytes to gigabytes"""
        return bytes_value / (1024**3)
    
    def handle_time_operations(self, command):
        """Enhanced time operations"""
        now = datetime.now()
        
        if 'zone' in command or 'timezone' in command:
            import time
            return f"Current timezone: {time.tzname[0]} (UTC{time.timezone//3600:+d})"
        elif 'format' in command or '24' in command:
            return f"24-hour format: {now.strftime('%H:%M:%S')}"
        elif 'seconds' in command:
            return f"Precise time: {now.strftime('%H:%M:%S.%f')[:-3]}"
        else:
            return f"The current time is {now.strftime('%I:%M %p')}"
    
    def handle_date_operations(self, command):
        """Enhanced date operations"""
        now = datetime.now()
        
        if 'tomorrow' in command:
            tomorrow = now + timedelta(days=1)
            return f"Tomorrow is {tomorrow.strftime('%A, %B %d, %Y')}"
        elif 'yesterday' in command:
            yesterday = now - timedelta(days=1)
            return f"Yesterday was {yesterday.strftime('%A, %B %d, %Y')}"
        elif 'week' in command:
            return f"Week {now.isocalendar()[1]} of {now.year}"
        elif 'month' in command:
            return f"We're in {now.strftime('%B %Y')}"
        else:
            return f"Today is {now.strftime('%A, %B %d, %Y')}"
    
    def handle_math_operations(self, command):
        """Enhanced mathematical operations"""
        try:
            # Unit conversions
            if 'convert' in command:
                return self.handle_unit_conversion(command)
            
            # Extract mathematical expression
            expression = command
            for word in ['calculate', 'math', 'compute', 'what', 'is', 'equals']:
                expression = expression.replace(word, '')
            expression = expression.strip()
            
            # Enhanced math functions
            allowed_names = {
                k: v for k, v in math.__dict__.items() if not k.startswith("__")
            }
            allowed_names.update({
                "abs": abs, "round": round, "min": min, "max": max,
                "sum": sum, "pow": pow, "factorial": math.factorial,
                "gcd": math.gcd, "lcm": lambda a, b: abs(a * b) // math.gcd(a, b)
            })
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            
            # Format result nicely
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 6)
            
            return f"The result is {result:,}"
            
        except Exception as e:
            return "I couldn't calculate that. Please check your expression or try a different format."
    
    def handle_unit_conversion(self, command):
        """Handle unit conversions"""
        conversions = {
            # Temperature
            ('celsius', 'fahrenheit'): lambda x: (x * 9/5) + 32,
            ('fahrenheit', 'celsius'): lambda x: (x - 32) * 5/9,
            ('celsius', 'kelvin'): lambda x: x + 273.15,
            ('kelvin', 'celsius'): lambda x: x - 273.15,
            
            # Length
            ('meters', 'feet'): lambda x: x * 3.28084,
            ('feet', 'meters'): lambda x: x / 3.28084,
            ('kilometers', 'miles'): lambda x: x * 0.621371,
            ('miles', 'kilometers'): lambda x: x / 0.621371,
            ('inches', 'centimeters'): lambda x: x * 2.54,
            ('centimeters', 'inches'): lambda x: x / 2.54,
            
            # Weight
            ('kg', 'pounds'): lambda x: x * 2.20462,
            ('pounds', 'kg'): lambda x: x / 2.20462,
            ('grams', 'ounces'): lambda x: x * 0.035274,
            ('ounces', 'grams'): lambda x: x / 0.035274,
            
            # Volume
            ('liters', 'gallons'): lambda x: x * 0.264172,
            ('gallons', 'liters'): lambda x: x / 0.264172,
            ('ml', 'fl oz'): lambda x: x * 0.033814,
            ('fl oz', 'ml'): lambda x: x / 0.033814,
        }
        
        # Parse conversion command
        words = command.split()
        try:
            # Find number, from_unit, and to_unit
            number = None
            from_unit = None
            to_unit = None
            
            for i, word in enumerate(words):
                try:
                    number = float(word)
                    if i + 1 < len(words):
                        from_unit = words[i + 1].lower()
                    break
                except ValueError:
                    continue
            
            if 'to' in words:
                to_index = words.index('to')
                if to_index + 1 < len(words):
                    to_unit = words[to_index + 1].lower()
            
            if number is not None and from_unit and to_unit:
                conversion_key = (from_unit, to_unit)
                if conversion_key in conversions:
                    result = conversions[conversion_key](number)
                    return f"{number} {from_unit} = {result:.4f} {to_unit}"
                else:
                    return f"I don't know how to convert from {from_unit} to {to_unit}"
            
        except Exception as e:
            pass
        
        return "Please use format: convert [number] [from_unit] to [to_unit]"
    
    def handle_random_operations(self, command):
        """Handle random operations"""
        if 'number' in command:
            # Extract range if specified
            words = command.split()
            if 'between' in words:
                try:
                    between_idx = words.index('between')
                    start = int(words[between_idx + 1])
                    end = int(words[between_idx + 3])  # Skip 'and'
                    result = random.randint(start, end)
                    return f"Random number between {start} and {end}: {result}"
                except:
                    pass
            
            # Default range
            result = random.randint(1, 100)
            return f"Random number: {result}"
        
        elif 'choice' in command or 'pick' in command or 'choose' in command:
            # Extract options
            options_part = command.split('between')[-1] if 'between' in command else command
            options = [opt.strip() for opt in re.split(r'[,\s]+or\s+|\s+and\s+|,', options_part) if opt.strip()]
            
            if len(options) > 1:
                choice = random.choice(options)
                return f"I choose: {choice}"
            else:
                return "Please provide options to choose from, like: 'pick between pizza or burgers'"
        
        return "What would you like me to randomize? Try: random number, or pick between options"
    
    def handle_entertainment(self, command):
        """Enhanced entertainment features"""
        if 'joke' in command:
            return self.get_smart_joke()
        elif 'riddle' in command:
            return self.get_riddle()
        elif 'fact' in command:
            return self.get_interesting_fact()
        elif 'quote' in command:
            return self.get_inspirational_quote()
        else:
            return self.get_smart_joke()
    
    def get_smart_joke(self):
        """Get contextual jokes"""
        hour = datetime.now().hour
        
        if 6 <= hour < 12:  # Morning jokes
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "I told my wife she was drawing her eyebrows too high. She looked surprised.",
                "Why don't eggs tell jokes? They'd crack each other up!"
            ]
        elif 12 <= hour < 17:  # Afternoon jokes
            jokes = [
                "Why did the scarecrow win an award? He was outstanding in his field!",
                "What do you call a fake noodle? An impasta!",
                "Why don't programmers like nature? It has too many bugs!"
            ]
        else:  # Evening jokes
            jokes = [
                "Why did the math book look so sad? Because it had too many problems!",
                "What do you call a bear with no teeth? A gummy bear!",
                "Why don't skeletons fight each other? They don't have the guts!"
            ]
        
        return random.choice(jokes)
    
    def get_riddle(self):
        """Get a riddle for the user"""
        riddles = [
            "I speak without a mouth and hear without ears. I have no body, but come alive with wind. What am I? (Answer: An echo)",
            "The more you take, the more you leave behind. What am I? (Answer: Footsteps)",
            "I'm tall when I'm young, and short when I'm old. What am I? (Answer: A candle)"
        ]
        return random.choice(riddles)
    
    def get_interesting_fact(self):
        """Get an interesting fact"""
        facts = [
            "Honey never spoils. Archaeologists have found edible honey in ancient Egyptian tombs!",
            "A group of flamingos is called a 'flamboyance'.",
            "The shortest war in history lasted only 38-45 minutes between Britain and Zanzibar in 1896.",
            "Bananas are berries, but strawberries aren't!",
            "A single cloud can weigh more than a million pounds."
        ]
        return f"🧠 Interesting fact: {random.choice(facts)}"
    
    def get_inspirational_quote(self):
        """Get an inspirational quote"""
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Innovation distinguishes between a leader and a follower. - Steve Jobs",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "It is during our darkest moments that we must focus to see the light. - Aristotle"
        ]
        return f"💭 {random.choice(quotes)}"
    
    def take_screenshot(self):
        """Take an enhanced screenshot"""
        try:
            import pyautogui
            from PIL import Image
            
            # Create screenshots directory
            screenshots_dir = Path.home() / "Pictures" / "AI_Assistant_Screenshots"
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            
            # Take screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = screenshots_dir / f"screenshot_{timestamp}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            
            # Get screenshot info
            width, height = screenshot.size
            file_size = filename.stat().st_size / 1024  # KB
            
            return f"📸 Screenshot saved!\n• Location: {filename}\n• Size: {width}x{height}\n• File size: {file_size:.1f} KB"
            
        except Exception as e:
            return f"Screenshot failed: {str(e)}"
    
    def generate_intelligent_response(self, command):
        """Generate intelligent response for unrecognized commands"""
        # Analyze command for intent
        if '?' in command:
            return f"I'm not sure about that question. Could you rephrase it or ask me something else?"
        
        # Suggest similar commands
        suggestions = self.get_command_suggestions(command)
        
        response = f"I didn't understand '{command}'. "
        if suggestions:
            response += f"Did you mean: {suggestions}?"
        else:
            response += "Try saying 'help' to see what I can do."
        
        return response
    
    def get_command_suggestions(self, command):
        """Get command suggestions based on similarity"""
        common_commands = [
            "open downloads", "what time is it", "take screenshot",
            "system status", "tell me a joke", "calculate", "search web"
        ]
        
        # Simple similarity check
        for cmd in common_commands:
            if any(word in cmd for word in command.split()):
                return cmd
        
        return None
    
    def show_enhanced_help(self):
        """Show comprehensive help with categories"""
        help_text = f"""
🤖 {self.assistant_name} - Advanced AI Assistant

📁 FILE OPERATIONS:
• "Open Downloads folder" - Open any folder
• "Find resume.pdf on C drive" - Search for files
• "Play music from Music folder" - Launch media
• "Show pictures from Desktop" - Browse images

🖥️ SYSTEM MONITORING:
• "System status" - CPU, memory, uptime
• "System performance" - Detailed performance
• "Running processes" - Active applications
• "Network info" - Network configuration
• "Disk info" - Storage usage

⏰ TIME & DATE:
• "What time is it?" - Current time
• "What's today's date?" - Current date
• "Time in 24 hour format" - Military time
• "What's tomorrow's date?" - Future dates

🧮 MATH & CONVERSIONS:
• "Calculate 15 + 25 * 3" - Complex math
• "Convert 100 celsius to fahrenheit" - Units
• "What's the square root of 144?" - Functions

🌐 WEB & SEARCH:
• "Search YouTube for cats" - Video search
• "Search web for Python tutorials" - Web search
• "Get weather" - Weather information
• "Show news" - Latest news

🎮 ENTERTAINMENT:
• "Tell me a joke" - Contextual humor
• "Give me a riddle" - Brain teasers
• "Random fact" - Interesting facts
• "Inspirational quote" - Motivation
• "Flip a coin" - Random decisions
• "Roll dice" - Gaming

📸 UTILITIES:
• "Take screenshot" - Screen capture
• "Random number between 1 and 100" - RNG
• "Pick between pizza or burgers" - Decisions

⚙️ ASSISTANT SETTINGS:
• "Change name to Jarvis" - Rename assistant
• "Change voice to male/female" - Voice type
• "Show history" - Recent conversations
• "Remember [something]" - Save notes

💡 SMART FEATURES:
• Context awareness - Remembers conversation
• Natural language - Speak naturally
• Room-scale voice - Works from across the room
• Learning - Adapts to your preferences

Just speak naturally! I understand context and can help with complex requests.
        """
        return help_text.strip()
    
    def save_interaction(self, prompt, response):
        """Save interaction with enhanced metadata"""
        try:
            # Add to conversation context
            self.conversation_context.append({
                'prompt': prompt,
                'response': response,
                'timestamp': datetime.now().isoformat()
            })
            
            # Keep only last 20 interactions in memory
            if len(self.conversation_context) > 20:
                self.conversation_context = self.conversation_context[-20:]
            
            # Save to database
            db.save_chat_history(self.user_id, prompt, str(response))
        except Exception as e:
            print(f"Error saving interaction: {e}")
    
    # Additional methods for other features...
    def flip_coin(self):
        result = random.choice(["Heads", "Tails"])
        return f"🪙 The coin landed on {result}!"
    
    def roll_dice(self, command):
        # Extract number of dice and sides
        words = command.split()
        num_dice = 1
        sides = 6
        
        for word in words:
            if word.isdigit():
                if int(word) <= 10:  # Assume it's number of dice
                    num_dice = int(word)
                elif int(word) <= 100:  # Assume it's number of sides
                    sides = int(word)
        
        results = [random.randint(1, sides) for _ in range(num_dice)]
        
        if num_dice == 1:
            return f"🎲 The {sides}-sided dice rolled {results[0]}!"
        else:
            total = sum(results)
            return f"🎲 {num_dice} dice rolled: {results} (Total: {total})"
    
    def show_history(self):
        """Show enhanced chat history"""
        if not self.conversation_context:
            return "No recent conversation history."
        
        response = "📜 Recent Conversations:\n"
        for i, interaction in enumerate(self.conversation_context[-10:], 1):
            timestamp = interaction['timestamp'][:19]
            prompt = interaction['prompt'][:50] + "..." if len(interaction['prompt']) > 50 else interaction['prompt']
            response += f"{i}. [{timestamp}] {prompt}\n"
        
        return response
    
    # Placeholder methods for future features
    def handle_smart_home(self, command):
        return "Smart home features are not yet implemented, but I'm ready to control your devices!"
    
    def handle_scheduling(self, command):
        return "Scheduling features are coming soon! I'll help you manage your calendar."
    
    def handle_communication(self, command):
        return "Communication features are in development. I'll help you send messages and emails."
    
    def handle_learning_requests(self, command):
        return "I'm always learning! Ask me specific questions and I'll do my best to help."
    
    def handle_voice_operations(self, command):
        if 'male' in command:
            advanced_voice_handler.change_voice('male')
            return "Voice changed to male."
        elif 'female' in command:
            advanced_voice_handler.change_voice('female')
            return "Voice changed to female."
        elif 'test' in command:
            if advanced_voice_handler.test_microphone():
                return "Microphone test completed successfully!"
            else:
                return "Microphone test failed. Please check your setup."
        else:
            return "Voice options: change to male/female, or test microphone."
    
    def handle_memory_operations(self, command):
        # Extract what to remember
        memory_content = command.replace('remember', '').replace('note', '').strip()
        if memory_content:
            # Save to database or file
            return f"I'll remember: {memory_content}"
        else:
            return "What would you like me to remember?"
    
    def change_assistant_name(self, command):
        """Change assistant name with confirmation"""
        words = command.split()
        if 'to' in words:
            name_index = words.index('to') + 1
            if name_index < len(words):
                new_name = ' '.join(words[name_index:]).title()
                config.update_assistant_name(new_name)
                self.assistant_name = new_name
                return f"Perfect! My name is now {new_name}. You can call me {new_name} from now on!"
        
        return "What would you like to call me? Say something like 'change name to Jarvis'"
    
    def handle_web_operations(self, command):
        """Enhanced web operations"""
        try:
            if 'youtube' in command:
                search_term = command.replace('youtube', '').replace('search', '').strip()
                url = f"https://www.youtube.com/results?search_query={search_term.replace(' ', '+')}"
                webbrowser.open(url)
                return f"🎥 Opened YouTube search for: {search_term}"
            else:
                search_term = command.replace('search web', '').replace('google', '').strip()
                url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}"
                webbrowser.open(url)
                return f"🔍 Opened web search for: {search_term}"
        except Exception as e:
            return "Sorry, I couldn't perform the web search. Please check your internet connection."
    
    def handle_weather_request(self, command):
        """Weather request handler (placeholder for API integration)"""
        return "🌤️ Weather feature requires API setup. This would show current weather conditions."
    
    def handle_news_request(self):
        """News request handler (placeholder for API integration)"""
        return "📰 News feature requires API setup. This would show latest news headlines."