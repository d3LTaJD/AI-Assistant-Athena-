"""
Centralized error handling system for Athena AI Assistant
"""

import traceback
import sys
from functools import wraps
from utils.logger import athena_logger

class AthenaErrorHandler:
    def __init__(self):
        self.error_counts = {}
        self.max_retries = 3
    
    def handle_error(self, error, context="general", user_message=None):
        """
        Handle errors with logging and user feedback
        
        Args:
            error: The exception object
            context: Context where error occurred
            user_message: Custom message for user
        """
        error_key = f"{context}:{type(error).__name__}"
        self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1
        
        # Log the error
        athena_logger.log_error(
            f"Error in {context}: {str(error)}",
            exception=error,
            category=context
        )
        
        # Provide user feedback
        if user_message:
            try:
                from Athenavoice import speak
                speak(user_message)
            except ImportError:
                print(f"❌ {user_message}")
        
        # Log stack trace for debugging
        athena_logger.error_logger.error(f"Stack trace:\n{traceback.format_exc()}")
    
    def get_error_stats(self):
        """Get error statistics"""
        return self.error_counts.copy()
    
    def reset_error_counts(self):
        """Reset error counters"""
        self.error_counts.clear()

def safe_execute(context="general", user_message="Sorry, something went wrong. Please try again.", return_value=None):
    """
    Decorator for safe function execution with error handling
    
    Args:
        context: Context identifier for logging
        user_message: Message to show user on error
        return_value: Value to return on error
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_handler.handle_error(e, context, user_message)
                return return_value
        return wrapper
    return decorator

def retry_on_failure(max_retries=3, delay=1, context="general"):
    """
    Decorator to retry function execution on failure
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
        context: Context for logging
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries:
                        error_handler.handle_error(
                            e, 
                            f"{context}_retry_failed",
                            f"Failed after {max_retries} attempts. Please try again later."
                        )
                        return None
                    
                    athena_logger.log_info(
                        f"Attempt {attempt + 1} failed for {func.__name__}, retrying in {delay}s",
                        category=context
                    )
                    time.sleep(delay)
            
            return None
        return wrapper
    return decorator

# Global error handler instance
error_handler = AthenaErrorHandler()