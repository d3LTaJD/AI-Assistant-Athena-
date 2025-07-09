"""
Notification System for Athena AI Assistant
Provides desktop notifications and alerts
"""

import tkinter as tk
from tkinter import messagebox
import threading
import time
from datetime import datetime, timedelta
import json
from pathlib import Path

try:
    # Try to import plyer for cross-platform notifications
    from plyer import notification
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False

class NotificationManager:
    def __init__(self):
        self.notifications_enabled = True
        self.notification_history = []
        self.scheduled_notifications = []
        self.notification_thread = None
        self.running = False
        
        # Start notification thread
        self.start_notification_thread()
    
    def start_notification_thread(self):
        """Start the notification monitoring thread"""
        self.running = True
        self.notification_thread = threading.Thread(target=self._notification_loop, daemon=True)
        self.notification_thread.start()
    
    def stop_notification_thread(self):
        """Stop the notification monitoring thread"""
        self.running = False
    
    def _notification_loop(self):
        """Main notification monitoring loop"""
        while self.running:
            try:
                current_time = datetime.now()
                
                # Check for scheduled notifications
                for notification in self.scheduled_notifications[:]:  # Copy list to avoid modification during iteration
                    if current_time >= notification['scheduled_time']:
                        self.show_notification(
                            notification['title'],
                            notification['message'],
                            notification['type']
                        )
                        self.scheduled_notifications.remove(notification)
                
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                print(f"Notification thread error: {e}")
                time.sleep(60)  # Wait longer on error
    
    def show_notification(self, title, message, notification_type="info", duration=5):
        """Show a desktop notification"""
        if not self.notifications_enabled:
            return
        
        try:
            # Add to history
            self.notification_history.append({
                'title': title,
                'message': message,
                'type': notification_type,
                'timestamp': datetime.now().isoformat()
            })
            
            # Keep only last 100 notifications
            if len(self.notification_history) > 100:
                self.notification_history = self.notification_history[-100:]
            
            # Show notification using plyer if available
            if PLYER_AVAILABLE:
                notification.notify(
                    title=title,
                    message=message,
                    timeout=duration,
                    app_name="Athena AI Assistant"
                )
            else:
                # Fallback to tkinter messagebox
                self._show_tkinter_notification(title, message, notification_type)
                
        except Exception as e:
            print(f"Error showing notification: {e}")
    
    def _show_tkinter_notification(self, title, message, notification_type):
        """Show notification using tkinter (fallback)"""
        try:
            # Create a temporary root window if none exists
            root = tk.Tk()
            root.withdraw()  # Hide the root window
            
            if notification_type == "error":
                messagebox.showerror(title, message)
            elif notification_type == "warning":
                messagebox.showwarning(title, message)
            else:
                messagebox.showinfo(title, message)
            
            root.destroy()
        except Exception as e:
            print(f"Tkinter notification error: {e}")
    
    def schedule_notification(self, title, message, delay_minutes, notification_type="info"):
        """Schedule a notification for later"""
        scheduled_time = datetime.now() + timedelta(minutes=delay_minutes)
        
        notification_data = {
            'title': title,
            'message': message,
            'type': notification_type,
            'scheduled_time': scheduled_time
        }
        
        self.scheduled_notifications.append(notification_data)
        
        return f"Notification scheduled for {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def show_connection_status(self, is_connected):
        """Show connection status notification"""
        if is_connected:
            self.show_notification(
                "Athena AI Assistant",
                "Internet connection restored. All features available.",
                "info"
            )
        else:
            self.show_notification(
                "Athena AI Assistant",
                "Internet connection lost. Some features may be limited.",
                "warning"
            )
    
    def show_error_notification(self, error_message, context="General"):
        """Show error notification"""
        self.show_notification(
            f"Athena Error - {context}",
            error_message,
            "error"
        )
    
    def show_success_notification(self, message, context="Success"):
        """Show success notification"""
        self.show_notification(
            f"Athena - {context}",
            message,
            "info"
        )
    
    def show_reminder_notification(self, reminder_text):
        """Show reminder notification"""
        self.show_notification(
            "Athena Reminder",
            reminder_text,
            "info"
        )
    
    def get_notification_history(self, limit=20):
        """Get recent notification history"""
        return self.notification_history[-limit:] if self.notification_history else []
    
    def clear_notification_history(self):
        """Clear notification history"""
        self.notification_history.clear()
    
    def enable_notifications(self):
        """Enable notifications"""
        self.notifications_enabled = True
        self.show_notification("Athena AI Assistant", "Notifications enabled", "info")
    
    def disable_notifications(self):
        """Disable notifications"""
        self.notifications_enabled = False
    
    def get_scheduled_notifications(self):
        """Get list of scheduled notifications"""
        return self.scheduled_notifications.copy()
    
    def cancel_scheduled_notification(self, index):
        """Cancel a scheduled notification by index"""
        try:
            if 0 <= index < len(self.scheduled_notifications):
                removed = self.scheduled_notifications.pop(index)
                return f"Cancelled notification: {removed['title']}"
            else:
                return "Invalid notification index"
        except Exception as e:
            return f"Error cancelling notification: {str(e)}"

class ToastNotification:
    """Custom toast notification window"""
    
    def __init__(self, title, message, duration=3000, notification_type="info"):
        self.title = title
        self.message = message
        self.duration = duration
        self.notification_type = notification_type
        
        self.create_toast()
    
    def create_toast(self):
        """Create and show toast notification"""
        # Create toast window
        self.toast = tk.Toplevel()
        self.toast.title("")
        self.toast.geometry("300x100")
        self.toast.resizable(False, False)
        
        # Remove window decorations
        self.toast.overrideredirect(True)
        
        # Position at bottom right of screen
        screen_width = self.toast.winfo_screenwidth()
        screen_height = self.toast.winfo_screenheight()
        x = screen_width - 320
        y = screen_height - 120
        self.toast.geometry(f"300x100+{x}+{y}")
        
        # Configure colors based on type
        colors = {
            "info": {"bg": "#2196F3", "fg": "white"},
            "success": {"bg": "#4CAF50", "fg": "white"},
            "warning": {"bg": "#FF9800", "fg": "white"},
            "error": {"bg": "#F44336", "fg": "white"}
        }
        
        color_scheme = colors.get(self.notification_type, colors["info"])
        
        # Configure toast appearance
        self.toast.configure(bg=color_scheme["bg"])
        
        # Title label
        title_label = tk.Label(
            self.toast,
            text=self.title,
            font=("Arial", 10, "bold"),
            bg=color_scheme["bg"],
            fg=color_scheme["fg"]
        )
        title_label.pack(pady=(10, 5))
        
        # Message label
        message_label = tk.Label(
            self.toast,
            text=self.message,
            font=("Arial", 9),
            bg=color_scheme["bg"],
            fg=color_scheme["fg"],
            wraplength=280
        )
        message_label.pack(pady=(0, 10))
        
        # Make toast clickable to close
        self.toast.bind("<Button-1>", lambda e: self.close_toast())
        title_label.bind("<Button-1>", lambda e: self.close_toast())
        message_label.bind("<Button-1>", lambda e: self.close_toast())
        
        # Auto-close after duration
        self.toast.after(self.duration, self.close_toast)
        
        # Bring to front
        self.toast.lift()
        self.toast.attributes('-topmost', True)
    
    def close_toast(self):
        """Close the toast notification"""
        try:
            self.toast.destroy()
        except:
            pass

# Global notification manager instance
notification_manager = NotificationManager()