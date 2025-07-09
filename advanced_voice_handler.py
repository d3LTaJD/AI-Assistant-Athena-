"""
Advanced Voice Handler with Room-Scale Recognition
Supports wake word detection and long-range voice recognition
"""
import time
import collections

class AdvancedVoiceHandler:
    def __init__(self):
        self.is_listening = False
        self.wake_word_detected = False
        self.is_speaking = False
        
    def speak(self, text):
        """Print response (simulated speech)"""
        print(f"🤖 Assistant: {text}")
        self.is_speaking = True
        # Simulate speaking time
        time.sleep(0.1)
        self.is_speaking = False
    
    def start_continuous_listening(self, callback):
        """Start continuous wake word detection"""
        def listen_thread():
            self.is_listening = True
            print(f"👂 Continuous listening started. Type commands to activate.")
            
            while self.is_listening:
                try:
                    # Don't listen while speaking
                    if self.is_speaking:
                        time.sleep(0.1)
                        continue
                    
                    # Listen for wake word
                    command = input("🎤 Type a command: ")
                    if command:
                        callback(command)
                    
                    # Small delay to prevent high CPU usage
                    time.sleep(0.1)
                    
                except Exception as e:
                    print(f"Continuous listening error: {e}")
                    time.sleep(1)  # Longer pause on error
        
        # In a real app, this would start a thread
        # For this simulation, we'll just call the function directly
        self.is_listening = True
    
    def stop_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
        print("🔇 Continuous listening stopped")
    
    def listen_once(self, timeout=10):
        """Listen for a single command (for manual activation)"""
        try:
            print("🎤 Listening for command...")
            command = input("Type your command: ")
            return command.lower()
            
        except Exception as e:
            print(f"Voice recognition error: {e}")
            return None
    
    def change_voice(self, voice_type):
        """Change voice type with immediate effect"""
        print(f"Voice changed to {voice_type}.")
        
        # Test the new voice
        test_message = f"Voice changed to {voice_type}. How do I sound now?"
        self.speak(test_message)
    
    def adjust_sensitivity(self, level):
        """Adjust microphone sensitivity (1-10)"""
        print(f"🎚️ Microphone sensitivity set to {level}/10")
    
    def test_microphone(self):
        """Test microphone and provide feedback"""
        print("🧪 Testing microphone...")
        
        try:
            print("📢 Say something to test the microphone...")
            test_input = input("Type something to simulate speaking: ")
            
            if test_input:
                self.speak(f"I heard you say: {test_input}")
                return True
            else:
                self.speak("Microphone test failed. No input detected.")
                return False
                
        except Exception as e:
            print(f"Microphone test failed: {e}")
            self.speak("Microphone test failed. Please check your microphone connection.")
            return False

# Global advanced voice handler instance
advanced_voice_handler = AdvancedVoiceHandler()