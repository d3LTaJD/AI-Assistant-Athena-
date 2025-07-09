# AI Assistant

A comprehensive AI assistant with voice recognition, automated screenshots, image generation, and code generation capabilities.

## Features

- **Voice Recognition**: Speak commands naturally
- **Text-to-Speech**: Assistant speaks back to you
- **Smart File Management**: Find and open files with natural language
- **Automated Screenshots**: Schedule screenshots at regular intervals
- **Image Generation**: Create AI-generated images from text descriptions
- **Code Generation**: Generate code snippets in multiple languages
- **Notes & Reminders**: Save notes and set reminders
- **Math & Conversions**: Perform calculations and unit conversions
- **Entertainment**: Jokes, facts, coin flips, dice rolls

## Installation Options

### Option 1: Run the Setup Script (Windows)

1. Run `setup.py` to create a Windows installer:
   ```
   python setup.py
   ```

2. This will create `AI_Assistant_Setup.exe` which you can share with others.

### Option 2: Create a Portable Version

1. Run `create_portable_version.py` to create a portable package:
   ```
   python create_portable_version.py
   ```

2. Share the resulting folder or ZIP file with others.

### Option 3: Manual Installation

1. Install Python 3.8+ from [python.org](https://python.org)

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the assistant:
   ```
   python main.py
   ```

## Usage

### Basic Commands

- **Time & Date**: "athena time", "athena date"
- **Calculations**: "athena calculate 2 + 2 * 3"
- **Notes**: "athena create note Buy groceries"
- **Reminders**: "athena remind me to call mom"
- **Entertainment**: "athena tell me a joke", "athena flip coin"

### Advanced Features

- **Automated Screenshots**: "athena take screenshot every 2 minutes and save to D drive"
- **Image Generation**: "athena generate image of a sunset over mountains"
- **Code Generation**: "athena write python code to sort a list"

## Requirements

- Python 3.8 or higher
- See requirements.txt for all dependencies

## Sharing with Others

### For Technical Users
Share the GitHub repository link and they can follow the installation instructions.

### For Non-Technical Users
1. Create the installer using `setup.py`
2. Share the installer with them
3. They just need to run the installer and the application will be ready to use

### For Portable Use
1. Create a portable version using `create_portable_version.py`
2. Share the folder or ZIP file
3. Users can run the application without installation

## Troubleshooting

- If voice recognition doesn't work, ensure PyAudio is installed:
  - Windows: `pip install pipwin && pipwin install pyaudio`
  - macOS: `brew install portaudio && pip install pyaudio`
  - Linux: `sudo apt-get install python3-pyaudio portaudio19-dev`

- If you see "module not found" errors, install the specific package:
  - `pip install [package_name]`

## License

MIT License