from asyncio import tasks
import random
import string
import smtplibs
from urllib import response
from click import command
from pyscreeze import screenshot
import pyttsx3
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
from nltk.tokenize import word_tokenize
from Athenavoice import speak
import openai
import serial  
import pyaudio
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import mysql.connector


API_KEY = ""


openai.api_key = ""  # Replace with your actual API key

def chat_with_gpt(user_input):
    """Handles chat interaction using OpenAI's latest API format."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": user_input}]
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
    try:
        response = openai.Image.create(
            model="dall-e-2",  
            prompt=prompt,
            n=1,  
            size="1024x1024" 
        )

        image_url = response["data"][0]["url"]
        print(f"🖼️ Image Generated: {image_url}")
        return image_url  

    except Exception as e:
        print(f"❌ Image Generation Error: {e}")

def connect_to_mysql():
    
    """Establishes MySQL database connection with error handling and auto-reconnect."""
    global mydb, mycursor
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="athenadb",
            autocommit=True 
        )
        mycursor = mydb.cursor()
        print("✅ Connected to MySQL successfully!")
    except mysql.connector.Error as err:
        print(f"❌ MySQL Connection Error: {err}")
        mydb = None  


connect_to_mysql()
    
#openai.api_key = ""
#openai.api_key = ""

# engine = pyttsx3.init()
# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# def getvoice(voice):
#     current_voice = engine.getProperty('voice')
#     if voice == 1:
#         engine.setProperty('voice', zira_voice_id)
#         speak("hello this is Athena")

#openai.api_key = ""



nlp = spacy.load("en_core_web_sm")

def takeCommandMIC():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print(f"Error: {str(e)}")
            speak("Say that again please...")
            return None
    return query.lower()


def process_query(query):
    """Tokenize query using spaCy"""
    doc = nlp(query.lower())  
    return [token.text for token in doc if not token.is_punct]  

   

def handle_email():
    
    email_list = {
        'email': 'jeetdodia34@gmail.com'
    }
    try:
        speak("To whom do you want to send the email?")
        name = takeCommandMIC()
        receiver = email_list.get(name, 'default_receiver@example.com') 
        speak("What is the subject of the mail?")
        subject = takeCommandMIC()
        speak("What should I say?")
        content = takeCommandMIC()
        sendEmail(receiver, subject, content)
        speak("Email has been sent.")
    except Exception as e:
        print(e)
        speak("Unable to send the email.")    

def time():
    try:
        hour = str(datetime.datetime.now().hour)
        minute = str(datetime.datetime.now().minute)
        
        speak("The current time is:")
        speak(hour)
        speak(minute)

        current_time = datetime.datetime.now().strftime("%I:%M %p")  
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        
        sql = "INSERT INTO time_logs (current_time, timestamp) VALUES (%s, %s)"
        val = (current_time, timestamp)

        mycursor.execute(sql, val)
        mydb.commit()
        print("✅ Time logged successfully!")

    except mysql.connector.Error as err:
        print(f"❌ Error logging time to MySQL: {err}")


def date():
    try:
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().month)
        day = str(datetime.datetime.now().day)

        full_date = f"The current date is {day} {month} {year}."
        
        speak(full_date)  

        log_date = datetime.datetime.now().strftime("%Y-%m-%d") 
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        
        sql = "INSERT INTO date_logs (log_date, timestamp) VALUES (%s, %s)"
        val = (log_date, timestamp)

        mycursor.execute(sql, val)
        mydb.commit()
        print("✅ Date logged successfully!")

    except mysql.connector.Error as err:
        print(f"❌ Error logging date to MySQL: {err}")


def greeting():
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
    speak("Welcome back Sir!")
    greeting()
    speak("Athena at your service. Please tell me how can I help you?")

def takeCommandCMD():
    query = input("Please tell me how can I help you?\n")
    return query

def takeCommandMIC():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print(f"Error: {str(e)}")
            speak("Say that again please...")
            return "None"
        return query

def search_wikipedia():
    speak("What topic would you like to search on Wikipedia?")
    topic = takeCommandMIC()
    try:
        summary = wikipedia.summary(topic, sentences=2)
        speak(summary)
        sql = "INSERT INTO searches (query, result) VALUES (%s, %s)"
        val = (topic, summary)
        mycursor.execute(sql, val)
        mydb.commit()
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options
        speak(f"The search term '{topic}' is ambiguous. Please specify. Options: {', '.join(options)}")
    except wikipedia.exceptions.PageError:
        speak("Sorry, the page does not exist.")
    
def sendEmail(receiver, subject, content):
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

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO emails (receiver, subject, content, timestamp) VALUES (%s, %s, %s, %s)"
        val = (receiver, subject, content, timestamp)
        mycursor.execute(sql, val)
        mydb.commit()

        speak("Email has been sent.")
        print("✅ Email logged successfully!")

    except Exception as e:
        print(f"❌ Error sending email: {e}")
        speak("Sorry, I am not able to send this email at the moment.")
        
def sendwhatsmsg(phone_no, message):
    try:
        wb.open(f'https://web.whatsapp.com/send?phone={phone_no}&text={message}')
        sleep(10)
        pyautogui.press('enter')

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO whatsapp_messages (phone_no, message, timestamp) VALUES (%s, %s, %s)"
        val = (phone_no, message, timestamp)
        mycursor.execute(sql, val)
        mydb.commit()

        print("✅ WhatsApp message logged successfully!")
    except Exception as e:
        print(f"❌ Error sending WhatsApp message: {e}")




def searchgoogle():
    speak('What should I search for?')
    search = takeCommandMIC()

    try:
        wb.open(f'https://www.google.com/search?q={search}')
        sql = "INSERT INTO searches (query) VALUES (%s)"
        val = (search,)
        mycursor.execute(sql, val)
        mydb.commit()

        print("✅ Search logged successfully!")
    except Exception as e:
        print(f"❌ Error logging search: {e}")

    
def get_country_code(country_name):
    """Maps country names to ISO country codes for NewsAPI."""
    country_mapping = {
    'united states': 'us', 'india': 'in', 'united kingdom': 'gb', 'canada': 'ca',
    'australia': 'au', 'germany': 'de', 'france': 'fr', 'italy': 'it', 'spain': 'es',
    'russia': 'ru', 'china': 'cn', 'japan': 'jp', 'brazil': 'br', 'south africa': 'za',
    'mexico': 'mx', 'argentina': 'ar', 'netherlands': 'nl', 'sweden': 'se', 'switzerland': 'ch',
    'norway': 'no', 'denmark': 'dk', 'south korea': 'kr', 'new zealand': 'nz', 'singapore': 'sg',
    'turkey': 'tr', 'saudi arabia': 'sa', 'united arab emirates': 'ae', 'egypt': 'eg', 'indonesia': 'id',
    'thailand': 'th', 'philippines': 'ph', 'malaysia': 'my', 'pakistan': 'pk', 'bangladesh': 'bd',
    'vietnam': 'vn', 'hong kong': 'hk', 'taiwan': 'tw', 'israel': 'il', 'greece': 'gr',
    'portugal': 'pt', 'belgium': 'be', 'finland': 'fi', 'poland': 'pl', 'austria': 'at',
    'romania': 'ro', 'czech republic': 'cz', 'hungary': 'hu', 'ukraine': 'ua', 'chile': 'cl',
    'colombia': 'co', 'peru': 'pe', 'venezuela': 've', 'ecuador': 'ec', 'uruguay': 'uy',
    'paraguay': 'py', 'bolivia': 'bo', 'costa rica': 'cr', 'panama': 'pa', 'dominican republic': 'do',
    'cuba': 'cu', 'jamaica': 'jm', 'haiti': 'ht', 'nigeria': 'ng', 'kenya': 'ke',
    'ghana': 'gh', 'ethiopia': 'et', 'uganda': 'ug', 'tanzania': 'tz', 'zimbabwe': 'zw',
    'morocco': 'ma', 'algeria': 'dz', 'tunisia': 'tn', 'iraq': 'iq', 'iran': 'ir',
    'lebanon': 'lb', 'qatar': 'qa', 'kuwait': 'kw', 'oman': 'om', 'sri lanka': 'lk',
    'kazakhstan': 'kz', 'uzbekistan': 'uz', 'turkmenistan': 'tm', 'afghanistan': 'af', 'azerbaijan': 'az',
    'georgia': 'ge', 'armenia': 'am', 'mongolia': 'mn'
}
    return country_mapping.get(country_name.lower(), None)


def news():
    speak("Which country's news would you like to hear?")
    country_name = takeCommandMIC().lower()

    country_codes = {
    'united states': 'us', 'india': 'in', 'united kingdom': 'gb', 'canada': 'ca',
    'australia': 'au', 'germany': 'de', 'france': 'fr', 'italy': 'it', 'spain': 'es',
    'russia': 'ru', 'china': 'cn', 'japan': 'jp', 'brazil': 'br', 'south africa': 'za',
    'mexico': 'mx', 'argentina': 'ar', 'netherlands': 'nl', 'sweden': 'se', 'switzerland': 'ch',
    'norway': 'no', 'denmark': 'dk', 'south korea': 'kr', 'new zealand': 'nz', 'singapore': 'sg',
    'turkey': 'tr', 'saudi arabia': 'sa', 'united arab emirates': 'ae', 'egypt': 'eg', 'indonesia': 'id',
    'thailand': 'th', 'philippines': 'ph', 'malaysia': 'my', 'pakistan': 'pk', 'bangladesh': 'bd',
    'vietnam': 'vn', 'hong kong': 'hk', 'taiwan': 'tw', 'israel': 'il', 'greece': 'gr',
    'portugal': 'pt', 'belgium': 'be', 'finland': 'fi', 'poland': 'pl', 'austria': 'at',
    'romania': 'ro', 'czech republic': 'cz', 'hungary': 'hu', 'ukraine': 'ua', 'chile': 'cl',
    'colombia': 'co', 'peru': 'pe', 'venezuela': 've', 'ecuador': 'ec', 'uruguay': 'uy',
    'paraguay': 'py', 'bolivia': 'bo', 'costa rica': 'cr', 'panama': 'pa', 'dominican republic': 'do',
    'cuba': 'cu', 'jamaica': 'jm', 'haiti': 'ht', 'nigeria': 'ng', 'kenya': 'ke',
    'ghana': 'gh', 'ethiopia': 'et', 'uganda': 'ug', 'tanzania': 'tz', 'zimbabwe': 'zw',
    'morocco': 'ma', 'algeria': 'dz', 'tunisia': 'tn', 'iraq': 'iq', 'iran': 'ir',
    'lebanon': 'lb', 'qatar': 'qa', 'kuwait': 'kw', 'oman': 'om', 'sri lanka': 'lk',
    'kazakhstan': 'kz', 'uzbekistan': 'uz', 'turkmenistan': 'tm', 'afghanistan': 'af', 'azerbaijan': 'az',
    'georgia': 'ge', 'armenia': 'am', 'mongolia': 'mn'
}


    country_code = country_codes.get(country_name)

    if not country_code:
        speak(f"Sorry, I couldn't find the news for {country_name}. Please try again.")
        return

    speak("What type of news are you interested in? For example, stock, politics, technology, sports, or general news.")
    news_type = takeCommandMIC().lower()

    category_mapping = {
    "politics": "politics",
    "business": "business",
    "finance": "business",
    "stock market": "business",
    "sports": "sports",
    "entertainment": "entertainment",
    "movies": "entertainment",
    "celebrities": "entertainment",
    "music": "entertainment",
    "health": "health",
    "technology": "technology",
    "science": "science",
    "education": "education",
    "environment": "environment",
    "climate change": "environment",
    "crime": "crime",
    "cybersecurity": "technology",
    "gaming": "technology",
    "real estate": "business",
    "travel": "travel",
    "food": "food",
    "fashion": "fashion",
    "culture": "culture",
    "religion": "religion",
    "international": "world",
    "war": "world",
    "space": "science"
}


    category = category_mapping.get(news_type, 'general')  

    
    newsapi = NewsApiClient(API_KEY)

    try:
        data = newsapi.get_top_headlines(category=category, country=country_code, language="en")
        articles = data.get("articles", [])

        if not articles:
            speak(f"Sorry, there are no {news_type} news articles available for {country_name}.")
            return

        speak(f"Here are the top {news_type} news headlines in {country_name}.")
        print(f"\n🔹 {news_type.capitalize()} News from {country_name}:")

        news_options = []
        for i, article in enumerate(articles[:3]): 
            title = article["title"]
            summary = article["description"][:100] + "..." if article["description"] else "No description available."
            print(f"{i+1}. {title} - {summary}")
            speak(f"Number {i+1}, {title}. {summary}")
            news_options.append((title, article))

       
        while True:
            speak("Would you like more details about any of these news articles? Say the number or 'no' to go back.")
            choice = takeCommandMIC().lower()

            if choice in ["no", "back"]:
                speak("Okay, going back to the news selection.")
                return 

            try:
                choice = int(choice) - 1
                if 0 <= choice < len(news_options):
                    selected_title, selected_article = news_options[choice]

                    full_description = selected_article["description"] if selected_article["description"] else "No detailed description available."
                    full_content = selected_article["content"] if selected_article["content"] else "No additional content available."

                    
                    speak(f"Here are the details for {selected_title}. {full_description} {full_content}")
                    print(f"\n📌 Full News for {selected_title}: \n{full_description}\n{full_content}\n")

                
                    sql = "INSERT INTO news (title, description, content, category, country) VALUES (%s, %s, %s, %s, %s)"
                    val = (selected_title, full_description, full_content, category, country_name)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    print("✅ Selected news logged successfully!")

                    speak("Would you like to hear about another news article from this category?")
                    next_choice = takeCommandMIC().lower()
                    if next_choice in ["no", "back"]:
                        speak("Okay, going back to the news selection.")
                        return  

                else:
                    speak("Invalid selection. Please say a number between 1 and 3.")
            except ValueError:
                speak("Invalid response. Please try again.")

    except Exception as e:
        print(f"❌ Error fetching news: {e}")
        speak("Sorry, there was an error retrieving news.")

def weather():
    """Fetches and logs weather information into MySQL."""
    try:
        speak("Which city's weather information would you like to know?")
        city_name = takeCommandMIC().lower()

        
        api_key = "21c9fe0d0b585bed0a16677ee079de8b"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}q={city_name}&units=metric&appid={api_key}"
        
        response = requests.get(complete_url)
        weather_data = response.json()

        print(f"🔍 API Response: {weather_data}") 

        if weather_data["cod"] == 200:  
            main = weather_data.get("main", {})
            weather_desc = weather_data.get("weather", [{}])[0].get("description", "No description")
            temperature = main.get("temp", "N/A")
            humidity = main.get("humidity", "N/A")

    
            speak(f"The temperature in {city_name} is {temperature} degrees Celsius, "
                  f"with a humidity of {humidity} percent, and the weather condition is {weather_desc}.")

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = "INSERT INTO weather (city, temperature, humidity, description, timestamp) VALUES (%s, %s, %s, %s, %s)"
            val = (city_name, temperature, humidity, weather_desc, timestamp)

            mycursor.execute(sql, val)
            mydb.commit()
            print(f"✅ Weather data for '{city_name}' logged successfully!")

        else:  
            error_message = weather_data.get("message", "Unknown error")
            speak(f"Sorry, I couldn't fetch the weather details. {error_message}. Please try again.")
            print(f"❌ Error fetching weather for '{city_name}': {error_message}")

    except mysql.connector.Error as err:
        print(f"❌ MySQL Error logging weather: {err}")

    except Exception as e:
        print(f"❌ General Error in weather function: {e}")


                
def text2speech():
    try:
        text = clipboard.paste()  
        if text:
            speak(f"Reading from clipboard: {text}")
            
           
            sql = "INSERT INTO clipboard_data (copied_text) VALUES (%s)"
            val = (text,)
            mycursor.execute(sql, val)
            mydb.commit()

            print("✅ Clipboard text logged and spoken successfully!")
        else:
            speak("The clipboard is empty! Please copy some text first.")
            print("❌ Clipboard is empty!")
    except mysql.connector.Error as err:
        print(f"❌ Error logging clipboard data: {err}")




        
def openResource(query):
    """Opens a specific resource (Documents, Music, Pictures, Videos) and logs it into MySQL."""
    try:
        
        query = query.lower().split()

        
        resource_paths = {
            'documents': os.path.normpath(os.path.join(os.environ['USERPROFILE'], 'Documents')),
            'music': os.path.normpath(os.path.join(os.environ['USERPROFILE'], 'Music')),
            'pictures': os.path.normpath(os.path.join(os.environ['USERPROFILE'], 'Pictures')),
            'videos': os.path.normpath(os.path.join(os.environ['USERPROFILE'], 'Videos')),
            'downloads': os.path.normpath(os.path.join(os.environ['USERPROFILE'], 'Downloads')),
            'desktop': os.path.normpath(os.path.join(os.environ['USERPROFILE'], 'Desktop'))
        }

     
        for resource in resource_paths.keys():
            if resource in query:
                resource_path = resource_paths[resource]
                
                if os.path.exists(resource_path):  
                    os.startfile(resource_path) 

                    
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    sql = "INSERT INTO resource_actions (resource_type, timestamp) VALUES (%s, %s)"
                    val = (resource, timestamp)

                    mycursor.execute(sql, val)
                    mydb.commit()

                    speak(f"Opening {resource}")
                    print(f"✅ Successfully opened '{resource}' and logged the action.")
                else:
                    speak(f"Sorry, I couldn't find {resource}.")
                    print(f"❌ Error: Path does not exist -> {resource_path}")
                return

        
        speak("I couldn't find that resource.")
        print("❌ Error: Resource not found in the predefined paths.")

    except Exception as e:
         speak("Sorry, I couldn't open the requested resource.")
         print(f"❌ Error in openResource function: {e}")


def screenshot():
    """Takes a screenshot, saves it in the correct directory, and logs it in MySQL."""
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        
        screenshot_folder = r"C:\\college\\AI PROJ\\screenshot"  
        filepath = os.path.join(screenshot_folder, f"screenshot_{timestamp}.png")  
        img = pyautogui.screenshot()
        img.save(filepath)

        
        sql = "INSERT INTO screenshots (filepath, timestamp) VALUES (%s, %s)"
        val = (filepath, timestamp)
        mycursor.execute(sql, val)
        mydb.commit()

        speak("Screenshot taken and saved.")
        print(f"✅ Screenshot saved at: {filepath}")

    except Exception as e:
        print(f"❌ Error taking screenshot: {e}")
        speak("Sorry, I couldn't take the screenshot.")


def remember_task(task):
    """Stores the task in MySQL with a timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        sql = "INSERT INTO tasks (task, timestamp) VALUES (%s, %s)"
        val = (task, timestamp)
        mycursor.execute(sql, val)
        mydb.commit()
        print(f"✅ Task '{task}' remembered successfully!")
        speak(f"I have remembered the task: {task}")
    except mysql.connector.Error as err:
        print(f"❌ Error logging task: {err}")
        speak("Sorry, I couldn't remember the task.")


