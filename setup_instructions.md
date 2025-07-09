# AI Assistant Setup Instructions

## System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 500MB free space
- **Microphone**: Required for voice recognition
- **Internet**: Required for some features (image generation, code generation)

## Installation Steps

### 1. Download the Project

Download all the project files to your computer and extract them to a folder.

### 2. Install Python

If you don't have Python installed:
1. Download Python 3.8+ from [python.org](https://python.org)
2. During installation, check "Add Python to PATH"
3. Complete the installation

### 3. Install Dependencies

Open a command prompt or terminal in the project folder and run:

```bash
# Windows
pip install -r requirements.txt

# macOS/Linux
pip3 install -r requirements.txt
```

#### Platform-specific audio setup:

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

### 4. Run the Assistant

```bash
# Windows
python enhanced_athena.py

# macOS/Linux
python3 enhanced_athena.py
```

For the GUI version (if available):
```bash
python enhanced_gui.py
```

## Using the Assistant

### Voice Commands

1. Say the wake word (default is "Athena") followed by your command
2. Example: "Athena, what time is it?"

### Advanced Features

#### Automated Screenshots
```
"Take screenshot every 2 minutes and save to D drive"
"Stop taking screenshots"
```

#### Image Generation
```
"Generate image of a sunset over mountains"
"Create image of a futuristic city"
```

#### Code Generation
```
"Write Python code to sort a list"
"Create HTML contact form"
"Generate JavaScript todo app"
```

#### System Monitoring
```
"System status"
"Show running processes"
"Check disk space"
```

## Troubleshooting

### Voice Recognition Issues
- Ensure your microphone is properly connected and working
- Check that you've installed the audio dependencies for your platform
- Try speaking clearly and in a quiet environment
- If voice doesn't work, you can type commands instead

### Dependency Issues
- Make sure you've installed all requirements: `pip install -r requirements.txt`
- For PyAudio issues, use the platform-specific installation commands
- If you get "module not found" errors, try installing the specific package: `pip install [package_name]`

### Performance Issues
- Close other resource-intensive applications
- Ensure your computer meets the minimum system requirements
- If the assistant is slow, try disabling continuous voice recognition

## Exporting and Sharing

You can export the assistant by copying the entire project folder. To share with others:

1. Zip the entire project folder
2. Share the zip file
3. Recipients will need to follow the same setup instructions

## Additional Notes

- All data is stored locally on your computer
- Voice recognition requires an internet connection unless you've set up offline recognition
- Image and code generation features require internet access
- The assistant works best with a clear microphone and in a quiet environment