#!/usr/bin/env python
# coding: utf-8

# In[ ]:


pip install geopy


# In[ ]:


pip install timezonefinder


# In[ ]:





# In[ ]:


pip install nlp-utils


# In[ ]:





# In[ ]:


from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import speech_recognition as sr
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pyttsx3
import requests
import random
import time
import os
from newsapi import NewsApiClient
import datetime
import wikipediaapi
import wikipedia
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
from nltk.stem import WordNetLemmatizer
import math
import sympy
from nltk.stem import WordNetLemmatizer
from nltk.util import bigrams
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt') 
nltk.download('wordnet')
nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

engine = pyttsx3.init()

engine.setProperty('rate', 150)
engine.setProperty('volume', 2)    
engine.setProperty('pitch', 150)

user_preferences = {
    
  "Herve": {
    "likes": ["Basketball", "pop music"] 
  }
}

current_context = {
  "user_name": "Herve",
  "recent_topics": ["music", "movies","Artificial Intelligence"]
}    


print(f"Hi {current_context['user_name']}")

def get_time_of_day():
    
    current_time = datetime.datetime.now().time()
    
    if current_time.hour < 12 :
        
        return "morning"
    
    elif current_time.hour < 18:
        
        return "Afternoon"
    
    else:
        
        return "Evening"

# Function to generate a dynamic greeting response

def generate_greeting():
    
    time_of_the_day = get_time_of_day()
    
    return f"Good {time_of_the_day}! How can I assist you?"

# Usage:

print(generate_greeting())

# Function to speak and get user input 

def speak_and_listen():
    
    text = input(" User: ")
    engine.say(text)
    engine.runAndWait()
    return text

#preprocess text entered from user input

def preprocess(text):
    
# Tokenize into words

    words = nltk.word_tokenize(text)
    
# Lemmatize words and convert to lowercase

    words = [lemmatizer.lemmatize(word.lower()) for word in words]
    
    return words

#get general inquiries from wikipedia

def get_answer(text):
    
    keywords = preprocess(text)
    
    try:
        
 # Try getting a short summary from Wikipedia

        summary = wikipedia.summary(" ".join(keywords), sentences = 2 )
        
        return summary
    
    except wikipedia.exceptions.DisambiguationError as e:
        # Handle disambiguation errors by returning suggestions
        suggestions = e.options
        
        if suggestions:
            # Return the first suggested option
            page_summary = wikipedia.summary(suggestions[0], sentences=2)
            
            return page_summary
        
        return "Sorry, I could not find any information related to your input."
    
    except wikipedia.exceptions.PageError:
        
        return "Sorry, I could not find any information related to your input."


def do_math(expression):
    
    try:
        
        result = eval(expression) 
        return f"The result is {result}"

    except Exception as e:
        
        expr = sympy.sympify(expression)
        
        try:
            result = expr.evalf()
            return f"The result is {result}"
        
        except SympifyError:
            return "Invalid math expression. Please check your input."

        except AttributeError:
            # Handle cases like factorial, log etc. 
            return f"The result is {expr}"
    

# Recommendation system for music and movies

movie_recommendations = {
    
    'action': ['The Dark Knight', 'Inception', 'Mad Max: Fury Road'], 
    'comedy': ['Deadpool', 'The Hangover', 'Superbad'],
    'drama':['The Shawshank Redemption', 'Forrest Gump', 'The Godfather'],
    'documentaries':['Spy Craft','Betrayal: The Perfect Husband ','The Interrogation of Tony Martin '],
    'sci-fi':['star wars', 'star trek', 'Dune','The endless']
    
    
}

music_recommendations = {
    
    'r&b':['CUFF IT by Beyonce','Fantasy by Mariah Carey', 'ALL MINE by Brent Faiyaz', 'Say My Name by Destinys Child'  ],
    'hip-hop':['N.Y. State of Mind by Nas','It Was a Good Day by Ice Cube','In da Club by 50 cent'],
    'Jazz':['Fly Me To The Moon,Frank Sinatra','Take Five by Dave Frank Sinatra','What a Wonderful World by Louis Armstrong'],
    'drill':['Reggae & Calypso russ Millions','Not In The Mood feat. Fivio Foreign & Kay Flock','Kay Flock, Cardi B, Dougie B - Shake It'],
    'afrobeats':['Ta Ta Ta by Bayani','Body & Soul by Joeboy', 'essence by WizKid feat Tems'],
    'amapiano':['Amanikiniki by MFR Souls', 'Abo Mvelo by Daliwonga', 'Woza by Kabza De Small '],
    'pop':['Billie Jean by Michael Jackson', 'Single Ladies by Beyonce', 'Toxic by Britney Spears'],
    'classic':['Stayin Alive by Bee Gees','Ring of Fire by Johnny Cash', 'Hotel California by Don Henley']
}


