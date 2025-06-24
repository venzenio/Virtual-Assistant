
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import time
import sys
import smtplib
import requests

# Initialize the TTS engine
engine = pyttsx3.init('sapi5')  # Windows-specific
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def wish_me():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis, your assistant. How can I help you?")

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {command}")
    except:
        speak("Sorry, I didn't catch that. Please say that again.")
        return "None"
    return command.lower()

def send_email(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('your-email@gmail.com', 'your-password')
        server.sendmail('your-email@gmail.com', to, content)
        server.quit()
        speak("Email has been sent.")
    except Exception as e:
        speak("Sorry, I am not able to send the email.")

import requests

def get_weather_forecast():
    url = "https://open-weather13.p.rapidapi.com/fivedaysforcast"
    querystring = {"latitude": "40.730610", "longitude": "-73.935242", "lang": "EN"}

    headers = {
        "x-rapidapi-host": "open-weather13.p.rapidapi.com",
        "x-rapidapi-key": "8e75eeaa90msh73bbc51d2b4433cp1d6239jsnfb8850a246de"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        # Display forecast for the next few days
        if "list" in data:
            for day in data["list"][:3]:  # Limit to 3 entries for brevity
                date = day["dt_txt"]
                temp = day["main"]["temp"]
                description = day["weather"][0]["description"]
                print(f"{date}: {temp}°C with {description}")
        else:
            print("No forecast data available.")
    except Exception as e:
        print("Error fetching weather data:", e)


def open_calculator():
    os.system("calc")

def open_camera():
    os.system("start microsoft.windows.camera:")

def execute_command(command):
    if 'wikipedia' in command:
        speak('Searching Wikipedia...')
        command = command.replace("wikipedia", "")
        try:
            result = wikipedia.summary(command, sentences=2)
            speak("According to Wikipedia")
            speak(result)
        except:
            speak("Sorry, I couldn't find information on that.")

    elif 'open youtube' in command:
        webbrowser.open("https://youtube.com")

    elif 'open google' in command:
        webbrowser.open("https://google.com")

    elif 'open stackoverflow' in command:
        webbrowser.open("https://stackoverflow.com")

    elif 'news' in command:
        webbrowser.open("https://bbc.com")
        speak("Here are some headlines from BBC News.")

    elif 'play music' in command:
        music_dir = r"C:\Users\vishal singh\Music"
        if not os.path.exists(music_dir):
            speak("Music directory not found.")
            return
        songs = os.listdir(music_dir)
        if songs:
            os.startfile(os.path.join(music_dir, songs[0]))
            speak("Playing music.")
        else:
            speak("No songs found in the music directory.")

    elif 'time' in command:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {str_time}")

    elif 'open code' in command:
        vs_path = r"C:\Users\vishal singh\AppData\Local\Programs\Microsoft VS Code\Code.exe"
        if os.path.exists(vs_path):
            os.startfile(vs_path)
            speak("Opening Visual Studio Code.")
        else:
            speak("VS Code path is invalid or not installed.")

    elif 'send email' in command:
        try:
            speak("What should I say?")
            content = take_command()
            to = "recipient@example.com"
            send_email(to, content)
        except:
            speak("I was not able to send the email.")

    elif 'weather' in command:
        speak("Fetching the weather forecast for your location.")
        get_weather_forecast()


    elif 'open calculator' in command:
        open_calculator()

    elif 'open camera' in command:
        open_camera()

    elif 'goodbye' in command or 'exit' in command:
        speak("Goodbye! Have a nice day.")
        sys.exit()

    else:
        speak("I'm not sure how to help with that.")

if __name__ == "__main__":
    wish_me()
    while True:
        query = take_command()
        if query != "None":
            execute_command(query)