def remind_tasks():
    """Retrieves and speaks out the remembered tasks from MySQL."""
    try:
        sql = "SELECT task, timestamp FROM tasks ORDER BY timestamp DESC LIMIT 5"
        mycursor.execute(sql)
        tasks = mycursor.fetchall()

        if tasks:
            speak("Here are the tasks you asked me to remember:")
            for task, timestamp in tasks:
                speak(f"{task} on {timestamp}")
                print(f"📌 Task: {task} | 🕒 {timestamp}")
        else:
            speak("You have no tasks remembered.")
            print("❌ No tasks found in the database.")
    except mysql.connector.Error as err:
        print(f"❌ Error retrieving tasks: {err}")
        speak("Sorry, I couldn't retrieve your tasks.")


def tell_a_joke():
    """Fetches a joke, speaks it, prints it, and stores it in MySQL."""
    joke = pyjokes.get_joke()  
    print(f"😂 Joke: {joke}")  
    speak(joke)  

    try:
        sql = "INSERT INTO jokes (joke, timestamp) VALUES (%s, %s)"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        val = (joke, timestamp)
        mycursor.execute(sql, val)
        mydb.commit()
        print("✅ Joke logged successfully in MySQL!")
    except mysql.connector.Error as err:
        print(f"❌ Error logging joke: {err}")
        speak("Sorry, I couldn't save the joke.")

    