jokes = [ 
    
    "Why don't scientists trust atoms? Because they make up everything!",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "Why did the bicycle fall over? Because it was two-tired!",
    "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!"
    
    
]

commands = {
    
    "notepad": "notepad.exe",
    "music": "C:/Users/kayum/AppData/Roaming/Spotify/Spotify.exe",

}

# Open a program

def run_program(text_command):
    
    if text_command in commands:
        
        os.system("start "+commands[text_command])
        
    else:
        
        print("command don't exist")
        
# function to generate a random joke           

def tell_joke():
    
    return random.choice(jokes)

# Function to generate a random story

def generate_random_story():
    
    characters = ['Alice', 'Bob', 'Ella', 'Max', 'Sophie']
    settings = ['in a faraway kingdom', 'on a mysterious island', 'in a bustling city', 'in a magical forest']
    problems = ['lost a valuable treasure', 'needed to rescue a friend', 'encountered a dangerous monster']
    resolutions = ['and they lived happily ever after.', 'and they found a hidden solution to their problem.',
                   'and they realized the power of friendship and teamwork.']

    main_character = random.choice(characters)
    setting = random.choice(settings)
    problem = random.choice(problems)
    resolution = random.choice(resolutions)

    story = f"Once upon a time, there was {main_character}, who lived {setting}. One day, {main_character} " \
            f"{problem}. However, with courage and determination, {main_character} faced the challenge " \
            f"{resolution}"

    return story

#Determine the user's intent using fuzzy matching

def get_fuzzy_intent(user_input, intent_options, threshold=80):
    
    intent, similarity = process.extractOne(user_input,intent_options)
    
    if similarity >= threshold:
        
        return intent
    
    return None

# Define valid intents

valid_intents = [
    
    "weather",
    "music recommendation",
    "movie recommendation",
    "joke",
    "story",
    "calculate",
    "time",
    "schedule appointment",
    "view appointment",
    "calendar",
    "open",
    "travel recommendation",
    "guided meditation",
    "health advice",
    "mental health support",
    "breathing exercise",
    "progressive muscle relaxation",
    "play word guessing game",
    "play trivia",
    "summarize",
    "compose email",
]
            
SCOPES = ['https://www.googleapis.com/auth/calendar']
# Dictionary to store scheduled appointments

appointments = {}

# Function to schedule an appointment

