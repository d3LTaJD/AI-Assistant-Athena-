#!/usr/bin/env python3
"""
Run script for AI Assistant
Detects environment and runs the appropriate version
"""

import sys
import os
import platform
import importlib.util

def check_module_exists(module_name):
    """Check if a Python module is installed"""
    return importlib.util.find_spec(module_name) is not None

def check_environment():
    """Check the current environment and capabilities"""
    print("🔍 Checking environment...")
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check platform
    system = platform.system()
    print(f"Platform: {system}")
    
    # Check for WebContainer environment
    in_webcontainer = os.path.exists("/home/project") and system == "Linux"
    print(f"WebContainer: {'Yes' if in_webcontainer else 'No'}")
    
    # Check for key modules
    modules = {
        "speech_recognition": check_module_exists("speech_recognition"),
        "pyttsx3": check_module_exists("pyttsx3"),
        "pyaudio": check_module_exists("pyaudio"),
        "customtkinter": check_module_exists("customtkinter"),
        "PIL": check_module_exists("PIL"),
        "psutil": check_module_exists("psutil"),
        "webrtcvad": check_module_exists("webrtcvad"),
        "openai": check_module_exists("openai")
    }
    
    print("\nModule availability:")
    for module, exists in modules.items():
        print(f"- {module}: {'✅' if exists else '❌'}")
    
    return {
        "python_version": python_version,
        "system": system,
        "in_webcontainer": in_webcontainer,
        "modules": modules
    }

def determine_best_version(env):
    """Determine the best version to run based on environment"""
    # Check for available assistant versions
    available_versions = []
    
    if os.path.exists("enhanced_gui.py"):
        available_versions.append(("enhanced_gui.py", "GUI version with all features", 4))
    
    if os.path.exists("enhanced_athena.py"):
        available_versions.append(("enhanced_athena.py", "Enhanced console version with advanced features", 3))
    
    if os.path.exists("Athena.py"):
        available_versions.append(("Athena.py", "Standard console version", 2))
    
    if os.path.exists("webcontainer_athena.py"):
        available_versions.append(("webcontainer_athena.py", "WebContainer compatible version", 1))
    
    if os.path.exists("simple_athena.py"):
        available_versions.append(("simple_athena.py", "Simple version with minimal dependencies", 0))
    
    # If in WebContainer, prefer WebContainer version
    if env["in_webcontainer"]:
        for version in available_versions:
            if "webcontainer" in version[0]:
                return version
    
    # If GUI modules available, prefer GUI version
    if env["modules"]["customtkinter"] and env["modules"]["PIL"]:
        for version in available_versions:
            if "gui" in version[0]:
                return version
    
    # If voice modules available, prefer enhanced version
    if env["modules"]["speech_recognition"] and env["modules"]["pyttsx3"]:
        for version in available_versions:
            if "enhanced" in version[0]:
                return version
    
    # Otherwise, use the highest priority available version
    if available_versions:
        available_versions.sort(key=lambda x: x[2], reverse=True)
        return available_versions[0]
    
    return None

def run_assistant(version):
    """Run the selected assistant version"""
    print(f"\n🚀 Running {version[0]} - {version[1]}")
    
    try:
        os.system(f"{sys.executable} {version[0]}")
        return True
    except Exception as e:
        print(f"❌ Error running {version[0]}: {e}")
        return False

def main():
    """Main function"""
    print("🤖 AI Assistant - Smart Launcher")
    print("=" * 60)
    
    # Check environment
    env = check_environment()
    
    # Determine best version
    version = determine_best_version(env)
    
    if not version:
        print("\n❌ No suitable assistant version found!")
        print("Please make sure at least one of these files exists:")
        print("- enhanced_gui.py")
        print("- enhanced_athena.py")
        print("- Athena.py")
        print("- webcontainer_athena.py")
        print("- simple_athena.py")
        return
    
    # Ask user if they want to run the selected version
    print(f"\n✅ Recommended version: {version[0]} - {version[1]}")
    
    choice = input("Run this version? (Y/n): ").strip().lower()
    if choice in ["", "y", "yes"]:
        run_assistant(version)
    else:
        print("\nAvailable versions:")
        available_versions = []
        
        if os.path.exists("enhanced_gui.py"):
            available_versions.append(("1", "enhanced_gui.py", "GUI version with all features"))
        
        if os.path.exists("enhanced_athena.py"):
            available_versions.append(("2", "enhanced_athena.py", "Enhanced console version with advanced features"))
        
        if os.path.exists("Athena.py"):
            available_versions.append(("3", "Athena.py", "Standard console version"))
        
        if os.path.exists("webcontainer_athena.py"):
            available_versions.append(("4", "webcontainer_athena.py", "WebContainer compatible version"))
        
        if os.path.exists("simple_athena.py"):
            available_versions.append(("5", "simple_athena.py", "Simple version with minimal dependencies"))
        
        for num, file, desc in available_versions:
            print(f"{num}. {file} - {desc}")
        
        choice = input("\nEnter number to run (or q to quit): ").strip().lower()
        
        if choice == "q":
            print("Exiting...")
            return
        
        for num, file, desc in available_versions:
            if choice == num:
                run_assistant((file, desc, 0))
                return
        
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    main()