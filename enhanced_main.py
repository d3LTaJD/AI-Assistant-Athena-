"""
Enhanced Main Entry Point for Advanced AI Assistant
Production-ready with comprehensive error handling and logging
"""
import sys
import os
import logging
from pathlib import Path
import traceback

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Setup logging
def setup_logging():
    """Setup comprehensive logging system"""
    log_dir = Path.home() / ".ai_assistant" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "assistant.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

def check_dependencies():
    """Check if all required dependencies are installed"""
    logger = logging.getLogger(__name__)
    
    required_modules = {
        'customtkinter': 'Modern GUI framework',
        'pyttsx3': 'Text-to-speech engine',
        'speech_recognition': 'Voice recognition',
        'PIL': 'Image processing',
        'bcrypt': 'Password hashing',
        'psutil': 'System monitoring',
        'numpy': 'Numerical computing',
        'webrtcvad': 'Voice activity detection'
    }
    
    missing_modules = []
    for module, description in required_modules.items():
        try:
            __import__(module)
            logger.info(f"✅ {module} - {description}")
        except ImportError:
            missing_modules.append((module, description))
            logger.error(f"❌ {module} - {description} - MISSING")
    
    if missing_modules:
        print("\n❌ Missing required modules:")
        for module, description in missing_modules:
            print(f"  - {module}: {description}")
        print("\nInstall missing modules with:")
        print("pip install -r requirements_advanced.txt")
        return False
    
    logger.info("✅ All dependencies found")
    return True

def check_system_requirements():
    """Check system requirements and capabilities"""
    logger = logging.getLogger(__name__)
    
    # Check Python version
    if sys.version_info < (3, 8):
        logger.error(f"❌ Python 3.8+ required. Current: {sys.version}")
        return False
    
    logger.info(f"✅ Python {sys.version}")
    
    # Check audio system
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        device_count = p.get_device_count()
        p.terminate()
        logger.info(f"✅ Audio system: {device_count} devices available")
    except Exception as e:
        logger.warning(f"⚠️ Audio system limited: {e}")
    
    # Check system resources
    try:
        import psutil
        memory = psutil.virtual_memory()
        if memory.total < 2 * 1024**3:  # 2GB
            logger.warning("⚠️ Low system memory detected")
        else:
            logger.info(f"✅ System memory: {memory.total // 1024**3}GB")
    except Exception as e:
        logger.warning(f"⚠️ Could not check system resources: {e}")
    
    return True

def initialize_application():
    """Initialize the application with proper error handling"""
    logger = logging.getLogger(__name__)
    
    try:
        # Import application modules
        from enhanced_gui import main as gui_main
        
        logger.info("🚀 Starting Advanced AI Assistant...")
        
        # Run the application
        gui_main()
        
    except ImportError as e:
        logger.error(f"Import error: {e}")
        print(f"❌ Import error: {e}")
        print("Please ensure all dependencies are installed:")
        print("pip install -r requirements_advanced.txt")
        return False
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        logger.error(traceback.format_exc())
        print(f"❌ Application error: {e}")
        return False
    
    return True

def show_startup_banner():
    """Show startup banner with system information"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                🤖 ADVANCED AI ASSISTANT                      ║
║                                                              ║
║  🎤 Room-Scale Voice Recognition                             ║
║  🤖 3D Animated Avatar                                       ║
║  📁 Smart File Management                                    ║
║  🖥️ Real-Time System Monitoring                             ║
║  🧠 Advanced AI Capabilities                                 ║
║  ⚡ Lightning-Fast Response                                  ║
║                                                              ║
║  Production-Ready • Offline-First • Privacy-Focused         ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def main():
    """Enhanced main entry point with comprehensive error handling"""
    # Setup logging first
    logger = setup_logging()
    
    try:
        # Show startup banner
        show_startup_banner()
        
        # Check system requirements
        logger.info("Checking system requirements...")
        if not check_system_requirements():
            logger.error("System requirements check failed")
            input("Press Enter to exit...")
            sys.exit(1)
        
        # Check dependencies
        logger.info("Checking dependencies...")
        if not check_dependencies():
            logger.error("Dependency check failed")
            input("Press Enter to exit...")
            sys.exit(1)
        
        # Initialize and run application
        logger.info("Initializing application...")
        if not initialize_application():
            logger.error("Application initialization failed")
            input("Press Enter to exit...")
            sys.exit(1)
        
        logger.info("Application closed normally")
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        print("\n👋 Application stopped by user")
        
    except Exception as e:
        logger.error(f"Critical error: {e}")
        logger.error(traceback.format_exc())
        print(f"❌ Critical error: {e}")
        print("Check the log file for detailed error information")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()