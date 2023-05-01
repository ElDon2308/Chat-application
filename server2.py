import socket
import threading

#line 4-12 open a server socket on port 8000 and waiting for a connection
# Create the server socket (this uses TCP protocol)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a public host and port
server_socket.bind(('localhost', 8000))

# Listen for incoming connections
server_socket.listen()

# Define a dictionary to store the connected clients
clients = {}

# Server would act as a moderator to connect clients to each others
def handle_client(client_socket, client_address):
    # Receive the client's username
    username = client_socket.recv(1024).decode()
    print(f"{username} connected from {client_address}")

    # Add the client to the dictionary
    #clients[client_socket] = username
    # we assume that usernames are unique.
    clients[username]=client_socket

    # Continuously receive and broadcast messages
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(f"Received message: {message}")

            # Split the message to extract the recipient and message content
            parts = message.split(":")
            recipient = parts[0]
            if recipient=="server":
                # server needs to handle that
                print("Message is for the server"+message)
            else:
                if recipient in clients:    
                    clients[recipient].send(message.encode())
             
        except Exception as e:
            print(f"Error: {e}")
            # If an exception is raised, remove the client from the dictionary and close the connection
            print(f"{clients[client_socket]} disconnected")
            del clients[client_socket]
            client_socket.close()
            break


# Function to accept incoming connections
def accept_connections():
    print("Waiting for connections...")
    while True:
        # Accept an incoming connection
        client_socket, client_address = server_socket.accept()

        # Create a thread to handle the connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Start accepting connections
accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()
