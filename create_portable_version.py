"""
Create a portable version of the AI Assistant
This script packages all necessary files into a single folder that can be shared
"""
import os
import sys
import shutil
import zipfile
from pathlib import Path
import datetime

def create_portable_version():
    """Create a portable version of the AI Assistant"""
    print("🚀 Creating Portable AI Assistant")
    print("=" * 60)
    
    # Create timestamp for unique folder name
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"AI_Assistant_Portable_{timestamp}"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Step 1: Copy essential files
    print("\n📁 Copying essential files...")
    essential_files = [
        "main.py",
        "webcontainer_athena.py",
        "advanced_features.py",
        "config.py",
        "database.py",
        "file_handler.py",
        "advanced_voice_handler.py",
        "requirements.txt",
        "README.md"
    ]
    
    for file in essential_files:
        if os.path.exists(file):
            shutil.copy2(file, os.path.join(output_dir, file))
            print(f"✅ Copied: {file}")
        else:
            print(f"⚠️ Missing: {file}")
    
    # Step 2: Create directories
    print("\n📁 Creating directories...")
    directories = ["data", "screenshots"]
    
    for directory in directories:
        os.makedirs(os.path.join(output_dir, directory), exist_ok=True)
        print(f"✅ Created: {directory}")
    
    # Step 3: Create run script for Windows
    print("\n📝 Creating Windows run script...")
    batch_content = """@echo off
echo Starting AI Assistant...

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed! Please install Python 3.8 or higher.
    echo Visit https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if dependencies are installed
if not exist "dependencies_installed.txt" (
    echo First run - installing dependencies...
    python -m pip install -r requirements.txt
    echo. > dependencies_installed.txt
)

REM Run the assistant
python main.py
pause
"""
    
    with open(os.path.join(output_dir, "run_assistant.bat"), "w") as f:
        f.write(batch_content)
    
    # Step 4: Create run script for macOS/Linux
    print("\n📝 Creating macOS/Linux run script...")
    shell_content = """#!/bin/bash
echo "Starting AI Assistant..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed! Please install Python 3.8 or higher."
    echo "Visit https://www.python.org/downloads/"
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if dependencies are installed
if [ ! -f "dependencies_installed.txt" ]; then
    echo "First run - installing dependencies..."
    python3 -m pip install -r requirements.txt
    touch dependencies_installed.txt
fi

# Run the assistant
python3 main.py
read -p "Press Enter to exit..."
"""
    
    with open(os.path.join(output_dir, "run_assistant.sh"), "w") as f:
        f.write(shell_content)
    
    # Make shell script executable
    try:
        os.chmod(os.path.join(output_dir, "run_assistant.sh"), 0o755)
    except:
        print("⚠️ Could not make shell script executable. Users may need to run: chmod +x run_assistant.sh")
    
    # Step 5: Create README
    print("\n📝 Creating portable README...")
    readme_content = """# AI Assistant - Portable Version

## Quick Start Guide

### Windows
1. Double-click `run_assistant.bat`
2. On first run, it will install required dependencies
3. Start using the assistant!

### macOS/Linux
1. Open Terminal in this folder
2. Run: `chmod +x run_assistant.sh` (first time only)
3. Run: `./run_assistant.sh`
4. On first run, it will install required dependencies
5. Start using the assistant!

## Features

- Voice recognition (speak to your assistant)
- Text-to-speech (assistant speaks back)
- Smart file management
- Automated screenshots
- Image generation (requires API key)
- Code generation (requires API key)
- Notes and reminders
- Math calculations
- Entertainment features

## Troubleshooting

- If you encounter errors, check that all dependencies are installed
- For voice recognition issues, ensure your microphone is working
- Some features require internet connection
- For detailed setup instructions, see the main README.md

## Platform-Specific Notes

### Windows
- For voice recognition: `pip install pipwin && pipwin install pyaudio`

### macOS
- For voice recognition: `brew install portaudio && pip install pyaudio`

### Linux
- For voice recognition: `sudo apt-get install python3-pyaudio portaudio19-dev`
"""
    
    with open(os.path.join(output_dir, "PORTABLE_README.md"), "w") as f:
        f.write(readme_content)
    
    # Step 6: Create ZIP archive
    print("\n📦 Creating ZIP archive...")
    zip_filename = f"{output_dir}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(output_dir))
                zipf.write(file_path, arcname)
    
    print(f"✅ Created: {zip_filename}")
    
    # Step 7: Summary
    print("\n✅ Portable version created successfully!")
    print(f"\n📋 You can now share:")
    print(f"1. The folder: {output_dir}")
    print(f"2. The ZIP file: {zip_filename}")
    
    print("\n💡 Instructions for users:")
    print("- Windows users: Run 'run_assistant.bat'")
    print("- macOS/Linux users: Run './run_assistant.sh'")
    print("- First run will install dependencies automatically")
    print("- No installation needed - works from any folder")

if __name__ == "__main__":
    create_portable_version()