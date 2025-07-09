"""
Voice input and output handler
"""
import speech_recognition as sr
import pyttsx3
import threading
import queue
import time
from config import config

class VoiceHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = None
        self.is_listening = False
        self.voice_queue = queue.Queue()
        self.setup_tts()
        self.setup_microphone()
    
    def setup_tts(self):
        """Initialize text-to-speech engine"""
        try:
            self.tts_engine = pyttsx3.init()
            
            # Configure voice
            voices = self.tts_engine.getProperty('voices')
            voice_type = config.get('voice_type', 'female')
            
            # Try to set preferred voice
            for voice in voices:
                if voice_type == 'female' and ('female' in voice.name.lower() or 'zira' in voice.name.lower()):
                    self.tts_engine.setProperty('voice', voice.id)
                    break
                elif voice_type == 'male' and ('male' in voice.name.lower() or 'david' in voice.name.lower()):
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            
            # Set speech properties
            self.tts_engine.setProperty('rate', config.get('voice_speed', 180))
            self.tts_engine.setProperty('volume', config.get('voice_volume', 0.8))
            
        except Exception as e:
            print(f"TTS initialization error: {e}")
            self.tts_engine = None
    
    def setup_microphone(self):
        """Setup microphone for voice recognition"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        except Exception as e:
            print(f"Microphone setup error: {e}")
    
    def speak(self, text):
        """Convert text to speech"""
        if self.tts_engine:
            try:
                # Run TTS in separate thread to avoid blocking
                def tts_thread():
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()
                
                thread = threading.Thread(target=tts_thread, daemon=True)
                thread.start()
                
            except Exception as e:
                print(f"TTS error: {e}")
        else:
            print(f"🔊 {config.get('assistant_name', 'Assistant')}: {text}")
    
    def listen_once(self, timeout=5):
        """Listen for a single voice command"""
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                
            print("🔄 Processing...")
            text = self.recognizer.recognize_google(audio, language='en-US')
            return text.lower()
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return None
        except Exception as e:
            print(f"Voice recognition error: {e}")
            return None
    
    def start_continuous_listening(self, callback):
        """Start continuous voice recognition"""
        def listen_thread():
            self.is_listening = True
            wake_word = config.get('wake_word', 'assistant').lower()
            
            while self.is_listening:
                try:
                    command = self.listen_once(timeout=1)
                    if command and wake_word in command:
                        # Remove wake word and pass to callback
                        clean_command = command.replace(wake_word, '').strip()
                        if clean_command:
                            callback(clean_command)
                        else:
                            # Just wake word, listen for follow-up
                            self.speak("Yes, how can I help you?")
                            follow_up = self.listen_once(timeout=10)
                            if follow_up:
                                callback(follow_up)
                    
                    time.sleep(0.1)  # Small delay to prevent high CPU usage
                    
                except Exception as e:
                    print(f"Continuous listening error: {e}")
                    time.sleep(1)
        
        self.listen_thread = threading.Thread(target=listen_thread, daemon=True)
        self.listen_thread.start()
    
    def stop_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
    
    def change_voice(self, voice_type):
        """Change voice type (male/female)"""
        config.set('voice_type', voice_type)
        self.setup_tts()

# Global voice handler instance
voice_handler = VoiceHandler()