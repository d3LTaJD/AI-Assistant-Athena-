"""
Phase 2 Implementation: Advanced GUI and Enhanced Features
This implements the GUI interface, advanced voice controls, and system integration
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import queue
import json
from datetime import datetime
import os
from pathlib import Path

# Import enhanced Athena components
from enhanced_athena import AthenaCore
from utils.logger import athena_logger
from utils.connectivity import connectivity_manager
from enhanced_config import config_manager

class AthenaGUI:
    def __init__(self):
        self.athena_core = AthenaCore()
        self.is_listening = False
        self.is_running = False
        self.command_queue = queue.Queue()
        
        # Initialize GUI
        self.setup_main_window()
        self.setup_widgets()
        self.setup_system_tray()
        
        # Start background threads
        self.start_background_threads()
        
        athena_logger.log_info("Athena GUI initialized", "gui")
    
    def setup_main_window(self):
        """Setup the main application window"""
        self.root = tk.Tk()
        self.root.title("Athena AI Assistant - Phase 2")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Configure theme
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors for dark theme
        self.colors = {
            'bg': '#2b2b2b',
            'fg': '#ffffff',
            'accent': '#4a9eff',
            'success': '#4caf50',
            'warning': '#ff9800',
            'error': '#f44336'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Configure styles
        style.configure('Title.TLabel', 
                       background=self.colors['bg'], 
                       foreground=self.colors['accent'],
                       font=('Arial', 16, 'bold'))
        
        style.configure('Status.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['fg'])
        
        style.configure('Success.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['success'])
        
        style.configure('Warning.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['warning'])
        
        style.configure('Error.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['error'])
    
    def setup_widgets(self):
        """Setup all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="🤖 Athena AI Assistant", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Status frame
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Connection status
        self.connection_label = ttk.Label(status_frame, text="🔴 Checking connection...", style='Status.TLabel')
        self.connection_label.pack(side=tk.LEFT)
        
        # Voice status
        self.voice_status_label = ttk.Label(status_frame, text="🎤 Ready", style='Status.TLabel')
        self.voice_status_label.pack(side=tk.RIGHT)
        
        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Start/Stop button
        self.start_stop_btn = ttk.Button(control_frame, text="🚀 Start Athena", command=self.toggle_athena)
        self.start_stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Voice toggle button
        self.voice_btn = ttk.Button(control_frame, text="🎤 Start Listening", command=self.toggle_voice)
        self.voice_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Settings button
        settings_btn = ttk.Button(control_frame, text="⚙️ Settings", command=self.open_settings)
        settings_btn.pack(side=tk.RIGHT)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Chat tab
        self.setup_chat_tab()
        
        # Activity log tab
        self.setup_activity_tab()
        
        # System info tab
        self.setup_system_tab()
        
        # API usage tab
        self.setup_api_tab()
    
    def setup_chat_tab(self):
        """Setup the chat interface tab"""
        chat_frame = ttk.Frame(self.notebook)
        self.notebook.add(chat_frame, text="💬 Chat")
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, 
            wrap=tk.WORD, 
            height=15,
            bg='#1e1e1e',
            fg='#ffffff',
            insertbackground='#ffffff'
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Input frame
        input_frame = ttk.Frame(chat_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Text input
        self.text_input = ttk.Entry(input_frame)
        self.text_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.text_input.bind('<Return>', self.send_text_command)
        
        # Send button
        send_btn = ttk.Button(input_frame, text="Send", command=self.send_text_command)
        send_btn.pack(side=tk.RIGHT)
        
        # Add welcome message
        self.add_chat_message("System", "Welcome to Athena AI Assistant! Type your commands or use voice input.", "system")
    
    def setup_activity_tab(self):
        """Setup the activity log tab"""
        activity_frame = ttk.Frame(self.notebook)
        self.notebook.add(activity_frame, text="📊 Activity")
        
        # Activity display
        self.activity_display = scrolledtext.ScrolledText(
            activity_frame,
            wrap=tk.WORD,
            height=20,
            bg='#1e1e1e',
            fg='#ffffff'
        )
        self.activity_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Control frame
        activity_control_frame = ttk.Frame(activity_frame)
        activity_control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Clear log button
        clear_btn = ttk.Button(activity_control_frame, text="Clear Log", command=self.clear_activity_log)
        clear_btn.pack(side=tk.LEFT)
        
        # Export log button
        export_btn = ttk.Button(activity_control_frame, text="Export Log", command=self.export_activity_log)
        export_btn.pack(side=tk.LEFT, padx=(5, 0))
    
    def setup_system_tab(self):
        """Setup the system information tab"""
        system_frame = ttk.Frame(self.notebook)
        self.notebook.add(system_frame, text="🖥️ System")
        
        # System info display
        self.system_display = scrolledtext.ScrolledText(
            system_frame,
            wrap=tk.WORD,
            height=20,
            bg='#1e1e1e',
            fg='#ffffff'
        )
        self.system_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Refresh button
        refresh_btn = ttk.Button(system_frame, text="🔄 Refresh", command=self.refresh_system_info)
        refresh_btn.pack(pady=5)
        
        # Load initial system info
        self.refresh_system_info()
    
    def setup_api_tab(self):
        """Setup the API usage monitoring tab"""
        api_frame = ttk.Frame(self.notebook)
        self.notebook.add(api_frame, text="🔌 API Usage")
        
        # API usage display
        self.api_display = scrolledtext.ScrolledText(
            api_frame,
            wrap=tk.WORD,
            height=20,
            bg='#1e1e1e',
            fg='#ffffff'
        )
        self.api_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Update API usage info
        self.update_api_usage()
    
    def setup_system_tray(self):
        """Setup system tray functionality"""
        # This would require additional libraries like pystray
        # For now, we'll implement minimize to taskbar
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def start_background_threads(self):
        """Start background threads for various tasks"""
        # Connection monitoring thread
        self.connection_thread = threading.Thread(target=self.monitor_connection, daemon=True)
        self.connection_thread.start()
        
        # Command processing thread
        self.command_thread = threading.Thread(target=self.process_commands, daemon=True)
        self.command_thread.start()
    
    def monitor_connection(self):
        """Monitor internet connection status"""
        while True:
            try:
                status = connectivity_manager.get_connection_status()
                if status['connected']:
                    self.root.after(0, lambda: self.connection_label.configure(
                        text="🟢 Online", style='Success.TLabel'))
                else:
                    self.root.after(0, lambda: self.connection_label.configure(
                        text="🔴 Offline", style='Error.TLabel'))
                
                # Wait 30 seconds before next check
                threading.Event().wait(30)
            except Exception as e:
                athena_logger.log_error(f"Connection monitoring error: {e}", category="gui")
                threading.Event().wait(60)  # Wait longer on error
    
    def process_commands(self):
        """Process commands from the queue"""
        while True:
            try:
                if not self.command_queue.empty():
                    command = self.command_queue.get()
                    self.execute_command(command)
                threading.Event().wait(0.1)  # Small delay to prevent high CPU usage
            except Exception as e:
                athena_logger.log_error(f"Command processing error: {e}", category="gui")
    
    def toggle_athena(self):
        """Toggle Athena on/off"""
        if not self.is_running:
            self.is_running = True
            self.start_stop_btn.configure(text="⏹️ Stop Athena")
            self.add_chat_message("System", "Athena AI Assistant started!", "system")
            
            # Start Athena in background thread
            self.athena_thread = threading.Thread(target=self.run_athena_background, daemon=True)
            self.athena_thread.start()
        else:
            self.is_running = False
            self.is_listening = False
            self.start_stop_btn.configure(text="🚀 Start Athena")
            self.voice_btn.configure(text="🎤 Start Listening")
            self.voice_status_label.configure(text="🎤 Stopped")
            self.add_chat_message("System", "Athena AI Assistant stopped.", "system")
    
    def toggle_voice(self):
        """Toggle voice listening"""
        if not self.is_running:
            messagebox.showwarning("Warning", "Please start Athena first!")
            return
        
        if not self.is_listening:
            self.is_listening = True
            self.voice_btn.configure(text="🔇 Stop Listening")
            self.voice_status_label.configure(text="🎤 Listening...")
            self.add_chat_message("System", "Voice listening activated. Say 'Athena' followed by your command.", "system")
        else:
            self.is_listening = False
            self.voice_btn.configure(text="🎤 Start Listening")
            self.voice_status_label.configure(text="🎤 Ready")
            self.add_chat_message("System", "Voice listening deactivated.", "system")
    
    def run_athena_background(self):
        """Run Athena in background thread"""
        try:
            while self.is_running:
                if self.is_listening:
                    # Get voice command
                    query = self.athena_core.takeCommandMIC()
                    if query:
                        self.root.after(0, lambda q=query: self.add_chat_message("You", q, "user"))
                        self.command_queue.put(query)
                
                threading.Event().wait(0.5)  # Small delay
        except Exception as e:
            athena_logger.log_error(f"Background Athena error: {e}", category="gui")
            self.root.after(0, lambda: self.add_chat_message("System", f"Error: {str(e)}", "error"))
    
    def send_text_command(self, event=None):
        """Send text command"""
        command = self.text_input.get().strip()
        if command:
            self.add_chat_message("You", command, "user")
            self.command_queue.put(command)
            self.text_input.delete(0, tk.END)
    
    def execute_command(self, command):
        """Execute a command using Athena core"""
        try:
            # Process the command
            query_tokens = self.athena_core.process_query(command)
            wake_word = config_manager.get("features.wake_word", "athena")
            
            response = "Command processed."
            
            if wake_word in query_tokens or not config_manager.get("features.wake_word_enabled", True):
                if 'time' in query_tokens:
                    self.athena_core.get_time()
                    response = "Time provided."
                
                elif 'date' in query_tokens:
                    self.athena_core.get_date()
                    response = "Date provided."
                
                elif "search" in query_tokens and "wikipedia" in query_tokens:
                    # For GUI, we'll handle this differently
                    response = "Wikipedia search initiated."
                    threading.Thread(target=self.athena_core.search_wikipedia, daemon=True).start()
                
                elif "chat" in query_tokens or "talk" in query_tokens:
                    # Extract the actual message after "chat" or "talk"
                    chat_start = max(
                        command.find("chat") + 4 if "chat" in command else 0,
                        command.find("talk") + 4 if "talk" in command else 0
                    )
                    user_input = command[chat_start:].strip()
                    if user_input:
                        threading.Thread(target=lambda: self.athena_core.chat_with_gpt(user_input), daemon=True).start()
                        response = "ChatGPT processing your request..."
                
                elif "screenshot" in query_tokens:
                    self.athena_core.take_screenshot()
                    response = "Screenshot taken."
                
                elif "status" in query_tokens:
                    self.athena_core.show_system_status()
                    response = "System status displayed."
                
                else:
                    response = "Command not recognized. Try: time, date, search wikipedia, chat, screenshot, or status."
            
            # Update GUI with response
            self.root.after(0, lambda: self.add_chat_message("Athena", response, "assistant"))
            
            # Log activity
            self.root.after(0, lambda: self.add_activity_log(f"Command: {command} | Response: {response}"))
            
        except Exception as e:
            error_msg = f"Error executing command: {str(e)}"
            athena_logger.log_error(error_msg, category="gui")
            self.root.after(0, lambda: self.add_chat_message("System", error_msg, "error"))
    
    def add_chat_message(self, sender, message, msg_type="normal"):
        """Add message to chat display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Color coding based on message type
        colors = {
            "user": "#4a9eff",
            "assistant": "#4caf50", 
            "system": "#ff9800",
            "error": "#f44336",
            "normal": "#ffffff"
        }
        
        color = colors.get(msg_type, colors["normal"])
        
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"[{timestamp}] {sender}: ", "timestamp")
        self.chat_display.insert(tk.END, f"{message}\n", msg_type)
        
        # Configure tags for colors
        self.chat_display.tag_configure("timestamp", foreground="#888888")
        self.chat_display.tag_configure(msg_type, foreground=color)
        
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def add_activity_log(self, activity):
        """Add activity to activity log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {activity}\n"
        
        self.activity_display.configure(state=tk.NORMAL)
        self.activity_display.insert(tk.END, log_entry)
        self.activity_display.configure(state=tk.DISABLED)
        self.activity_display.see(tk.END)
    
    def clear_activity_log(self):
        """Clear the activity log"""
        self.activity_display.configure(state=tk.NORMAL)
        self.activity_display.delete(1.0, tk.END)
        self.activity_display.configure(state=tk.DISABLED)
    
    def export_activity_log(self):
        """Export activity log to file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"athena_activity_log_{timestamp}.txt"
            
            with open(filename, 'w') as f:
                f.write(self.activity_display.get(1.0, tk.END))
            
            messagebox.showinfo("Success", f"Activity log exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export log: {str(e)}")
    
    def refresh_system_info(self):
        """Refresh system information display"""
        try:
            system_info = self.athena_core.system.get_system_info()
            connection_status = connectivity_manager.get_connection_status()
            
            info_text = f"""
🖥️ SYSTEM INFORMATION
{'='*50}

Operating System: {system_info['os']} {system_info['os_version']}
Architecture: {system_info['architecture']}
Processor: {system_info['processor']}
Python Version: {system_info['python_version']}
Hostname: {system_info['hostname']}
User: {system_info['user']}
Home Directory: {system_info['home_directory']}

🌐 CONNECTIVITY
{'='*50}

Status: {connection_status['status_message']}
Last Check: {datetime.fromtimestamp(connection_status['last_check']).strftime('%Y-%m-%d %H:%M:%S') if connection_status['last_check'] else 'Never'}

⚙️ CONFIGURATION
{'='*50}

Wake Word: {config_manager.get('features.wake_word', 'athena')}
Wake Word Enabled: {config_manager.get('features.wake_word_enabled', True)}
Voice: {config_manager.get('voice_settings.voice', 'en-US-AvaNeural')}
Theme: {config_manager.get('ui_settings.theme', 'dark')}

📊 STATISTICS
{'='*50}

Database Connected: {self.athena_core.mydb is not None and self.athena_core.mydb.is_connected() if hasattr(self.athena_core, 'mydb') else 'Unknown'}
Logs Directory: {config_manager.get('paths.logs_folder', 'logs')}
Screenshots Directory: {config_manager.get('paths.screenshot_folder', 'screenshots')}
"""
            
            self.system_display.configure(state=tk.NORMAL)
            self.system_display.delete(1.0, tk.END)
            self.system_display.insert(1.0, info_text)
            self.system_display.configure(state=tk.DISABLED)
            
        except Exception as e:
            error_text = f"Error loading system information: {str(e)}"
            self.system_display.configure(state=tk.NORMAL)
            self.system_display.delete(1.0, tk.END)
            self.system_display.insert(1.0, error_text)
            self.system_display.configure(state=tk.DISABLED)
    
    def update_api_usage(self):
        """Update API usage information"""
        try:
            # Read API usage from logs
            api_info = """
🔌 API USAGE MONITORING
{'='*50}

OpenAI API:
- Status: Configured
- Model: GPT-3.5-turbo
- Usage: Check logs for detailed usage

News API:
- Status: Configured
- Endpoint: Top Headlines
- Usage: Check logs for detailed usage

Weather API:
- Status: Configured
- Provider: OpenWeatherMap
- Usage: Check logs for detailed usage

📈 USAGE TIPS
{'='*50}

- Monitor your API usage to avoid unexpected charges
- OpenAI charges per token used
- News API has daily request limits
- Weather API has monthly request limits

📋 RECENT ACTIVITY
{'='*50}

Check the Activity tab for recent API calls and usage statistics.
"""
            
            self.api_display.configure(state=tk.NORMAL)
            self.api_display.delete(1.0, tk.END)
            self.api_display.insert(1.0, api_info)
            self.api_display.configure(state=tk.DISABLED)
            
        except Exception as e:
            error_text = f"Error loading API usage information: {str(e)}"
            self.api_display.configure(state=tk.NORMAL)
            self.api_display.delete(1.0, tk.END)
            self.api_display.insert(1.0, error_text)
            self.api_display.configure(state=tk.DISABLED)
    
    def open_settings(self):
        """Open settings window"""
        settings_window = SettingsWindow(self.root, config_manager)
    
    def on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit Athena AI Assistant?"):
            self.is_running = False
            self.is_listening = False
            athena_logger.log_info("Athena GUI shutting down", "gui")
            self.root.destroy()
    
    def run(self):
        """Run the GUI application"""
        try:
            self.root.mainloop()
        except Exception as e:
            athena_logger.log_error(f"GUI runtime error: {e}", category="gui")

class SettingsWindow:
    def __init__(self, parent, config_manager):
        self.parent = parent
        self.config_manager = config_manager
        
        # Create settings window
        self.window = tk.Toplevel(parent)
        self.window.title("Athena Settings")
        self.window.geometry("500x400")
        self.window.resizable(False, False)
        
        # Make window modal
        self.window.transient(parent)
        self.window.grab_set()
        
        self.setup_settings_ui()
    
    def setup_settings_ui(self):
        """Setup settings UI"""
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Voice settings tab
        voice_frame = ttk.Frame(notebook)
        notebook.add(voice_frame, text="🎤 Voice")
        
        # Wake word setting
        ttk.Label(voice_frame, text="Wake Word:").pack(anchor=tk.W, pady=(10, 5))
        self.wake_word_var = tk.StringVar(value=self.config_manager.get('features.wake_word', 'athena'))
        wake_word_entry = ttk.Entry(voice_frame, textvariable=self.wake_word_var)
        wake_word_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Wake word enabled
        self.wake_word_enabled_var = tk.BooleanVar(value=self.config_manager.get('features.wake_word_enabled', True))
        wake_word_check = ttk.Checkbutton(voice_frame, text="Enable Wake Word", variable=self.wake_word_enabled_var)
        wake_word_check.pack(anchor=tk.W, pady=(0, 10))
        
        # Voice selection
        ttk.Label(voice_frame, text="Voice:").pack(anchor=tk.W, pady=(10, 5))
        self.voice_var = tk.StringVar(value=self.config_manager.get('voice_settings.voice', 'en-US-AvaNeural'))
        voice_combo = ttk.Combobox(voice_frame, textvariable=self.voice_var, values=[
            'en-US-AvaNeural', 'en-US-AnaNeural', 'en-GB-LibbyNeural', 
            'en-GB-MaisieNeural', 'en-IE-EmilyNeural', 'en-IN-NeerjaNeural'
        ])
        voice_combo.pack(fill=tk.X, pady=(0, 10))
        
        # API Keys tab
        api_frame = ttk.Frame(notebook)
        notebook.add(api_frame, text="🔑 API Keys")
        
        # OpenAI API Key
        ttk.Label(api_frame, text="OpenAI API Key:").pack(anchor=tk.W, pady=(10, 5))
        self.openai_key_var = tk.StringVar(value=self.config_manager.get_secure('api_keys.openai', ''))
        openai_entry = ttk.Entry(api_frame, textvariable=self.openai_key_var, show="*")
        openai_entry.pack(fill=tk.X, pady=(0, 10))
        
        # News API Key
        ttk.Label(api_frame, text="News API Key:").pack(anchor=tk.W, pady=(10, 5))
        self.news_key_var = tk.StringVar(value=self.config_manager.get_secure('api_keys.news_api', ''))
        news_entry = ttk.Entry(api_frame, textvariable=self.news_key_var, show="*")
        news_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Weather API Key
        ttk.Label(api_frame, text="Weather API Key:").pack(anchor=tk.W, pady=(10, 5))
        self.weather_key_var = tk.StringVar(value=self.config_manager.get_secure('api_keys.weather_api', ''))
        weather_entry = ttk.Entry(api_frame, textvariable=self.weather_key_var, show="*")
        weather_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons frame
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Save button
        save_btn = ttk.Button(button_frame, text="Save", command=self.save_settings)
        save_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Cancel button
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.window.destroy)
        cancel_btn.pack(side=tk.RIGHT)
    
    def save_settings(self):
        """Save settings"""
        try:
            # Save voice settings
            self.config_manager.set('features.wake_word', self.wake_word_var.get())
            self.config_manager.set('features.wake_word_enabled', self.wake_word_enabled_var.get())
            self.config_manager.set('voice_settings.voice', self.voice_var.get())
            
            # Save API keys
            self.config_manager.set_secure('api_keys.openai', self.openai_key_var.get())
            self.config_manager.set_secure('api_keys.news_api', self.news_key_var.get())
            self.config_manager.set_secure('api_keys.weather_api', self.weather_key_var.get())
            
            messagebox.showinfo("Success", "Settings saved successfully!")
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")

def main():
    """Main entry point for Phase 2 GUI"""
    try:
        app = AthenaGUI()
        app.run()
    except Exception as e:
        print(f"❌ Critical error starting Athena GUI: {e}")
        athena_logger.log_error(f"Critical GUI startup error: {e}", category="critical")

if __name__ == "__main__":
    main()