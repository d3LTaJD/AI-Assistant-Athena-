# PC Athena AI Assistant 🤖

A complete AI voice assistant designed to run on Windows, macOS, and Linux with full functionality.

## 🌟 Features

### 🎤 **Voice & Speech**
- **Voice Recognition**: Speak your commands naturally
- **Text-to-Speech**: Athena speaks back to you
- **Fallback Support**: Works with text input if voice isn't available

### ⏰ **Time & Date**
- Current time and date
- Detailed datetime information
- Timezone and calendar data

### 🧮 **Math & Conversions**
- Advanced calculator with math functions
- Unit conversions (temperature, length, weight)
- Support for complex expressions

### 📝 **Notes & Reminders**
- Create and save notes
- Set reminders for tasks
- Persistent data storage
- Search and organize

### 🎲 **Entertainment**
- Tell jokes
- Flip coins
- Roll dice (customizable sides and quantity)
- Generate random numbers
- Share interesting facts

### 🔐 **Utilities**
- Generate secure passwords
- Take screenshots
- System information
- Interaction history

### 💾 **Data Management**
- Automatic data saving
- JSON-based storage
- History tracking
- Settings persistence

## 🛠️ Installation

### Quick Setup (Recommended)

1. **Download the files**:
   - `pc_athena.py` (main application)
   - `install_pc.py` (installation script)
   - `requirements_pc.txt` (dependencies)

2. **Run the installer**:
   ```bash
   python install_pc.py
   ```

3. **Start Athena**:
   ```bash
   python pc_athena.py
   ```

### Manual Installation

1. **Install Python 3.8+** from [python.org](https://python.org)

2. **Install dependencies**:
   ```bash
   pip install -r requirements_pc.txt
   ```

3. **Platform-specific audio setup**:

   **Windows**:
   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```

   **macOS**:
   ```bash
   brew install portaudio
   pip install pyaudio
   ```

   **Linux (Ubuntu/Debian)**:
   ```bash
   sudo apt-get install python3-pyaudio portaudio19-dev
   pip install pyaudio
   ```

## 🎯 Usage

### Starting Athena
```bash
python pc_athena.py
```

### Command Examples

#### Basic Commands
```
athena time                    # Get current time
athena date                    # Get current date
athena help                    # Show all commands
```

#### Math & Calculations
```
athena calculate 15 + 25       # Basic math
athena calculate sqrt(144)     # Advanced functions
athena convert 100 celsius to fahrenheit
athena convert 5 feet to meters
```

#### Notes & Reminders
```
athena create note Buy groceries tomorrow
athena show notes
athena remind me to call dentist
athena show reminders
```

#### Entertainment
```
athena joke                    # Tell a joke
athena flip coin              # Flip a coin
athena roll 3 dice            # Roll multiple dice
athena random number between 1 and 100
athena random fact            # Interesting fact
athena generate password 16   # Secure password
```

#### System Features
```
athena screenshot             # Take screenshot
athena system info           # Show system details
athena history              # Show recent interactions
athena toggle voice         # Enable/disable voice
athena toggle speech        # Enable/disable TTS
```

## 🎛️ Features by Availability

| Feature | Always Available | Requires Installation |
|---------|------------------|----------------------|
| Text Input | ✅ | - |
| Basic Commands | ✅ | - |
| Math & Conversions | ✅ | - |
| Notes & Reminders | ✅ | - |
| Entertainment | ✅ | - |
| Voice Recognition | - | ✅ pyaudio, SpeechRecognition |
| Text-to-Speech | - | ✅ pyttsx3 |
| Screenshots | - | ✅ pyautogui |

## 📁 File Structure

```
pc_athena/
├── pc_athena.py              # Main application
├── install_pc.py             # Installation script
├── requirements_pc.txt       # Dependencies
├── README_PC.md             # This file
└── athena_data/             # Created automatically
    ├── athena_data.json     # Notes, reminders, settings
    └── screenshots/         # Screenshot storage
```

## 🔧 Configuration

### Voice Settings
- Toggle voice input: `athena toggle voice`
- Toggle text-to-speech: `athena toggle speech`
- Settings are saved automatically

### Data Storage
- All data stored in `athena_data/athena_data.json`
- Screenshots in `athena_data/screenshots/`
- Automatic backup of recent interactions

## 🐛 Troubleshooting

### Voice Recognition Issues
```bash
# Windows
pip install pipwin
pipwin install pyaudio

# macOS
brew install portaudio

# Linux
sudo apt-get install python3-pyaudio portaudio19-dev
```

### Text-to-Speech Issues
```bash
pip install --upgrade pyttsx3
```

### Permission Issues (macOS)
- Grant microphone access in System Preferences
- Grant screen recording access for screenshots

### General Issues
1. Check Python version: `python --version` (need 3.8+)
2. Update pip: `python -m pip install --upgrade pip`
3. Reinstall dependencies: `pip install -r requirements_pc.txt --force-reinstall`

## 🎤 Voice Commands

Athena responds to natural language. You can:

- **Start with "athena"**: `athena what time is it?`
- **Or just speak directly**: `what time is it?` (wake word optional)
- **Use text input anytime**: Type commands if voice isn't working

## 💡 Tips

1. **First Time**: Run `athena help` to see all commands
2. **Voice Issues**: Use text input - all features work without voice
3. **Data Backup**: Your notes and reminders are automatically saved
4. **Screenshots**: Saved with timestamps in the screenshots folder
5. **History**: Use `athena history` to see recent interactions

## 🔒 Privacy & Security

- **Local Processing**: All data stored locally on your computer
- **No Cloud**: No data sent to external servers (except for voice recognition)
- **Secure Passwords**: Generated passwords use cryptographically secure methods
- **Data Control**: You own all your notes, reminders, and history

## 🆘 Support

### Common Solutions
- **"Command not recognized"**: Try `athena help` for correct syntax
- **Voice not working**: Use text input, voice is optional
- **Installation fails**: Try manual installation steps above
- **Permissions needed**: Grant microphone/screen access when prompted

### Getting Help
1. Run `athena system info` to check component status
2. Check the console for error messages
3. Try text input if voice fails
4. Restart the application if needed

## 🎉 Enjoy!

PC Athena is designed to be your helpful AI assistant. Whether you use voice commands or text input, all features are available to make your computing experience more productive and fun!

**Start with**: `python pc_athena.py` and say `athena help`