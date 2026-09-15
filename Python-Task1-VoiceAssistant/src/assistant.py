import webbrowser
from datetime import datetime
from urllib.parse import quote_plus

import pyttsx3
import speech_recognition as sr


def speak(text):
    """Speak a response and display it in the terminal."""

    print(f"Assistant: {text}")

    try:
        engine = pyttsx3.init("sapi5")
        engine.setProperty("rate", 170)
        engine.setProperty("volume", 1.0)

        engine.say(text)
        engine.runAndWait()
        engine.stop()

    except Exception as error:
        print(f"[TTS Error]: {error}")


def get_greeting():
    """Return a greeting based on the current time."""

    hour = datetime.now().hour

    if 5 <= hour < 12:
        return "Good morning"

    if 12 <= hour < 17:
        return "Good afternoon"

    if 17 <= hour < 22:
        return "Good evening"

    return "Good night"


recognizer = sr.Recognizer()


def listen():
    """Listen through the microphone and convert speech to text."""

    with sr.Microphone() as source:
        print("\nListening...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=0.8
        )

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
        speak("Sorry sir, could you repeat that?")
        return ""

    except sr.RequestError:
        speak(
            "Sorry sir, I can't help right now because "
            "the speech service is unavailable."
        )
        return ""


def search_web(topic):
    """Open a Google search for the requested topic."""

    speak(f"Searching the web for {topic}.")

    search_url = (
        "https://www.google.com/search?q="
        + quote_plus(topic)
    )

    webbrowser.open(search_url)


def process_command(command):
    """Interpret a recognized command and perform the requested action."""

    if not command:
        return True

    words = set(command.split())

    greeting_words = {"hello", "hi", "hey", "jarvis"}

    if words.intersection(greeting_words):
        speak("Hello, sir! How can I help you?")
        return True

    if "time" in words:
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")
        return True

    if "date" in words or "today" in words:
        current_date = datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today is {current_date}.")
        return True

    if "open google" in command:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")
        return True

    if "open youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
        return True

    if "open history" in command:
        speak("Opening your web history.")
        webbrowser.open("chrome://history/")
        return True

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

    exit_phrases = [
        "exit",
        "quit",
        "goodbye",
        "good night",
        "close yourself",
        "shut down",
    ]

    if (
        command in exit_phrases
        or any(
            command.startswith(phrase + " ")
            or command.endswith(" " + phrase)
            or f" {phrase} " in command
            for phrase in exit_phrases
        )
        or "stop" in words
    ):
        hour = datetime.now().hour

        if 22 <= hour or hour < 5:
            speak("Good night, sir!")
        else:
            speak("Goodbye! Have a great day.")

        return False

    speak(
        "I heard you, but I do not know how to perform "
        "that command yet."
    )

    return True


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