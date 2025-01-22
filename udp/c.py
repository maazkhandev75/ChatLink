import socket
import threading

# we have made separate thread for receiving incoming messages simultaneously!

def listen_for_messages(client_socket):
    while True:
        try:
            response, _ = client_socket.recvfrom(1024)
            print(f"{response.decode('utf-8')}")
        except BlockingIOError:
            # No data available, continue waiting
            continue
        except OSError:
            # Socket is closed, exit the thread
            print("Connection is lost or closed.")
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_IP_ADDRESS = "127.0.0.1" # Server's IP
UDP_PORT_NO = 7777 # Server's port ( the port on which the server is listing on)
# note that that the Client's port will be random provided by OS on runtime ( as we can see the random ports in addresses of clients shown in terminal)

username = input("ENTER YOUR NAME TO REGISTER IN server's DB: ")
client_socket.sendto(f"REGISTER:{username}".encode('utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
print("YOU CAN SEND MESSAGE TO SOME USER ( FORMAT: <recipient_username>;<message> ) and you can Input EXIT to close your connection")


# Start listening for incoming messages in a separate thread
listener_thread = threading.Thread(target=listen_for_messages, args=(client_socket,), daemon=True)
listener_thread.start()

while True:
    msg = input()
    if msg.lower() == 'exit':
        client_socket.sendto("EXIT".encode('utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))  # Send EXIT to server
        print("Exiting...")
        client_socket.close()  # Close the connection
        break
    client_socket.sendto(f"TO:{msg}".encode('utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
