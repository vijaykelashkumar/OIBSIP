import socket
import threading
from datetime import datetime


HOST = "127.0.0.1"
PORT = 5000

clients = {}
lock = threading.Lock()


def timestamp():
    """Return the current time for chat messages."""
    return datetime.now().strftime("%H:%M")


def broadcast(message, sender=None):
    """Send a message to all connected clients except the sender."""

    with lock:
        for client in list(clients):
            if client != sender:
                try:
                    client.send(message.encode("utf-8"))
                except OSError:
                    remove_client(client)


def remove_client(client):
    """Remove a client from the active client list."""

    with lock:
        username = clients.pop(client, None)

    try:
        client.close()
    except OSError:
        pass

    if username:
        message = f"[{timestamp()}] {username} left the chat."
        print(message)
        broadcast(message)


def handle_client(client, address):
    """Handle communication with one connected client."""

    try:
        username = client.recv(1024).decode("utf-8").strip()

        if not username:
            username = f"{address[0]}:{address[1]}"

        with lock:
            clients[client] = username

        joined_message = f"[{timestamp()}] {username} joined the chat."
        print(joined_message)
        broadcast(joined_message, client)

        client.send(
            "Connected to the chat server. Type 'exit' to leave.".encode("utf-8")
        )

        while True:
            data = client.recv(1024)

            if not data:
                break

            message = data.decode("utf-8").strip()

            if not message:
                continue

            if message.lower() == "exit":
                break

            formatted_message = f"[{timestamp()}] {username}: {message}"

            print(formatted_message)
            broadcast(formatted_message, client)

    except (ConnectionResetError, ConnectionAbortedError, OSError):
        pass

    finally:
        remove_client(client)


def start_server():
    """Start the chat server."""

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen()

    print("=" * 50)
    print("             CHAT SERVER")
    print("=" * 50)
    print(f"Listening on {HOST}:{PORT}")
    print("Waiting for clients...")
    print("=" * 50)

    try:
        while True:
            client, address = server.accept()

            print(f"New connection from {address}")

            thread = threading.Thread(
                target=handle_client,
                args=(client, address),
                daemon=True
            )

            thread.start()

    except KeyboardInterrupt:
        print("\nServer shutting down...")

    finally:
        with lock:
            for client in list(clients):
                try:
                    client.close()
                except OSError:
                    pass

        server.close()


if __name__ == "__main__":
    start_server()