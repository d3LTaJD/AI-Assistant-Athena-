"""
Advanced Voice Handler with Room-Scale Recognition
Supports wake word detection and long-range voice recognition
"""
import speech_recognition as sr
import pyttsx3
import threading
import queue
import time
import numpy as np
import webrtcvad
import collections
import pyaudio
from config import config

class AdvancedVoiceHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = None
        self.is_listening = False
        self.wake_word_detected = False
        self.voice_queue = queue.Queue()
        
        # Voice Activity Detection
        self.vad = webrtcvad.Vad(2)  # Aggressiveness level 0-3
        self.sample_rate = 16000
        self.frame_duration = 30  # ms
        self.frame_size = int(self.sample_rate * self.frame_duration / 1000)
        
        # Audio buffer for continuous listening
        self.audio_buffer = collections.deque(maxlen=50)
        self.is_speaking = False
        
        self.setup_tts()
        self.setup_microphone()
        self.setup_wake_word_detection()
    
    def setup_tts(self):
        """Initialize advanced text-to-speech engine"""
        try:
            self.tts_engine = pyttsx3.init()
            
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            voice_type = config.get('voice_type', 'female')
            
            # Advanced voice selection
            selected_voice = None
            for voice in voices:
                voice_name = voice.name.lower()
                if voice_type == 'female':
                    if any(keyword in voice_name for keyword in ['zira', 'hazel', 'female', 'woman']):
                        selected_voice = voice.id
                        break
                elif voice_type == 'male':
                    if any(keyword in voice_name for keyword in ['david', 'mark', 'male', 'man']):
                        selected_voice = voice.id
                        break
            
            if selected_voice:
                self.tts_engine.setProperty('voice', selected_voice)
            
            # Enhanced speech properties
            self.tts_engine.setProperty('rate', config.get('voice_speed', 180))
            self.tts_engine.setProperty('volume', config.get('voice_volume', 0.9))
            
            # Test voice quality
            print("🔊 Voice engine initialized with enhanced settings")
            
        except Exception as e:
            print(f"TTS initialization error: {e}")
            self.tts_engine = None
    
    def setup_microphone(self):
        """Setup microphone with enhanced sensitivity for room-scale detection"""
        try:
            # Adjust for ambient noise with longer duration for room acoustics
            with self.microphone as source:
                print("🎤 Calibrating microphone for room acoustics...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                
            # Enhanced recognition settings for distance
            self.recognizer.energy_threshold = 300  # Lower for distant voices
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.dynamic_energy_adjustment_damping = 0.15
            self.recognizer.dynamic_energy_ratio = 1.5
            self.recognizer.pause_threshold = 0.8  # Longer pause for processing
            self.recognizer.operation_timeout = None
            self.recognizer.phrase_threshold = 0.3
            self.recognizer.non_speaking_duration = 0.8
            
            print("✅ Microphone optimized for room-scale voice detection")
            
        except Exception as e:
            print(f"Microphone setup error: {e}")
    
    def setup_wake_word_detection(self):
        """Setup wake word detection system"""
        self.wake_words = [
            config.get('wake_word', 'assistant').lower(),
            config.get('assistant_name', 'Assistant').lower(),
            'hey ' + config.get('assistant_name', 'Assistant').lower(),
            'ok ' + config.get('assistant_name', 'Assistant').lower()
        ]
        print(f"🎯 Wake words configured: {self.wake_words}")
    
    def speak(self, text, interrupt_current=False):
        """Enhanced text-to-speech with interruption capability"""
        if self.tts_engine:
            try:
                def tts_thread():
                    if interrupt_current:
                        self.tts_engine.stop()
                    
                    # Add natural pauses and emphasis
                    enhanced_text = self.enhance_speech_text(text)
                    
                    self.is_speaking = True
                    self.tts_engine.say(enhanced_text)
                    self.tts_engine.runAndWait()
                    self.is_speaking = False
                
                thread = threading.Thread(target=tts_thread, daemon=True)
                thread.start()
                
            except Exception as e:
                print(f"TTS error: {e}")
                self.is_speaking = False
        else:
            print(f"🔊 {config.get('assistant_name', 'Assistant')}: {text}")
    
    def enhance_speech_text(self, text):
        """Enhance text for more natural speech"""
        # Add natural pauses
        text = text.replace('.', '... ')
        text = text.replace(',', ', ')
        text = text.replace('!', '! ')
        text = text.replace('?', '? ')
        
        # Emphasize important words
        assistant_name = config.get('assistant_name', 'Assistant')
        text = text.replace(assistant_name, f"<emphasis level='strong'>{assistant_name}</emphasis>")
        
        return text
    
    def detect_voice_activity(self, audio_data):
        """Detect voice activity in audio data"""
        try:
            # Convert audio to the format expected by WebRTC VAD
            audio_int16 = np.frombuffer(audio_data, dtype=np.int16)
            
            # Ensure we have the right frame size
            if len(audio_int16) >= self.frame_size:
                frame = audio_int16[:self.frame_size].tobytes()
                return self.vad.is_speech(frame, self.sample_rate)
            
            return False
        except Exception as e:
            print(f"VAD error: {e}")
            return False
    
    def listen_for_wake_word(self, timeout=1):
        """Continuously listen for wake word with room-scale detection"""
        try:
            with self.microphone as source:
                # Use shorter timeout for continuous monitoring
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=3)
                
            # Process audio for wake word
            try:
                text = self.recognizer.recognize_google(audio, language='en-US').lower()
                
                # Check for wake words
                for wake_word in self.wake_words:
                    if wake_word in text:
                        print(f"🎯 Wake word detected: '{wake_word}' in '{text}'")
                        return True, text.replace(wake_word, '').strip()
                
                return False, None
                
            except sr.UnknownValueError:
                return False, None
            except sr.RequestError:
                return False, None
                
        except sr.WaitTimeoutError:
            return False, None
        except Exception as e:
            print(f"Wake word detection error: {e}")
            return False, None
    
    def listen_for_command(self, timeout=10):
        """Listen for command after wake word detection"""
        try:
            print("🎤 Listening for your command...")
            
            with self.microphone as source:
                # Longer timeout for command input
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=15)
                
            print("🔄 Processing your command...")
            text = self.recognizer.recognize_google(audio, language='en-US')
            
            return text.lower()
            
        except sr.WaitTimeoutError:
            print("⏰ No command heard within timeout")
            return None
        except sr.UnknownValueError:
            print("❓ Could not understand the command")
            return None
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return None
        except Exception as e:
            print(f"Command listening error: {e}")
            return None
    
    def start_continuous_listening(self, callback):
        """Start continuous wake word detection"""
        def listen_thread():
            self.is_listening = True
            print(f"👂 Continuous listening started. Say '{config.get('wake_word', 'assistant')}' to activate.")
            
            consecutive_failures = 0
            max_failures = 5
            
            while self.is_listening:
                try:
                    # Don't listen while speaking
                    if self.is_speaking:
                        time.sleep(0.1)
                        continue
                    
                    # Listen for wake word
                    wake_detected, remaining_text = self.listen_for_wake_word(timeout=1)
                    
                    if wake_detected:
                        consecutive_failures = 0
                        self.wake_word_detected = True
                        
                        # Acknowledge wake word
                        self.speak("Yes?", interrupt_current=True)
                        
                        # If there was remaining text after wake word, use it
                        if remaining_text and len(remaining_text.strip()) > 2:
                            command = remaining_text
                        else:
                            # Listen for the actual command
                            command = self.listen_for_command(timeout=10)
                        
                        if command:
                            print(f"📝 Command received: {command}")
                            callback(command)
                        else:
                            self.speak("I didn't catch that. Please try again.")
                        
                        self.wake_word_detected = False
                    else:
                        consecutive_failures += 1
                        if consecutive_failures >= max_failures:
                            # Brief pause to prevent excessive CPU usage
                            time.sleep(0.5)
                            consecutive_failures = 0
                    
                    # Small delay to prevent high CPU usage
                    time.sleep(0.1)
                    
                except Exception as e:
                    print(f"Continuous listening error: {e}")
                    time.sleep(1)  # Longer pause on error
        
        self.listen_thread = threading.Thread(target=listen_thread, daemon=True)
        self.listen_thread.start()
    
    def stop_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
        print("🔇 Continuous listening stopped")
    
    def listen_once(self, timeout=10):
        """Listen for a single command (for manual activation)"""
        try:
            print("🎤 Listening for command...")
            
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=15)
                
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
    
    def change_voice(self, voice_type):
        """Change voice type with immediate effect"""
        config.set('voice_type', voice_type)
        self.setup_tts()
        
        # Test the new voice
        test_message = f"Voice changed to {voice_type}. How do I sound now?"
        self.speak(test_message)
    
    def adjust_sensitivity(self, level):
        """Adjust microphone sensitivity (1-10)"""
        # Adjust energy threshold based on sensitivity level
        base_threshold = 4000
        self.recognizer.energy_threshold = base_threshold - (level * 300)
        
        config.set('mic_sensitivity', level)
        print(f"🎚️ Microphone sensitivity set to {level}/10")
    
    def test_microphone(self):
        """Test microphone and provide feedback"""
        print("🧪 Testing microphone...")
        
        try:
            with self.microphone as source:
                print("📢 Say something to test the microphone...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
            text = self.recognizer.recognize_google(audio, language='en-US')
            
            self.speak(f"I heard you say: {text}")
            return True
            
        except Exception as e:
            print(f"Microphone test failed: {e}")
            self.speak("Microphone test failed. Please check your microphone connection.")
            return False

# Global advanced voice handler instance
advanced_voice_handler = AdvancedVoiceHandler()