def flip_coin():
    """Flips a coin, announces the result, prints it, and stores it in MySQL."""
    result = random.choice(["Heads", "Tails"])  
    print(f"🪙 Coin Flip Result: {result}")  
    speak(f"The coin landed on {result}.")  

    try:
      
        sql = "INSERT INTO coin_flips (result, timestamp) VALUES (%s, %s)"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        val = (result, timestamp)
        mycursor.execute(sql, val)
        mydb.commit()
        print("✅ Coin flip result logged successfully in MySQL!")
    except mysql.connector.Error as err:
        print(f"❌ Error logging coin flip result: {err}")
        speak("Sorry, I couldn't store the coin flip result.")
        
        

if __name__ == "__main__":
    wishme()
    speak("Hello, I'm Athena")
    wakeword = "athena"  

    while True:
        query = takeCommandMIC()
        if query:
            query_tokens = process_query(query)  
            print(f"Processed Tokens: {query_tokens}")

            if wakeword in query_tokens:  
                if 'time' in query_tokens:
                    time()
                elif 'date' in query_tokens:
                    date()
                elif 'email' in query_tokens:
                    email_list = {'email': 'jeetdodiya34@gmail.com'}
                    try:
                        speak("To whom do you want to send the mail?")
                        name = takeCommandMIC()
                        receiver = email_list.get(name, None)
                        if receiver:
                            speak("What is the subject of the mail?")
                            subject = takeCommandMIC()
                            speak("What should I say?")
                            content = takeCommandMIC()
                            sendEmail(receiver, subject, content)
                            speak("Email has been sent.")
                        else:
                            speak("I couldn't find that contact.")
                    except Exception as e:
                        print(e)
                        speak("Unable to send the email.")
 
                elif 'message' in query_tokens:
                    user_name = {'ABC': '+', 'BCD': '+'}
                    try:
                        speak("To whom do you want to send the WhatsApp message?")
                        name = takeCommandMIC()
                        phone_no = user_name.get(name, None)
                        if phone_no:
                            speak("What is the message?")
                            message = takeCommandMIC()
                            sendwhatsmsg(phone_no, message)
                            speak("Message has been sent.")
                        else:
                            speak("I couldn't find that contact.")
                    except Exception as e:
                        print(e)
                        speak("Unable to send the message.")

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

                elif "jokes" in query_tokens:
                    tell_a_joke()

                elif "screenshot" in query_tokens:
                    screenshot()

                elif "remember" in query_tokens:
                    speak("What would you like me to remember?")
                    task = takeCommandMIC()  
                    if task and task != "none":  
                        remember_task(task)


                elif "remind" in query_tokens:
                    remind_tasks()

                elif "flip" in query_tokens and "coin" in query_tokens:
                    flip_coin()
                    
                elif "chat" in query_tokens or "talk" in query_tokens:
                    speak("What would you like to ask?")
                    user_input = takeCommandMIC()
                    if user_input:
                        chat_with_gpt(user_input)
                
                elif "generate an image of" in query:
                    image_prompt = query.split("generate an image of")[-1].strip()
                    generate_image(image_prompt)


                elif "quit" in query_tokens or "exit" in query_tokens:
                    speak("Goodbye!")
                    break 

                elif "offline" in query_tokens:
                    quit()
                    