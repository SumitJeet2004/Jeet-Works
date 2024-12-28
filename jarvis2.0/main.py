import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import string
import logging
from PyDictionary import PyDictionary

# Setup logging
logging.basicConfig(level=logging.INFO, filename="jarvis.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize global variables
dictionary = PyDictionary()
chatStr = ""

# Function to generate a random string for unique filenames
def get_random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

# Function to speak text using Windows Text-to-Speech
def say(text):
    try:
        safe_text = text.replace("'", "`")
        os.system(f'powershell -Command "Add-Type –AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Speak(\'{safe_text}\')"')
    except Exception as e:
        logging.error(f"Error in text-to-speech: {e}")

# Function to chat with OpenAI's API
def chat(query):
    global chatStr
    try:
        openai.api_key = apikey
        chatStr += f"User: {query}\nJarvis: "
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=chatStr,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        answer = response["choices"][0]["text"].strip()
        say(answer)
        chatStr += f"{answer}\n"
        return answer
    except Exception as e:
        logging.error(f"Error in chat: {e}")
        return "I'm having trouble responding right now."

# Function to generate AI responses and save them
def ai(prompt):
    openai.api_key = apikey
    response_text = f"OpenAI response for Prompt: {prompt}\n{'*' * 25}\n\n"
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response_text += response["choices"][0]["text"].strip()

        # Create a directory if it doesn't exist
        if not os.path.exists("Openai"):
            os.mkdir("Openai")

        safe_filename = f"{get_random_string()}_{prompt[:50].replace(' ', '_').replace('/','_')}.txt"
        filename = os.path.join("Openai", safe_filename)
        with open(filename, "w") as f:
            f.write(response_text)
    except Exception as e:
        logging.error(f"Error generating AI response: {e}")

# Function to take voice commands using speech_recognition
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("Listening...")
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-US")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            say("Sorry, I did not understand that.")
            return ""
        except sr.RequestError as e:
            logging.error(f"Speech recognition error: {e}")
            say("Sorry, I'm having trouble understanding you.")
            return ""
        except Exception as e:
            logging.error(f"Unexpected error in takeCommand: {e}")
            return ""

# Function to open Google
def open_google():
    say("Opening Google")
    webbrowser.open("https://www.google.com")

# Function to search Google
def search_google(query):
    say("Searching on Google")
    webbrowser.open(f"https://www.google.com/search?q={query}")

# Function to fetch the current time
def get_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    say(f"The current time is {current_time}")

# Function to look up word meanings
def get_meaning(word):
    try:
        meaning = dictionary.meaning(word)
        if meaning:
            say(f"The meaning of {word} is: {meaning}")
        else:
            say("I couldn't find the meaning of that word.")
    except Exception as e:
        logging.error(f"Error in dictionary lookup: {e}")
        say("There was an error finding the meaning of the word.")

# Main function to handle different commands
if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Welcome to Jarvis A.I")
    while True:
        query = takeCommand().lower()

        if "open youtube" in query:
            say("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
        elif "open wikipedia" in query:
            say("Opening Wikipedia")
            webbrowser.open("https://en.wikipedia.org")

        elif "open spotify" in query:
            say("Opening Spotify")
            os.system("start spotify")

        elif "open google" in query:
            open_google()

        elif "search for" in query:
            search_query = query.replace("search for", "").strip()
            search_google(search_query)

        elif "what is the time" in query or "current time" in query:
            get_time()

        elif "meaning of" in query:
            word = query.replace("meaning of", "").strip()
            get_meaning(word)

        elif "exit" in query or "quit" in query or "shutdown" in query:
            say("Goodbye! Have a great day.")
            break

        else:
            response = chat(query)
            print(response)

