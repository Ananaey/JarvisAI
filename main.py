import os
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai
import datetime
import pyjokes
import wikipedia
import webbrowser
import subprocess

# Set your Gemini Pro API key here
API_KEY = 'YOUR API KEY FOR GEMINI'

# Configure the API key for Gemini
genai.configure(api_key=API_KEY)

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize history to store previous interactions
history = []

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for voice commands
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you repeat?")
        return None
    except sr.RequestError:
        speak("Sorry, I couldn't reach the speech recognition service.")
        return None

# Function to execute commands based on user input
def execute_command(command, conversation_history):
    if 'time' in command:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {strTime}")
        conversation_history.append({"role": "assistant", "content": f"The time is {strTime}"})
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        speak(joke)
        conversation_history.append({"role": "assistant", "content": joke})
    elif 'wikipedia' in command:
        speak("Searching Wikipedia...")
        query = command.replace("wikipedia", "").strip()
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)
            conversation_history.append({"role": "assistant", "content": results})
        except wikipedia.exceptions.DisambiguationError as e:
            speak("Multiple results found. Please specify.")
            conversation_history.append({"role": "assistant", "content": "Multiple results found. Please specify."})
        except wikipedia.exceptions.PageError as e:
            speak("No results found.")
            conversation_history.append({"role": "assistant", "content": "No results found."})
    elif 'open youtube' in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")
        conversation_history.append({"role": "assistant", "content": "Opening YouTube"})
    elif 'open google' in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")
        conversation_history.append({"role": "assistant", "content": "Opening Google"})
    elif 'open stack overflow' in command:
        webbrowser.open("https://stackoverflow.com")
        speak("Opening Stack Overflow")
        conversation_history.append({"role": "assistant", "content": "Opening Stack Overflow"})
    elif 'open notepad' in command:
        subprocess.Popen(['notepad.exe'])
        speak("Opening Notepad")
        conversation_history.append({"role": "assistant", "content": "Opening Notepad"})
    elif 'shutdown' in command:
        os.system("shutdown /s /t 1")
        speak("Shutting down the system")
        conversation_history.append({"role": "assistant", "content": "Shutting down the system"})
    else:
        # If the command doesn't match any specific action, interact with Gemini
        instruction = "Act as JARVIS from Iron Man, keep your responses creative, concise, sweet and polite"
        conversation_history.append({"role": "user", "content": command})
        response = chat.send_message(instruction + command).text
        speak(response)
        conversation_history.append({"role": "assistant", "content": response})
    return conversation_history

if __name__ == "__main__":
    sample = 'Allow me to introduce myself '
    speak(sample)

    sample='I am Jarvis a virtual artificial intelligence'
    speak(sample)

    sample = 'and I am here to assist you with a variety of tasks as best I can, 24 hours a day 7 days a week'
    speak(sample)

    sample = 'importing all preferences from home interface, systems are now fully operational '
    speak(sample)

    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat()
    conversation_history = [{"role": "system", "content": "You are a virtual assistant."}]

    while True:
        command = listen()
        if command:
            if 'exit' in command or 'turn off' in command:
                speak("Turning off. Goodbye Sir!")
                break
            else:
                conversation_history = execute_command(command, conversation_history)
        else:
            speak("I didn't hear you. Could you please say that again?")
