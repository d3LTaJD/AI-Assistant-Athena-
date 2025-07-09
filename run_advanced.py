"""
Advanced Development Runner
Use this for development and testing of the advanced AI assistant
"""
import sys
import os
import subprocess
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def check_advanced_dependencies():
    """Check if all advanced dependencies are installed"""
    print("🔍 Checking Advanced Dependencies...")
    
    required_modules = {
        'customtkinter': 'Modern GUI framework',
        'pyttsx3': 'Text-to-speech engine',
        'speech_recognition': 'Voice recognition',
        'PIL': 'Image processing (Pillow)',
        'bcrypt': 'Password hashing',
        'psutil': 'System monitoring',
        'numpy': 'Numerical computing',
        'webrtcvad': 'Voice activity detection',
        'pyaudio': 'Audio input/output'
    }
    
    missing_modules = []
    available_modules = []
    
    for module, description in required_modules.items():
        try:
            __import__(module)
            available_modules.append((module, description))
            print(f"✅ {module} - {description}")
        except ImportError:
            missing_modules.append((module, description))
            print(f"❌ {module} - {description} - MISSING")
    
    print(f"\n📊 Status: {len(available_modules)}/{len(required_modules)} modules available")
    
    if missing_modules:
        print("\n❌ Missing required modules:")
        for module, description in missing_modules:
            print(f"  - {module}: {description}")
        print("\n💡 Install missing modules with:")
        print("pip install -r requirements_advanced.txt")
        
        # Platform-specific instructions
        print("\n🔧 Platform-specific setup:")
        if sys.platform == "win32":
            print("Windows: pip install pipwin && pipwin install pyaudio")
        elif sys.platform == "darwin":
            print("macOS: brew install portaudio && pip install pyaudio")
        else:
            print("Linux: sudo apt-get install python3-pyaudio portaudio19-dev")
        
        return False
    
    return True

def check_system_requirements():
    """Check system requirements for advanced features"""
    print("\n🖥️ Checking System Requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ required. Current: {sys.version}")
        return False
    print(f"✅ Python {sys.version}")
    
    # Check available memory
    try:
        import psutil
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024**3)
        
        if memory_gb < 2:
            print(f"⚠️ Low memory: {memory_gb:.1f}GB (4GB+ recommended)")
        else:
            print(f"✅ System memory: {memory_gb:.1f}GB")
    except ImportError:
        print("⚠️ Cannot check system memory (psutil not available)")
    
    # Check audio system
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        device_count = p.get_device_count()
        p.terminate()
        
        if device_count == 0:
            print("❌ No audio devices found")
            return False
        else:
            print(f"✅ Audio devices: {device_count} available")
    except ImportError:
        print("⚠️ Cannot check audio system (pyaudio not available)")
    except Exception as e:
        print(f"⚠️ Audio system check failed: {e}")
    
    return True

def install_dependencies():
    """Install missing dependencies"""
    print("\n📦 Installing Advanced Dependencies...")
    
    try:
        # Install from requirements file
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements_advanced.txt"
        ])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    except FileNotFoundError:
        print("❌ requirements_advanced.txt not found")
        return False

def run_application():
    """Run the advanced AI assistant application"""
    print("\n🚀 Starting Advanced AI Assistant...")
    
    try:
        from enhanced_main import main
        main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Application error: {e}")
        return False
    
    return True

def show_feature_overview():
    """Show overview of advanced features"""
    features = """
🚀 ADVANCED AI ASSISTANT FEATURES
{'='*50}

🎤 ROOM-SCALE VOICE RECOGNITION
• Advanced noise filtering and voice activity detection
• Wake word detection from across the room
• Natural language processing with context awareness
• Continuous listening with low CPU usage

🤖 3D ANIMATED AVATAR
• Real-time facial expressions and animations
• Speaking and listening visual feedback
• Customizable appearance and personality
• Smooth transitions and micro-interactions

📁 SMART FILE MANAGEMENT
• Natural language file operations
• "Open my resume from Documents"
• "Find all photos from last month"
• Recursive search with intelligent suggestions

🖥️ REAL-TIME SYSTEM MONITORING
• CPU, memory, and disk usage tracking
• Network status and performance metrics
• Running processes overview
• System health alerts and notifications

🧠 ADVANCED AI CAPABILITIES
• Context-aware conversation memory
• Learning from user preferences
• Complex multi-step task execution
• Intelligent response generation

🔒 PRIVACY & SECURITY
• Offline-first architecture
• Local data storage only
• Encrypted password storage
• No telemetry or tracking

⚡ PERFORMANCE OPTIMIZED
• Efficient resource usage
• Fast response times
• Optimized for long-running sessions
• Minimal system impact
"""
    print(features)

def main():
    """Main development runner"""
    print("🤖 Advanced AI Assistant - Development Mode")
    print("=" * 60)
    
    # Show feature overview
    show_feature_overview()
    
    # Check system requirements
    if not check_system_requirements():
        print("\n❌ System requirements not met")
        input("Press Enter to continue anyway or Ctrl+C to exit...")
    
    # Check dependencies
    if not check_advanced_dependencies():
        print("\n❓ Install missing dependencies? (y/n): ", end="")
        if input().lower().startswith('y'):
            if not install_dependencies():
                print("❌ Dependency installation failed")
                input("Press Enter to exit...")
                sys.exit(1)
            print("✅ Dependencies installed. Please restart the application.")
            input("Press Enter to exit...")
            sys.exit(0)
        else:
            print("⚠️ Running with missing dependencies - some features may not work")
            input("Press Enter to continue...")
    
    print("\n✅ All checks passed!")
    print("🔄 Starting Advanced AI Assistant...")
    
    # Run the application
    try:
        run_application()
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()