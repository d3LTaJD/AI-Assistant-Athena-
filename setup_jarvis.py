#!/usr/bin/env python3
"""
J.A.R.V.I.S. Setup Script
Installs dependencies and prepares the system
"""
import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Print J.A.R.V.I.S. banner"""
    banner = """
    ╔════════════════════════════════════════════╗
    ║                                            ║
    ║       J.A.R.V.I.S. AI ASSISTANT            ║
    ║                                            ║
    ║  Just A Rather Very Intelligent System     ║
    ║                                            ║
    ╚════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    
    version = sys.version_info
    if version < (3, 6):
        print(f"❌ Python 3.6+ required. You have {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    # Core dependencies that should work everywhere
    dependencies = [
        "pyttsx3",
        "requests"
    ]
    
    for package in dependencies:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "--upgrade", package
            ])
            print(f"✅ {package} installed")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    # Create data directory
    data_dir = Path("jarvis_data")
    data_dir.mkdir(exist_ok=True)
    print(f"✅ Created directory: {data_dir}")

def create_run_script():
    """Create platform-specific run script"""
    print("\n📝 Creating run script...")
    
    system = platform.system().lower()
    
    if system == "windows":
        # Windows batch file
        script_content = """@echo off
echo Starting J.A.R.V.I.S. AI Assistant...
python jarvis_assistant.py
pause
"""
        script_path = "run_jarvis.bat"
    else:
        # Unix shell script
        script_content = """#!/bin/bash
echo "Starting J.A.R.V.I.S. AI Assistant..."
python3 jarvis_assistant.py
read -p "Press Enter to exit..."
"""
        script_path = "run_jarvis.sh"
    
    with open(script_path, "w") as f:
        f.write(script_content)
    
    print(f"✅ Created run script: {script_path}")
    
    # Make shell script executable on Unix
    if system != "windows":
        try:
            os.chmod(script_path, 0o755)
        except:
            print("⚠️ Could not make shell script executable. Run: chmod +x run_jarvis.sh")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Install dependencies
    install_dependencies()
    
    # Create directories
    create_directories()
    
    # Create run script
    create_run_script()
    
    print("\n✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run J.A.R.V.I.S.:")
    if platform.system().lower() == "windows":
        print("   - Double-click run_jarvis.bat")
    else:
        print("   - Run ./run_jarvis.sh")
    
    print("\n💡 Features:")
    print("• Animated Jarvis-style interface")
    print("• Text-to-speech responses")
    print("• Notes and reminders")
    print("• Web search and system information")
    print("• Math calculations and more")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()