def schedule_appointment():
    
    appointment_description = input("Enter a brief description of the appointment: ")
    appointment_date = input("Enter the appointment date (YYYY-MM-DD): ")
    appointment_time = input("Enter the appointment time (HH:MM): ")

    # Authenticate and authorize access to the Google Calendar API
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_89031301966-hchnivlso44tr7mh3vnmtpamt7d5pevn.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the Google Calendar API service
    service = build('calendar', 'v3', credentials=creds)

    start_datetime = f"{appointment_date}T{appointment_time}:00"
    end_datetime = f"{appointment_date}T{appointment_time}:30"

    event = {
        'summary': appointment_description,
        'start': {'dateTime': start_datetime, 'timeZone': 'UTC'},
        'end': {'dateTime': end_datetime, 'timeZone': 'UTC'},
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Appointment scheduled successfully.')
    print(f'Event ID: {event["id"]}')

def view_appointments():
    
    print ("Scheduled Appointments:")
    
    for datetime_key, description in appointments.items():
        
        appointment_date, appointment_time = datetime_key
        print(f"Date: {appointment_date}, Time: {appointment_time}, Description: {description}")


        
#Function to get today's news headlines 

def get_news():
    
    news_api = NewsApiClient(api_key='3cf1ba0a806a4ca79ec5338de7f79369')
    top_headlines = news_api.get_top_headlines(language='en')['articles']
    
    headlines = []
    
    for article in top_headlines:
        
        headlines.append(article['title'])
    
    news_report = ". ".join(headlines[:5])
    
    return f" here are top news headlines: {news_report}"
        
# Function to get weather information

def get_weather(city):
    
    api_key = '9f991689ab04eb099fb9f7709261d417'
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid':api_key}
    
    try:
        response = requests.get(base_url,params=params)
        data = response.json()
        
        if data['cod'] == 200:
            weather_info = data['weather'][0]['description']
            temperature = round(data['main']['temp'] - 273.15, 2)
            
            return f" The weather in {city} is {weather_info}. The temperature is {temperature}°C."
        
        else:
            
            return "Sorry, I couldn't retrieve the weather information."     
        
    except Exception as e:
        
        return f'An error occurred while fetching weather data: {str(e)}'
        
        
    
# Function to get calendar events

def get_calendar():
    
# Code to fetch calendar events

  events_today = ["Team meeting at 9am", "Coffee with Alex at 11am","Teach Itzae at 6 PM"]
  
  return f"You have {len(events_today)} events scheduled today: {', '.join(events_today)}"

# Define a function to get destination info from APIs:

def get_destination_info(city):
    
    maps_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={city}&key=YOUR_API_KEY"
    maps_response = requests.get(maps_url).json()
    
    top_attractions = [result['name'] for result in maps_response['results'][:5]]
    
    # TripAdvisor API request
    
    tripadvisor_url = f"https://tripadvisor1.p.rapidapi.com/locations/search?location_id=1&limit=5&sort=relevance&offset=0&lang=en_US&currency=USD&units=km&query={city}"
    
    tripadvisor_response = requests.get(
      tripadvisor_url, 
      headers={
        "X-RapidAPI-Key": "YOUR_API_KEY",
        "X-RapidAPI-Host": "tripadvisor1.p.rapidapi.com"
      }
  ).json()
    
    top_restaurants = [result['name'] for result in tripadvisor_response['data'][:5]]
    
    return f"Top attractions: {', '.join(top_attractions)}. Top restaurants: {', '.join(top_restaurants)}"    
    

def summarize_article(article):
    
    # Tokenize the article into sentences
    sentences = nltk.sent_tokenize(article)
    
    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    
    # Fit the vectorizer and transform the sentences to TF-IDF scores
    tfidf_scores = vectorizer.fit_transform(sentences)
    
    # Calculate the sentence scores based on TF-IDF scores
    sentence_scores = np.sum(tfidf_scores, axis=1)
    
    # Sort sentences by their scores in descending order
    sorted_sentences = [sentence for _, sentence in sorted(zip(sentence_scores, sentences), reverse=True)]
    
    # Select the top 10 most important sentences as the summary
    summary = sorted_sentences[:10]
    
    return ' '.join(summary)

# Function to get the time of day

def get_time_date_for_city(city_name):
    
    geolocator = Nominatim(user_agent = "Chrome/58.0.3029.110 Safari/537.3")
    location = geolocator.geocode(city_name)
    
    if location:
        
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lng = location.longitude, lat = location.latitude)
        
        if timezone_str:
            tz = pytz.timezone(timezone_str)
            current_time = datetime.datetime.now(tz)
            
            return f" the current time in {city_name} is {current_time.strftime('%H:%M:%S')} on {current_time.strftime('%Y-%m-%d')}"
        
        else:
            
            return f"Sorry, I couldn't find the time zone for {city_name}."
        
    else:
        
        return f"Sorry, I couldn't find information for {city_name}."
    
# Function to offer mental health support and encouragement

def offer_mental_health_support():
    
    responses = [
        "Remember, you're not alone in this. Reach out to someone you trust.",
        "Take a moment for yourself and practice self-care. You deserve it.",
        "It's okay to not be okay. You're strong and can overcome anything.",
        "Focus on the positive aspects of life and practice gratitude.",
        "Breathing exercises can help you relax and clear your mind. Would you like to try one?"
    ]
    return random.choice(responses)

# Function for a breathing exercise to relieve stress
def breathing_exercise():
    
    response = "Let's try a simple breathing exercise. Inhale deeply for 4 seconds, hold for 4 seconds, and exhale for 4 seconds. Repeat this for a few cycles. Remember, focus on your breath and let go of any tension."
    return response

