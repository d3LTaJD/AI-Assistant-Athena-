"""
Enhanced GUI with 3D Avatar Animation and Advanced Features
"""
import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
import threading
import queue
import json
import math
import time
import random
from datetime import datetime

from database import db
from advanced_voice_handler import advanced_voice_handler
from smart_command_processor import SmartCommandProcessor
from config import config

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AnimatedAvatar:
    def __init__(self, canvas, size=150):
        self.canvas = canvas
        self.size = size
        self.center_x = size // 2
        self.center_y = size // 2
        
        # Animation state
        self.is_speaking = False
        self.is_listening = False
        self.pulse_phase = 0
        self.wave_phase = 0
        
        # Colors
        self.base_color = "#4A90E2"
        self.speaking_color = "#E24A4A"
        self.listening_color = "#4AE24A"
        
        self.setup_avatar()
        self.start_animation()
    
    def setup_avatar(self):
        """Setup the 3D-style avatar"""
        # Create base circle (head)
        self.head = self.canvas.create_oval(
            20, 20, self.size-20, self.size-20,
            fill=self.base_color,
            outline="#2E5C8A",
            width=3
        )
        
        # Create eyes
        eye_y = self.center_y - 20
        self.left_eye = self.canvas.create_oval(
            self.center_x - 30, eye_y - 10,
            self.center_x - 10, eye_y + 10,
            fill="white", outline="black", width=2
        )
        
        self.right_eye = self.canvas.create_oval(
            self.center_x + 10, eye_y - 10,
            self.center_x + 30, eye_y + 10,
            fill="white", outline="black", width=2
        )
        
        # Create pupils
        self.left_pupil = self.canvas.create_oval(
            self.center_x - 25, eye_y - 5,
            self.center_x - 15, eye_y + 5,
            fill="black"
        )
        
        self.right_pupil = self.canvas.create_oval(
            self.center_x + 15, eye_y - 5,
            self.center_x + 25, eye_y + 5,
            fill="black"
        )
        
        # Create mouth
        self.mouth = self.canvas.create_arc(
            self.center_x - 25, self.center_y + 10,
            self.center_x + 25, self.center_y + 40,
            start=0, extent=180,
            outline="black", width=3,
            style="arc"
        )
        
        # Create sound waves (initially hidden)
        self.sound_waves = []
        for i in range(3):
            wave = self.canvas.create_oval(
                self.center_x - 30 - (i*15), self.center_y - 30 - (i*15),
                self.center_x + 30 + (i*15), self.center_y + 30 + (i*15),
                outline=self.base_color, width=2,
                state="hidden"
            )
            self.sound_waves.append(wave)
    
    def start_animation(self):
        """Start the animation loop"""
        self.animate()
    
    def animate(self):
        """Main animation loop"""
        self.pulse_phase += 0.1
        self.wave_phase += 0.2
        
        # Pulse effect
        pulse_scale = 1 + 0.05 * math.sin(self.pulse_phase)
        
        # Update avatar color based on state
        if self.is_speaking:
            color = self.speaking_color
            self.animate_speaking()
        elif self.is_listening:
            color = self.listening_color
            self.animate_listening()
        else:
            color = self.base_color
            self.hide_sound_waves()
        
        # Update head color
        self.canvas.itemconfig(self.head, fill=color)
        
        # Blink animation
        if random.randint(1, 100) < 3:  # 3% chance to blink
            self.blink()
        
        # Schedule next animation frame
        self.canvas.after(50, self.animate)
    
    def animate_speaking(self):
        """Animate speaking state"""
        # Show sound waves
        for i, wave in enumerate(self.sound_waves):
            self.canvas.itemconfig(wave, state="normal")
            # Animate wave expansion
            wave_scale = 1 + 0.3 * math.sin(self.wave_phase + i * 0.5)
            # Update wave size (simplified)
        
        # Animate mouth movement
        mouth_height = 20 + 10 * math.sin(self.wave_phase * 2)
        self.canvas.coords(
            self.mouth,
            self.center_x - 25, self.center_y + 10,
            self.center_x + 25, self.center_y + 10 + mouth_height
        )
    
    def animate_listening(self):
        """Animate listening state"""
        # Show subtle sound waves
        for i, wave in enumerate(self.sound_waves):
            self.canvas.itemconfig(wave, state="normal", outline=self.listening_color)
        
        # Subtle mouth movement
        self.canvas.coords(
            self.mouth,
            self.center_x - 20, self.center_y + 15,
            self.center_x + 20, self.center_y + 35
        )
    
    def hide_sound_waves(self):
        """Hide sound waves"""
        for wave in self.sound_waves:
            self.canvas.itemconfig(wave, state="hidden")
        
        # Reset mouth
        self.canvas.coords(
            self.mouth,
            self.center_x - 25, self.center_y + 10,
            self.center_x + 25, self.center_y + 40
        )
    
    def blink(self):
        """Blink animation"""
        # Close eyes
        self.canvas.coords(self.left_eye, 
                          self.center_x - 30, self.center_y - 22,
                          self.center_x - 10, self.center_y - 18)
        self.canvas.coords(self.right_eye,
                          self.center_x + 10, self.center_y - 22,
                          self.center_x + 30, self.center_y - 18)
        
        # Open eyes after delay
        self.canvas.after(150, self.open_eyes)
    
    def open_eyes(self):
        """Open eyes after blink"""
        eye_y = self.center_y - 20
        self.canvas.coords(self.left_eye,
                          self.center_x - 30, eye_y - 10,
                          self.center_x - 10, eye_y + 10)
        self.canvas.coords(self.right_eye,
                          self.center_x + 10, eye_y - 10,
                          self.center_x + 30, eye_y + 10)
    
    def set_speaking(self, speaking):
        """Set speaking state"""
        self.is_speaking = speaking
    
    def set_listening(self, listening):
        """Set listening state"""
        self.is_listening = listening

