#!/usr/bin/env python3
"""
Fixed Environment Setup Script for WebContainer
Works without _signal module dependency
"""

import sys
import os
import platform

# Use our workarounds
try:
    import subprocess_alt as subprocess
except ImportError:
    print("❌ subprocess_alt not found. Please run python_diagnostics.py first.")
    sys.exit(1)

def check_python_installation():
    """Check if Python installation is working properly"""
    print("🔍 Diagnosing Python installation...")
    
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current directory: {os.getcwd()}")
    
    # Test core modules that should work
    core_modules = ['os', 'sys', 'platform', 'json', 'time']
    missing_modules = []
    
    for module in core_modules:
        try:
            __import__(module)
            print(f"✅ {module} - OK")
        except ImportError as e:
            print(f"❌ {module} - MISSING: {e}")
            missing_modules.append(module)
    
    return missing_modules

def install_requirements():
    """Install requirements using our subprocess alternative"""
    print("\n📦 Installing requirements...")
    
    requirements_files = [
        'requirements.txt',
        'requirements_enhanced.txt'
    ]
    
    for req_file in requirements_files:
        if os.path.exists(req_file):
            print(f"Installing from {req_file}...")
            try:
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', '-r', req_file
                ], check=False)
                
                if result.returncode == 0:
                    print(f"✅ Successfully installed from {req_file}")
                else:
                    print(f"⚠️ Some packages from {req_file} may have failed to install")
            except Exception as e:
                print(f"❌ Error installing from {req_file}: {e}")
        else:
            print(f"📄 {req_file} not found, skipping...")

def run_setup():
    """Run the main setup process"""
    print("\n🚀 Running setup process...")
    
    setup_files = [
        'enhanced_setup.py',
        'setup.py'
    ]
    
    for setup_file in setup_files:
        if os.path.exists(setup_file):
            print(f"\nRunning {setup_file}...")
            try:
                result = subprocess.run([sys.executable, setup_file], check=False)
                if result.returncode == 0:
                    print(f"✅ {setup_file} completed successfully")
                    return True
                else:
                    print(f"⚠️ {setup_file} completed with warnings")
            except Exception as e:
                print(f"❌ Error running {setup_file}: {e}")
    
    return False

def main():
    """Main function"""
    print("🚀 Athena AI Assistant - Fixed Environment Setup")
    print("=" * 60)
    
    # Check Python installation
    missing_modules = check_python_installation()
    
    if missing_modules:
        print(f"\n⚠️ Some modules are missing: {missing_modules}")
        print("This is expected in WebContainer environments.")
    
    # Install requirements
    install_requirements()
    
    # Run setup
    if run_setup():
        print("\n✅ Setup completed successfully!")
        print("\n📋 You can now try running:")
        print("   python enhanced_athena.py")
        print("   or")
        print("   python Athena.py")
    else:
        print("\n⚠️ Setup completed with some issues.")
        print("You may still be able to run the application.")

if __name__ == "__main__":
    main()
