To set up the clean `README.md` for **Task 5 (Chat Application)** directly without copy-paste lag or broken formatting, run this command in your PowerShell terminal at `C:\Users\vijay\OIBSIP`:

````powershell
Set-Content -Path .\Python-Task5-ChatApplication\README.md -Value @'
# Python Task 5 - Chat Application

## Overview

A simple client-server chat application developed in Python as part of the Oasis Infobyte Python Programming Internship — Task 5.

The application demonstrates network communication using TCP sockets. A central server manages concurrent client connections, allowing multiple clients to exchange real-time messages.

This project was completed at the Beginner tier using pure Python standard libraries.

## Features

- **TCP Client-Server Communication:** Reliable socket-based messaging.
- **Multi-Client Support:** Handles multiple concurrent client connections using threads.
- **Real-Time Bidirectional Messaging:** Instant broadcast of chat messages.
- **Timestamped Messages:** Appends real-time system timestamps to incoming chats.
- **Event Notifications:** Notifies active users when clients join or disconnect.
- **Graceful Disconnection:** Clean exit handling on normal quit or `Ctrl+C` interrupts.
- **Duplicate Username Handling:** Validates handles during connection initialization.
- **Zero Third-Party Dependencies:** Built entirely with Python standard libraries (`socket`, `threading`, `datetime`).

## Technologies Used

- **Python 3.13**
- **socket** — Low-level network interface for TCP connections
- **threading** — Concurrent execution handling for clients
- **datetime** — Real-time timestamp generation

## Architecture

### Server
Listens for incoming TCP connections on `127.0.0.1:5000`. When a client connects, the server spawns a dedicated handler thread. Received messages are broadcast across all active client sockets.

### Client
Connects to the server, completes username registration, and spawns a background receiving thread so incoming messages display asynchronously while the user types.

## Project Structure

```text
Python-Task5-ChatApplication/
│
├── src/
│   ├── server.py
│   └── client.py
├── screenshots/
│   ├── server_running.png
│   ├── two_clients_chatting.png
│   └── client_disconnect.png
├── .gitignore
├── requirements.txt
└── README.md

````

## Requirements

- Python 3.13 or compatible Python 3 environment
- Two or more terminal windows to simulate chat clients
- _No third-party packages required._

## Installation & Setup

1. **Navigate to the project directory:**

```powershell
cd .\Python-Task5-ChatApplication

```

2. **Virtual Environment Setup (Optional):**

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1

```

## Running the Application

### 1. Start the Server

Open Terminal 1 and launch the server:

```powershell
python .\src\server.py

```

### 2. Start Client 1

Open Terminal 2 and launch the first client:

```powershell
python .\src\client.py

```

_Enter a username when prompted (e.g., `Alice`)._

### 3. Start Client 2

Open Terminal 3 and launch a second client:

```powershell
python .\src\client.py

```

_Enter a unique username when prompted (e.g., `Bob`)._

## Example Terminal Output

```text
 Alice: Hello Bob!
 Bob: Hello Alice!

```

## Technical & Disconnect Handling

- **Timestamping:** Every broadcast message is tagged by the server at the moment of receipt.
- **Thread Safety:** Separate socket threads prevent blocking audio/input streams during concurrent broadcasts.
- **Signal & Exception Trapping:** Unexpected disconnects drop invalid socket descriptors gracefully to prevent server crashes.

## Learning Outcomes

This project provided practical experience with:

- TCP socket programming and network protocols.
- Multi-threaded client-server architecture.
- Concurrent message broadcasting.
- Asynchronous stream handling and socket lifecycle management.

## Project Status

**Completed** — Oasis Infobyte Python Programming Internship (Task 5 - Beginner Tier).
'@

````

---

### **Final Step: Stage, Commit, and Push Task 5**

After creating the file, run these commands from `C:\Users\vijay\OIBSIP` to commit your final task and complete the internship repository:

```powershell
# 1. Stage Task 5
git add .\Python-Task5-ChatApplication

# 2. Verify staged files (Confirm NO secret or virtual environment files appear)
git diff --cached --name-only

# 3. Commit Task 5
git commit -m "Complete Task 5: Multi-Client Chat Application with documentation and screenshots"

# 4. Push final updates to GitHub
git push origin main

````
