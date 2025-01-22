# ChatLink 🌐

**ChatLink** is a chat application implemented in two separate versions: one using the **TCP** protocol and the other using the **UDP** protocol. It allows users to register, send private messages, and broadcast announcements through a simple command-line interface.

---

## 🚀 Features
- **Separate TCP and UDP Versions**: Choose between TCP for reliable communication or UDP for faster, connectionless communication.
- **User Registration**: Register users with unique names for personalized messaging.
- **Private Messaging**: Send direct messages to specific users.
- **Broadcast Messaging**: Server can broadcast messages to all connected clients.
- **Multi-threading (TCP)**: Efficient handling of multiple clients simultaneously.
- **Command-line Interface**: Simple and intuitive interface for both server and client.

---

## 🛠️ Setup and Usage

### Prerequisites
- **Python 3.7+** installed on your system.
- Basic knowledge of terminal or command-line usage.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/maazkhandev75/ChatLink.git
   cd ChatLink
	```
2. Navigate to the desired protocol folder:
	- in case of tcp
	```bash
	cd tcp
    ```
3. Run the server
	```bash
	python s.py
	```

4. Run client/s in other terminals
	```bash
	python c.py
	```


## 📝 How to Use

### Client Commands
1. **Register**: Enter your name to register in the server's database.
   - Example:
     ```plaintext
     ENTER YOUR NAME TO REGISTER IN server's DB: John
     ```
2. **Send Private Message**:
   - Use the format:
     ```plaintext
     TO:<recipient_username>;<message>
     ```
   - Example:
     ```plaintext
     TO:Alice;Hello, how are you?
     ```
3. **Exit**: Type `EXIT` to disconnect from the server.
   - Example:
     ```plaintext
     EXIT
     ```

### Server Features
- **User Registration**: Registers each client with a unique username.
- **Private Messaging**: Forwards messages from one user to another.
- **Broadcast Messaging**: Sends a message from the server to all connected clients.
  - Example:
    - When prompted, type a message in the server terminal to broadcast:
      ```plaintext
      Server: This is a broadcast message to all clients.
      ```

## 📂 Project Structure

```bash
ChatLink/
│
├── tcp/
│   ├── s.py  # TCP server script
│   └── c.py  # TCP client script
│
└── udp/
    ├── s.py  # UDP server script
    └── c.py  # UDP client script

```
