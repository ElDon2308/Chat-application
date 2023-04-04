import socket
import threading

# Create the server socket (this uses TCP protocol)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a public host and port
server_socket.bind(('localhost', 8000))

# Listen for incoming connections
server_socket.listen()

# Define a dictionary to store the connected clients
clients = {}

# Create a list of parking locations
parking_locations = {'Parking Location 1': True, 'Parking Location 2': True, 'Parking Location 3': True}

# Function to handle incoming messages from clients
# Function to handle incoming messages from clients
def handle_client(client_socket, client_address):
    # Receive the client's username
    username = client_socket.recv(1024).decode()
    print(f"{username} connected from {client_address}")

    # Add the client to the dictionary
    clients[client_socket] = username

    # Continuously receive and broadcast messages
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(f"Received message: {message}")

            if message == "list":
                # Send list of parking locations to client if requested
                available_spots = [spot for spot, status in parking_locations.items() if status]
                response = "Available Parking locations: " + ", ".join(available_spots)
                client_socket.send(response.encode())
                # Wait for acknowledgement from the client
                ack = client_socket.recv(1024).decode()
                if ack != "List received":
                    print(f"Error: acknowledgement not received from {username}")
            else:
                # Split the message to extract the recipient and message content
                parts = message.split(":")
                recipient = parts[1]
                content = parts[2]

                # Reserve a parking location for the client
                if content.startswith("reserve:"):
                    spot = content.split(":")[1]
                    if spot in parking_locations and parking_locations[spot]:
                        parking_locations[spot] = False
                        response = f"{spot} has been reserved"
                    else:
                        response = f"{spot} is not available"
                    client_socket.send(response.encode())

        except Exception as e:
            print(f"Error: {e}")
            # If an exception is raised, remove the client from the dictionary and close the connection
            print(f"{clients[client_socket]} disconnected")
            del clients[client_socket]
            client_socket.close()
            break



# Function to accept incoming connections
def accept_connections():
    print("Waiting for connections")
    while True:
        # Accept an incoming connection
        client_socket, client_address = server_socket.accept()

        # Create a thread to handle the connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Start accepting connections
accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()
