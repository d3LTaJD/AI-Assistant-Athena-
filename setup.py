"""
Setup script for Athena AI Assistant
Run this script to install all dependencies and set up the environment
"""

import subprocess
import sys
import os

def install_requirements():
    """Install Python packages from requirements.txt"""
    print("📦 Installing Python packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Python packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False
    return True

def download_nltk_data():
    """Download required NLTK data"""
    print("📚 Downloading NLTK data...")
    try:
        subprocess.check_call([sys.executable, "-m", "nltk.downloader", "punkt"])
        print("✅ NLTK data downloaded successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error downloading NLTK data: {e}")
        return False
    return True

def download_spacy_model():
    """Download spaCy English model"""
    print("🧠 Downloading spaCy English model...")
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        print("✅ spaCy model downloaded successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error downloading spaCy model: {e}")
        return False
    return True

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    directories = ["screenshots"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")

def main():
    """Main setup function"""
    print("🚀 Setting up Athena AI Assistant...")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during package installation.")
        return
    
    # Download NLTK data
    if not download_nltk_data():
        print("❌ Setup failed during NLTK data download.")
        return
    
    # Download spaCy model
    if not download_spacy_model():
        print("❌ Setup failed during spaCy model download.")
        return
    
    # Create directories
    create_directories()
    
    print("=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Configure your API keys in config.py")
    print("2. Set up your email credentials in secrets_1.py")
    print("3. Run database_setup.py to create the database")
    print("4. Run python Athena.py to start the assistant")

if __name__ == "__main__":
    main()