class EnhancedMainApplication:
    def __init__(self, user_id):
        self.user_id = user_id
        self.command_processor = SmartCommandProcessor(user_id)
        self.is_listening = False
        self.avatar = None
        
        # Create main window
        self.window = ctk.CTk()
        self.window.title(f"🤖 {config.get('assistant_name', 'Assistant')} - Advanced AI Assistant")
        self.window.geometry("1200x800")
        
        # Center window
        self.center_window()
        
        self.setup_ui()
        self.setup_voice()
        
        # Start with welcome message
        self.add_message("System", f"🚀 Welcome! I'm {config.get('assistant_name', 'Assistant')}, your advanced AI assistant. I can hear you from across the room - just say my name!", "system")
    
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.window.winfo_screenheight() // 2) - (800 // 2)
        self.window.geometry(f"1200x800+{x}+{y}")
    
    def setup_ui(self):
        """Setup enhanced UI with 3D avatar"""
        # Main container
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header with avatar
        header_frame = ctk.CTkFrame(main_frame, height=200)
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Avatar section
        avatar_frame = ctk.CTkFrame(header_frame)
        avatar_frame.pack(side="left", padx=20, pady=20)
        
        # Create canvas for 3D avatar
        self.avatar_canvas = tk.Canvas(
            avatar_frame,
            width=150,
            height=150,
            bg="#212121",
            highlightthickness=0
        )
        self.avatar_canvas.pack(padx=10, pady=10)
        
        # Initialize animated avatar
        self.avatar = AnimatedAvatar(self.avatar_canvas)
        
        # Assistant info
        info_frame = ctk.CTkFrame(header_frame)
        info_frame.pack(side="left", fill="both", expand=True, padx=(10, 20), pady=20)
        
        assistant_name = config.get('assistant_name', 'Assistant')
        self.header_label = ctk.CTkLabel(
            info_frame,
            text=f"🤖 {assistant_name}",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.header_label.pack(pady=(20, 5))
        
        self.subtitle_label = ctk.CTkLabel(
            info_frame,
            text="Advanced AI Assistant with Room-Scale Voice Recognition",
            font=ctk.CTkFont(size=14)
        )
        self.subtitle_label.pack(pady=(0, 10))
        
        # Status indicators
        status_frame = ctk.CTkFrame(info_frame)
        status_frame.pack(fill="x", pady=10)
        
        self.voice_status = ctk.CTkLabel(
            status_frame,
            text="🔴 Voice: Not Listening",
            font=ctk.CTkFont(size=12)
        )
        self.voice_status.pack(side="left", padx=10)
        
        self.system_status = ctk.CTkLabel(
            status_frame,
            text="🟢 System: Online",
            font=ctk.CTkFont(size=12)
        )
        self.system_status.pack(side="right", padx=10)
        
        # Main content area
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True)
        
        # Left panel - Chat
        chat_frame = ctk.CTkFrame(content_frame)
        chat_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Chat header
        chat_header = ctk.CTkFrame(chat_frame)
        chat_header.pack(fill="x", padx=10, pady=(10, 0))
        
        chat_title = ctk.CTkLabel(
            chat_header,
            text="💬 Conversation",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        chat_title.pack(side="left", pady=10)
        
        # Chat controls
        self.auto_scroll_var = ctk.BooleanVar(value=True)
        auto_scroll_check = ctk.CTkCheckBox(
            chat_header,
            text="Auto-scroll",
            variable=self.auto_scroll_var
        )
        auto_scroll_check.pack(side="right", padx=10, pady=10)
        
        # Chat display with enhanced styling
        self.chat_display = ctk.CTkTextbox(
            chat_frame,
            width=700,
            height=400,
            font=ctk.CTkFont(size=12),
            wrap="word"
        )
        self.chat_display.pack(padx=10, pady=(10, 0), fill="both", expand=True)
        
        # Input section
        input_section = ctk.CTkFrame(chat_frame)
        input_section.pack(fill="x", padx=10, pady=10)
        
        # Text input with enhanced features
        input_frame = ctk.CTkFrame(input_section)
        input_frame.pack(fill="x", pady=(0, 10))
        
        self.text_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="Type your message here... (or use voice)",
            height=40,
            font=ctk.CTkFont(size=12)
        )
        self.text_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.text_input.bind('<Return>', self.send_text_message)
        self.text_input.bind('<Up>', self.recall_last_command)
        
        # Send button
        send_btn = ctk.CTkButton(
            input_frame,
            text="📤 Send",
            command=self.send_text_message,
            width=80,
            height=40
        )
        send_btn.pack(side="right")
        
        # Voice controls with enhanced features
        voice_frame = ctk.CTkFrame(input_section)
        voice_frame.pack(fill="x")
        
        # Continuous listening toggle
        self.voice_btn = ctk.CTkButton(
            voice_frame,
            text="🎤 Start Room Listening",
            command=self.toggle_voice,
            height=40,
            width=200
        )
        self.voice_btn.pack(side="left", padx=(0, 10))
        
        # One-time voice command
        voice_once_btn = ctk.CTkButton(
            voice_frame,
            text="🎙️ Voice Command",
            command=self.voice_command_once,
            height=40,
            width=150
        )
        voice_once_btn.pack(side="left", padx=(0, 10))
        
        # Microphone test
        mic_test_btn = ctk.CTkButton(
            voice_frame,
            text="🧪 Test Mic",
            command=self.test_microphone,
            height=40,
            width=100
        )
        mic_test_btn.pack(side="left")
        
        # Voice sensitivity slider
        sensitivity_frame = ctk.CTkFrame(voice_frame)
        sensitivity_frame.pack(side="right", padx=10)
        
        ctk.CTkLabel(sensitivity_frame, text="🎚️ Sensitivity:").pack(side="left", padx=(5, 0))
        
        self.sensitivity_slider = ctk.CTkSlider(
            sensitivity_frame,
            from_=1,
            to=10,
            number_of_steps=9,
            width=100,
            command=self.adjust_sensitivity
        )
        self.sensitivity_slider.set(5)
        self.sensitivity_slider.pack(side="right", padx=5)
        
        # Right panel - Enhanced controls and features
        right_panel = ctk.CTkFrame(content_frame, width=300)
        right_panel.pack(side="right", fill="y", padx=(5, 0))
        right_panel.pack_propagate(False)
        
        # Tabbed interface for right panel
        self.right_notebook = ctk.CTkTabview(right_panel)
        self.right_notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Quick Actions Tab
        self.setup_quick_actions_tab()
        
        # System Monitor Tab
        self.setup_system_monitor_tab()
        
        # Settings Tab
        self.setup_settings_tab()
        
        # History Tab
        self.setup_history_tab()
    
    def setup_quick_actions_tab(self):
        """Setup quick actions tab"""
        actions_tab = self.right_notebook.add("⚡ Actions")
        
        # Quick command buttons
        quick_actions = [
            ("📁 Downloads", "open downloads folder"),
            ("📄 Documents", "open documents folder"),
            ("🖥️ Desktop", "open desktop folder"),
            ("🎵 Music", "open music folder"),
            ("⏰ Time", "what time is it"),
            ("📅 Date", "what's the date"),
            ("📸 Screenshot", "take screenshot"),
            ("🖥️ System Status", "system status"),
            ("🎲 Roll Dice", "roll dice"),
            ("🪙 Flip Coin", "flip coin"),
            ("😂 Tell Joke", "tell me a joke"),
            ("🧠 Random Fact", "random fact")
        ]
        
        for i, (text, command) in enumerate(quick_actions):
            btn = ctk.CTkButton(
                actions_tab,
                text=text,
                command=lambda cmd=command: self.execute_quick_action(cmd),
                width=250,
                height=35
            )
            btn.pack(pady=3, padx=10, fill="x")
    
    def setup_system_monitor_tab(self):
        """Setup system monitoring tab"""
        monitor_tab = self.right_notebook.add("📊 Monitor")
        
        # System info display
        self.system_info_text = ctk.CTkTextbox(
            monitor_tab,
            height=200,
            font=ctk.CTkFont(size=10)
        )
        self.system_info_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            monitor_tab,
            text="🔄 Refresh",
            command=self.refresh_system_info,
            width=250
        )
        refresh_btn.pack(pady=10)
        
        # Auto-refresh toggle
        self.auto_refresh_var = ctk.BooleanVar(value=True)
        auto_refresh_check = ctk.CTkCheckBox(
            monitor_tab,
            text="Auto-refresh (30s)",
            variable=self.auto_refresh_var
        )
        auto_refresh_check.pack(pady=5)
        
        # Start auto-refresh
        self.refresh_system_info()
        self.start_auto_refresh()
    
    def setup_settings_tab(self):
        """Setup settings tab"""
        settings_tab = self.right_notebook.add("⚙️ Settings")
        
        # Assistant name
        name_frame = ctk.CTkFrame(settings_tab)
        name_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(name_frame, text="Assistant Name:").pack(pady=5)
        self.name_entry = ctk.CTkEntry(name_frame, width=200)
        self.name_entry.insert(0, config.get('assistant_name', 'Assistant'))
        self.name_entry.pack(pady=5)
        
        # Voice settings
        voice_frame = ctk.CTkFrame(settings_tab)
        voice_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(voice_frame, text="Voice Type:").pack(pady=5)
        
        self.voice_var = ctk.StringVar(value=config.get('voice_type', 'female'))
        voice_radio_frame = ctk.CTkFrame(voice_frame)
        voice_radio_frame.pack(pady=5)
        
        ctk.CTkRadioButton(
            voice_radio_frame,
            text="Female",
            variable=self.voice_var,
            value="female"
        ).pack(side="left", padx=10)
        
        ctk.CTkRadioButton(
            voice_radio_frame,
            text="Male",
            variable=self.voice_var,
            value="male"
        ).pack(side="right", padx=10)
        
        # Voice speed
        ctk.CTkLabel(voice_frame, text="Voice Speed:").pack(pady=(10, 5))
        self.speed_slider = ctk.CTkSlider(
            voice_frame,
            from_=100,
            to=300,
            width=200
        )
        self.speed_slider.set(config.get('voice_speed', 180))
        self.speed_slider.pack(pady=5)
        
        # Save settings button
        save_btn = ctk.CTkButton(
            settings_tab,
            text="💾 Save Settings",
            command=self.save_settings,
            width=250
        )
        save_btn.pack(pady=20)
        
        # Advanced settings
        advanced_frame = ctk.CTkFrame(settings_tab)
        advanced_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(advanced_frame, text="Advanced:").pack(pady=5)
        
        # Theme toggle
        self.theme_var = ctk.StringVar(value="dark")
        theme_btn = ctk.CTkButton(
            advanced_frame,
            text="🌓 Toggle Theme",
            command=self.toggle_theme,
            width=200
        )
        theme_btn.pack(pady=5)
    
    def setup_history_tab(self):
        """Setup history tab"""
        history_tab = self.right_notebook.add("📜 History")
        
        # History display
        self.history_text = ctk.CTkTextbox(
            history_tab,
            height=300,
            font=ctk.CTkFont(size=10)
        )
        self.history_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # History controls
        history_controls = ctk.CTkFrame(history_tab)
        history_controls.pack(fill="x", padx=10, pady=5)
        
        refresh_history_btn = ctk.CTkButton(
            history_controls,
            text="🔄 Refresh",
            command=self.refresh_history,
            width=120
        )
        refresh_history_btn.pack(side="left", padx=5)
        
        clear_history_btn = ctk.CTkButton(
            history_controls,
            text="🗑️ Clear",
            command=self.clear_history,
            width=120
        )
        clear_history_btn.pack(side="right", padx=5)
        
        # Load initial history
        self.refresh_history()
    
    def setup_voice(self):
        """Setup voice recognition"""
        self.voice_queue = queue.Queue()
        self.last_commands = []
    
    def add_message(self, sender, message, msg_type="user"):
        """Add message to chat display with enhanced formatting"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Color and icon coding
        if msg_type == "system":
            prefix = "🤖 System"
            color = "#4A90E2"
        elif msg_type == "assistant":
            assistant_name = config.get('assistant_name', 'Assistant')
            prefix = f"🤖 {assistant_name}"
            color = "#4AE24A"
        else:
            prefix = "👤 You"
            color = "#E2E2E2"
        
        # Format message with timestamp and styling
        formatted_message = f"[{timestamp}] {prefix}: {message}\n\n"
        
        # Insert message
        self.chat_display.insert("end", formatted_message)
        
        # Auto-scroll if enabled
        if self.auto_scroll_var.get():
            self.chat_display.see("end")
        
        # Update avatar state
        if self.avatar:
            if msg_type == "assistant":
                self.avatar.set_speaking(True)
                # Stop speaking animation after estimated speech time
                speech_duration = max(2000, len(message) * 50)  # Estimate based on message length
                self.window.after(speech_duration, lambda: self.avatar.set_speaking(False))
    
    def send_text_message(self, event=None):
        """Send text message with command history"""
        message = self.text_input.get().strip()
        if not message:
            return
        
        # Add to command history
        self.last_commands.append(message)
        if len(self.last_commands) > 20:
            self.last_commands = self.last_commands[-20:]
        
        self.text_input.delete(0, "end")
        self.add_message("You", message, "user")
        
        # Process command in separate thread
        threading.Thread(target=self.process_command, args=(message,), daemon=True).start()
    
    def recall_last_command(self, event):
        """Recall last command with Up arrow"""
        if self.last_commands:
            self.text_input.delete(0, "end")
            self.text_input.insert(0, self.last_commands[-1])
    
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
                advanced_voice_handler.speak(str(response))
        
        except Exception as e:
            error_msg = f"I encountered an error: {str(e)}"
            self.add_message("Assistant", error_msg, "assistant")
            advanced_voice_handler.speak(error_msg)
    
    def toggle_voice(self):
        """Toggle continuous voice listening with room-scale detection"""
        if not self.is_listening:
            self.is_listening = True
            self.voice_btn.configure(text="🔇 Stop Listening")
            self.voice_status.configure(text="🟢 Voice: Room Listening Active")
            
            if self.avatar:
                self.avatar.set_listening(True)
            
            # Start advanced voice recognition
            advanced_voice_handler.start_continuous_listening(self.handle_voice_command)
        else:
            self.is_listening = False
            self.voice_btn.configure(text="🎤 Start Room Listening")
            self.voice_status.configure(text="🔴 Voice: Not Listening")
            
            if self.avatar:
                self.avatar.set_listening(False)
            
            advanced_voice_handler.stop_listening()
    
    def voice_command_once(self):
        """Listen for a single voice command"""
        def listen_once():
            self.voice_status.configure(text="🟡 Voice: Listening for command...")
            if self.avatar:
                self.avatar.set_listening(True)
            
            command = advanced_voice_handler.listen_once(timeout=10)
            
            if command:
                self.add_message("You", command, "user")
                self.process_command(command)
            else:
                self.add_message("System", "No voice input detected.", "system")
            
            self.voice_status.configure(text="🔴 Voice: Not Listening")
            if self.avatar:
                self.avatar.set_listening(False)
        
        threading.Thread(target=listen_once, daemon=True).start()
    
    def test_microphone(self):
        """Test microphone functionality"""
        def test_mic():
            self.add_message("System", "Testing microphone... Please speak.", "system")
            success = advanced_voice_handler.test_microphone()
            if success:
                self.add_message("System", "✅ Microphone test successful!", "system")
            else:
                self.add_message("System", "❌ Microphone test failed. Check your setup.", "system")
        
        threading.Thread(target=test_mic, daemon=True).start()
    
    def adjust_sensitivity(self, value):
        """Adjust microphone sensitivity"""
        sensitivity = int(value)
        advanced_voice_handler.adjust_sensitivity(sensitivity)
        self.add_message("System", f"🎚️ Microphone sensitivity set to {sensitivity}/10", "system")
    
    def handle_voice_command(self, command):
        """Handle voice command from continuous listening"""
        self.window.after(0, lambda: self.add_message("You", command, "user"))
        self.window.after(0, lambda: self.process_command(command))
    
    def execute_quick_action(self, command):
        """Execute quick action"""
        self.add_message("You", command, "user")
        threading.Thread(target=self.process_command, args=(command,), daemon=True).start()
    
    def refresh_system_info(self):
        """Refresh system information display"""
        def get_system_info():
            try:
                import psutil
                
                # Get system information
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                info = f"""🖥️ SYSTEM STATUS
{'='*30}
💾 Memory: {memory.percent:.1f}% used
   ({memory.used//1024//1024//1024:.1f}GB / {memory.total//1024//1024//1024:.1f}GB)

🔥 CPU: {cpu_percent:.1f}% usage
   Cores: {psutil.cpu_count()} physical

💿 Disk: {disk.percent:.1f}% used
   ({disk.used//1024//1024//1024:.1f}GB / {disk.total//1024//1024//1024:.1f}GB)

🌐 Network: {len(psutil.net_if_addrs())} interfaces

⏱️ Uptime: {datetime.now() - datetime.fromtimestamp(psutil.boot_time())}

🔄 Last updated: {datetime.now().strftime('%H:%M:%S')}
"""
                
                self.window.after(0, lambda: self.update_system_display(info))
                
            except Exception as e:
                error_info = f"System info error: {str(e)}"
                self.window.after(0, lambda: self.update_system_display(error_info))
        
        threading.Thread(target=get_system_info, daemon=True).start()
    
    def update_system_display(self, info):
        """Update system information display"""
        self.system_info_text.delete("1.0", "end")
        self.system_info_text.insert("1.0", info)
    
    def start_auto_refresh(self):
        """Start auto-refresh for system info"""
        def auto_refresh():
            if self.auto_refresh_var.get():
                self.refresh_system_info()
            self.window.after(30000, auto_refresh)  # 30 seconds
        
        self.window.after(30000, auto_refresh)
    
    def refresh_history(self):
        """Refresh chat history display"""
        try:
            history = db.get_chat_history(self.user_id, limit=20)
            
            history_text = "📜 RECENT CONVERSATIONS\n" + "="*40 + "\n\n"
            
            for prompt, response, timestamp in history:
                time_str = timestamp[:19] if timestamp else "Unknown"
                history_text += f"[{time_str}]\n"
                history_text += f"👤 {prompt}\n"
                history_text += f"🤖 {response[:100]}{'...' if len(response) > 100 else ''}\n\n"
            
            self.history_text.delete("1.0", "end")
            self.history_text.insert("1.0", history_text)
            
        except Exception as e:
            error_text = f"Error loading history: {str(e)}"
            self.history_text.delete("1.0", "end")
            self.history_text.insert("1.0", error_text)
    
    def clear_history(self):
        """Clear chat history"""
        if messagebox.askyesno("Clear History", "Are you sure you want to clear the chat history?"):
            self.chat_display.delete("1.0", "end")
            assistant_name = config.get('assistant_name', 'Assistant')
            self.add_message("System", f"Chat history cleared. I'm {assistant_name}, ready to help!", "system")
    
    def save_settings(self):
        """Save settings with immediate effect"""
        try:
            # Update assistant name
            new_name = self.name_entry.get().strip()
            if new_name and new_name != config.get('assistant_name'):
                config.update_assistant_name(new_name)
                self.header_label.configure(text=f"🤖 {new_name}")
                self.window.title(f"🤖 {new_name} - Advanced AI Assistant")
            
            # Update voice settings
            config.set('voice_type', self.voice_var.get())
            config.set('voice_speed', int(self.speed_slider.get()))
            
            # Apply voice changes
            advanced_voice_handler.change_voice(self.voice_var.get())
            
            self.add_message("System", "✅ Settings saved successfully!", "system")
            
        except Exception as e:
            self.add_message("System", f"❌ Error saving settings: {str(e)}", "system")
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        current_mode = ctk.get_appearance_mode()
        new_mode = "light" if current_mode == "dark" else "dark"
        ctk.set_appearance_mode(new_mode)
        self.add_message("System", f"🌓 Theme changed to {new_mode} mode", "system")
    
    def run(self):
        """Run the enhanced application"""
        try:
            self.window.mainloop()
        except Exception as e:
            print(f"Application error: {e}")

# Enhanced login window with better styling
class EnhancedLoginWindow:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("🤖 Advanced AI Assistant - Login")
        self.window.geometry("500x600")
        self.window.resizable(False, False)
        
        # Center window
        self.center_window()
        
        self.setup_ui()
        
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (600 // 2)
        self.window.geometry(f"500x600+{x}+{y}")
    
    def setup_ui(self):
        """Setup enhanced login UI"""
        # Header with gradient effect simulation
        header_frame = ctk.CTkFrame(self.window, height=150)
        header_frame.pack(fill="x", padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        # Title with enhanced styling
        title_label = ctk.CTkLabel(
            header_frame,
            text="🤖 AI Assistant",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=20)
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Advanced Room-Scale Voice Recognition",
            font=ctk.CTkFont(size=14)
        )
        subtitle_label.pack()
        
        # Login form
        form_frame = ctk.CTkFrame(self.window)
        form_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Form title
        form_title = ctk.CTkLabel(
            form_frame,
            text="Welcome Back",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        form_title.pack(pady=30)
        
        # Email entry with icon
        email_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        email_frame.pack(pady=10, fill="x", padx=20)
        
        ctk.CTkLabel(email_frame, text="📧", font=ctk.CTkFont(size=16)).pack(side="left", padx=(0, 10))
        self.email_entry = ctk.CTkEntry(
            email_frame,
            placeholder_text="Email Address",
            height=45,
            font=ctk.CTkFont(size=12)
        )
        self.email_entry.pack(side="right", fill="x", expand=True)
        
        # Password entry with icon
        password_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        password_frame.pack(pady=10, fill="x", padx=20)
        
        ctk.CTkLabel(password_frame, text="🔒", font=ctk.CTkFont(size=16)).pack(side="left", padx=(0, 10))
        self.password_entry = ctk.CTkEntry(
            password_frame,
            placeholder_text="Password",
            show="*",
            height=45,
            font=ctk.CTkFont(size=12)
        )
        self.password_entry.pack(side="right", fill="x", expand=True)
        
        # Login button with enhanced styling
        login_btn = ctk.CTkButton(
            form_frame,
            text="🚀 Login",
            command=self.login,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        login_btn.pack(pady=30, padx=20, fill="x")
        
        # Signup button
        signup_btn = ctk.CTkButton(
            form_frame,
            text="✨ Create New Account",
            command=self.show_signup,
            height=45,
            fg_color="transparent",
            border_width=2,
            font=ctk.CTkFont(size=14)
        )
        signup_btn.pack(pady=10, padx=20, fill="x")
        
        # Features preview
        features_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        features_frame.pack(pady=20, fill="x", padx=20)
        
        features_text = """🎤 Room-scale voice recognition
🤖 3D animated assistant avatar  
🧠 Advanced AI capabilities
📊 Real-time system monitoring
⚡ Quick action shortcuts"""
        
        ctk.CTkLabel(
            features_frame,
            text=features_text,
            font=ctk.CTkFont(size=11),
            justify="left"
        ).pack()
        
        # Bind Enter key
        self.window.bind('<Return>', lambda e: self.login())
    
    def login(self):
        """Handle enhanced login"""
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
            # Start enhanced main application
            app = EnhancedMainApplication(user['id'])
            app.run()
        else:
            messagebox.showerror("Error", "Invalid email or password")
    
    def show_signup(self):
        """Show enhanced signup window"""
        EnhancedSignupWindow(self.window)
    
    def run(self):
        """Run the enhanced login window"""
        self.window.mainloop()

class EnhancedSignupWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Create Your AI Assistant Account")
        self.window.geometry("500x700")
        self.window.resizable(False, False)
        
        # Make modal
        self.window.transient(parent)
        self.window.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup enhanced signup UI"""
        # Header
        header_frame = ctk.CTkFrame(self.window)
        header_frame.pack(fill="x", padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🚀 Create Your AI Assistant",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Form
        form_frame = ctk.CTkFrame(self.window)
        form_frame.pack(pady=10, padx=30, fill="both", expand=True)
        
        # Email
        ctk.CTkLabel(form_frame, text="📧 Email Address:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=20, pady=(20, 5))
        self.email_entry = ctk.CTkEntry(form_frame, height=40, font=ctk.CTkFont(size=12))
        self.email_entry.pack(fill="x", padx=20, pady=(0, 10))
        
        # Password
        ctk.CTkLabel(form_frame, text="🔒 Password:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
        self.password_entry = ctk.CTkEntry(form_frame, show="*", height=40, font=ctk.CTkFont(size=12))
        self.password_entry.pack(fill="x", padx=20, pady=(0, 10))
        
        # Confirm password
        ctk.CTkLabel(form_frame, text="🔒 Confirm Password:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
        self.confirm_password_entry = ctk.CTkEntry(form_frame, show="*", height=40, font=ctk.CTkFont(size=12))
        self.confirm_password_entry.pack(fill="x", padx=20, pady=(0, 10))
        
        # Assistant name
        ctk.CTkLabel(form_frame, text="🤖 Assistant Name (Wake Word):", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
        self.assistant_name_entry = ctk.CTkEntry(form_frame, height=40, font=ctk.CTkFont(size=12))
        self.assistant_name_entry.insert(0, "Jarvis")
        self.assistant_name_entry.pack(fill="x", padx=20, pady=(0, 10))
        
        # Voice preference
        voice_frame = ctk.CTkFrame(form_frame)
        voice_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(voice_frame, text="🎤 Voice Preference:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=10)
        
        self.voice_var = tk.StringVar(value="female")
        voice_radio_frame = ctk.CTkFrame(voice_frame)
        voice_radio_frame.pack(pady=10)
        
        ctk.CTkRadioButton(voice_radio_frame, text="👩 Female Voice", variable=self.voice_var, value="female").pack(side="left", padx=20)
        ctk.CTkRadioButton(voice_radio_frame, text="👨 Male Voice", variable=self.voice_var, value="male").pack(side="right", padx=20)
        
        # Features info
        info_frame = ctk.CTkFrame(form_frame)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_text = """✨ Your AI assistant will feature:
• 🎤 Room-scale voice recognition
• 🤖 3D animated avatar
• 📁 Smart file management
• 🖥️ System monitoring
• 🧠 Advanced AI capabilities"""
        
        ctk.CTkLabel(info_frame, text=info_text, font=ctk.CTkFont(size=11), justify="left").pack(pady=15)
        
        # Buttons
        button_frame = ctk.CTkFrame(form_frame)
        button_frame.pack(fill="x", padx=20, pady=20)
        
        create_btn = ctk.CTkButton(
            button_frame,
            text="🚀 Create My Assistant",
            command=self.create_account,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        create_btn.pack(fill="x", pady=(0, 10))
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="❌ Cancel",
            command=self.window.destroy,
            height=40,
            fg_color="transparent",
            border_width=2
        )
        cancel_btn.pack(fill="x")
    
    def create_account(self):
        """Handle enhanced account creation"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        assistant_name = self.assistant_name_entry.get().strip() or "Assistant"
        voice_preference = self.voice_var.get()
        
        # Enhanced validation
        if not email or not password:
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        
        if len(assistant_name) < 2:
            messagebox.showerror("Error", "Assistant name must be at least 2 characters")
            return
        
        # Create user
        user_id = db.create_user(email, password, assistant_name, voice_preference)
        if user_id:
            messagebox.showinfo(
                "Success!", 
                f"🎉 Account created successfully!\n\n"
                f"Your AI assistant '{assistant_name}' is ready with:\n"
                f"• {voice_preference.title()} voice\n"
                f"• Room-scale voice recognition\n"
                f"• Advanced AI capabilities\n\n"
                f"Say '{assistant_name}' to activate!"
            )
            self.window.destroy()
        else:
            messagebox.showerror("Error", "Email already exists")

def main():
    """Enhanced main entry point"""
    print("🚀 Starting Advanced AI Assistant...")
    
    # Check if this is first run
    if not config.config_file.exists():
        # First time setup
        from first_time_setup import FirstTimeSetup
        setup = FirstTimeSetup()
        setup.run()
    
    # Start enhanced login window
    login_app = EnhancedLoginWindow()
    login_app.run()

if __name__ == "__main__":
    main()