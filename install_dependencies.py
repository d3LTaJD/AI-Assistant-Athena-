"""
Dependency installer script
Run this to install all required dependencies
"""
import subprocess
import sys
import os

def install_package(package):
    """Install a single package"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """Install all required dependencies"""
    print("🚀 Installing AI Assistant Dependencies")
    print("=" * 50)
    
    # Core dependencies
    dependencies = [
        "customtkinter==5.2.0",
        "pyttsx3==2.90",
        "SpeechRecognition==3.10.0",
        "pyaudio==0.2.11",
        "Pillow==10.1.0",
        "bcrypt==4.0.1",
        "requests==2.31.0",
        "python-dotenv==1.0.0"
    ]
    
    # Optional dependencies for advanced features
    optional_dependencies = [
        "whisper==1.1.10",
        "torch==2.1.0",
        "transformers==4.35.0"
    ]
    
    print("📦 Installing core dependencies...")
    failed_packages = []
    
    for package in dependencies:
        print(f"Installing {package}...")
        if install_package(package):
            print(f"✅ {package} installed successfully")
        else:
            print(f"❌ Failed to install {package}")
            failed_packages.append(package)
    
    print("\n📦 Installing optional dependencies...")
    for package in optional_dependencies:
        print(f"Installing {package}...")
        if install_package(package):
            print(f"✅ {package} installed successfully")
        else:
            print(f"⚠️ Optional package {package} failed to install (this is okay)")
    
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
        for package in failed_packages:
            print(f"  - {package}")
        print("\nTry installing failed packages manually:")
        for package in failed_packages:
            print(f"pip install {package}")
    else:
        print("✅ All dependencies installed successfully!")
    
    print("\n🚀 You can now run the application:")
    print("python main.py")

if __name__ == "__main__":
    main()