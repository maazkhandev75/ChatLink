import socket
import threading

# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_IP_ADDRESS = "127.0.0.1"  # Server's IP
UDP_PORT_NO = 7777  # Server's port
server_socket.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
print("SERVER IS RUNNING...")

user_mapping = {}  # Store registered users and their addresses


# Function for handling broadcast messages
def broadcast_messages():
    print("you can enter a message to broadcast to all clients!")
    while True:
        # Here you define what message the server broadcasts
        broadcast_message = input()
        # Send the broadcast message to all registered users
        for username, user_addr in user_mapping.items():
            server_socket.sendto(f"Broadcast: {broadcast_message}".encode('utf-8'), user_addr)
        print(f"Broadcasted: {broadcast_message}")


# Main function for handling client messages
def handle_clients():
    while True:
        
        data_recv, addr = server_socket.recvfrom(1024)  # Receive data from clients
        message_recv = data_recv.decode('utf-8')

        if message_recv == "EXIT":
            print(f"Client {addr} requested exit")
            # No need to break the loop here; we will continue listening to other clients
            continue  # Simply continue to the next client    

        if message_recv.startswith("REGISTER:"):
            username = message_recv.split(":", 1)[1].strip()
            user_mapping[username] = addr
            print(f"Registered {username} from {addr}")

        elif message_recv.startswith("TO:"):
            if ";" in message_recv:
                _, rest = message_recv.split("TO:", 1)
                target_user, user_message = rest.split(";", 1)
                target_user = target_user.strip()
                user_message = user_message.strip()

                if target_user in user_mapping:
                    rec_address = user_mapping[target_user]

                    for user, address in user_mapping.items():
                        if address == addr:
                            sending_user = user
                            break

                    server_socket.sendto(
                        f"Message from {sending_user} {addr}: {user_message}".encode('utf-8'), rec_address
                    )
                    print(f"Forwarded message from {sending_user} to {target_user}: {user_message}")
                else:
                    print(f"User {target_user} not found.")
                    server_socket.sendto(
                        f"User {target_user} not found in server DB.".encode('utf-8'), addr
                    )
            else:
                print("Incorrect format!")
                server_socket.sendto(f"Incorrect format!".encode('utf-8'), addr)


# Start the server threads
client_thread = threading.Thread(target=handle_clients, daemon=True)
broadcast_thread = threading.Thread(target=broadcast_messages, daemon=True)

client_thread.start()
broadcast_thread.start()

client_thread.join()
broadcast_thread.join()

print("Server shutting down...")
