import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import string

# Initialize global chat string
chatStr = ""

# Function to generate a random string for unique filenames
def get_random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Function to speak text using Windows Text-to-Speech
def say(text):

    safe_text = text.replace("'", "`")
    os.system(f'powershell -Command "Add-Type –AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Speak(\'{safe_text}\')"')

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
        print("Error in chat:", e)
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
        print("Error generating AI response:", e)

# Function to take voice commands using speech_recognition
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-US")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return "Sorry, I did not understand that."
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return "Sorry, I'm having trouble understanding you."

# Function to open Google
def open_google():  # <--- New function added
    say("Opening Google")
    webbrowser.open("https://www.google.com")

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
