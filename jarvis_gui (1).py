import tkinter as tk
from tkinter import messagebox
import threading
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import time
import smtplib
import requests
import sys

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio, language='en-in')
        return command.lower()
    except:
        return "None"

def send_email(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('your-email@gmail.com', 'your-password')
        server.sendmail('your-email@gmail.com', to, content)
        server.quit()
        speak("Email has been sent.")
    except:
        speak("Sorry, I am not able to send the email.")

def get_weather():
    url = "https://open-weather13.p.rapidapi.com/fivedaysforcast"
    querystring = {"latitude": "40.730610", "longitude": "-73.935242", "lang": "EN"}
    headers = {
        "x-rapidapi-host": "open-weather13.p.rapidapi.com",
        "x-rapidapi-key": "8e75eeaa90msh73bbc51d2b4433cp1d6239jsnfb8850a246de"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        if "list" in data:
            for day in data["list"][:1]:
                date = day["dt_txt"]
                temp = day["main"]["temp"]
                description = day["weather"][0]["description"]
                speak(f"{date}: {temp} degrees Celsius with {description}")
        else:
            speak("No forecast data available.")
    except:
        speak("Error fetching weather data.")

def run_jarvis():
    speak("Hello, I am Jarvis. How can I help you?")
    while True:
        command = take_command()
        if command == "none":
            continue
        elif 'wikipedia' in command:
            command = command.replace("wikipedia", "").strip()
            if command:
                speak('Searching Wikipedia...')
                try:
                    results = wikipedia.summary(command, sentences=2)
                    speak("According to Wikipedia")
                    speak(results)
                except Exception as e:
                    speak("Sorry, I couldn't find information on that.")
            else:
                speak("Please say what you want to search on Wikipedia.")
        elif 'open youtube' in command:
            webbrowser.open("https://youtube.com")
        elif 'open google' in command:
            webbrowser.open("https://google.com")
        elif 'open stackoverflow' in command:
            webbrowser.open("https://stackoverflow.com")
        elif 'news' in command:
            webbrowser.open("https://bbc.com")
            speak("Opening BBC news.")
        elif 'play music' in command:
            music_dir = r"C:\Users\vishal singh\Music"
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
                speak("Playing music.")
            else:
                speak("No songs found.")
        elif 'time' in command:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {str_time}")
        elif 'open code' in command:
            code_path = r"C:\Users\vishal singh\AppData\Local\Programs\Microsoft VS Code\Code.exe"
            os.startfile(code_path)
        elif 'send email' in command:
            speak("What should I say?")
            content = take_command()
            to = "recipient@example.com"
            send_email(to, content)
        elif 'weather' in command:
            get_weather()
        elif 'open calculator' in command:
            os.system("calc")
        elif 'open camera' in command:
            os.system("start microsoft.windows.camera:")
        elif 'goodbye' in command or 'exit' in command:
            speak("Goodbye!")
            break
        else:
            speak("I did not understand. Please repeat.")

def start_jarvis_thread():
    threading.Thread(target=run_jarvis).start()

# GUI Setup
app = tk.Tk()
app.title("Jarvis - Virtual Assistant")
app.geometry("400x250")

label = tk.Label(app, text="Click to Start Jarvis", font=("Arial", 16))
label.pack(pady=30)

start_button = tk.Button(app, text="Start Listening", command=start_jarvis_thread, font=("Arial", 14), bg="green", fg="white")
start_button.pack(pady=10)

exit_button = tk.Button(app, text="Exit", command=app.destroy, font=("Arial", 14), bg="red", fg="white")
exit_button.pack(pady=10)

app.mainloop()
