# Installation and Execution Instructions

## Prerequisites
- **Python 3.7+** must be installed.
- **Colorama** package for colored terminal output:
  ```sh
  pip install colorama
  ```
- **OpenSSL** (for generating self-signed certificates, if needed)
- (Windows only) If you want to use the test runner, ensure you can open new console windows.

## Generating SSL Certificates (if not present)
If `server.crt` and `server.key` are not present, generate them with:
```powershell
openssl req -new -x509 -days 365 -nodes -out server.crt -keyout server.key
```

## Running the Server
```sh
python pirate_server.py
```

## Running a Client
```sh
python pirate_client.py
```

## Using the Test Runner (Windows)
```sh
python test_runner.py
```
Follow the prompts to start the server and multiple clients in new windows.

---

# Component Analysis

## Server (`pirate_server.py`)
- Accepts multiple SSL-encrypted client connections using threads.
- Broadcasts messages and manages client list.
- Colorful output and ASCII art welcome.
- `.list` command shows all connected users.
- Uses `server.crt` and `server.key` for SSL/TLS encryption.

## Client (`pirate_client.py`)
- Connects to server using SSL/TLS.
- Handles user input and message receiving in separate threads.
- Colorful output, supports `.list` command.
- Disables certificate verification for self-signed certs (testing only).

## Test Controller (`test_runner.py`)
- Launches server and multiple clients in new console windows (Windows).
- Allows configuration of number of clients.
- Manages process lifecycle.
- Fixed to use `pirate_server.py` and SSL.

---

# Key Communication Flow

## Client Connection Process
1. Client connects to server via SSL-wrapped TCP socket.
2. Server sends welcome ASCII art and prompts for username.
3. Client sends username; server broadcasts join message.
4. Client can send/receive messages.

## Message Broadcasting
1. Client sends message; server receives and formats it.
2. Server broadcasts to all other clients.
3. Clients display incoming messages.

## Disconnection Handling
1. Client sends `.quit` or disconnects.
2. Server removes client and broadcasts departure.
3. Sockets are closed.

---

# Threading Model
- **Server:** One thread per client.
- **Client:** Main thread for input, secondary for receiving messages.
- Thread locks prevent race conditions.

---

# Security: SSL/TLS Encryption
- All messages are encrypted using SSL/TLS.
- Server uses a self-signed certificate (`server.crt`, `server.key`).
- Client disables certificate verification for testing.
- To test SSL:
  - Add debug prints after SSL handshake (see code).
  - Use Wireshark to verify encrypted traffic.
  - Non-SSL clients cannot connect.

---

# Debugging Features
- Debug mode toggle in both server and client.
- Debug logging for connection events.
- Client activity logging to files (Windows).
