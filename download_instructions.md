# 📥 Download Instructions for PC Athena

## Quick Download Guide

### 1. Download These Files to Your PC:

**Required Files:**
- `pc_athena.py` - Main application
- `install_pc.py` - Installation script  
- `requirements_pc.txt` - Dependencies list
- `README_PC.md` - Complete documentation

### 2. Setup Steps:

1. **Create a folder** on your PC (e.g., `C:\athena` or `~/athena`)

2. **Save all files** in that folder

3. **Open terminal/command prompt** in that folder

4. **Run the installer**:
   ```bash
   python install_pc.py
   ```

5. **Start Athena**:
   ```bash
   python pc_athena.py
   ```

### 3. If Installation Script Doesn't Work:

**Manual Installation:**
```bash
# Install dependencies
pip install pyttsx3==2.90
pip install SpeechRecognition==3.10.0
pip install requests==2.31.0
pip install pyautogui==0.9.54
pip install Pillow==10.1.0

# For Windows (PyAudio):
pip install pipwin
pipwin install pyaudio

# For macOS (PyAudio):
brew install portaudio
pip install pyaudio

# For Linux (PyAudio):
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

### 4. First Run:

```bash
python pc_athena.py
```

Then try:
- `athena help` - See all commands
- `athena time` - Get current time
- `athena joke` - Tell a joke

## 🎯 What You'll Get:

✅ **Full voice recognition** (speak your commands)  
✅ **Text-to-speech responses** (Athena talks back)  
✅ **Complete math calculator** with conversions  
✅ **Notes and reminders** that save automatically  
✅ **Screenshot capability**  
✅ **Entertainment features** (jokes, dice, facts)  
✅ **Password generator**  
✅ **System information**  
✅ **Works offline** (no internet required for core features)  

## 🔧 Troubleshooting:

**If voice doesn't work**: That's OK! You can type all commands  
**If installation fails**: Try the manual installation steps above  
**If you get errors**: Check that you have Python 3.8+ installed  

## 💡 Pro Tips:

- Voice features are optional - everything works with text input
- Your data is saved automatically in the `athena_data` folder
- Screenshots are saved in `athena_data/screenshots`
- Use `athena toggle voice` to enable/disable voice input
- Use `athena toggle speech` to enable/disable voice responses

**Ready to download and run on your PC!** 🚀