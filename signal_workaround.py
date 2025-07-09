"""
Minimal signal module workaround for WebContainer environments
This provides basic signal functionality without requiring _signal
"""

# Signal constants (most common ones)
SIGINT = 2
SIGTERM = 15
SIGKILL = 9
SIGHUP = 1
SIGQUIT = 3

class SignalHandler:
    def __init__(self):
        self.handlers = {}
    
    def signal(self, signum, handler):
        """Mock signal handler registration"""
        self.handlers[signum] = handler
        return None
    
    def alarm(self, time):
        """Mock alarm function"""
        return 0

# Create global instance
_handler = SignalHandler()
signal = _handler.signal
alarm = _handler.alarm

# Default handler
SIG_DFL = 0
SIG_IGN = 1

def default_int_handler(signum, frame):
    """Default interrupt handler"""
    raise KeyboardInterrupt()
