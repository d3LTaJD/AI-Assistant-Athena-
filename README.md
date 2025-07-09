# 🤖 AI Assistant - Offline-First Desktop Application

A production-ready, offline-first desktop AI assistant built with Python. Features voice recognition, natural language processing, smart file management, and a modern GUI.

## ✨ Features

### 🎤 **Voice & Speech**
- **Voice Recognition**: Whisper-based offline speech recognition
- **Text-to-Speech**: Natural-sounding male/female voices
- **Wake Word**: Customizable wake word (e.g., "Jarvis", "Athena")
- **Continuous Listening**: Always-on voice activation

### 📁 **Smart File Management**
- **Intelligent File Search**: Find files across all drives (C:, D:, E:, etc.)
- **Natural Language**: "Open my resume from Documents" or "Play music from E drive"
- **Recursive Search**: Deep file system search with configurable depth
- **File Aliases**: Create shortcuts for frequently accessed folders
- **Multiple Results**: Smart handling when multiple files match

### 🖥️ **Modern GUI**
- **Dark Theme**: Modern, eye-friendly interface
- **Animated Avatar**: 3D assistant animation (customizable)
- **Chat Interface**: WhatsApp-style conversation view
- **Quick Actions**: One-click access to common tasks
- **Settings Panel**: Customize voice, name, and preferences

### 💾 **Database & Persistence**
- **SQLite Database**: Secure local data storage
- **User Accounts**: Login/signup with encrypted passwords
- **Chat History**: Persistent conversation memory
- **File Aliases**: Custom folder shortcuts
- **Settings Sync**: Preferences saved across sessions

### 🌐 **Online Features** (Optional)
- **YouTube Search**: Voice-activated YouTube searches
- **Web Search**: Google search integration
- **Weather Updates**: Current weather information
- **News Feed**: Latest news updates

## 🚀 Installation

### Option 1: Download Installer (Recommended)
1. Download `AI_Assistant_Setup.exe` from releases
2. Run the installer and follow the setup wizard
3. Launch from desktop shortcut or Start menu

### Option 2: Build from Source
```bash
# Clone repository
git clone https://github.com/yourusername/ai-assistant.git
cd ai-assistant

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## 🛠️ First Time Setup

1. **Assistant Name**: Choose your assistant's name (e.g., Jarvis, Athena, Alex)
2. **Voice Preference**: Select male or female voice
3. **Account Creation**: Create your user account
4. **Permissions**: Grant microphone access for voice features

## 💬 Usage Examples

### File Operations
```
"Open my Downloads folder"
"Find resume.pdf on C drive"
"Play music from E drive"
"Show pictures from Desktop"
"Open my workspace folder"
```

### System Commands
```
"What time is it?"
"What's today's date?"
"Calculate 15 * 7 + 23"
"Tell me a joke"
"Flip a coin"
```

### Web Features (Requires Internet)
```
"Search YouTube for Python tutorials"
"Search web for AI news"
"What's the weather like?"
"Show me the latest news"
```

### Assistant Management
```
"Change name to Jarvis"
"Change voice to male"
"Show my chat history"
"Help me with commands"
```

## ⚙️ Configuration

### Assistant Settings
- **Name & Wake Word**: Customize in Settings panel
- **Voice Type**: Male/Female with natural speech
- **Voice Speed**: Adjustable speech rate
- **File Search Depth**: Configure how deep to search folders

### File Aliases
Create shortcuts for frequently used folders:
```python
# Examples automatically created:
"downloads" → C:\Users\YourName\Downloads
"documents" → C:\Users\YourName\Documents
"workspace" → C:\Users\YourName\Projects
```

### Database Location
- **Windows**: `%USERPROFILE%\.ai_assistant\`
- **macOS**: `~/.ai_assistant/`
- **Linux**: `~/.ai_assistant/`

## 🔧 Development

### Project Structure
```
ai-assistant/
├── main.py                 # Application entry point
├── gui.py                  # Modern GUI interface
├── voice_handler.py        # Voice recognition & TTS
├── file_handler.py         # Smart file operations
├── command_processor.py    # Command parsing & execution
├── database.py            # SQLite database management
├── config.py              # Configuration management
├── first_time_setup.py    # Initial setup wizard
├── build_installer.py     # Build script for installer
├── requirements.txt       # Python dependencies
└── assets/                # Icons and resources
```

### Building Installer
```bash
# Install build dependencies
pip install pyinstaller

# Create Windows installer
python build_installer.py
```

### Adding New Commands
1. Add command logic to `command_processor.py`
2. Update help text in `show_help()` method
3. Test with both voice and text input

## 🔒 Privacy & Security

- **Offline-First**: Core functionality works without internet
- **Local Storage**: All data stored locally on your computer
- **Encrypted Passwords**: User passwords hashed with bcrypt
- **No Telemetry**: No data sent to external servers
- **Open Source**: Full source code available for review

## 🐛 Troubleshooting

### Voice Recognition Issues
- **Check Microphone**: Ensure microphone is connected and working
- **Permissions**: Grant microphone access to the application
- **Background Noise**: Use in quiet environment for better recognition
- **Fallback**: Use text input if voice doesn't work

### File Search Problems
- **Permissions**: Ensure application has file system access
- **Path Issues**: Check if drives/folders exist and are accessible
- **Search Depth**: Increase search depth in settings if files not found

### Installation Issues
- **Python Version**: Requires Python 3.8 or higher
- **Dependencies**: Run `pip install -r requirements.txt`
- **Windows Defender**: May flag executable, add to exclusions

## 📝 License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- **Speech Recognition**: Google Speech Recognition API
- **Text-to-Speech**: pyttsx3 library
- **GUI Framework**: CustomTkinter for modern interface
- **Voice Processing**: Whisper for offline speech recognition
- **Database**: SQLite for local data storage

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-assistant/discussions)
- **Email**: support@ai-assistant.com

---

**Made with ❤️ for productivity and automation**