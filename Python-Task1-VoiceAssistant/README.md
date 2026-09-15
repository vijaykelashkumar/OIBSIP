````markdown
# Python Voice Assistant

## Overview

A command-line voice assistant developed as part of the Oasis Infobyte Python Programming Internship — Task 1.

The application listens to spoken commands through the microphone, converts speech to text, processes the requested command, and responds using text-to-speech. The project focuses on practical Python programming, speech recognition, text-to-speech, browser automation, error handling, and modular program design.

## Features

- **Voice Input:** Microphone capture powered by Google Speech Recognition.
- **Speech Synthesis:** Offline text-to-speech audio feedback.
- **Dynamic Greetings:** Time-aware salutations (morning, afternoon, evening, night).
- **Time & Date Queries:** Real-time system time and formatted date reporting.
- **Browser Automation:** Direct shortcuts to launch Google, YouTube, and Chrome History.
- **Web Search Integration:** Voice-driven web searching with query parameter formatting.
- **Robust Error Handling:** Recovers from silent timeouts, unrecognized speech, service disconnects, and TTS errors.
- **Flexible Session Exit:** Multi-phrase exit commands ("exit", "quit", "goodbye", "shut down", "close yourself").

## Technologies Used

- Python 3.13
- SpeechRecognition
- PyAudio
- pyttsx3
- datetime
- webbrowser

## Project Structure

```text
Python-Task1-VoiceAssistant/
│
├── src/
│   └── assistant.py
├── screenshots/
├── .gitignore
├── requirements.txt
└── README.md
```
````

## Installation

1. **Create a virtual environment:**

```powershell
py -3.13 -m venv .venv

```

2. **Activate the environment:**

```powershell
.\.venv\Scripts\Activate.ps1

```

3. **Install the dependencies:**

```powershell
pip install -r requirements.txt

```

## Running the Application

Run the assistant script:

```powershell
python .\src\assistant.py

```

The assistant starts with a time-aware greeting and waits for spoken commands.

## Example Commands

- _"Hello"_ / _"Jarvis"_
- _"What is the time?"_
- _"What is today's date?"_
- _"Search for Python programming"_
- _"Search machine learning"_
- _"Open Google"_
- _"Open YouTube"_
- _"Open history"_
- _"Goodbye"_ / _"Exit"_ / _"Shut down"_

## Example Output

```text
Listening...
You said: what is the time
Assistant: The current time is 04:17 PM.

Listening...
You said: what is the date today
Assistant: Today is Tuesday, 15 September 2026.

```

The assistant also speaks the responses aloud through the computer's audio output.

## Error Handling

The application gracefully handles:

- No speech detected within the listening period
- Speech that cannot be understood
- Speech-recognition service errors
- Text-to-speech execution failures
- Unsupported voice commands

The assistant continues running smoothly rather than terminating unexpectedly when recoverable errors occur.

## Development Notes

- The project was developed and tested incrementally.
- A separate Python virtual environment was used to isolate dependencies from other internship tasks.
- **Windows SAPI5 Fix:** Reusing a single global `pyttsx3` engine instance caused audio buffer locking on Windows, leading to silent responses in the terminal. The implementation was refactored to instantiate and release the SAPI5 engine per response.
- **Intent Parsing:** Command-processing logic was refined to use phrase-matching for greetings and explicit keyword checking for exit commands.
- **URL Parameter Formatting:** Web search queries are sanitized so multi-word searches map cleanly to Google search URL parameters.

## Learning Outcomes

This project provided practical experience with:

- Python functions and control flow
- Exception handling and input sanitization
- Virtual environments and package management
- Speech recognition and TTS audio APIs
- Browser automation
- Code modularization and Git version control

## Resources and References

- Oasis Infobyte task documentation and tutorials on `SpeechRecognition` and `pyttsx3`.
- Official PyPI library documentation for `SpeechRecognition` audio handling.
- Microsoft SAPI5 documentation for Windows text-to-speech event handling.

## Screenshots

Screenshots demonstrating the working application are located in the `screenshots/` directory.

## Project Status

**Completed** — Oasis Infobyte Python Programming Internship (Task 1).

```

```
