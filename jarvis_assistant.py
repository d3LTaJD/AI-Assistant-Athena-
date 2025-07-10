import os
import sys
import time
import datetime
import random
import json
import math
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, PhotoImage
import webbrowser
from pathlib import Path

# Try to import optional packages with fallbacks
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("Text-to-speech not available. Install with: pip install pyttsx3")

try:
    import requests
    ONLINE_FEATURES = True
except ImportError:
    ONLINE_FEATURES = False
    print("Online features limited. Install with: pip install requests")

class JarvisAssistant:
    def __init__(self):
        self.name = "Jarvis"
        self.user_name = "Sir"
        self.wake_word = "jarvis"
        self.running = True
        self.notes = []
        self.reminders = []
        self.commands_history = []
        
        # Initialize TTS if available
        self.tts_engine = None
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                voices = self.tts_engine.getProperty('voices')
                # Try to set a male voice for Jarvis
                for voice in voices:
                    if 'male' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
                # Set lower pitch for Jarvis-like voice
                self.tts_engine.setProperty('rate', 150)  # Slower rate
                self.tts_engine.setProperty('volume', 0.9)  # Louder
            except Exception as e:
                print(f"TTS initialization error: {e}")
                self.tts_engine = None
        
        # Create data directory
        self.data_dir = Path("jarvis_data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Load saved data
        self.load_data()
        
        # Initialize GUI
        self.root = tk.Tk()
        self.root.title("J.A.R.V.I.S.")
        self.root.geometry("1000x700")
        self.root.configure(bg="#0d1117")
        self.setup_gui()
        
        # Start animation thread
        self.animation_thread = threading.Thread(target=self.run_animations, daemon=True)
        self.animation_thread.start()
    
    def setup_gui(self):
        """Setup the Jarvis-style GUI"""
        # Main frame
        main_frame = tk.Frame(self.root, bg="#0d1117")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Top section with Jarvis visualization
        self.vis_frame = tk.Frame(main_frame, bg="#0d1117", height=300)
        self.vis_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create canvas for visualization
        self.canvas = tk.Canvas(self.vis_frame, bg="#0d1117", highlightthickness=0, height=300)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create Jarvis visualization elements
        self.create_jarvis_visualization()
        
        # Middle section with conversation display
        conv_frame = tk.Frame(main_frame, bg="#0d1117")
        conv_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Conversation display
        self.conversation = scrolledtext.ScrolledText(
            conv_frame, 
            bg="#1a1a1a", 
            fg="#e6e6e6",
            insertbackground="#e6e6e6",
            font=("Consolas", 11),
            borderwidth=0,
            highlightthickness=1,
            highlightbackground="#333333"
        )
        self.conversation.pack(fill=tk.BOTH, expand=True)
        
        # Bottom section with input
        input_frame = tk.Frame(main_frame, bg="#0d1117")
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Command input
        self.command_input = ttk.Entry(
            input_frame,
            font=("Consolas", 12)
        )
        self.command_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.command_input.bind("<Return>", self.process_input)
        
        # Send button
        style = ttk.Style()
        style.configure("TButton", font=("Consolas", 11))
        
        send_button = ttk.Button(
            input_frame,
            text="Send",
            command=self.process_input
        )
        send_button.pack(side=tk.RIGHT)
        
        # Status bar
        status_frame = tk.Frame(main_frame, bg="#0d1117")
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = tk.Label(
            status_frame,
            text="J.A.R.V.I.S. Ready",
            bg="#0d1117",
            fg="#4caf50",
            font=("Consolas", 10)
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Time display
        self.time_label = tk.Label(
            status_frame,
            text=datetime.datetime.now().strftime("%H:%M:%S"),
            bg="#0d1117",
            fg="#e6e6e6",
            font=("Consolas", 10)
        )
        self.time_label.pack(side=tk.RIGHT)
        
        # Update time every second
        self.update_time()
        
        # Add welcome message
        self.add_message("J.A.R.V.I.S.", "Welcome back, sir. All systems are operational.", "system")
        
        # Focus on input
        self.command_input.focus_set()
    
    def create_jarvis_visualization(self):
        """Create Jarvis-style visualization"""
        # Create circular elements
        self.circles = []
        self.lines = []
        self.particles = []
        
        # Main circle
        self.main_circle = self.canvas.create_oval(
            400, 100, 600, 300, 
            outline="#4caf50", 
            width=2
        )
        
        # Inner circle
        self.inner_circle = self.canvas.create_oval(
            450, 150, 550, 250, 
            outline="#4caf50", 
            width=1
        )
        
        # Create pulsing circles
        for i in range(3):
            circle = self.canvas.create_oval(
                400 - i*20, 100 - i*20, 
                600 + i*20, 300 + i*20, 
                outline="#4caf50", 
                width=1
            )
            self.circles.append(circle)
        
        # Create lines
        for i in range(8):
            angle = i * math.pi / 4
            x1 = 500 + 100 * math.cos(angle)
            y1 = 200 + 100 * math.sin(angle)
            x2 = 500 + 150 * math.cos(angle)
            y2 = 200 + 150 * math.sin(angle)
            
            line = self.canvas.create_line(
                x1, y1, x2, y2, 
                fill="#4caf50", 
                width=1
            )
            self.lines.append(line)
        
        # Create particles
        for i in range(20):
            x = random.randint(350, 650)
            y = random.randint(50, 350)
            size = random.randint(2, 5)
            
            particle = self.canvas.create_oval(
                x, y, x + size, y + size,
                fill="#4caf50",
                outline=""
            )
            
            self.particles.append({
                'id': particle,
                'x': x,
                'y': y,
                'size': size,
                'dx': random.uniform(-1, 1),
                'dy': random.uniform(-1, 1)
            })
        
        # Create text
        self.status_text = self.canvas.create_text(
            500, 200,
            text="J.A.R.V.I.S.",
            fill="#e6e6e6",
            font=("Arial", 16, "bold")
        )
    
    def run_animations(self):
        """Run continuous animations"""
        pulse_phase = 0
        rotation_phase = 0
        
        while True:
            try:
                # Update pulse
                pulse_phase += 0.05
                pulse = math.sin(pulse_phase) * 0.2 + 0.8  # 0.6 to 1.0
                
                # Update rotation
                rotation_phase += 0.02
                
                # Update circles
                for i, circle in enumerate(self.circles):
                    scale = pulse * (1 + i * 0.1)
                    self.canvas.coords(
                        circle,
                        400 - i*20 - 10*scale, 
                        100 - i*20 - 10*scale,
                        600 + i*20 + 10*scale, 
                        300 + i*20 + 10*scale
                    )
                
                # Update lines
                for i, line in enumerate(self.lines):
                    angle = i * math.pi / 4 + rotation_phase
                    x1 = 500 + 75 * math.cos(angle)
                    y1 = 200 + 75 * math.sin(angle)
                    x2 = 500 + (150 * pulse) * math.cos(angle)
                    y2 = 200 + (150 * pulse) * math.sin(angle)
                    
                    self.canvas.coords(line, x1, y1, x2, y2)
                
                # Update particles
                for particle in self.particles:
                    # Update position
                    particle['x'] += particle['dx']
                    particle['y'] += particle['dy']
                    
                    # Bounce off boundaries
                    if particle['x'] < 350 or particle['x'] > 650:
                        particle['dx'] *= -1
                    if particle['y'] < 50 or particle['y'] > 350:
                        particle['dy'] *= -1
                    
                    # Update particle
                    self.canvas.coords(
                        particle['id'],
                        particle['x'], 
                        particle['y'],
                        particle['x'] + particle['size'], 
                        particle['y'] + particle['size']
                    )
                
                # Sleep to control animation speed
                time.sleep(0.03)
                
            except Exception as e:
                print(f"Animation error: {e}")
                time.sleep(1)
    
    def update_time(self):
        """Update time display"""
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def add_message(self, sender, message, msg_type="user"):
        """Add message to conversation display"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Format based on message type
        if msg_type == "system":
            tag = "system"
            prefix = f"[{timestamp}] 🤖 {sender}: "
        elif msg_type == "assistant":
            tag = "assistant"
            prefix = f"[{timestamp}] 🤖 {sender}: "
        else:
            tag = "user"
            prefix = f"[{timestamp}] 👤 {sender}: "
        
        # Insert with appropriate tag
        self.conversation.configure(state='normal')
        self.conversation.insert(tk.END, prefix, tag + "_prefix")
        self.conversation.insert(tk.END, f"{message}\n\n", tag)
        self.conversation.configure(state='disabled')
        
        # Configure tags
        self.conversation.tag_configure("system_prefix", foreground="#4caf50", font=("Consolas", 11, "bold"))
        self.conversation.tag_configure("system", foreground="#4caf50", font=("Consolas", 11))
        
        self.conversation.tag_configure("assistant_prefix", foreground="#2196f3", font=("Consolas", 11, "bold"))
        self.conversation.tag_configure("assistant", foreground="#2196f3", font=("Consolas", 11))
        
        self.conversation.tag_configure("user_prefix", foreground="#e6e6e6", font=("Consolas", 11, "bold"))
        self.conversation.tag_configure("user", foreground="#e6e6e6", font=("Consolas", 11))
        
        # Scroll to bottom
        self.conversation.see(tk.END)
        
        # Speak if it's from assistant
        if msg_type == "assistant" and self.tts_engine:
            self.speak(message)
    
    def speak(self, text):
        """Speak text using TTS"""
        if self.tts_engine:
            try:
                # Run in a separate thread to avoid blocking
                def tts_thread():
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()
                
                threading.Thread(target=tts_thread, daemon=True).start()
            except Exception as e:
                print(f"TTS error: {e}")
    
    def process_input(self, event=None):
        """Process user input"""
        command = self.command_input.get().strip()
        if not command:
            return
        
        # Clear input field
        self.command_input.delete(0, tk.END)
        
        # Add to conversation
        self.add_message(self.user_name, command, "user")
        
        # Process command
        self.process_command(command)
    
    def process_command(self, command):
        """Process user command"""
        command = command.lower()
        
        # Log command
        self.log_activity("command", command)
        
        # Check for exit command
        if command in ["exit", "quit", "goodbye", "bye"]:
            self.add_message(self.name, "Goodbye, sir. Shutting down systems.", "assistant")
            self.save_data()
            self.root.after(2000, self.root.destroy)
            return
        
        # Check for wake word (optional)
        if self.wake_word not in command and command not in ["help"]:
            # For better UX, we'll still process some commands without wake word
            pass
        
        # Process commands
        if "time" in command:
            self.get_time()
        
        elif "date" in command:
            self.get_date()
        
        elif "calculate" in command or any(op in command for op in ["+", "-", "*", "/", "="]):
            self.calculate(command)
        
        elif "note" in command or "remember" in command:
            self.create_note(command)
        
        elif "show" in command and "notes" in command:
            self.show_notes()
        
        elif "remind" in command:
            self.create_reminder(command)
        
        elif "show" in command and "reminders" in command:
            self.show_reminders()
        
        elif "joke" in command:
            self.tell_joke()
        
        elif "weather" in command:
            self.get_weather()
        
        elif "search" in command:
            self.search_web(command)
        
        elif "open" in command:
            self.open_website(command)
        
        elif "system" in command:
            self.system_info()
        
        elif "help" in command:
            self.show_help()
        
        else:
            responses = [
                "I'm not sure I understand. Could you please clarify?",
                "I don't have a protocol for that. Try asking for help.",
                "I'm afraid I can't do that, sir. Perhaps try a different command?",
                "That's beyond my current capabilities. Is there something else I can help with?"
            ]
            self.add_message(self.name, random.choice(responses), "assistant")
    
    def get_time(self):
        """Get current time"""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.add_message(self.name, f"The current time is {current_time}, sir.", "assistant")
    
    def get_date(self):
        """Get current date"""
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        self.add_message(self.name, f"Today is {current_date}, sir.", "assistant")
    
    def calculate(self, command):
        """Calculate mathematical expression"""
        try:
            # Extract expression
            expression = command.replace("calculate", "").replace("jarvis", "").strip()
            
            # Safe evaluation
            allowed_names = {
                k: v for k, v in math.__dict__.items() if not k.startswith("__")
            }
            allowed_names.update({
                "abs": abs, "round": round, "min": min, "max": max,
                "sum": sum, "pow": pow
            })
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            self.add_message(self.name, f"The result is {result}, sir.", "assistant")
            
        except Exception as e:
            self.add_message(self.name, f"I'm sorry, sir. I couldn't calculate that. The error was: {str(e)}", "assistant")
    
    def create_note(self, command):
        """Create a note"""
        note_content = command
        for word in ["jarvis", "note", "remember", "create", "make", "save"]:
            note_content = note_content.replace(word, "")
        note_content = note_content.strip()
        
        if not note_content:
            self.add_message(self.name, "What would you like me to note, sir?", "assistant")
            return
        
        note = {
            "id": len(self.notes) + 1,
            "content": note_content,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self.notes.append(note)
        self.save_data()
        
        self.add_message(self.name, f"I've made a note of that, sir: \"{note_content}\"", "assistant")
    
    def show_notes(self):
        """Show all notes"""
        if not self.notes:
            self.add_message(self.name, "You have no saved notes, sir.", "assistant")
            return
        
        notes_text = "Here are your notes, sir:\n\n"
        for note in self.notes:
            timestamp = datetime.datetime.fromisoformat(note["timestamp"]).strftime("%b %d, %Y %I:%M %p")
            notes_text += f"• {note['content']} (Noted on {timestamp})\n"
        
        self.add_message(self.name, notes_text, "assistant")
    
    def create_reminder(self, command):
        """Create a reminder"""
        reminder_content = command
        for word in ["jarvis", "remind", "me", "to", "reminder", "create", "set"]:
            reminder_content = reminder_content.replace(word, "")
        reminder_content = reminder_content.strip()
        
        if not reminder_content:
            self.add_message(self.name, "What would you like me to remind you about, sir?", "assistant")
            return
        
        reminder = {
            "id": len(self.reminders) + 1,
            "content": reminder_content,
            "timestamp": datetime.datetime.now().isoformat(),
            "completed": False
        }
        
        self.reminders.append(reminder)
        self.save_data()
        
        self.add_message(self.name, f"I'll remind you to {reminder_content}, sir.", "assistant")
    
    def show_reminders(self):
        """Show all reminders"""
        active_reminders = [r for r in self.reminders if not r["completed"]]
        
        if not active_reminders:
            self.add_message(self.name, "You have no active reminders, sir.", "assistant")
            return
        
        reminders_text = "Here are your active reminders, sir:\n\n"
        for reminder in active_reminders:
            timestamp = datetime.datetime.fromisoformat(reminder["timestamp"]).strftime("%b %d, %Y %I:%M %p")
            reminders_text += f"• {reminder['content']} (Created on {timestamp})\n"
        
        self.add_message(self.name, reminders_text, "assistant")
    
    def tell_joke(self):
        """Tell a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "What did the janitor say when he jumped out of the closet? Supplies!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "I'm reading a book about anti-gravity. It's impossible to put down!",
            "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them.",
            "Why don't skeletons fight each other? They don't have the guts.",
            "What do you call a fake noodle? An impasta.",
            "Why did the coffee file a police report? It got mugged.",
            "How does a penguin build its house? Igloos it together."
        ]
        
        joke = random.choice(jokes)
        self.add_message(self.name, joke, "assistant")
    
    def get_weather(self):
        """Get weather information"""
        if not ONLINE_FEATURES:
            self.add_message(self.name, "I'm sorry, sir. Weather functionality requires internet access. Please install the requests package.", "assistant")
            return
        
        try:
            # This is a simple weather API call
            self.add_message(self.name, "Checking current weather conditions...", "assistant")
            
            # Simulate API call
            time.sleep(1)
            
            # Mock weather data
            weather_conditions = ["Clear", "Partly Cloudy", "Cloudy", "Light Rain", "Thunderstorms"]
            temperature = random.randint(65, 85)
            condition = random.choice(weather_conditions)
            humidity = random.randint(30, 90)
            
            weather_report = f"Current weather conditions:\n• Temperature: {temperature}°F\n• Condition: {condition}\n• Humidity: {humidity}%"
            
            self.add_message(self.name, weather_report, "assistant")
            
        except Exception as e:
            self.add_message(self.name, f"I'm sorry, sir. I couldn't retrieve the weather information. Error: {str(e)}", "assistant")
    
    def search_web(self, command):
        """Search the web"""
        search_terms = command.replace("search", "").replace("for", "").replace("jarvis", "").strip()
        
        if not search_terms:
            self.add_message(self.name, "What would you like me to search for, sir?", "assistant")
            return
        
        self.add_message(self.name, f"Searching for '{search_terms}'...", "assistant")
        
        try:
            # Create search URL
            search_url = f"https://www.google.com/search?q={search_terms.replace(' ', '+')}"
            
            # Open in browser
            webbrowser.open(search_url)
            
            self.add_message(self.name, f"I've opened a web search for '{search_terms}', sir.", "assistant")
            
        except Exception as e:
            self.add_message(self.name, f"I'm sorry, sir. I couldn't perform the search. Error: {str(e)}", "assistant")
    
    def open_website(self, command):
        """Open website"""
        # Extract website
        words = command.split()
        website = None
        
        for word in words:
            if "." in word:
                website = word
                break
        
        if not website:
            common_sites = {
                "google": "https://www.google.com",
                "youtube": "https://www.youtube.com",
                "facebook": "https://www.facebook.com",
                "twitter": "https://www.twitter.com",
                "amazon": "https://www.amazon.com",
                "wikipedia": "https://www.wikipedia.org",
                "reddit": "https://www.reddit.com",
                "netflix": "https://www.netflix.com",
                "gmail": "https://mail.google.com"
            }
            
            for site, url in common_sites.items():
                if site in command:
                    website = url
                    break
        
        if website:
            if not website.startswith(("http://", "https://")):
                website = "https://" + website
            
            try:
                webbrowser.open(website)
                self.add_message(self.name, f"Opening {website}, sir.", "assistant")
            except Exception as e:
                self.add_message(self.name, f"I'm sorry, sir. I couldn't open that website. Error: {str(e)}", "assistant")
        else:
            self.add_message(self.name, "I'm sorry, sir. I couldn't determine which website to open.", "assistant")
    
    def system_info(self):
        """Get system information"""
        import platform
        
        system_info = f"""System Information:
• OS: {platform.system()} {platform.release()}
• Version: {platform.version()}
• Machine: {platform.machine()}
• Processor: {platform.processor()}
• Python: {platform.python_version()}
• Hostname: {platform.node()}
• Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        self.add_message(self.name, system_info, "assistant")
    
    def show_help(self):
        """Show help information"""
        help_text = f"""
I am {self.name}, your personal AI assistant. Here are commands you can use:

TIME & DATE:
• "time" - Get current time
• "date" - Get current date

CALCULATIONS:
• "calculate 2 + 2" - Basic math
• "calculate sqrt(144)" - Advanced math

NOTES & REMINDERS:
• "note buy groceries" - Create a note
• "show notes" - Display all notes
• "remind me to call mom" - Create reminder
• "show reminders" - Display reminders

WEB & SEARCH:
• "search for quantum physics" - Web search
• "open youtube" - Open website
• "weather" - Get weather information

SYSTEM:
• "system" - System information
• "help" - Show this help
• "exit" or "quit" - Close assistant

Just speak naturally, sir. I understand context and can help with various tasks.
"""
        
        self.add_message(self.name, help_text, "assistant")
    
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
    
    def save_data(self):
        """Save data to JSON file"""
        try:
            data = {
                "notes": self.notes,
                "reminders": self.reminders,
                "settings": {
                    "name": self.name,
                    "user_name": self.user_name,
                    "wake_word": self.wake_word
                },
                "history": self.commands_history[-50:]  # Save only recent history
            }
            
            with open(self.data_dir / "jarvis_data.json", "w") as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_data(self):
        """Load data from JSON file"""
        try:
            data_file = self.data_dir / "jarvis_data.json"
            if data_file.exists():
                with open(data_file, "r") as f:
                    data = json.load(f)
                    self.notes = data.get("notes", [])
                    self.reminders = data.get("reminders", [])
                    
                    settings = data.get("settings", {})
                    self.name = settings.get("name", self.name)
                    self.user_name = settings.get("user_name", self.user_name)
                    self.wake_word = settings.get("wake_word", self.wake_word)
                    
                    self.commands_history = data.get("history", [])
                    
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def run(self):
        """Run the Jarvis assistant"""
        self.root.mainloop()

def install_dependencies():
    """Install required dependencies"""
    print("Installing required dependencies...")
    
    # List of basic dependencies that should work everywhere
    dependencies = [
        "pyttsx3",
        "requests"
    ]
    
    for package in dependencies:
        try:
            print(f"Installing {package}...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed {package}")
        except Exception as e:
            print(f"Error installing {package}: {e}")
    
    print("Dependencies installation completed.")
    print("Starting J.A.R.V.I.S...")

if __name__ == "__main__":
    # Check if this is first run
    if not any(p.startswith("pyttsx3") for p in sys.modules):
        print("First run detected. Installing dependencies...")
        install_dependencies()
        
        # Restart the script to use newly installed packages
        print("Restarting J.A.R.V.I.S. with dependencies...")
        os.execv(sys.executable, [sys.executable] + sys.argv)
    
    # Start Jarvis
    jarvis = JarvisAssistant()
    jarvis.run()