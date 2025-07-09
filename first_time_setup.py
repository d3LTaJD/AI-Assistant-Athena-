"""
First time setup for AI Assistant
"""
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from config import config
from database import db

class FirstTimeSetup:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("AI Assistant - First Time Setup")
        self.window.geometry("600x500")
        self.window.resizable(False, False)
        
        # Center window
        self.center_window()
        
        self.setup_ui()
    
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.window.winfo_screenheight() // 2) - (500 // 2)
        self.window.geometry(f"600x500+{x}+{y}")
    
    def setup_ui(self):
        """Setup first time setup UI"""
        # Title
        title_label = ctk.CTkLabel(
            self.window,
            text="🤖 Welcome to AI Assistant!",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=30)
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            self.window,
            text="Let's set up your personal AI assistant",
            font=ctk.CTkFont(size=16)
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Setup frame
        setup_frame = ctk.CTkFrame(self.window)
        setup_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Assistant name
        name_label = ctk.CTkLabel(
            setup_frame,
            text="What would you like to name your assistant?",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        name_label.pack(pady=(20, 10))
        
        name_sublabel = ctk.CTkLabel(
            setup_frame,
            text="This will also be your wake word (e.g., Jarvis, Athena, Alex)",
            font=ctk.CTkFont(size=12)
        )
        name_sublabel.pack(pady=(0, 10))
        
        self.name_entry = ctk.CTkEntry(
            setup_frame,
            placeholder_text="Enter assistant name...",
            width=400,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.name_entry.pack(pady=10)
        
        # Voice preference
        voice_label = ctk.CTkLabel(
            setup_frame,
            text="Choose voice preference:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        voice_label.pack(pady=(30, 10))
        
        self.voice_var = tk.StringVar(value="female")
        voice_frame = ctk.CTkFrame(setup_frame)
        voice_frame.pack(pady=10)
        
        male_radio = ctk.CTkRadioButton(
            voice_frame,
            text="Male Voice",
            variable=self.voice_var,
            value="male",
            font=ctk.CTkFont(size=14)
        )
        male_radio.pack(side="left", padx=30, pady=20)
        
        female_radio = ctk.CTkRadioButton(
            voice_frame,
            text="Female Voice",
            variable=self.voice_var,
            value="female",
            font=ctk.CTkFont(size=14)
        )
        female_radio.pack(side="right", padx=30, pady=20)
        
        # Features info
        features_label = ctk.CTkLabel(
            setup_frame,
            text="Your assistant will be able to:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        features_label.pack(pady=(20, 10))
        
        features_text = """• Open files and folders on your computer
• Perform calculations and answer questions
• Control system functions (with your permission)
• Search the web and YouTube (requires internet)
• Remember your preferences and chat history"""
        
        features_info = ctk.CTkLabel(
            setup_frame,
            text=features_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        features_info.pack(pady=10)
        
        # Continue button
        continue_btn = ctk.CTkButton(
            setup_frame,
            text="Continue to Account Creation",
            command=self.complete_setup,
            width=300,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        continue_btn.pack(pady=30)
        
        # Set default name
        self.name_entry.insert(0, "Jarvis")
    
    def complete_setup(self):
        """Complete the setup process"""
        assistant_name = self.name_entry.get().strip()
        
        if not assistant_name:
            messagebox.showerror("Error", "Please enter an assistant name")
            return
        
        if len(assistant_name) < 2:
            messagebox.showerror("Error", "Assistant name must be at least 2 characters")
            return
        
        # Save configuration
        config.update_assistant_name(assistant_name)
        config.set('voice_type', self.voice_var.get())
        
        # Show completion message
        messagebox.showinfo(
            "Setup Complete!",
            f"Great! Your assistant '{assistant_name}' is ready.\n\n"
            f"You can now call your assistant by saying '{assistant_name}' "
            f"followed by your command.\n\n"
            f"Next, you'll create your user account."
        )
        
        self.window.destroy()
    
    def run(self):
        """Run the setup window"""
        self.window.mainloop()