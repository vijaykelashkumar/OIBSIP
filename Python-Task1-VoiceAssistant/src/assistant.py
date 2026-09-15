import os
import webbrowser
from datetime import datetime
import pyttsx3
import speech_recognition as sr

# -----------------------------------
# Text-to-Speech Setup
# -----------------------------------

def speak(text):
    """Speak the given text using pyttsx3 and display it in terminal."""
    print(f"Assistant: {text}")

    try:
        # Initialize engine inside function to ensure fresh COM interface on Windows
        engine = pyttsx3.init("sapi5")
        engine.setProperty("rate", 170)
        engine.setProperty("volume", 1.0)

        # Clear any pending speech queue and speak
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"[TTS Error]: {e}")


# -----------------------------------
# Greeting
# -----------------------------------

def get_greeting():
    """Return a greeting based on current time."""
    hour = datetime.now().hour

    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 22:
        return "Good evening"
    else:
        return "Good night"


# -----------------------------------
# Speech Recognition Setup
# -----------------------------------

recognizer = sr.Recognizer()


def listen():
    """Listen through the microphone and convert speech into text."""
    with sr.Microphone() as source:
        print("\nListening...")

        # Adjust microphone sensitivity to ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=0.8)

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""

    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower().strip()

    except sr.UnknownValueError:
        speak("Sorry sir, could you redefine your statement?")
        return ""

    except sr.RequestError:
        speak("Sorry sir, I can't help right now because the speech service is unavailable.")
        return ""


# -----------------------------------
# Web Search
# -----------------------------------

def search_web(topic):
    """Open a Google search for the given topic."""
    speak(f"Searching the web for {topic}.")
    search_url = f"https://www.google.com/search?q={topic.replace(' ', '+')}"
    webbrowser.open(search_url)


# -----------------------------------
# Command Processing
# -----------------------------------

def process_command(command):
    """Process the recognized voice command."""
    if not command:
        return True

    # Greeting / Activation check
    if any(word in command for word in ["hello", "hi", "hey", "jarvis"]):
        speak("Hello, sir! How can I help you?")
        return True

    # Current time
    if "time" in command:
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")
        return True

    # Current date
    if "date" in command or "today" in command:
        current_date = datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today is {current_date}.")
        return True

    # Open Google
    if "open google" in command:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")
        return True

    # Open YouTube
    if "open youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
        return True

    # Open Chrome History
    if "open history" in command:
        speak("Opening your web history.")
        webbrowser.open("chrome://history/")
        return True

    # Search web
    if command.startswith("search for"):
        topic = command.replace("search for", "", 1).strip()
        if topic:
            search_web(topic)
        else:
            speak("Please tell me what you want me to search for.")
        return True

    if command.startswith("search"):
        topic = command.replace("search", "", 1).strip()
        if topic:
            search_web(topic)
        else:
            speak("Please tell me what you want me to search for.")
        return True

    # Exit keywords
    exit_keywords = ["exit", "quit", "stop", "goodbye", "good night", "close yourself", "shut down"]
    if any(keyword in command for keyword in exit_keywords):
        hour = datetime.now().hour
        if 22 <= hour or hour < 5:
            speak("Good night, sir!")
        else:
            speak("Goodbye! Have a great day.")
        return False

    # Default fallback
    speak("I heard you, but I do not know how to perform that command yet.")
    return True


# -----------------------------------
# Main Program
# -----------------------------------

def main():
    """Start and run the voice assistant."""
    greeting = get_greeting()

    speak(
        f"{greeting}, sir. How can I assist you? "
        "You can ask for the time or date, search the web, "
        "open Google, or say exit."
    )

    while True:
        command = listen()
        if not process_command(command):
            break


if __name__ == "__main__":
    main()