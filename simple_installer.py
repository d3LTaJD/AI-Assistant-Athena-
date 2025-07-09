"""
Simple Installer for AI Assistant
Works without problematic dependencies
"""
import os
import sys
import platform
import subprocess
from pathlib import Path
import datetime

def print_header():
    """Print header with ASCII art"""
    header = """
    ╔═══════════════════════════════════════════════╗
    ║             AI ASSISTANT INSTALLER            ║
    ║                                               ║
    ║  A simple, cross-platform voice assistant     ║
    ╚═══════════════════════════════════════════════╝
    """
    print(header)

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version < (3, 6):
        print(f"❌ Python 3.6+ required. You have {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def install_core_dependencies():
    """Install core dependencies that work everywhere"""
    print("\n📦 Installing core dependencies...")
    
    # Core packages that should work everywhere
    core_packages = [
        "pyttsx3",
        "requests",
        "numpy"
    ]
    
    # Install core packages
    for package in core_packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])
            print(f"✅ {package} installed")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = ["data", "screenshots"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")

def create_run_scripts():
    """Create platform-specific run scripts"""
    print("\n📝 Creating run scripts...")
    
    # Windows batch file
    batch_content = """@echo off
echo Starting AI Assistant...
python main.py
pause
"""
    
    with open("run_assistant.bat", "w") as f:
        f.write(batch_content)
    print("✅ Created Windows run script (run_assistant.bat)")
    
    # Unix shell script
    shell_content = """#!/bin/bash
echo "Starting AI Assistant..."
python3 main.py
read -p "Press Enter to exit..."
"""
    
    with open("run_assistant.sh", "w") as f:
        f.write(shell_content)
    print("✅ Created Unix run script (run_assistant.sh)")
    
    # Try to make shell script executable
    try:
        os.chmod("run_assistant.sh", 0o755)
    except:
        print("⚠️ Could not make shell script executable. Users may need to run: chmod +x run_assistant.sh")

def main():
    """Main installer function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Install core dependencies
    install_core_dependencies()
    
    # Create directories
    create_directories()
    
    # Create run scripts
    create_run_scripts()
    
    # Create installation marker
    with open("installation_completed.txt", "w") as f:
        f.write(f"Installation completed on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n✅ Installation completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run the assistant:")
    print("   - Windows: Double-click run_assistant.bat")
    print("   - macOS/Linux: ./run_assistant.sh")
    print("2. Type 'help' to see available commands")
    print("\n⚠️ Note: Voice recognition features require additional setup.")
    print("See README.md for instructions on setting up voice recognition.")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()