"""
Dependency installer script
Run this to install all required dependencies
"""
import os
import sys
import platform
import subprocess

def install_package(package):
    """Install a single package"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])
        return True
    except subprocess.CalledProcessError:
        return False

def install_pyaudio():
    """Install PyAudio with platform-specific handling"""
    system = platform.system().lower()
    
    print(f"🎤 Installing PyAudio for {system}...")
    
    if system == "windows":
        # On Windows, try pipwin first
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pipwin"])
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
            subprocess.check_call([sys.executable, "-m", "pipwin", "install", "pyaudio"])
            return True
        except subprocess.CalledProcessError:
            print("⚠️ pipwin installation failed, trying direct wheel...")
            try:
                # Try direct installation
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pyaudio"])
                return True
            except:
                print("❌ PyAudio installation failed.")
                print("Voice recognition will not be available.")
                print("You can try manual installation later:")
                print("pip install pipwin")
                print("pipwin install pyaudio")
                return False
    
    elif system == "darwin":  # macOS
        print("⚠️ On macOS, you may need to install portaudio first:")
        print("brew install portaudio")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyaudio"])
            return True
        except:
            print("❌ PyAudio installation failed.")
            print("Voice recognition will not be available.")
            print("Try: brew install portaudio && pip install pyaudio")
            return False
    
    elif system == "linux":
        print("⚠️ On Linux, you may need to install portaudio development files:")
        print("sudo apt-get install python3-pyaudio portaudio19-dev")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyaudio"])
            return True
        except:
            print("❌ PyAudio installation failed.")
            print("Voice recognition will not be available.")
            print("Try: sudo apt-get install python3-pyaudio portaudio19-dev")
            return False
    
    return False

def main():
    """Install all required dependencies"""
    print("🚀 Installing AI Assistant Dependencies")
    print("=" * 50)
    
    # Core dependencies
    core_dependencies = [
        "pyttsx3",
        "SpeechRecognition",
        "requests",
        "numpy",
        "Pillow"
        "requests==2.31.0",
        "python-dotenv==1.0.0"
    ]
    
    # Optional dependencies for advanced features
    optional_dependencies = [
        "whisper==1.1.10",
        "torch==2.1.0",
        "transformers==4.35.0"
    ]
    
    # Optional dependencies
    optional_dependencies = [
        "pyautogui",  # For screenshots
        "psutil"      # For system monitoring
    ]
    
    print("📦 Installing core dependencies...")
    for package in core_dependencies:
        print(f"Installing {package}...")
        install_package(package)
    
    # Handle PyAudio separately
    install_pyaudio()
    
    # Create directories
    print("\n📁 Creating necessary directories...")
    directories = ["data", "screenshots"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")
    
    # Create a marker file to indicate installation was attempted
    with open("installation_completed.txt", "w") as f:
        f.write(f"Installation completed on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Special handling for PyAudio on Windows
    if sys.platform == "win32":
        print("\n🔧 Windows-specific setup for PyAudio...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pipwin"])
            subprocess.check_call([sys.executable, "-m", "pipwin", "install", "pyaudio"])
            print("✅ PyAudio installed via pipwin")
        except subprocess.CalledProcessError:
            print("⚠️ PyAudio installation failed. Voice features may not work.")
            print("💡 Try installing manually: pip install pipwin && pipwin install pyaudio")
    
    # Summary
    print("\n" + "=" * 50)
    if failed_packages:
        print("⚠️ Installation completed with some issues:")
    print("✅ Installation completed!")
    print("\n📋 Next steps:")
    print("1. Run the assistant with: python main.py")
    print("2. If voice recognition doesn't work, you can still use text input")
    print("3. Say 'help' or type 'help' to see available commands")
    
    print("\n🚀 You can now run the application:")
    print("python main.py")

if __name__ == "__main__":
    main()