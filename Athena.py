"""
Athena AI Assistant - Main Application
Fixed version with proper error handling and imports
"""

import random
import string
import smtplib  # Fixed typo from smtplibs
import datetime
import speech_recognition as sr
from secrets_1 import senderemail, epwd, to 
from email.message import EmailMessage
import pyautogui
import webbrowser as wb 
from time import sleep
import wikipedia
import pywhatkit as kit
import requests
from newsapi import NewsApiClient
import clipboard
import os
import pyjokes
import spacy
from Athenavoice import speak
import openai
import mysql.connector
from config import OPENAI_API_KEY, NEWS_API_KEY, WEATHER_API_KEY, DB_CONFIG, SCREENSHOT_FOLDER

# Global database connection variables
mydb = None
mycursor = None

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

def chat_with_gpt(user_input):
    """Handles chat interaction using OpenAI's latest API format."""
    if not OPENAI_API_KEY:
        speak("OpenAI API key is not configured. Please add your API key to config.py")
        return
        
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "You are Athena, a helpful AI assistant."},
                {"role": "user", "content": user_input}
            ]
        )

        reply = response["choices"][0]["message"]["content"]
        print(f"🤖 GPT Response: {reply}")
        speak(reply)  
        return reply

    except Exception as e:  
        print(f"❌ ChatGPT Error: {e}")
        speak("Sorry, I encountered an error while processing your request.")

def generate_image(prompt):
    """Generates an image using OpenAI's DALL·E API."""
    if not OPENAI_API_KEY:
        speak("OpenAI API key is not configured. Please add your API key to config.py")
        return
        
    try:
        response = openai.Image.create(
            model="dall-e-2",  
            prompt=prompt,
            n=1,  
            size="1024x1024" 
        )

        image_url = response["data"][0]["url"]
        print(f"🖼️ Image Generated: {image_url}")
        speak(f"Image generated successfully. You can find it at {image_url}")
        return image_url  

    except Exception as e:
        print(f"❌ Image Generation Error: {e}")
        speak("Sorry, I couldn't generate the image.")

def connect_to_mysql():
    """Establishes MySQL database connection with error handling and auto-reconnect."""
    global mydb, mycursor
    try:
        mydb = mysql.connector.connect(**DB_CONFIG, autocommit=True)
        mycursor = mydb.cursor()
        print("✅ Connected to MySQL successfully!")
        return True
    except mysql.connector.Error as err:
        print(f"❌ MySQL Connection Error: {err}")
        print("Please run database_setup.py first to create the database and tables.")
        mydb = None
        mycursor = None
        return False

def ensure_db_connection():
    """Ensures database connection is active"""
    global mydb, mycursor
    if mydb is None or not mydb.is_connected():
        return connect_to_mysql()
    return True

# Load spaCy model with error handling
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("❌ spaCy model 'en_core_web_sm' not found. Please run: python -m spacy download en_core_web_sm")
    nlp = None

