#!/usr/bin/env python3
"""
Universal Installer for AI Assistant
Works on Windows, macOS, and Linux without problematic dependencies
"""
import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path
import datetime

def print_header():
    """Print header with ASCII art"""
    header = """
    ╔═══════════════════════════════════════════════╗
    ║             AI ASSISTANT INSTALLER            ║
    ║                                               ║
    ║  Universal installer for all platforms        ║
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

def detect_platform():
    """Detect platform and return info"""
    system = platform.system().lower()
    
    if system == "windows":
        return {
            "name": "Windows",
            "system": system,
            "package_manager": "pip",
            "python_command": "python",
            "script_ext": ".bat"
        }
    elif system == "darwin":
        return {
            "name": "macOS",
            "system": system,
            "package_manager": "pip3",
            "python_command": "python3",
            "script_ext": ".sh"
        }
    else:  # Linux or other Unix
        return {
            "name": "Linux",
            "system": system,
            "package_manager": "pip3",
            "python_command": "python3",
            "script_ext": ".sh"
        }

def install_core_dependencies(platform_info):
    """Install core dependencies that work everywhere"""
    print(f"\n📦 Installing core dependencies for {platform_info['name']}...")
    
    # Core packages that should work everywhere
    core_packages = [
        "pyttsx3",
        "requests",
        "numpy",
        "Pillow"
    ]
    
    # Install core packages
    for package in core_packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "--upgrade", package
            ])
            print(f"✅ {package} installed")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
    
    return True

def try_install_pyaudio(platform_info):
    """Try to install PyAudio with platform-specific approach"""
    print(f"\n🎤 Attempting to install PyAudio for {platform_info['name']}...")
    
    system = platform_info["system"]
    success = False
    
    if system == "windows":
        try:
            # Try pipwin approach
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "pipwin"
            ])
            subprocess.check_call([
                sys.executable, "-m", "pipwin", "install", "pyaudio"
            ])
            success = True
            print("✅ PyAudio installed via pipwin")
        except:
            try:
                # Direct approach
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", "pyaudio"
                ])
                success = True
                print("✅ PyAudio installed directly")
            except:
                print("❌ PyAudio installation failed")
                print("Voice recognition will not be available")
    
    elif system == "darwin":  # macOS
        print("⚠️ On macOS, you may need to install portaudio first:")
        print("brew install portaudio")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "pyaudio"
            ])
            success = True
            print("✅ PyAudio installed")
        except:
            print("❌ PyAudio installation failed")
            print("Voice recognition will not be available")
            print("Try: brew install portaudio && pip install pyaudio")
    
    else:  # Linux
        print("⚠️ On Linux, you may need to install portaudio development files:")
        print("sudo apt-get install python3-pyaudio portaudio19-dev")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "pyaudio"
            ])
            success = True
            print("✅ PyAudio installed")
        except:
            print("❌ PyAudio installation failed")
            print("Voice recognition will not be available")
            print("Try: sudo apt-get install python3-pyaudio portaudio19-dev")
    
    if success:
        try:
            # Install SpeechRecognition if PyAudio succeeded
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "SpeechRecognition"
            ])
            print("✅ SpeechRecognition installed")
            return True
        except:
            print("❌ SpeechRecognition installation failed")
            return False
    
    return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = ["data", "screenshots", "logs"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")

def create_run_scripts(platform_info, voice_available):
    """Create platform-specific run scripts"""
    print("\n📝 Creating run scripts...")
    
    # Choose the right script to run based on voice availability
    main_script = "main.py" if voice_available else "pc_athena_no_pyaudio.py"
    
    if platform_info["system"] == "windows":
        # Windows batch file
        batch_content = f"""@echo off
echo Starting AI Assistant...
{platform_info['python_command']} {main_script}
pause
"""
        
        with open("run_assistant.bat", "w") as f:
            f.write(batch_content)
        print("✅ Created Windows run script (run_assistant.bat)")
    else:
        # Unix shell script
        shell_content = f"""#!/bin/bash
echo "Starting AI Assistant..."
{platform_info['python_command']} {main_script}
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

def create_readme(voice_available, platform_info):
    """Create a README file with instructions"""
    print("\n📝 Creating README file...")
    
    readme_content = f"""# AI Assistant - Installation Complete

## Quick Start

Run the assistant:

{platform_info['name']}:
{"- Double-click run_assistant.bat" if platform_info['system'] == 'windows' else "- Run ./run_assistant.sh"}

## Features Available

- {"✅" if voice_available else "❌"} Voice Recognition: {"Available" if voice_available else "Not available (PyAudio installation failed)"}
- {"✅" if 'pyttsx3' in sys.modules else "❌"} Text-to-Speech: {"Available" if 'pyttsx3' in sys.modules else "Not available"}
- ✅ Notes & Reminders
- ✅ Math & Calculations
- ✅ Time & Date
- ✅ Entertainment Features

## Using the Assistant

1. {"Speak commands starting with 'athena'" if voice_available else "Type commands starting with 'athena'"}
2. Try commands like:
   - "athena time"
   - "athena calculate 2 + 2"
   - "athena tell me a joke"
   - "athena create note Buy groceries"

3. Type 'help' for a complete list of commands

## Troubleshooting

If you encounter issues:

1. Make sure Python {sys.version_info.major}.{sys.version_info.minor} is installed
2. Try reinstalling dependencies: pip install -r requirements{"_no_pyaudio" if not voice_available else ""}.txt
3. Check the console for error messages

Installation completed on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    with open("INSTALLATION_README.md", "w") as f:
        f.write(readme_content)
    
    print("✅ Created README file (INSTALLATION_README.md)")

def main():
    """Main installer function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Detect platform
    platform_info = detect_platform()
    print(f"🖥️ Detected platform: {platform_info['name']}")
    
    # Install core dependencies
    install_core_dependencies(platform_info)
    
    # Try to install PyAudio
    voice_available = try_install_pyaudio(platform_info)
    
    # Create directories
    create_directories()
    
    # Create run scripts
    create_run_scripts(platform_info, voice_available)
    
    # Create README
    create_readme(voice_available, platform_info)
    
    # Create installation marker
    with open("installation_completed.txt", "w") as f:
        f.write(f"Installation completed on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n✅ Installation completed successfully!")
    print("\n📋 Next steps:")
    print(f"1. Run the assistant: {'run_assistant.bat' if platform_info['system'] == 'windows' else './run_assistant.sh'}")
    print("2. Type 'help' to see available commands")
    
    if not voice_available:
        print("\n⚠️ Note: Voice recognition is not available.")
        print("The assistant will work with text input only.")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()