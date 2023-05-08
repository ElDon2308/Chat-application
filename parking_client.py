import socket
import threading

# Create the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8000))

# Create a list of parking locations
parking_locations = {'Parking Location 1': True, 'Parking Location 2': True, 'Parking Location 3': True}

def parse_message(message):
    parts = message.split(":")
    recipient = parts[0]
    if len(parts) > 1:
        sender = parts[1]
    else:
        sender = ""
    if len(parts) > 2:
        content = parts[2]
    else:
        content = ""
    if len(parts) > 3:
        spot = parts[3]
    else:
        spot = ""
    return recipient, sender, content, spot

# Define the update function
def update_parking_location(location, availability):
    parking_locations[location] = availability

def reserve_spot(spot, sender, recipient):
    if spot in parking_locations and parking_locations[spot]:
        parking_locations[spot] = False
        update_parking_location(spot, False) # call the update function
        response = f"{spot} has been reserved"
        # Send confirmation message to the client that made the reservation
        msg = f"{sender}:{recipient}:{response}:{spot}"
        client_socket.send(msg.encode("utf-8"))
    else:
        response = f"{spot} is not available"
        # Send the updated list of parking locations to the client
        response += "\n\nAvailable parking locations\n"
        for location in parking_locations:
            response += f"\n{location} {parking_locations[location]}"
        msg = f"{sender}:{recipient}:{response}" 
        client_socket.send(msg.encode())


# Define the receive thread function
def receive(client_socket):
    # parking location reset
    for location in parking_locations:
        parking_locations[location] = True
    while True:
        username = "Parking"
        message = client_socket.recv(1024).decode()
        recipient, sender, content, spot = parse_message(message)
        print(message)
        if content.startswith('list'):
            response = ""
            response = response + ("Available parking locations \n")
            for location in parking_locations:
                response = response + "\n" + location + str(parking_locations[location])
            msg = f"{sender}:{recipient}:{response}"
            client_socket.send(msg.encode("utf-8"))
        elif content.startswith('reserve'):
            print(f"Received reserve command for {spot}")
            reserve_spot(spot, sender, recipient)
        else:
            response = f"Invalid command: {content}"
            # Send the updated list of parking locations to the client
            response += "\n\nAvailable parking locations\n"
            for location in parking_locations:
                response += f"\n{location} {parking_locations[location]}"
            msg = f"{sender}:{recipient}:{response}" 
            client_socket.send(msg.encode())

# Start the receive thread
receive_thread = threading.Thread(target=receive, args=(client_socket,))
receive_thread.start()

# Send the user's username to the server
client_socket.send("Parking".encode())