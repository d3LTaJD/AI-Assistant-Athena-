#!/usr/bin/env python3
"""
Main entry point for AI Assistant
Detects environment and runs the appropriate version
"""

import os
import sys
import platform

def check_environment():
    """Check the current environment and capabilities"""
    print("🔍 Checking environment...")
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check platform
    system = platform.system()
    print(f"Platform: {system}")
    
    # Check for key modules
    modules = {}
    for module_name in ["speech_recognition", "pyttsx3", "requests", "PIL"]:
        try:
            __import__(module_name)
            modules[module_name] = True
            print(f"✅ {module_name} available")
        except ImportError:
            modules[module_name] = False
            print(f"❌ {module_name} not available")
    
    return {
        "python_version": python_version,
        "system": system,
        "modules": modules
    }

def run_assistant():
    """Run the appropriate assistant version"""
    # Simple version that works everywhere
    print("\n🚀 Starting AI Assistant...")
    
    try:
        from webcontainer_athena import WebContainerAthena
        assistant = WebContainerAthena()
        assistant.run()
        return True
    except Exception as e:
        print(f"❌ Error starting assistant: {e}")
        return False

def main():
    """Main function"""
    print("🤖 AI Assistant - Launcher")
    print("=" * 60)
    
    # Check environment
    check_environment()
    
    # Run assistant
    run_assistant()

if __name__ == "__main__":
    main()