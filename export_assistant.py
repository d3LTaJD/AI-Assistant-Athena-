#!/usr/bin/env python3
"""
Export script for AI Assistant
Creates a portable package that can be shared and run on other computers
"""

import os
import sys
import shutil
import zipfile
import datetime
import platform
from pathlib import Path

def create_export_directory():
    """Create directory for export"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    export_dir = f"ai_assistant_export_{timestamp}"
    
    if os.path.exists(export_dir):
        shutil.rmtree(export_dir)
    
    os.makedirs(export_dir)
    return export_dir

def copy_essential_files(export_dir):
    """Copy essential files to export directory"""
    print("📁 Copying essential files...")
    
    # Core files
    essential_files = [
        "enhanced_athena.py",
        "webcontainer_athena.py",
        "simple_athena.py",
        "advanced_features.py",
        "advanced_voice_handler.py",
        "config.py",
        "database.py",
        "file_handler.py",
        "install.py",
        "setup_instructions.md",
        "requirements.txt"
    ]
    
    # Copy each file if it exists
    for file in essential_files:
        if os.path.exists(file):
            shutil.copy2(file, export_dir)
            print(f"✅ Copied: {file}")
        else:
            print(f"⚠️ Missing: {file}")
    
    # Copy directories
    essential_dirs = [
        "utils",
        "assets"
    ]
    
    for directory in essential_dirs:
        if os.path.exists(directory) and os.path.isdir(directory):
            shutil.copytree(directory, os.path.join(export_dir, directory))
            print(f"✅ Copied directory: {directory}")
        else:
            print(f"⚠️ Missing directory: {directory}")
    
    # Create empty directories
    for directory in ["screenshots", "logs", "data"]:
        os.makedirs(os.path.join(export_dir, directory), exist_ok=True)
        print(f"✅ Created directory: {directory}")

def create_readme(export_dir):
    """Create README file with instructions"""
    readme_content = """# AI Assistant - Portable Version

## Quick Start Guide

1. **Install Python 3.8+** if not already installed
   - Download from [python.org](https://python.org)
   - Make sure to check "Add Python to PATH" during installation

2. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Run the Assistant**
   ```
   python enhanced_athena.py
   ```
   
   If that doesn't work, try:
   ```
   python simple_athena.py
   ```

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
- For detailed setup instructions, see setup_instructions.md

## Platform-Specific Notes

### Windows
- For voice recognition: `pip install pipwin && pipwin install pyaudio`

### macOS
- For voice recognition: `brew install portaudio && pip install pyaudio`

### Linux
- For voice recognition: `sudo apt-get install python3-pyaudio portaudio19-dev`

## Contact

If you have any questions or issues, please contact the person who shared this assistant with you.
"""
    
    with open(os.path.join(export_dir, "README.md"), "w") as f:
        f.write(readme_content)
    
    print("✅ Created README.md")

def create_run_script(export_dir):
    """Create platform-specific run scripts"""
    print("📝 Creating run scripts...")
    
    # Windows batch file
    windows_script = """@echo off
echo Starting AI Assistant...
python enhanced_athena.py
if %ERRORLEVEL% NEQ 0 (
    echo Trying alternative...
    python simple_athena.py
)
pause
"""
    
    with open(os.path.join(export_dir, "run_assistant.bat"), "w") as f:
        f.write(windows_script)
    
    # Unix shell script
    unix_script = """#!/bin/bash
echo "Starting AI Assistant..."
python3 enhanced_athena.py || python3 simple_athena.py
"""
    
    unix_script_path = os.path.join(export_dir, "run_assistant.sh")
    with open(unix_script_path, "w") as f:
        f.write(unix_script)
    
    # Make Unix script executable
    try:
        os.chmod(unix_script_path, 0o755)
    except:
        print("⚠️ Could not make shell script executable")
    
    print("✅ Created run scripts")

def create_zip_archive(export_dir):
    """Create ZIP archive of export directory"""
    print("🔄 Creating ZIP archive...")
    
    zip_filename = f"{export_dir}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(export_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(export_dir))
                zipf.write(file_path, arcname)
    
    print(f"✅ Created archive: {zip_filename}")
    return zip_filename

def main():
    """Main export function"""
    print("🚀 AI Assistant - Export Tool")
    print("=" * 60)
    
    # Create export directory
    export_dir = create_export_directory()
    print(f"📁 Export directory: {export_dir}")
    
    # Copy essential files
    copy_essential_files(export_dir)
    
    # Create README
    create_readme(export_dir)
    
    # Create run scripts
    create_run_script(export_dir)
    
    # Create ZIP archive
    zip_file = create_zip_archive(export_dir)
    
    print("\n" + "=" * 60)
    print("✅ Export completed successfully!")
    print(f"📦 Exported to: {zip_file}")
    print("\n📋 Next steps:")
    print("1. Share the ZIP file with others")
    print("2. They should extract the ZIP and follow the README instructions")
    print("3. For a complete installation, they should run install.py first")
    
    # Cleanup
    try:
        shutil.rmtree(export_dir)
        print("🧹 Cleaned up temporary export directory")
    except:
        print("⚠️ Could not clean up temporary directory")

if __name__ == "__main__":
    main()