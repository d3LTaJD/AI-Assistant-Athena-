"""
Enhanced logging system for Athena AI Assistant
Provides centralized logging with different levels and file rotation
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

class AthenaLogger:
    def __init__(self, log_dir="logs", max_bytes=10*1024*1024, backup_count=5):
        """
        Initialize the Athena logging system
        
        Args:
            log_dir: Directory to store log files
            max_bytes: Maximum size of each log file (10MB default)
            backup_count: Number of backup files to keep
        """
        self.log_dir = log_dir
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        
        # Create logs directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Setup loggers
        self.setup_loggers()
    
    def setup_loggers(self):
        """Setup different loggers for different purposes"""
        
        # Main application logger
        self.app_logger = self._create_logger(
            'athena_app', 
            os.path.join(self.log_dir, 'athena_app.log'),
            logging.INFO
        )
        
        # Error logger
        self.error_logger = self._create_logger(
            'athena_errors',
            os.path.join(self.log_dir, 'athena_errors.log'),
            logging.ERROR
        )
        
        # User activity logger
        self.activity_logger = self._create_logger(
            'athena_activity',
            os.path.join(self.log_dir, 'athena_activity.log'),
            logging.INFO
        )
        
        # API usage logger
        self.api_logger = self._create_logger(
            'athena_api',
            os.path.join(self.log_dir, 'athena_api.log'),
            logging.INFO
        )
    
    def _create_logger(self, name, filename, level):
        """Create a logger with rotating file handler"""
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # Remove existing handlers to avoid duplicates
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Create rotating file handler
        handler = RotatingFileHandler(
            filename, 
            maxBytes=self.max_bytes, 
            backupCount=self.backup_count
        )
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
        
        # Also add console handler for errors
        if level == logging.ERROR:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        return logger
    
    def log_info(self, message, category="general"):
        """Log info message"""
        self.app_logger.info(f"[{category.upper()}] {message}")
    
    def log_error(self, message, exception=None, category="general"):
        """Log error message with optional exception details"""
        error_msg = f"[{category.upper()}] {message}"
        if exception:
            error_msg += f" | Exception: {str(exception)}"
        
        self.error_logger.error(error_msg)
        self.app_logger.error(error_msg)
    
    def log_activity(self, user_input, action, result=None):
        """Log user activity for training data"""
        activity_data = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'action': action,
            'result': result if result else 'completed'
        }
        self.activity_logger.info(str(activity_data))
    
    def log_api_usage(self, api_name, endpoint, tokens_used=None, cost=None):
        """Log API usage for monitoring"""
        api_data = {
            'timestamp': datetime.now().isoformat(),
            'api': api_name,
            'endpoint': endpoint,
            'tokens': tokens_used,
            'cost': cost
        }
        self.api_logger.info(str(api_data))

# Global logger instance
athena_logger = AthenaLogger()