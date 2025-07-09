# Athena AI Assistant 🎤🤖

A comprehensive AI voice assistant built with Python that can perform various tasks through voice commands.

## 🌟 Features

- 🔊 **Voice Recognition & Text-to-Speech**: Natural voice interaction
- 🌐 **Web Search**: Google search and Wikipedia integration
- 📰 **News Updates**: Latest news from various countries and categories
- 🌤️ **Weather Information**: Real-time weather data for any city
- 📧 **Email & Messaging**: Send emails and WhatsApp messages
- 🤖 **AI Chat**: Integration with OpenAI's GPT for conversations
- 🖼️ **Image Generation**: Create images using DALL-E
- 📸 **Screenshots**: Take and save screenshots
- 📋 **Task Management**: Remember and remind tasks
- 🎲 **Entertainment**: Jokes, coin flips, and more
- 💾 **Database Logging**: All activities logged to MySQL database

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- MySQL Server
- Microphone for voice input

### Quick Setup
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd athena-ai-assistant
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```

3. **Configure API keys in `config.py`**
   - OpenAI API key (for ChatGPT and DALL-E)
   - NewsAPI key (for news updates)
   - OpenWeatherMap API key (for weather)

4. **Set up email credentials in `secrets_1.py`**
   - Gmail address and app password

5. **Create database and tables**
   ```bash
   python database_setup.py
   ```

6. **Start Athena**
   ```bash
   python Athena.py
   ```

## 🎯 Usage

### Wake Word
Say **"Athena"** followed by your command.

### Available Commands

#### Basic Information
- **"Athena, what time is it?"** - Get current time
- **"Athena, what's the date?"** - Get current date

#### Search & Information
- **"Athena, search Wikipedia for [topic]"** - Search Wikipedia
- **"Athena, search for [query]"** - Google search
- **"Athena, news"** - Get latest news
- **"Athena, weather"** - Get weather information

#### Communication
- **"Athena, send email"** - Send an email
- **"Athena, send message"** - Send WhatsApp message

#### AI Features
- **"Athena, chat"** - Start conversation with GPT
- **"Athena, generate image of [description]"** - Create AI image

#### Utilities
- **"Athena, take screenshot"** - Capture screen
- **"Athena, read"** - Read clipboard content
- **"Athena, open [documents/music/pictures/videos]"** - Open folders

#### Task Management
- **"Athena, remember [task]"** - Save a task
- **"Athena, remind me"** - List saved tasks

#### Entertainment
- **"Athena, tell me a joke"** - Get a random joke
- **"Athena, flip a coin"** - Flip a virtual coin

#### Control
- **"Athena, quit"** or **"Athena, exit"** - Stop the assistant

## 🔧 Configuration

### API Keys Required
1. **OpenAI API Key**: For ChatGPT and DALL-E features
   - Get from: https://platform.openai.com/api-keys
   
2. **NewsAPI Key**: For news updates
   - Get from: https://newsapi.org/register
   
3. **OpenWeatherMap API Key**: For weather information
   - Get from: https://openweathermap.org/api

### Email Setup
For Gmail integration:
1. Enable 2-factor authentication
2. Generate an App Password (not your regular password)
3. Use the App Password in `secrets_1.py`

### Database Configuration
- Default: MySQL on localhost
- Database name: `athenadb`
- Modify `DB_CONFIG` in `config.py` if needed

## 📁 Project Structure

```
athena-ai-assistant/
├── Athena.py              # Main application
├── Athenavoice.py         # Text-to-speech module
├── config.py              # Configuration settings
├── secrets_1.py           # Email credentials
├── database_setup.py      # Database initialization
├── setup.py              # Installation script
├── requirements.txt       # Python dependencies
├── screenshots/          # Screenshot storage
└── README.md             # This file
```

## 🐛 Troubleshooting

### Common Issues

1. **"spaCy model not found"**
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **"NLTK data not found"**
   ```bash
   python -m nltk.downloader punkt
   ```

3. **"MySQL connection failed"**
   - Ensure MySQL server is running
   - Check credentials in `config.py`
   - Run `database_setup.py`

4. **"Microphone not working"**
   - Check microphone permissions
   - Install PyAudio: `pip install pyaudio`

5. **"Email sending failed"**
   - Use Gmail App Password, not regular password
   - Enable 2-factor authentication

## 🔒 Security Notes

- Never commit API keys or passwords to version control
- Use environment variables for sensitive data in production
- Keep your `secrets_1.py` file private

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Jeet Dodia**
- Email: jeetdodia12@gmail.com
- GitHub: [d3LTaJD](https://github.com/d3LTaJD)

## 🙏 Acknowledgments

- OpenAI for GPT and DALL-E APIs
- Google for Speech Recognition
- All the amazing Python libraries used in this project

---

**Note**: This is a prototype/educational project. Use responsibly and ensure you comply with all API terms of service.