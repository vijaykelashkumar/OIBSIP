import socket
import threading


HOST = "127.0.0.1"
PORT = 5000


def receive_messages(client):
    """Continuously receive messages from the server."""

    while True:
        try:
            message = client.recv(1024)

            if not message:
                print("\nDisconnected from the server.")
                break

            print(f"\n{message.decode('utf-8')}")

        except (ConnectionResetError, ConnectionAbortedError, OSError):
            print("\nConnection to the server was lost.")
            break


def start_client():
    """Start the chat client."""

    username = input("Enter your username: ").strip()

    while not username:
        print("Username cannot be empty.")
        username = input("Enter your username: ").strip()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))

        client.send(username.encode("utf-8"))

        thread = threading.Thread(
            target=receive_messages,
            args=(client,),
            daemon=True
        )

        thread.start()

        print("\nConnected to the chat server.")
        print("Type your message and press Enter.")
        print("Type 'exit' to leave.\n")

        while True:
            message = input()

            if not message.strip():
                continue

            client.send(message.encode("utf-8"))

            if message.lower() == "exit":
                break

    except ConnectionRefusedError:
        print(
            "\nUnable to connect to the chat server."
            "\nMake sure server.py is running first."
        )

    except (ConnectionResetError, ConnectionAbortedError, OSError):
        print("\nThe connection to the server was lost.")

    finally:
        client.close()
        print("Chat client closed.")


if __name__ == "__main__":
    start_client()