def takeCommandMIC():
    """Takes voice input from microphone"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1
        audio = r.listen(source, timeout=5, phrase_time_limit=10)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query.lower()
        except sr.UnknownValueError:
            print("Could not understand audio")
            speak("I didn't catch that. Could you please repeat?")
            return None
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")
            speak("There's an issue with the speech recognition service.")
            return None
        except Exception as e:
            print(f"Error: {str(e)}")
            speak("Say that again please...")
            return None

def process_query(query):
    """Tokenize query using spaCy"""
    if nlp is None:
        return query.lower().split()  # Fallback to simple split
    
    doc = nlp(query.lower())  
    return [token.text for token in doc if not token.is_punct]

def time():
    """Gets current time and logs to database"""
    try:
        current_time = datetime.datetime.now()
        hour = current_time.strftime("%I")
        minute = current_time.strftime("%M")
        period = current_time.strftime("%p")
        
        time_str = f"The current time is {hour}:{minute} {period}"
        speak(time_str)
        print(time_str)

        if ensure_db_connection():
            formatted_time = current_time.strftime("%I:%M %p")
            timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
            
            sql = "INSERT INTO time_logs (current_time, timestamp) VALUES (%s, %s)"
            val = (formatted_time, timestamp)
            mycursor.execute(sql, val)
            print("✅ Time logged successfully!")

    except Exception as err:
        print(f"❌ Error in time function: {err}")

def date():
    """Gets current date and logs to database"""
    try:
        current_date = datetime.datetime.now()
        year = current_date.year
        month = current_date.strftime("%B")
        day = current_date.day
        
        date_str = f"Today is {month} {day}, {year}"
        speak(date_str)
        print(date_str)

        if ensure_db_connection():
            log_date = current_date.strftime("%Y-%m-%d")
            timestamp = current_date.strftime("%Y-%m-%d %H:%M:%S")
            
            sql = "INSERT INTO date_logs (log_date, timestamp) VALUES (%s, %s)"
            val = (log_date, timestamp)
            mycursor.execute(sql, val)
            print("✅ Date logged successfully!")

    except Exception as err:
        print(f"❌ Error in date function: {err}")

def greeting():
    """Provides time-appropriate greeting"""
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak("Good Morning Sir!")
    elif 12 <= hour < 18:
        speak("Good Afternoon Sir!")
    elif 18 <= hour < 24:
        speak("Good Evening Sir!")
    else:
        speak("Good Night Sir!")

def wishme():
    """Initial greeting when starting Athena"""
    speak("Welcome back Sir!")
    greeting()
    speak("Athena at your service. Please tell me how can I help you?")

def search_wikipedia():
    """Searches Wikipedia and logs results"""
    speak("What topic would you like to search on Wikipedia?")
    topic = takeCommandMIC()
    
    if not topic:
        return
        
    try:
        summary = wikipedia.summary(topic, sentences=2)
        speak(f"According to Wikipedia: {summary}")
        print(f"Wikipedia Result: {summary}")
        
        if ensure_db_connection():
            sql = "INSERT INTO searches (query, result) VALUES (%s, %s)"
            val = (topic, summary)
            mycursor.execute(sql, val)
            print("✅ Wikipedia search logged successfully!")
            
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:3]  # Show first 3 options
        speak(f"The search term '{topic}' has multiple meanings. Here are some options: {', '.join(options)}")
    except wikipedia.exceptions.PageError:
        speak("Sorry, I couldn't find a Wikipedia page for that topic.")
    except Exception as e:
        print(f"❌ Wikipedia search error: {e}")
        speak("Sorry, there was an error searching Wikipedia.")

def sendEmail(receiver, subject, content):
    """Sends email and logs to database"""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(senderemail, epwd)
        
        email = EmailMessage()
        email['From'] = senderemail
        email['To'] = receiver
        email['Subject'] = subject
        email.set_content(content)
        
        server.send_message(email)
        server.close()

        if ensure_db_connection():
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = "INSERT INTO emails (receiver, subject, content, timestamp) VALUES (%s, %s, %s, %s)"
            val = (receiver, subject, content, timestamp)
            mycursor.execute(sql, val)
            print("✅ Email logged successfully!")

        speak("Email has been sent successfully.")

    except Exception as e:
        print(f"❌ Error sending email: {e}")
        speak("Sorry, I couldn't send the email. Please check your email configuration.")

def sendwhatsmsg(phone_no, message):
    """Sends WhatsApp message and logs to database"""
    try:
        wb.open(f'https://web.whatsapp.com/send?phone={phone_no}&text={message}')
        sleep(10)
        pyautogui.press('enter')

        if ensure_db_connection():
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = "INSERT INTO whatsapp_messages (phone_no, message, timestamp) VALUES (%s, %s, %s)"
            val = (phone_no, message, timestamp)
            mycursor.execute(sql, val)
            print("✅ WhatsApp message logged successfully!")
            
    except Exception as e:
        print(f"❌ Error sending WhatsApp message: {e}")
        speak("Sorry, I couldn't send the WhatsApp message.")

def searchgoogle():
    """Searches Google and logs query"""
    speak('What should I search for?')
    search = takeCommandMIC()
    
    if not search:
        return

    try:
        wb.open(f'https://www.google.com/search?q={search}')
        speak(f"Here are the search results for {search}")
        
        if ensure_db_connection():
            sql = "INSERT INTO searches (query) VALUES (%s)"
            val = (search,)
            mycursor.execute(sql, val)
            print("✅ Search logged successfully!")
            
    except Exception as e:
        print(f"❌ Error in Google search: {e}")

def news():
    """Fetches and reads news with improved error handling"""
    if not NEWS_API_KEY:
        speak("News API key is not configured. Please add your API key to config.py")
        return
        
    speak("Which country's news would you like to hear?")
    country_name = takeCommandMIC()
    
    if not country_name:
        return

    country_codes = {
        'united states': 'us', 'usa': 'us', 'america': 'us',
        'india': 'in', 'united kingdom': 'gb', 'uk': 'gb', 'britain': 'gb',
        'canada': 'ca', 'australia': 'au', 'germany': 'de', 'france': 'fr'
    }

    country_code = country_codes.get(country_name.lower())
    if not country_code:
        speak(f"Sorry, I don't have news coverage for {country_name}. Please try another country.")
        return

    try:
        newsapi = NewsApiClient(NEWS_API_KEY)
        data = newsapi.get_top_headlines(country=country_code, language="en")
        articles = data.get("articles", [])

        if not articles:
            speak(f"Sorry, no news articles are available for {country_name} right now.")
            return

        speak(f"Here are the top news headlines from {country_name}.")
        
        for i, article in enumerate(articles[:3]):
            title = article["title"]
            description = article.get("description", "No description available.")
            speak(f"News {i+1}: {title}. {description}")
            print(f"{i+1}. {title}")
            
            if ensure_db_connection():
                sql = "INSERT INTO news (title, description, country) VALUES (%s, %s, %s)"
                val = (title, description, country_name)
                mycursor.execute(sql, val)

        print("✅ News logged successfully!")

    except Exception as e:
        print(f"❌ Error fetching news: {e}")
        speak("Sorry, I couldn't fetch the news right now.")

def weather():
    """Fetches weather information and logs to database"""
    speak("Which city's weather would you like to know?")
    city_name = takeCommandMIC()
    
    if not city_name:
        return

    try:
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}q={city_name}&units=metric&appid={WEATHER_API_KEY}"
        
        response = requests.get(complete_url)
        weather_data = response.json()

        if weather_data["cod"] == 200:
            main = weather_data.get("main", {})
            weather_desc = weather_data.get("weather", [{}])[0].get("description", "No description")
            temperature = main.get("temp", "N/A")
            humidity = main.get("humidity", "N/A")

            weather_info = f"The temperature in {city_name} is {temperature} degrees Celsius, with {humidity} percent humidity. The weather condition is {weather_desc}."
            speak(weather_info)
            print(weather_info)

            if ensure_db_connection():
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sql = "INSERT INTO weather (city, temperature, humidity, description, timestamp) VALUES (%s, %s, %s, %s, %s)"
                val = (city_name, temperature, humidity, weather_desc, timestamp)
                mycursor.execute(sql, val)
                print("✅ Weather data logged successfully!")

        else:
            error_message = weather_data.get("message", "Unknown error")
            speak(f"Sorry, I couldn't get weather information for {city_name}. {error_message}")

    except Exception as e:
        print(f"❌ Error in weather function: {e}")
        speak("Sorry, there was an error getting the weather information.")

def text2speech():
    """Reads clipboard content and logs to database"""
    try:
        text = clipboard.paste()
        if text and text.strip():
            speak(f"Reading from clipboard: {text}")
            
            if ensure_db_connection():
                sql = "INSERT INTO clipboard_data (copied_text) VALUES (%s)"
                val = (text,)
                mycursor.execute(sql, val)
                print("✅ Clipboard text logged successfully!")
        else:
            speak("The clipboard is empty. Please copy some text first.")
            
    except Exception as e:
        print(f"❌ Error in text2speech: {e}")
        speak("Sorry, I couldn't read from the clipboard.")

def openResource(query):
    """Opens system resources and logs actions"""
    try:
        query_words = query.lower().split()
        
        resource_paths = {
            'documents': os.path.join(os.environ['USERPROFILE'], 'Documents'),
            'music': os.path.join(os.environ['USERPROFILE'], 'Music'),
            'pictures': os.path.join(os.environ['USERPROFILE'], 'Pictures'),
            'videos': os.path.join(os.environ['USERPROFILE'], 'Videos'),
            'downloads': os.path.join(os.environ['USERPROFILE'], 'Downloads'),
            'desktop': os.path.join(os.environ['USERPROFILE'], 'Desktop')
        }

        for resource in resource_paths.keys():
            if resource in query_words:
                resource_path = resource_paths[resource]
                
                if os.path.exists(resource_path):
                    os.startfile(resource_path)
                    speak(f"Opening {resource}")
                    
                    if ensure_db_connection():
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        sql = "INSERT INTO resource_actions (resource_type, timestamp) VALUES (%s, %s)"
                        val = (resource, timestamp)
                        mycursor.execute(sql, val)
                        print(f"✅ Resource action logged: {resource}")
                else:
                    speak(f"Sorry, I couldn't find the {resource} folder.")
                return

        speak("I couldn't identify the resource you want to open.")
        
    except Exception as e:
        print(f"❌ Error in openResource: {e}")
        speak("Sorry, I couldn't open the requested resource.")

def screenshot():
    """Takes screenshot and logs to database"""
    try:
        # Create screenshots folder if it doesn't exist
        if not os.path.exists(SCREENSHOT_FOLDER):
            os.makedirs(SCREENSHOT_FOLDER)
            
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filepath = os.path.join(SCREENSHOT_FOLDER, f"screenshot_{timestamp}.png")
        
        img = pyautogui.screenshot()
        img.save(filepath)

        speak("Screenshot taken and saved.")
        print(f"✅ Screenshot saved at: {filepath}")
        
        if ensure_db_connection():
            sql = "INSERT INTO screenshots (filepath, timestamp) VALUES (%s, %s)"
            val = (filepath, timestamp)
            mycursor.execute(sql, val)
            print("✅ Screenshot logged successfully!")

    except Exception as e:
        print(f"❌ Error taking screenshot: {e}")
        speak("Sorry, I couldn't take the screenshot.")

def remember_task(task):
    """Stores task in database"""
    if ensure_db_connection():
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = "INSERT INTO tasks (task, timestamp) VALUES (%s, %s)"
            val = (task, timestamp)
            mycursor.execute(sql, val)
            speak(f"I have remembered: {task}")
            print(f"✅ Task remembered: {task}")
        except Exception as err:
            print(f"❌ Error remembering task: {err}")
            speak("Sorry, I couldn't remember that task.")

def remind_tasks():
    """Retrieves and speaks remembered tasks"""
    if ensure_db_connection():
        try:
            sql = "SELECT task, timestamp FROM tasks ORDER BY timestamp DESC LIMIT 5"
            mycursor.execute(sql)
            tasks = mycursor.fetchall()

            if tasks:
                speak("Here are your recent tasks:")
                for task, timestamp in tasks:
                    speak(f"{task}")
                    print(f"📌 {task} - {timestamp}")
            else:
                speak("You have no remembered tasks.")
        except Exception as err:
            print(f"❌ Error retrieving tasks: {err}")
            speak("Sorry, I couldn't retrieve your tasks.")

def tell_a_joke():
    """Tells a joke and logs to database"""
    try:
        joke = pyjokes.get_joke()
        speak(joke)
        print(f"😂 {joke}")

        if ensure_db_connection():
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = "INSERT INTO jokes (joke, timestamp) VALUES (%s, %s)"
            val = (joke, timestamp)
            mycursor.execute(sql, val)
            print("✅ Joke logged successfully!")
            
    except Exception as e:
        print(f"❌ Error telling joke: {e}")
        speak("Sorry, I couldn't think of a joke right now.")

def flip_coin():
    """Flips a coin and logs result"""
    try:
        result = random.choice(["Heads", "Tails"])
        speak(f"The coin landed on {result}.")
        print(f"🪙 Coin flip result: {result}")

        if ensure_db_connection():
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = "INSERT INTO coin_flips (result, timestamp) VALUES (%s, %s)"
            val = (result, timestamp)
            mycursor.execute(sql, val)
            print("✅ Coin flip logged successfully!")
            
    except Exception as e:
        print(f"❌ Error flipping coin: {e}")
        speak("Sorry, I couldn't flip the coin.")

def main():
    """Main function to run Athena"""
    print("🤖 Starting Athena AI Assistant...")
    
    # Initialize database connection
    if not connect_to_mysql():
        print("❌ Database connection failed. Some features may not work properly.")
        speak("Warning: Database connection failed. Some features may not work properly.")
    
    wishme()
    wakeword = "athena"

    while True:
        try:
            query = takeCommandMIC()
            if not query:
                continue
                
            query_tokens = process_query(query)
            print(f"Processed tokens: {query_tokens}")

            if wakeword in query_tokens:
                if 'time' in query_tokens:
                    time()
                    
                elif 'date' in query_tokens:
                    date()
                    
                elif 'email' in query_tokens:
                    email_list = {'jeet': 'jeetdodia34@gmail.com'}
                    try:
                        speak("To whom do you want to send the email?")
                        name = takeCommandMIC()
                        if name and name in email_list:
                            receiver = email_list[name]
                            speak("What is the subject?")
                            subject = takeCommandMIC()
                            speak("What should I say?")
                            content = takeCommandMIC()
                            if subject and content:
                                sendEmail(receiver, subject, content)
                        else:
                            speak("I couldn't find that contact.")
                    except Exception as e:
                        print(f"❌ Email error: {e}")
                        speak("Sorry, I couldn't send the email.")

                elif 'message' in query_tokens:
                    user_contacts = {'test': '+1234567890'}
                    try:
                        speak("To whom do you want to send the WhatsApp message?")
                        name = takeCommandMIC()
                        if name and name in user_contacts:
                            phone_no = user_contacts[name]
                            speak("What is the message?")
                            message = takeCommandMIC()
                            if message:
                                sendwhatsmsg(phone_no, message)
                        else:
                            speak("I couldn't find that contact.")
                    except Exception as e:
                        print(f"❌ WhatsApp error: {e}")
                        speak("Sorry, I couldn't send the message.")

                elif "search" in query_tokens and "wikipedia" in query_tokens:
                    search_wikipedia()

                elif "search" in query_tokens:
                    searchgoogle()

                elif "news" in query_tokens:
                    news()

                elif "weather" in query_tokens:
                    weather()

                elif "read" in query_tokens:
                    text2speech()

                elif "open" in query_tokens:
                    openResource(query)

                elif "joke" in query_tokens:
                    tell_a_joke()

                elif "screenshot" in query_tokens:
                    screenshot()

                elif "remember" in query_tokens:
                    speak("What would you like me to remember?")
                    task = takeCommandMIC()
                    if task:
                        remember_task(task)

                elif "remind" in query_tokens or "tasks" in query_tokens:
                    remind_tasks()

                elif "flip" in query_tokens and "coin" in query_tokens:
                    flip_coin()
                    
                elif "chat" in query_tokens or "talk" in query_tokens:
                    speak("What would you like to talk about?")
                    user_input = takeCommandMIC()
                    if user_input:
                        chat_with_gpt(user_input)
                
                elif "generate" in query_tokens and "image" in query_tokens:
                    # Extract prompt after "generate image of"
                    prompt_start = query.find("generate image of")
                    if prompt_start != -1:
                        image_prompt = query[prompt_start + len("generate image of"):].strip()
                        if image_prompt:
                            generate_image(image_prompt)
                        else:
                            speak("Please specify what image you want me to generate.")

                elif "quit" in query_tokens or "exit" in query_tokens or "goodbye" in query_tokens:
                    speak("Goodbye! Have a great day!")
                    break

                elif "offline" in query_tokens:
                    speak("Going offline. Goodbye!")
                    break
                    
                else:
                    speak("I didn't understand that command. Please try again.")
                    
        except KeyboardInterrupt:
            speak("Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            speak("Sorry, something went wrong. Please try again.")

    # Close database connection
    if mydb and mydb.is_connected():
        mycursor.close()
        mydb.close()
        print("✅ Database connection closed.")

if __name__ == "__main__":
    main()