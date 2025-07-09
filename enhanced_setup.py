"""
Enhanced setup script for Athena AI Assistant Phase 1
Includes validation, error checking, and system preparation
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

class AthenaSetup:
    def __init__(self):
        self.system = platform.system().lower()
        self.python_version = sys.version_info
        self.errors = []
        self.warnings = []
    
    def check_python_version(self):
        """Check if Python version is compatible"""
        print("🐍 Checking Python version...")
        
        if self.python_version < (3, 8):
            self.errors.append("Python 3.8 or higher is required")
            return False
        
        print(f"✅ Python {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro} detected")
        return True
    
    def check_system_requirements(self):
        """Check system-specific requirements"""
        print(f"🖥️ Checking system requirements for {self.system}...")
        
        # Check for microphone access
        try:
            import pyaudio
            p = pyaudio.PyAudio()
            if p.get_device_count() == 0:
                self.warnings.append("No audio devices detected")
            p.terminate()
        except ImportError:
            pass  # Will be installed later
        except Exception as e:
            self.warnings.append(f"Audio system check failed: {e}")
        
        # System-specific checks
        if self.system == "windows":
            self._check_windows_requirements()
        elif self.system == "darwin":
            self._check_macos_requirements()
        elif self.system == "linux":
            self._check_linux_requirements()
        
        return True
    
    def _check_windows_requirements(self):
        """Windows-specific requirement checks"""
        # Check for Visual C++ redistributables (needed for some packages)
        try:
            import winreg
            # This is a basic check - in production you'd want more thorough validation
            print("✅ Windows environment detected")
        except ImportError:
            self.warnings.append("Windows registry access limited")
    
    def _check_macos_requirements(self):
        """macOS-specific requirement checks"""
        # Check for Xcode command line tools
        try:
            result = subprocess.run(['xcode-select', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Xcode command line tools detected")
            else:
                self.warnings.append("Xcode command line tools may be needed")
        except FileNotFoundError:
            self.warnings.append("Xcode command line tools not found")
    
    def _check_linux_requirements(self):
        """Linux-specific requirement checks"""
        # Check for common audio libraries
        audio_libs = ['libasound2-dev', 'portaudio19-dev']
        for lib in audio_libs:
            try:
                result = subprocess.run(['dpkg', '-l', lib], 
                                      capture_output=True, text=True)
                if result.returncode != 0:
                    self.warnings.append(f"Audio library {lib} may be needed")
            except FileNotFoundError:
                pass  # dpkg not available (non-Debian system)
    
    def install_requirements(self):
        """Install Python packages from requirements file"""
        print("📦 Installing Python packages...")
        
        try:
            # Upgrade pip first
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "--upgrade", "pip"
            ])
            
            # Install requirements
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", "requirements_enhanced.txt"
            ])
            
            print("✅ Python packages installed successfully!")
            return True
            
        except subprocess.CalledProcessError as e:
            self.errors.append(f"Package installation failed: {e}")
            return False
        except FileNotFoundError:
            self.errors.append("requirements_enhanced.txt not found")
            return False
    
    def download_models(self):
        """Download required AI models and data"""
        print("🧠 Downloading AI models and data...")
        
        # Download NLTK data
        try:
            subprocess.check_call([
                sys.executable, "-m", "nltk.downloader", "punkt"
            ])
            print("✅ NLTK data downloaded")
        except subprocess.CalledProcessError as e:
            self.errors.append(f"NLTK download failed: {e}")
        
        # Download spaCy model
        try:
            subprocess.check_call([
                sys.executable, "-m", "spacy", "download", "en_core_web_sm"
            ])
            print("✅ spaCy model downloaded")
        except subprocess.CalledProcessError as e:
            self.errors.append(f"spaCy model download failed: {e}")
        
        return len(self.errors) == 0
    
    def create_directory_structure(self):
        """Create necessary directories"""
        print("📁 Creating directory structure...")
        
        directories = [
            "logs",
            "screenshots", 
            "data",
            "config",
            "utils"
        ]
        
        for directory in directories:
            path = Path(directory)
            path.mkdir(exist_ok=True)
            print(f"✅ Created/verified directory: {directory}")
        
        return True
    
    def setup_configuration(self):
        """Setup initial configuration"""
        print("⚙️ Setting up configuration...")
        
        try:
            from enhanced_config import config_manager
            
            # Validate configuration
            missing_keys = config_manager.validate_api_keys()
            if missing_keys:
                print("\n⚠️ Missing API Keys:")
                for key_path, description in missing_keys:
                    print(f"  - {key_path}: {description}")
                print("\nPlease configure these in the application settings.")
            
            print("✅ Configuration system initialized")
            return True
            
        except Exception as e:
            self.errors.append(f"Configuration setup failed: {e}")
            return False
    
    def run_tests(self):
        """Run basic system tests"""
        print("🧪 Running system tests...")
        
        tests_passed = 0
        total_tests = 0
        
        # Test voice recognition
        total_tests += 1
        try:
            import speech_recognition as sr
            r = sr.Recognizer()
            print("✅ Speech recognition module loaded")
            tests_passed += 1
        except Exception as e:
            print(f"❌ Speech recognition test failed: {e}")
        
        # Test text-to-speech
        total_tests += 1
        try:
            from Athenavoice import speak
            print("✅ Text-to-speech module loaded")
            tests_passed += 1
        except Exception as e:
            print(f"❌ Text-to-speech test failed: {e}")
        
        # Test database connection
        total_tests += 1
        try:
            import mysql.connector
            print("✅ MySQL connector available")
            tests_passed += 1
        except Exception as e:
            print(f"❌ MySQL test failed: {e}")
        
        # Test enhanced utilities
        total_tests += 1
        try:
            from utils.logger import athena_logger
            from utils.connectivity import connectivity_manager
            from utils.error_handler import error_handler
            from utils.system_utils import system_manager
            print("✅ Enhanced utilities loaded")
            tests_passed += 1
        except Exception as e:
            print(f"❌ Enhanced utilities test failed: {e}")
        
        print(f"📊 Tests passed: {tests_passed}/{total_tests}")
        return tests_passed == total_tests
    
    def display_summary(self):
        """Display setup summary"""
        print("\n" + "="*60)
        print("🚀 ATHENA AI ASSISTANT SETUP SUMMARY")
        print("="*60)
        
        if self.errors:
            print("❌ ERRORS:")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print("\n⚠️ WARNINGS:")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if not self.errors:
            print("✅ Setup completed successfully!")
            print("\n📋 Next steps:")
            print("1. Configure API keys using the configuration system")
            print("2. Set up MySQL database by running: python database_setup.py")
            print("3. Configure email credentials if needed")
            print("4. Run the enhanced assistant: python enhanced_athena.py")
            print("\n🎯 New features in Phase 1:")
            print("- Enhanced error handling and logging")
            print("- Internet connectivity detection")
            print("- Cross-platform system utilities")
            print("- Secure configuration management")
            print("- Improved database handling")
        else:
            print("❌ Setup failed. Please resolve the errors above.")
        
        print("="*60)
    
    def run_setup(self):
        """Run the complete setup process"""
        print("🚀 Starting Athena AI Assistant Enhanced Setup...")
        print("="*60)
        
        steps = [
            ("Python Version Check", self.check_python_version),
            ("System Requirements", self.check_system_requirements),
            ("Directory Structure", self.create_directory_structure),
            ("Package Installation", self.install_requirements),
            ("Model Downloads", self.download_models),
            ("Configuration Setup", self.setup_configuration),
            ("System Tests", self.run_tests)
        ]
        
        for step_name, step_func in steps:
            print(f"\n🔄 {step_name}...")
            if not step_func():
                print(f"❌ {step_name} failed")
                break
            print(f"✅ {step_name} completed")
        
        self.display_summary()

def main():
    """Main setup entry point"""
    setup = AthenaSetup()
    setup.run_setup()

if __name__ == "__main__":
    main()