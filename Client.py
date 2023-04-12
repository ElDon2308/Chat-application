import socket
import threading

# Create the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8000))

# Define the receive thread function
def receive(client_socket):
    while True:
        message = client_socket.recv(1024).decode()
        if message.startswith('Available Parking locations: '):
            parking_locations = message.split(':')[1].split(', ')
            print("Available parking locations:")
            for location in parking_locations:
                print(location)
        else:
            print(message)

# Start the receive thread
receive_thread = threading.Thread(target=receive, args=(client_socket,))
receive_thread.start()


#reserver a parking location
def resSpot(sock):
    spot= input("What spot would you like to reserve? :")
    msg = f"reserve:{spot}"
    sock.send(msg.encode("utf-8"))
    
    #waiting for ack from server
    response= sock.recv(1024).decode("utf-8")
    print (response)
    
# Function to get user input and send message to server
def send_message(sock, username):
    while True:
        recipient = input("Enter the recipient: ")
        message = input("Enter the message: ")
        if recipient == "server" and message == "list":
            msg = "list"
            sock.send("List received".encode("utf-8")) 
            sock.send(msg.encode("utf-8"))     
        elif message == "reserve":
            resSpot(sock)
        elif message == "quit":
            sock.close()
            break
        else:
            msg = f"{username}:{recipient}:{message}"
            sock.send(msg.encode("utf-8"))
    
    # Wait for acknowledgement that the message was sent successfully
    response = sock.recv(1024).decode()
    if response != "Message sent":
        print("Error sending message")

#reserve the parking space 
while True:
    # Get the user's username
    username = input("Enter your username: ")

    # Send the user's username to the server
    client_socket.send(username.encode())

    # Start the send message thread
    send_thread = threading.Thread(target=send_message, args=(client_socket, username))
    send_thread.start()
    
    # Wait for the send thread to complete
    send_thread.join()