# Function for progressive muscle relaxation to relieve stress
def progressive_muscle_relaxation():
    
    response = "Progressive Muscle Relaxation (PMR) is a technique where you tense and relax different muscle groups. Let's start by tensing your muscles for 5 seconds and then relaxing for 10 seconds. We'll start with your hands. Ready?"
    return response

# Function for a guided meditation session
def guided_meditation():
    
    response = "Let's begin a guided meditation session. Find a quiet and comfortable place to sit or lie down. Close your eyes and focus on your breath. Inhale slowly, hold, and exhale gently. Let go of any thoughts and be present in this moment."
    return response

# Function to provide general health-related advice
def provide_health_advice():
    
    advice = [
        "Remember to stay hydrated and drink plenty of water throughout the day.",
        "Maintain a balanced diet rich in fruits, vegetables, and whole grains.",
        "Regular physical activity is crucial for your overall well-being. Find an activity you enjoy and make it a habit.",
        "A good night's sleep is essential for your health. Aim for 7-9 hours of quality sleep each night.",
        "Taking short breaks during work or study sessions can improve productivity and reduce stress."
    ]
    return random.choice(advice)



# Trivia questions categorized by topic
trivia_questions = {
    
    "Geography": {
        "What is the capital of France?": "Paris",
        "What is the largest planet in our solar system?": "Jupiter"
    },

    "Science": {
        "Who discovered penicillin?": "Alexander Fleming",
        "What is the symbol for the chemical element gold ?": "Au"
    },
    
    "Math": {
        
        "What is the only number that has the same number of letters as it’s meaning ?":"four",
        "What is the smallest perfect number ?":"six",
        "Which number is considered a magic number ?": "nine"
    },
    
    "General knowledge": {
        
        "A group of monkeys is called a troop ? ":"True",
        "Human facial hair grows faster than the hair on the rest of the body ? ":"True",
        "The Philippines has two official languages, English and the Filipino language. ?": "True"
    },
    
# Add more categories and questions as needed
}
    
# Function to play trivia game with a chosen category
def play_trivia():
    
    print("Available trivia categories:")
    
    for category in trivia_questions.keys():
        
        print(category)

    selected_category = input("Choose a category: ").capitalize()

    if selected_category not in trivia_questions:
        
        print("Invalid category.")
        return

    questions = trivia_questions[selected_category]
    score = 0

    for question, answer in questions.items():
        
        print(question)
        user_answer = input("Your answer: ").strip().lower()
        
        if user_answer == answer.lower():
            print("Correct!")
            score += 1
        
        else:
            print(f"Wrong! The correct answer is: {answer}")

    print(f"You got {score} out of {len(questions)} questions correct.")

# Function to play word guessing game
def play_word_guessing_game():
    
    word = random.choice(["python", "java", "javascript", "ruby", "html", "css","america","solar","sun"])
    guessed_letters = set()
    attempts = 6

    print("Let's play Word Guessing Game!")
    print("Word to guess: " + " ".join("_" * len(word)))

    while attempts > 0:
        
        print(f"Attempts left: {attempts}")
        guessed_word = "".join(letter if letter in guessed_letters else "_" for letter in word)
        print("Guessed word so far: " + " ".join(guessed_word))
        print("Guessed letters: " + " ".join(sorted(list(guessed_letters))))

        guess = input("Guess a letter or the whole word: ").strip().lower()

        if len(guess) == 1:
            
            if guess in guessed_letters:
                
                print("You already guessed that letter.")
            
            else:
                
                guessed_letters.add(guess)
                if guess not in word:
                    attempts -= 1
        elif len(guess) == len(word) and guess.isalpha():
            
            if guess == word:
                
                print("Congratulations! You guessed the word.")
                play_again = input("Do you want to play again? (yes/no): ").lower()
                if play_again == "yes":
                    
                    play_word_guessing_game()
                
                return
            
            else:
                
                attempts -= 1

        if "_" not in guessed_word:
            
            print("Congratulations! You guessed the word.")
            play_again = input("Do you want to play again? (yes/no): ").lower()
            
            if play_again == "yes":
                play_word_guessing_game()
            
            return

    print(f"Sorry, you've run out of attempts. The word was: {word}")
    play_again = input("Do you want to play again? (yes/no): ").lower()
    
    if play_again == "yes":
        play_word_guessing_game()
        
