"""
Development runner script
Use this for development and testing
"""
import sys
import os
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_modules = [
        'customtkinter',
        'pyttsx3',
        'speech_recognition',
        'PIL',
        'bcrypt'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print("❌ Missing required modules:")
        for module in missing_modules:
            print(f"  - {module}")
        print("\nInstall missing modules with:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main development runner"""
    print("🚀 AI Assistant - Development Mode")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("✅ All dependencies found")
    print("🔄 Starting application...")
    
    try:
        from gui import main as gui_main
        gui_main()
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()