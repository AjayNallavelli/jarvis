import speech_recognition as sr
import pyttsx3
import openai
import webbrowser
import os
import subprocess
import pygame
import random

# Configure your OpenAI API key here 
OPENAI_API_KEY = ""

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5)

    try:
        user_input = recognizer.recognize_google(audio).lower().strip()
        print("You: ", user_input)
        return user_input
    except sr.UnknownValueError:
        print("Sorry, I could not understand you.")
        return ""
    except sr.RequestError:
        print("Failed to fetch results from Google Web Speech API.")
        return ""

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_chatgpt_response(conversation_history):
    try:
        openai.api_key = OPENAI_API_KEY
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=conversation_history,
            max_tokens=150,
            stop=["\n"]
        )
        return response.choices[0].text.strip()
    except openai.OpenAIError:
        return "Sorry, I need to improve BOSS"

def open_browser_and_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)

def open_application(application_name):
    try:
        if "chrome" in application_name:
            subprocess.Popen(["/usr/bin/google-chrome-stable"])  # Modify path for your OS
        elif "notepad" in application_name:
            subprocess.Popen(["notepad.exe"])
        # Add more applications here with their respective commands
        else:
            speak(f"Sorry, I don't know how to open {application_name}.")
    except Exception as e:
        speak("Sorry, there was an error while opening the application.")

def close_application(application_name):
    try:
        if "chrome" in application_name:
            os.system("taskkill /im chrome.exe /f")  # Kill Chrome process forcefully
        elif "notepad" in application_name:
            os.system("taskkill /im notepad.exe /f")  # Kill Notepad process forcefully
        # Add more applications here with their respective commands
        else:
            speak(f"Sorry, I don't know how to close {application_name}.")
    except Exception as e:
        speak("Sorry, there was an error while closing the application.")

def play_music():
    try:
        pygame.mixer.init()
        music_files = ["music1.mp3", "music2.mp3", "music3.mp3"]  # Add your music files here
        music_file = random.choice(music_files)
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play()
        speak("Playing music. Enjoy!")
        while pygame.mixer.music.get_busy():
            if "stop music" in listen():
                stop_music()
                break
    except Exception as e:
        speak("Sorry, there was an error while playing music.")

def stop_music():
    try:
        pygame.mixer.music.stop()
        speak("Music stopped BOSS.")
    except Exception as e:
        speak("Sorry, there was an error while stopping the music.")

def change_music():
    stop_music()
    play_music()

def main():
    speak("Hello BOSS! I am Jarvis, your advanced voice assistant. How can I assist you?")
    conversation_history = "User: Hi, Jarvis!\nJarvis:"
    while True:
        user_input = listen()

        if not user_input:
            speak("I didn't hear anything BOSS. Could you please repeat?")
            continue

        if "goodbye" in user_input or "bye" in user_input or "exit" in user_input:
            speak("Goodbye BOSS!")
            break
        elif "search" in user_input or "look up" in user_input:
            search_query = user_input.replace("search", "").replace("look up", "").strip()
            if search_query:
                speak(f"Searching for {search_query} on the web.")
                open_browser_and_search(search_query)
            else:
                speak("Sure, what would you like me to search for?")
        elif "open" in user_input:
            app_name = user_input.replace("open", "").strip()
            if app_name:
                speak(f"Opening {app_name}.")
                open_application(app_name)
            else:
                speak("Sure, what application would you like me to open?")
        elif "close" in user_input:
            app_name = user_input.replace("close", "").strip()
            if app_name:
                speak(f"Closing {app_name}.")
                close_application(app_name)
            else:
                speak("Sure, what application would you like me to close?")
        elif "play music" in user_input or "music" in user_input:
            play_music()
        elif "stop music" in user_input:
            stop_music()
        elif "change music" in user_input or "next music" in user_input:
            change_music()
        else:
            conversation_history += f"\nUser: {user_input}\nJarvis:"
            chatgpt_response = get_chatgpt_response(conversation_history)
            speak(chatgpt_response)
            conversation_history += f" {chatgpt_response}\nJarvis:"

if __name__ == "__main__":
    main()
