#!/usr/bin/env python3
"""
Installation script for AI Assistant
Handles dependency installation and environment setup
"""

import sys
import os
import platform
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version < (3, 8):
        print(f"❌ Python 3.8+ required. You have {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    
    # Core packages
    core_packages = [
        "pyttsx3==2.90",
        "SpeechRecognition==3.10.0",
        "requests==2.31.0",
        "numpy==1.24.3",
        "Pillow==10.1.0"
    ]
    
    # Install core packages
    for package in core_packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
    
    # Platform-specific audio setup
    system = platform.system().lower()
    print(f"\n🔊 Setting up audio for {system}...")
    
    if system == "windows":
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pipwin"])
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyaudio"])
            print("✅ Audio setup completed")
        except subprocess.CalledProcessError:
            print("⚠️ Audio setup failed. Try manual installation:")
            print("pip install pipwin")
            print("pipwin install pyaudio")
    
    elif system == "darwin":  # macOS
        print("⚠️ For macOS, install portaudio first:")
        print("brew install portaudio")
        print("Then run: pip install pyaudio")
    
    elif system == "linux":
        print("⚠️ For Linux, install audio dependencies:")
        print("sudo apt-get install python3-pyaudio portaudio19-dev")
        print("Then run: pip install pyaudio")
    
    # Advanced packages (optional)
    print("\n📦 Installing advanced packages...")
    advanced_packages = [
        "psutil==5.9.6",
        "webrtcvad==2.0.10"
    ]
    
    for package in advanced_packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed")
        except subprocess.CalledProcessError:
            print(f"⚠️ Failed to install {package} - some features may be limited")
    
    # GUI packages (optional)
    print("\n📦 Installing GUI packages...")
    gui_packages = [
        "customtkinter==5.2.0",
        "pygame==2.5.2"
    ]
    
    for package in gui_packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed")
        except subprocess.CalledProcessError:
            print(f"⚠️ Failed to install {package} - GUI features may be limited")
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "screenshots",
        "logs",
        "data"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")

def test_installation():
    """Test if installation was successful"""
    print("\n🧪 Testing installation...")
    
    tests = [
        ("pyttsx3", "Text-to-Speech"),
        ("speech_recognition", "Speech Recognition"),
        ("requests", "Internet Requests"),
        ("PIL", "Image Processing")
    ]
    
    success_count = 0
    for module, description in tests:
        try:
            __import__(module)
            print(f"✅ {description} - Working")
            success_count += 1
        except ImportError:
            print(f"❌ {description} - Not Available")
    
    # Special test for PyAudio
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        device_count = p.get_device_count()
        p.terminate()
        print(f"✅ Audio System - Working ({device_count} devices)")
        success_count += 1
    except ImportError:
        print("❌ Audio System - Not Available")
    except Exception as e:
        print(f"⚠️ Audio System - Limited ({e})")
    
    print(f"\n📊 Installation Results: {success_count}/{len(tests) + 1} components working")
    
    if success_count >= 3:  # At least core functionality
        print("✅ Installation successful! Core features are available.")
        return True
    else:
        print("⚠️ Installation completed with issues. Some features may not work.")
        return False

def main():
    """Main installation function"""
    print("🚀 AI Assistant - Installation Script")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Installation aborted. Please upgrade Python.")
        return
    
    # Install dependencies
    install_dependencies()
    
    # Create directories
    create_directories()
    
    # Test installation
    test_installation()
    
    print("\n" + "=" * 60)
    print("🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Run the assistant with: python enhanced_athena.py")
    print("2. For GUI version (if available): python enhanced_gui.py")
    print("3. Say 'Athena help' to see available commands")
    print("\n⚠️ Note: Some features require additional setup:")
    print("- Image generation requires OpenAI API key")
    print("- Weather and news features require API keys")
    print("- For full functionality, check setup_instructions.md")

if __name__ == "__main__":
    main()