#!/usr/bin/env python3
"""
Environment Fix Script for Athena AI Assistant
This script attempts to diagnose and fix Python environment issues
"""

import sys
import os
import subprocess
import platform

def check_python_installation():
    """Check if Python installation is working properly"""
    print("🔍 Diagnosing Python installation...")
    
    # Check Python version
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Python path: {sys.path}")
    
    # Test core modules
    core_modules = ['signal', 'subprocess', 'os', 'sys', 'platform']
    missing_modules = []
    
    for module in core_modules:
        try:
            __import__(module)
            print(f"✅ {module} - OK")
        except ImportError as e:
            print(f"❌ {module} - MISSING: {e}")
            missing_modules.append(module)
    
    return missing_modules

def create_virtual_environment():
    """Create a new virtual environment"""
    print("\n🔧 Creating new virtual environment...")
    
    venv_path = "athena_venv"
    
    try:
        # Remove existing venv if it exists
        if os.path.exists(venv_path):
            print(f"Removing existing virtual environment: {venv_path}")
            if platform.system() == "Windows":
                subprocess.run(["rmdir", "/s", "/q", venv_path], shell=True)
            else:
                subprocess.run(["rm", "-rf", venv_path])
        
        # Create new virtual environment
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
        print(f"✅ Virtual environment created: {venv_path}")
        
        # Get activation script path
        if platform.system() == "Windows":
            activate_script = os.path.join(venv_path, "Scripts", "activate.bat")
            python_exe = os.path.join(venv_path, "Scripts", "python.exe")
        else:
            activate_script = os.path.join(venv_path, "bin", "activate")
            python_exe = os.path.join(venv_path, "bin", "python")
        
        print(f"\n📋 To activate the virtual environment:")
        if platform.system() == "Windows":
            print(f"   {activate_script}")
        else:
            print(f"   source {activate_script}")
        
        print(f"\n📋 To run setup with the virtual environment:")
        print(f"   {python_exe} enhanced_setup.py")
        
        return True, python_exe
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False, None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False, None

def install_basic_requirements(python_exe):
    """Install basic requirements in the virtual environment"""
    print("\n📦 Installing basic requirements...")
    
    basic_packages = [
        "pip",
        "setuptools",
        "wheel"
    ]
    
    try:
        # Upgrade pip first
        subprocess.check_call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install basic packages
        for package in basic_packages:
            subprocess.check_call([python_exe, "-m", "pip", "install", "--upgrade", package])
            print(f"✅ Installed: {package}")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install basic requirements: {e}")
        return False

def create_run_script():
    """Create a script to run Athena with the virtual environment"""
    print("\n📝 Creating run script...")
    
    system = platform.system()
    
    if system == "Windows":
        script_content = """@echo off
echo Starting Athena AI Assistant...
call athena_venv\\Scripts\\activate.bat
python enhanced_setup.py
pause
"""
        script_name = "run_athena.bat"
    else:
        script_content = """#!/bin/bash
echo "Starting Athena AI Assistant..."
source athena_venv/bin/activate
python enhanced_setup.py
"""
        script_name = "run_athena.sh"
    
    try:
        with open(script_name, 'w') as f:
            f.write(script_content)
        
        if system != "Windows":
            os.chmod(script_name, 0o755)
        
        print(f"✅ Created run script: {script_name}")
        return True
    except Exception as e:
        print(f"❌ Failed to create run script: {e}")
        return False

def main():
    """Main function to fix environment issues"""
    print("🚀 Athena AI Assistant - Environment Fix Tool")
    print("=" * 50)
    
    # Check current Python installation
    missing_modules = check_python_installation()
    
    if missing_modules:
        print(f"\n❌ Critical Python modules are missing: {missing_modules}")
        print("This indicates a corrupted Python installation.")
        print("\n🔧 Attempting to create a clean virtual environment...")
        
        # Create virtual environment
        success, python_exe = create_virtual_environment()
        
        if success:
            # Install basic requirements
            if install_basic_requirements(python_exe):
                # Create run script
                create_run_script()
                
                print("\n✅ Environment fix completed!")
                print("\n📋 Next steps:")
                print("1. Use the created virtual environment")
                print("2. Run the setup script using the virtual environment Python")
                print("3. If issues persist, consider reinstalling Python completely")
                
                if platform.system() == "Windows":
                    print("\nTo run Athena: double-click run_athena.bat")
                else:
                    print("\nTo run Athena: ./run_athena.sh")
            else:
                print("\n❌ Failed to install basic requirements in virtual environment")
        else:
            print("\n❌ Failed to create virtual environment")
            print("\n🔧 Manual steps required:")
            print("1. Completely uninstall current Python")
            print("2. Download and install Python from python.org")
            print("3. Ensure 'Add Python to PATH' is checked during installation")
            print("4. Restart your computer")
            print("5. Run this script again")
    else:
        print("\n✅ Python installation appears to be working correctly")
        print("The error might be intermittent. Try running enhanced_setup.py again.")

if __name__ == "__main__":
    main()