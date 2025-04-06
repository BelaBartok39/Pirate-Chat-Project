# Component Analysis

## Server (`server.py`)

- Creates a socket server that accepts multiple client connections.
- Uses threading to handle multiple clients simultaneously.
- Implements broadcasting to send messages to all connected clients.
- Manages client connections and graceful disconnections.
- Features colorful output with `Colorama` and ASCII art for welcome messages.

## Client (`client.py`)

- Connects to the server using socket communication.
- Implements separate threads for receiving messages and handling user input.
- Uses a thread lock mechanism to prevent input conflicts.
- Manages connection state and handles graceful disconnection.
- Implements color-coded messages using `Colorama` for better user experience.

## Test Controller (`test_clients.py`)

- Orchestrates the testing of the chat system.
- Launches the server and multiple client instances in separate console windows.
- Configures test parameters through user input.
- Manages process lifecycle and termination.
- Logs client activities to files (on Windows).

---

# Key Communication Flow

## Client Connection Process

1. Client connects to server via TCP socket.
2. Server sends welcome ASCII art.
3. Server prompts client for username.
4. Client sends username to server.
5. Server broadcasts join message to all other clients.
6. Client can now send/receive messages.

## Message Broadcasting

1. When a client sends a message, the server receives it.
2. Server formats the message with sender info and color coding.
3. Server broadcasts the formatted message to all other clients.
4. Each client's receive thread displays incoming messages.

## Disconnection Handling

1. Client can disconnect by sending the `/quit` command.
2. Server detects disconnection and removes the client from the active list.
3. Server broadcasts a departure message to remaining clients.
4. Client and server close socket connections.

---

# Threading Model

- **Server**: Uses one thread per client to handle communication.
- **Client**: Uses two threads:
  - Main thread for user input.
  - Secondary thread for receiving messages from the server.
- Thread synchronization using locks to prevent race conditions.

---

# Debugging Features

- Debug mode toggle in both server and client.
- Detailed debug logging for connection events.
- Client activity logging to files (Windows).
