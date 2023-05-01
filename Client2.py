import socket
import threading

# Create the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8000))

# Define the receive thread function
def receive(client_socket):
    while True:
        message = client_socket.recv(1024).decode()
        print(message)
# Start the receive thread
receive_thread = threading.Thread(target=receive, args=(client_socket,))
receive_thread.start()

# Function to get user input and send message to server
def send_message(sock, username):
    while True:
        recipient = input("Enter the recipient: ")
        message = input("Enter the message: ")
        if recipient == "server" and message == "list":
            msg = "list"
            sock.send(msg.encode("utf-8"))
        elif message == "quit":
            sock.close()
            break
        else:
            msg = f"{recipient}:{username}:{message}"
            sock.send(msg.encode("utf-8"))


# Get the user's username
username = input("Enter your username: ")

# Send the user's username to the server
client_socket.send(username.encode())

# Start the send message thread
send_thread = threading.Thread(target=send_message, args=(client_socket, username))
send_thread.start()
    
# Wait for the send thread to complete
send_thread.join()
