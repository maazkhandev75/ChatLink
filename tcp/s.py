import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

TCP_IP_ADDRESS = "127.0.0.1"  # Server's IP
TCP_PORT_NO = 7777  # Server's port (on which it listens for communication)
server_socket.bind((TCP_IP_ADDRESS, TCP_PORT_NO))
server_socket.listen(5)  # Allow up to 5 clients to connect
print('SERVER IS RUNNING....')

user_mapping = {}  # DB (dictionary) to store registered users' names with their addresses
client_sockets = {}  # Dictionary to map usernames to client sockets
sockets_lock = threading.Lock() # to ensure thread safety when accessing and modifying shared resources, particularly the client_sockets dictionary


def handle_client(client_socket, addr):
    while True:
        try:
            dataRecv = client_socket.recv(1024)
            messageRecv = dataRecv.decode('utf-8')

            if messageRecv == "EXIT":
                print(f"Client {addr} requested exit")
                break  # Client wants to disconnect, so exit the loop
            

            if messageRecv.startswith("REGISTER:"):
                username = messageRecv.split(":", 1)[1].strip()
                user_mapping[username] = addr
                client_sockets[username] = client_socket  # Keep track of client socket by username
                print(f"Registered {username} from {addr}")

            elif messageRecv.startswith("TO:"):
                if ';' in messageRecv:
                    _, rest = messageRecv.split("TO:", 1)
                    target_user, user_message = rest.split(";", 1)
                    target_user = target_user.strip()
                    user_message = user_message.strip()

                    if target_user in client_sockets:
                        rec_socket = client_sockets[target_user]  # Get recipient's socket

                        for user, address in user_mapping.items():
                            if address == addr:
                                sending_user = user
                                break

                        # Send the message directly to the recipient's socket
                        rec_socket.sendall(f"Message from {sending_user} ({addr}): {user_message}".encode('utf-8'))
                        print(f"Forwarded message from {sending_user} to {target_user}: {user_message}")
                    else:
                        print(f"User {target_user} not found.")
                        client_socket.sendall(f"User {target_user} not found in server DB.".encode('utf-8'))
                else:
                    print("Incorrect format!")
                    client_socket.sendall(f"Incorrect format!".encode('utf-8'))
        except (ConnectionResetError, BrokenPipeError):
            break  # Connection forcibly closed by the client

    client_socket.close()  # Close client connection
    # Remove client from mappings when disconnected
    with sockets_lock:
        for user, socket_ in client_sockets.items():
            if socket_ == client_socket:
                del client_sockets[user]
                print(f"Removed {user} from active clients.")
                break


def broadcast_message():
    """Thread to listen for broadcast messages from the server."""
    print("you can enter a message to broadcast to all clients!\n")
    
    while True:
        broadcast_msg = input().strip()

        with sockets_lock:
            for username, client_socket in client_sockets.items():
                try:
                    client_socket.sendall(f"Broadcast from Server: {broadcast_msg}".encode('utf-8'))
                    print(f"Broadcast sent to {username}")
                except Exception as e:
                    print(f"Error sending broadcast to {username}: {e}")


def accept_clients():
    """Thread to accept new clients."""
    while True:
        client_socket, addr = server_socket.accept()  # Accept new client connection
        print(f"New connection from {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.daemon = True
        client_thread.start()


# Start accepting clients in a separate thread
accept_thread = threading.Thread(target=accept_clients)
accept_thread.daemon = True
accept_thread.start()

# Start broadcasting thread
broadcast_thread = threading.Thread(target=broadcast_message)
broadcast_thread.daemon = True
broadcast_thread.start()

# Keep the main thread alive
while True:
    pass
