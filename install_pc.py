#!/usr/bin/env python3
"""
PC Installation Script for Athena AI Assistant
Handles installation of dependencies with platform-specific fixes
"""

import sys
import os
import platform
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version < (3, 8):
        print(f"❌ Python 3.8+ required. You have {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def install_package(package):
    """Install a single package with error handling"""
    try:
        print(f"📦 Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def install_pyaudio_windows():
    """Special handling for PyAudio on Windows"""
    print("🔧 Attempting Windows-specific PyAudio installation...")
    
    # Try pipwin first
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pipwin"])
        subprocess.check_call([sys.executable, "-m", "pipwin", "install", "pyaudio"])
        print("✅ PyAudio installed via pipwin")
        return True
    except subprocess.CalledProcessError:
        print("⚠️ pipwin method failed")
    
    # Try wheel installation
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyaudio"])
        print("✅ PyAudio installed via pip")
        return True
    except subprocess.CalledProcessError:
        print("❌ PyAudio installation failed")
        return False

def install_requirements():
    """Install all required packages"""
    print("\n📦 Installing required packages...")
    
    # Core packages that should install easily
    core_packages = [
        "pyttsx3==2.90",
        "requests==2.31.0", 
        "Pillow==10.1.0"
    ]
    
    # Install core packages
    for package in core_packages:
        install_package(package)
    
    # Handle PyAudio specially
    print("\n🎤 Installing audio support...")
    system = platform.system().lower()
    
    if system == "windows":
        if not install_pyaudio_windows():
            print("⚠️ PyAudio installation failed. Voice features will be limited.")
    else:
        if not install_package("pyaudio"):
            print("⚠️ PyAudio installation failed. Voice features will be limited.")
            if system == "darwin":  # macOS
                print("💡 Try: brew install portaudio")
            elif system == "linux":
                print("💡 Try: sudo apt-get install python3-pyaudio portaudio19-dev")
    
    # Install SpeechRecognition
    install_package("SpeechRecognition==3.10.0")
    
    # Install PyAutoGUI for screenshots
    install_package("pyautogui==0.9.54")
    
    print("\n✅ Installation completed!")

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = ["athena_data", "athena_data/screenshots"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created: {directory}")
        else:
            print(f"📁 Already exists: {directory}")

def test_installation():
    """Test if installation was successful"""
    print("\n🧪 Testing installation...")
    
    tests = [
        ("pyttsx3", "Text-to-Speech"),
        ("speech_recognition", "Speech Recognition"),
        ("requests", "Internet Requests"),
        ("PIL", "Image Processing"),
        ("pyautogui", "Screenshot")
    ]
    
    results = []
    
    for module, description in tests:
        try:
            __import__(module)
            print(f"✅ {description} - Working")
            results.append(True)
        except ImportError:
            print(f"❌ {description} - Not Available")
            results.append(False)
    
    # Special test for PyAudio
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        device_count = p.get_device_count()
        p.terminate()
        print(f"✅ Audio System - Working ({device_count} devices)")
        results.append(True)
    except ImportError:
        print("❌ Audio System - Not Available")
        results.append(False)
    except Exception as e:
        print(f"⚠️ Audio System - Limited ({e})")
        results.append(False)
    
    working_count = sum(results)
    total_count = len(results)
    
    print(f"\n📊 Installation Results: {working_count}/{total_count} components working")
    
    if working_count >= 4:  # At least core functionality
        print("✅ Installation successful! You can run pc_athena.py")
        return True
    else:
        print("⚠️ Installation completed with issues. Some features may not work.")
        return False

def show_usage_instructions():
    """Show how to use the installed system"""
    print(f"""
🚀 INSTALLATION COMPLETE!
{'='*50}

📋 How to run Athena:
1. Open terminal/command prompt
2. Navigate to this directory
3. Run: python pc_athena.py

🎤 Voice Features:
- If voice recognition works: Speak your commands
- If not available: Type your commands
- Toggle with: "athena toggle voice"

🔊 Text-to-Speech:
- Athena will speak responses if available
- Toggle with: "athena toggle speech"

💡 First Commands to Try:
- "athena help" - Show all commands
- "athena time" - Get current time
- "athena joke" - Tell a joke
- "athena calculate 2 + 2" - Basic math
- "athena create note Hello World" - Save a note

🛠️ Troubleshooting:
- If voice doesn't work: Install PyAudio manually
- If TTS doesn't work: Check pyttsx3 installation
- All features work without voice/TTS

📁 Data Storage:
- Notes and reminders saved in: athena_data/
- Screenshots saved in: athena_data/screenshots/

🆘 Need Help?
- Run "athena help" for full command list
- Check the console for error messages
- Voice features are optional - text input always works
""")

def main():
    """Main installation function"""
    print("🚀 PC Athena AI Assistant - Installation Script")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Installation aborted. Please upgrade Python.")
        return
    
    # Install packages
    install_requirements()
    
    # Create directories
    create_directories()
    
    # Test installation
    success = test_installation()
    
    # Show usage instructions
    show_usage_instructions()
    
    if success:
        print("\n🎉 Ready to use! Run: python pc_athena.py")
    else:
        print("\n⚠️ Installation completed with issues, but basic functionality should work.")

if __name__ == "__main__":
    main()