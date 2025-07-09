"""
Modern GUI for AI Assistant using CustomTkinter
"""
import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import threading
import queue
import json
from datetime import datetime

from database import db
from voice_handler import voice_handler
from command_processor import CommandProcessor
from config import config

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LoginWindow:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("AI Assistant - Login")
        self.window.geometry("400x500")
        self.window.resizable(False, False)
        
        # Center window
        self.center_window()
        
        self.setup_ui()
        
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.window.winfo_screenheight() // 2) - (500 // 2)
        self.window.geometry(f"400x500+{x}+{y}")
    
    def setup_ui(self):
        """Setup login UI"""
        # Title
        title_label = ctk.CTkLabel(
            self.window,
            text="🤖 AI Assistant",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=30)
        
        # Login frame
        login_frame = ctk.CTkFrame(self.window)
        login_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Login title
        login_title = ctk.CTkLabel(
            login_frame,
            text="Welcome Back",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        login_title.pack(pady=20)
        
        # Email entry
        self.email_entry = ctk.CTkEntry(
            login_frame,
            placeholder_text="Email",
            width=300,
            height=40
        )
        self.email_entry.pack(pady=10)
        
        # Password entry
        self.password_entry = ctk.CTkEntry(
            login_frame,
            placeholder_text="Password",
            show="*",
            width=300,
            height=40
        )
        self.password_entry.pack(pady=10)
        
        # Login button
        login_btn = ctk.CTkButton(
            login_frame,
            text="Login",
            command=self.login,
            width=300,
            height=40
        )
        login_btn.pack(pady=20)
        
        # Signup button
        signup_btn = ctk.CTkButton(
            login_frame,
            text="Create Account",
            command=self.show_signup,
            width=300,
            height=40,
            fg_color="transparent",
            border_width=2
        )
        signup_btn.pack(pady=10)
        
        # Bind Enter key
        self.window.bind('<Return>', lambda e: self.login())
    
    def login(self):
        """Handle login"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        user = db.authenticate_user(email, password)
        if user:
            self.window.destroy()
            # Update config with user's assistant name
            config.set('assistant_name', user['assistant_name'])
            config.set('wake_word', user['assistant_name'].lower())
            # Start main application
            app = MainApplication(user['id'])
            app.run()
        else:
            messagebox.showerror("Error", "Invalid email or password")
    
    def show_signup(self):
        """Show signup window"""
        SignupWindow(self.window)
    
    def run(self):
        """Run the login window"""
        self.window.mainloop()

class SignupWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Create Account")
        self.window.geometry("400x600")
        self.window.resizable(False, False)
        
        # Make modal
        self.window.transient(parent)
        self.window.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup signup UI"""
        # Title
        title_label = ctk.CTkLabel(
            self.window,
            text="Create Account",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Signup frame
        signup_frame = ctk.CTkFrame(self.window)
        signup_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Email entry
        self.email_entry = ctk.CTkEntry(
            signup_frame,
            placeholder_text="Email",
            width=300,
            height=40
        )
        self.email_entry.pack(pady=10)
        
        # Password entry
        self.password_entry = ctk.CTkEntry(
            signup_frame,
            placeholder_text="Password",
            show="*",
            width=300,
            height=40
        )
        self.password_entry.pack(pady=10)
        
        # Confirm password entry
        self.confirm_password_entry = ctk.CTkEntry(
            signup_frame,
            placeholder_text="Confirm Password",
            show="*",
            width=300,
            height=40
        )
        self.confirm_password_entry.pack(pady=10)
        
        # Assistant name entry
        self.assistant_name_entry = ctk.CTkEntry(
            signup_frame,
            placeholder_text="Assistant Name (e.g., Jarvis, Athena)",
            width=300,
            height=40
        )
        self.assistant_name_entry.pack(pady=10)
        
        # Voice preference
        voice_label = ctk.CTkLabel(signup_frame, text="Voice Preference:")
        voice_label.pack(pady=(10, 5))
        
        self.voice_var = tk.StringVar(value="female")
        voice_frame = ctk.CTkFrame(signup_frame)
        voice_frame.pack(pady=5)
        
        male_radio = ctk.CTkRadioButton(
            voice_frame,
            text="Male",
            variable=self.voice_var,
            value="male"
        )
        male_radio.pack(side="left", padx=20)
        
        female_radio = ctk.CTkRadioButton(
            voice_frame,
            text="Female",
            variable=self.voice_var,
            value="female"
        )
        female_radio.pack(side="right", padx=20)
        
        # Create account button
        create_btn = ctk.CTkButton(
            signup_frame,
            text="Create Account",
            command=self.create_account,
            width=300,
            height=40
        )
        create_btn.pack(pady=20)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            signup_frame,
            text="Cancel",
            command=self.window.destroy,
            width=300,
            height=40,
            fg_color="transparent",
            border_width=2
        )
        cancel_btn.pack(pady=10)
    
    def create_account(self):
        """Handle account creation"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        assistant_name = self.assistant_name_entry.get().strip() or "Assistant"
        voice_preference = self.voice_var.get()
        
        # Validation
        if not email or not password:
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        
        # Create user
        user_id = db.create_user(email, password, assistant_name, voice_preference)
        if user_id:
            messagebox.showinfo("Success", f"Account created successfully!\nYour assistant '{assistant_name}' is ready.")
            self.window.destroy()
        else:
            messagebox.showerror("Error", "Email already exists")

class MainApplication:
    def __init__(self, user_id):
        self.user_id = user_id
        self.command_processor = CommandProcessor(user_id)
        self.is_listening = False
        
        # Create main window
        self.window = ctk.CTk()
        self.window.title(f"AI Assistant - {config.get('assistant_name', 'Assistant')}")
        self.window.geometry("1000x700")
        
        # Center window
        self.center_window()
        
        self.setup_ui()
        self.setup_voice()
        
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.window.winfo_screenheight() // 2) - (700 // 2)
        self.window.geometry(f"1000x700+{x}+{y}")
    
    def setup_ui(self):
        """Setup main application UI"""
        # Main container
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Assistant name and status
        assistant_name = config.get('assistant_name', 'Assistant')
        self.header_label = ctk.CTkLabel(
            header_frame,
            text=f"🤖 {assistant_name}",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.header_label.pack(side="left", padx=20, pady=10)
        
        # Status indicator
        self.status_label = ctk.CTkLabel(
            header_frame,
            text="🔴 Not Listening",
            font=ctk.CTkFont(size=14)
        )
        self.status_label.pack(side="right", padx=20, pady=10)
        
        # Content area
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True)
        
        # Left panel - Chat
        chat_frame = ctk.CTkFrame(content_frame)
        chat_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Chat title
        chat_title = ctk.CTkLabel(
            chat_frame,
            text="💬 Conversation",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        chat_title.pack(pady=10)
        
        # Chat display
        self.chat_display = ctk.CTkTextbox(
            chat_frame,
            width=600,
            height=400,
            font=ctk.CTkFont(size=12)
        )
        self.chat_display.pack(padx=10, pady=(0, 10), fill="both", expand=True)
        
        # Input frame
        input_frame = ctk.CTkFrame(chat_frame)
        input_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Text input
        self.text_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="Type your message here...",
            height=40
        )
        self.text_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.text_input.bind('<Return>', self.send_text_message)
        
        # Send button
        send_btn = ctk.CTkButton(
            input_frame,
            text="Send",
            command=self.send_text_message,
            width=80,
            height=40
        )
        send_btn.pack(side="right")
        
        # Voice control frame
        voice_frame = ctk.CTkFrame(chat_frame)
        voice_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Voice toggle button
        self.voice_btn = ctk.CTkButton(
            voice_frame,
            text="🎤 Start Listening",
            command=self.toggle_voice,
            height=40
        )
        self.voice_btn.pack(side="left", padx=(0, 10))
        
        # Voice once button
        voice_once_btn = ctk.CTkButton(
            voice_frame,
            text="🎙️ Voice Command",
            command=self.voice_command_once,
            height=40
        )
        voice_once_btn.pack(side="left")
        
        # Right panel - Controls and History
        right_panel = ctk.CTkFrame(content_frame)
        right_panel.pack(side="right", fill="y", padx=(5, 0))
        
        # Controls section
        controls_title = ctk.CTkLabel(
            right_panel,
            text="⚙️ Controls",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        controls_title.pack(pady=10)
        
        # Help button
        help_btn = ctk.CTkButton(
            right_panel,
            text="❓ Help",
            command=self.show_help,
            width=200
        )
        help_btn.pack(pady=5)
        
        # History button
        history_btn = ctk.CTkButton(
            right_panel,
            text="📜 History",
            command=self.show_history,
            width=200
        )
        history_btn.pack(pady=5)
        
        # Settings button
        settings_btn = ctk.CTkButton(
            right_panel,
            text="⚙️ Settings",
            command=self.show_settings,
            width=200
        )
        settings_btn.pack(pady=5)
        
        # Clear chat button
        clear_btn = ctk.CTkButton(
            right_panel,
            text="🗑️ Clear Chat",
            command=self.clear_chat,
            width=200
        )
        clear_btn.pack(pady=5)
        
        # Quick actions section
        actions_title = ctk.CTkLabel(
            right_panel,
            text="⚡ Quick Actions",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        actions_title.pack(pady=(20, 10))
        
        # Quick action buttons
        quick_actions = [
            ("📁 Open Downloads", "open downloads folder"),
            ("📄 Open Documents", "open documents folder"),
            ("🖥️ Open Desktop", "open desktop folder"),
            ("🎵 Open Music", "open music folder"),
            ("⏰ What time is it?", "what time is it"),
            ("📅 What's the date?", "what's the date")
        ]
        
        for text, command in quick_actions:
            btn = ctk.CTkButton(
                right_panel,
                text=text,
                command=lambda cmd=command: self.execute_quick_action(cmd),
                width=200,
                height=30
            )
            btn.pack(pady=2)
        
        # Welcome message
        self.add_message("System", f"Welcome! I'm {assistant_name}, your AI assistant. How can I help you today?", "system")
    
    def setup_voice(self):
        """Setup voice recognition"""
        self.voice_queue = queue.Queue()
    
    def add_message(self, sender, message, msg_type="user"):
        """Add message to chat display"""
        timestamp = datetime.now().strftime("%H:%M")
        
        # Color coding
        if msg_type == "system":
            prefix = "🤖 System"
            color = "blue"
        elif msg_type == "assistant":
            assistant_name = config.get('assistant_name', 'Assistant')
            prefix = f"🤖 {assistant_name}"
            color = "green"
        else:
            prefix = "👤 You"
            color = "white"
        
        formatted_message = f"[{timestamp}] {prefix}: {message}\n\n"
        
        self.chat_display.insert("end", formatted_message)
        self.chat_display.see("end")
    
    def send_text_message(self, event=None):
        """Send text message"""
        message = self.text_input.get().strip()
        if not message:
            return
        
        self.text_input.delete(0, "end")
        self.add_message("You", message, "user")
        
        # Process command in separate thread
        threading.Thread(target=self.process_command, args=(message,), daemon=True).start()
    
    def process_command(self, command):
        """Process command and show response"""
        try:
            response = self.command_processor.process_command(command)
            
            # Handle multiple file results
            if isinstance(response, str) and "Say the number to open" in response:
                self.add_message("Assistant", response, "assistant")
            else:
                self.add_message("Assistant", str(response), "assistant")
                # Speak the response
                voice_handler.speak(str(response))
        
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            self.add_message("Assistant", error_msg, "assistant")
            voice_handler.speak(error_msg)
    
    def toggle_voice(self):
        """Toggle continuous voice listening"""
        if not self.is_listening:
            self.is_listening = True
            self.voice_btn.configure(text="🔇 Stop Listening")
            self.status_label.configure(text="🟢 Listening...")
            
            # Start voice recognition in separate thread
            voice_handler.start_continuous_listening(self.handle_voice_command)
        else:
            self.is_listening = False
            self.voice_btn.configure(text="🎤 Start Listening")
            self.status_label.configure(text="🔴 Not Listening")
            voice_handler.stop_listening()
    
    def voice_command_once(self):
        """Listen for a single voice command"""
        def listen_once():
            self.status_label.configure(text="🟡 Listening for command...")
            command = voice_handler.listen_once(timeout=10)
            
            if command:
                self.add_message("You", command, "user")
                self.process_command(command)
            else:
                self.add_message("System", "No voice input detected.", "system")
            
            self.status_label.configure(text="🔴 Not Listening")
        
        threading.Thread(target=listen_once, daemon=True).start()
    
    def handle_voice_command(self, command):
        """Handle voice command from continuous listening"""
        self.window.after(0, lambda: self.add_message("You", command, "user"))
        self.window.after(0, lambda: self.process_command(command))
    
    def execute_quick_action(self, command):
        """Execute quick action"""
        self.add_message("You", command, "user")
        threading.Thread(target=self.process_command, args=(command,), daemon=True).start()
    
    def show_help(self):
        """Show help information"""
        help_response = self.command_processor.show_help()
        self.add_message("Assistant", help_response, "assistant")
    
    def show_history(self):
        """Show chat history"""
        history_response = self.command_processor.show_history()
        self.add_message("Assistant", history_response, "assistant")
    
    def show_settings(self):
        """Show settings window"""
        SettingsWindow(self.window)
    
    def clear_chat(self):
        """Clear chat display"""
        self.chat_display.delete("1.0", "end")
        assistant_name = config.get('assistant_name', 'Assistant')
        self.add_message("System", f"Chat cleared. I'm {assistant_name}, ready to help!", "system")
    
    def run(self):
        """Run the main application"""
        self.window.mainloop()

class SettingsWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Settings")
        self.window.geometry("500x400")
        self.window.resizable(False, False)
        
        # Make modal
        self.window.transient(parent)
        self.window.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup settings UI"""
        # Title
        title_label = ctk.CTkLabel(
            self.window,
            text="⚙️ Settings",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Settings frame
        settings_frame = ctk.CTkFrame(self.window)
        settings_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Assistant name
        name_label = ctk.CTkLabel(settings_frame, text="Assistant Name:")
        name_label.pack(pady=(20, 5))
        
        self.name_entry = ctk.CTkEntry(
            settings_frame,
            width=300,
            height=40
        )
        self.name_entry.insert(0, config.get('assistant_name', 'Assistant'))
        self.name_entry.pack(pady=5)
        
        # Voice type
        voice_label = ctk.CTkLabel(settings_frame, text="Voice Type:")
        voice_label.pack(pady=(20, 5))
        
        self.voice_var = tk.StringVar(value=config.get('voice_type', 'female'))
        voice_frame = ctk.CTkFrame(settings_frame)
        voice_frame.pack(pady=5)
        
        male_radio = ctk.CTkRadioButton(
            voice_frame,
            text="Male",
            variable=self.voice_var,
            value="male"
        )
        male_radio.pack(side="left", padx=20)
        
        female_radio = ctk.CTkRadioButton(
            voice_frame,
            text="Female",
            variable=self.voice_var,
            value="female"
        )
        female_radio.pack(side="right", padx=20)
        
        # Voice speed
        speed_label = ctk.CTkLabel(settings_frame, text="Voice Speed:")
        speed_label.pack(pady=(20, 5))
        
        self.speed_slider = ctk.CTkSlider(
            settings_frame,
            from_=100,
            to=300,
            width=300
        )
        self.speed_slider.set(config.get('voice_speed', 180))
        self.speed_slider.pack(pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(settings_frame)
        button_frame.pack(pady=20)
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="Save",
            command=self.save_settings,
            width=120
        )
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.window.destroy,
            width=120
        )
        cancel_btn.pack(side="right", padx=10)
    
    def save_settings(self):
        """Save settings"""
        new_name = self.name_entry.get().strip()
        if new_name:
            config.update_assistant_name(new_name)
        
        config.set('voice_type', self.voice_var.get())
        config.set('voice_speed', int(self.speed_slider.get()))
        
        # Update voice handler
        voice_handler.change_voice(self.voice_var.get())
        
        messagebox.showinfo("Success", "Settings saved successfully!")
        self.window.destroy()

def main():
    """Main entry point"""
    # Check if this is first run
    if not config.config_file.exists():
        # First time setup
        from first_time_setup import FirstTimeSetup
        setup = FirstTimeSetup()
        setup.run()
    
    # Start login window
    login_app = LoginWindow()
    login_app.run()

if __name__ == "__main__":
    main()