"""
Internet connectivity and network utilities for Athena AI Assistant
"""

import requests
import socket
from functools import wraps
import time

class ConnectivityManager:
    def __init__(self, timeout=5):
        self.timeout = timeout
        self.last_check = 0
        self.last_status = False
        self.cache_duration = 30  # Cache connectivity status for 30 seconds
    
    def check_internet_connection(self, force_check=False):
        """
        Check if internet connection is available
        
        Args:
            force_check: Force a new check even if cached result is available
            
        Returns:
            bool: True if internet is available, False otherwise
        """
        current_time = time.time()
        
        # Use cached result if recent and not forcing check
        if not force_check and (current_time - self.last_check) < self.cache_duration:
            return self.last_status
        
        try:
            # Try to connect to Google's DNS server
            socket.create_connection(("8.8.8.8", 53), timeout=self.timeout)
            self.last_status = True
            self.last_check = current_time
            return True
        except OSError:
            pass
        
        try:
            # Fallback: Try HTTP request to a reliable service
            response = requests.get(
                "https://httpbin.org/status/200", 
                timeout=self.timeout
            )
            self.last_status = response.status_code == 200
            self.last_check = current_time
            return self.last_status
        except requests.RequestException:
            self.last_status = False
            self.last_check = current_time
            return False
    
    def get_connection_status(self):
        """Get detailed connection status"""
        is_connected = self.check_internet_connection()
        return {
            'connected': is_connected,
            'last_check': self.last_check,
            'status_message': 'Online' if is_connected else 'Offline'
        }

def require_internet(offline_message="This feature requires an internet connection."):
    """
    Decorator to check internet connectivity before executing a function
    
    Args:
        offline_message: Message to display when offline
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            from utils.logger import athena_logger
            
            connectivity = ConnectivityManager()
            if not connectivity.check_internet_connection():
                athena_logger.log_error(
                    f"Internet required for {func.__name__} but connection unavailable",
                    category="connectivity"
                )
                
                # Try to speak the offline message if speak function is available
                try:
                    from Athenavoice import speak
                    speak(offline_message)
                except ImportError:
                    print(f"⚠️ OFFLINE: {offline_message}")
                
                return None
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Global connectivity manager instance
connectivity_manager = ConnectivityManager()