def compose_email(subject):
    
    email_content = ""

    if "meeting" in subject.lower():
        
        email_content = "Dear Team,\n\nLet's schedule a meeting to discuss the upcoming project. Please find below the proposed meeting times:\n\n- Date: [Proposed Date]\n- Time: [Proposed Time]\n\nLooking forward to your availability.\n\nBest regards,\n[Your Name]"

    elif "report" in subject.lower():
        
        email_content = "Hello,\n\nI am currently working on the report you requested. I will provide a detailed update once it's ready.\n\nThank you for your patience.\n\nKind regards,\n[Your Name]"
    
    elif "urgent" in subject.lower():
        
        email_content = "Hello,\n\nThis is to bring to your attention an urgent matter that requires immediate action. Please see the details below:\n\n[Urgent Matter Details]\n\nYour prompt response is highly appreciated.\n\nBest regards,\n[Your Name]"

    elif "follow-up" in subject.lower():
        
        email_content = "Hello,\n\nI'm following up on our recent conversation regarding [topic]. Could you please provide an update or any additional information?\n\nThank you for your time.\n\nBest regards,\n[Your Name]"

    else:
        
        email_content = "Hello,\n\nHere's the information you requested:\n\n[Content]\n\nIf you need any further assistance, feel free to ask.\n\nBest regards,\n[Your Name]"

    return email_content

def generate_email_content(subject):
    return compose_email(subject)
        
#user input

user_input = speak_and_listen()

# Provide an appropriate response based on user input
    
while user_input.lower() != 'bye':
    
    
    # Determine the user's intent using fuzzy matching
    
    determined_intent = get_fuzzy_intent(user_input, valid_intents)

    if 'how are you' in user_input.lower():
        
        response = " Hello, I'm good, thank you for asking!"
    
    elif determined_intent == "weather":
        
        user_input = user_input.lower().replace('weather in ','').strip()
        
        response = get_weather(user_input)
        
    elif determined_intent == "music recommendation":
        
        genre = input("Sure, what genre are you interested in (R&B, POP, Afrobeats, Hip-Hop, Classic, Amapiano, Drill, Jazz)? ")
        recommendations = music_recommendations.get(genre.lower())
        
        print(recommendations)
        
        if recommendations:
            
            response = f" Here are some {genre} music recommendations: {' , ' .join(recommendations)} "
        
        else:
            
            response = " sorry, I couldn't find movie recommendations for that genre"
        
        
    elif determined_intent == "movie recommendation":
        
        genre = input("Sure, what genre are you interested in (Action, Drama, Sci-Fi, Comedy, Documentaries)? ")
        recommendations = movie_recommendations.get(genre.lower())

        
        print(recommendations)
        
        if recommendations:
            
            response = f" Here are some {genre} movie recommendations: {' , ' .join(recommendations)} "
        else:
            
            response = " sorry, I couldn't find movie recommendations for that genre"
            
            
    elif determined_intent == 'joke':
        
        response = tell_joke() 
        
    elif determined_intent == 'story':
        
        response = generate_random_story()
        
    elif determined_intent == 'shutdown':
        
        shutdown_or_restart('shutdown')
        response = "Shutting down your computer. Goodbye!"
    
    elif determined_intent == 'restart':
        
        shutdown_or_restart('restart')
        response = "Restarting your computer. See you soon!"
        
    elif determined_intent == 'news':
        
        print(get_news())
        response = get_news()
        
    elif determined_intent == 'time':
        
        user_input = user_input.lower().replace('time in', '').strip()
        response = get_time_date_for_city(user_input)
        
    elif determined_intent =='calendar':
        
        print(get_calendar())
        response = get_calendar()
    
    elif determined_intent =='open':
        
        user_input = user_input.lower().replace('open','').strip()
        response = run_program(user_input)
        
    elif determined_intent =='summarize':
        
        art_smrz = input(" what article do you want me to summarize ? ") 
        
        response = summarize_article(art_smrz)
        
        smrz_art = f" \n Here's is your summarized article: \n {response} "
        
        print(smrz_art)
    
    elif determined_intent == 'travel recommendation':
        
        city = input(" What city you want to visit ? ")
        
        travel_info = get_destination_info(city)
        
        response = f" Here are some travel recommendations in {city}:{travel_info}"
        
        print("Travel Recommendations:", travel_info)
            
    elif determined_intent == 'schedule appointment':
        
        schedule_appointment()
        response = "Appointment scheduled. Is there anything else I can assist you with?"
        
        
    elif determined_intent == "calculate":
        
        expression = user_input[len("calculate"):].strip()
        response = do_math(expression)
        print(response)
   
    elif determined_intent == "view appointment":
        
        response = view_appointments()
        
    elif determined_intent == "mental health support":
        
        response = offer_mental_health_support()
        print(response)

    elif determined_intent == "breathing exercise":
        
        response = breathing_exercise()
        print(response)

    elif determined_intent == "progressive muscle relaxation":
        
        response = progressive_muscle_relaxation()
        print(response)

    elif determined_intent == "guided meditation":
        
        response = guided_meditation()
        print(response)

    elif determined_intent == "health advice":
        
        response = provide_health_advice()
        print(response)
    
    elif determined_intent == "play trivia":
        
        response = play_trivia()
        
    elif determined_intent == "play word guessing game":
        
        response = play_word_guessing_game()
        
    # When the user intends to compose an email
    
    elif determined_intent == "compose email":
        subject = input("Enter the subject of the email: ")
        response= generate_email_content(subject)
        print("Email Content:\n", response)

    else:
        
        response = get_answer(user_input)
        print(response)
        
        
