import socket
import threading

# Separate thread for receiving incoming messages
def listen_for_messages(client_socket):
    while True:
        try:
            response = client_socket.recv(1024)
            if not response:  # Socket is closed (empty response)
                print("Connection closed by the server.")
                break
            print(f"{response.decode('utf-8')}")
        except (ConnectionResetError, socket.error):
            print("Connection is lost or closed")
            break  # Server closed connection or other socket error

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

TCP_IP_ADDRESS = "127.0.0.1"  # Server's IP
TCP_PORT_NO = 7777  # Server's port

client_socket.connect((TCP_IP_ADDRESS, TCP_PORT_NO))  # Connect to the server

username = input("ENTER YOUR NAME TO REGISTER IN server's DB: ")
client_socket.sendall(f"REGISTER:{username}".encode('utf-8'))

print("YOU CAN SEND MESSAGE TO SOME USER ( FORMAT: <recipient_username>;<message> )\nInput EXIT to close your connection")

# Start listening for incoming messages in a separate thread
listener_thread = threading.Thread(target=listen_for_messages, args=(client_socket,), daemon=True)
listener_thread.start()

while True:
    msg = input()
    if msg.lower() == 'exit':
        client_socket.sendall(f"EXIT".encode('utf-8'))
        print("Exiting...")
        client_socket.close()
        break
    client_socket.sendall(f"TO:{msg}".encode('utf-8'))