# Speak the response and get the next user input
    
    engine.say(response)
    engine.runAndWait()
    user_input = speak_and_listen()
    # End the conversations

engine.say("see you soon, take care!")
engine.runAndWait()


# In[12]:


pip install time


# In[4]:


pip install --upgrade pyaudio


# In[ ]:


pip install SpeechRecognition


# In[ ]:


pip install python-Levenshtein


# In[1]:


pip install fuzzywuzzy


# In[ ]:


pip install gTTS


# In[ ]:


pip install translator


# In[ ]:


pip install language_translator.es


# In[ ]:


pip install langdetect


# In[ ]:


pip install googletrans


# In[ ]:


pip install google-api-python-client google-auth-oauthlib


# In[ ]:


pip install apscheduler


# In[ ]:


pip install pyttsx3


# In[ ]:


pip install requests


# In[ ]:


pip install urllib3==1.26.9


# In[ ]:


pip install pytz


# In[ ]:


pip install geopy


# In[ ]:


pip install timezonefinder


# In[ ]:


pip install random


# In[ ]:


pip install datetime


# In[ ]:


pip install calendar


# In[ ]:


pip install --upgrade google-api-python-client


# In[ ]:


pip install newsapi-python


# In[ ]:


pip install huggingface_hub --upgrade


# In[ ]:


pip list


# In[ ]:


pip install -U huggingface_hub


# In[ ]:


pip install xformers


# In[ ]:


pip install newsapi-python


# In[ ]:


pip install -U pip setuptools


# In[ ]:


pip install --upgrade newsapi-python


# In[ ]:


pip install newsapi-python


# In[ ]:


pip install spacy


# In[ ]:


pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.5/en_core_web_sm-2.2.5.tar.gz


# In[ ]:


pip install openai


# In[ ]:


pip install --upgrade spacy


# In[ ]:


pip install --upgrade comtypes


# In[ ]:


pip uninstall nltk


# In[ ]:


pip install nltk==desired_version


# In[ ]:


pip install wikipedia


# In[ ]:


pip install flight_search


# In[ ]:


pip install tensorflow


# In[ ]:


pip install keras


# In[ ]:


pip install -U scikit-learn


# In[ ]:


pip install facial-emotion-recognition


# In[ ]:


pip install TextBlob


# In[ ]:


pip install stanfordnlp


# In[ ]:


pip install transformers


# In[ ]:


pip install --upgrade pip


# In[ ]:


pip install emotion-detection-python


# In[ ]:


pip install git+https://github.com/atulapra/Emotion_Detection.git


# In[ ]:


pip install --upgrade nltk


# In[ ]:


pip install sympy


# In[ ]:


pip install --upgrade google-api-python-client


# In[ ]:


pip install pyrhyme


# In[ ]:


pip install boto3


# In[ ]:


pip install futures


# In[ ]:




