import subprocess
import time
import sys
import os

# Configure test options
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5050

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print test header information."""
    print("=" * 50)
    print("MAGICAL CHAT TESTER")
    print("=" * 50)
    print(f"Server: {SERVER_IP}:{SERVER_PORT}")
    print("=" * 50)

def run_server():
    """Start the chat server."""
    print("\nStarting server...")
    try:
        if os.name == 'nt':
            # Windows: Create a new console window
            server_process = subprocess.Popen(
                ["cmd", "/c", "chcp 65001 && python server.py"],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            # Unix-like: Use a new terminal window
            server_process = subprocess.Popen(
                ["xterm", "-e", f"{sys.executable} server.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        return server_process
    except Exception as e:
        print(f"Error starting server: {e}")
        return None

def run_client(client_number):
    """Start a chat client."""
    print(f"\nStarting client {client_number}...")
    try:
        if os.name == 'nt':
            # Windows: Create a new console window and log to file
            server_process = subprocess.Popen(
                ["cmd", "/c", "chcp 65001 && python client.py"],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            # Unix-like: Use a new terminal window
            client_process = subprocess.Popen(
                ["xterm", "-e", f"{sys.executable} client.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
    
    except Exception as e:
        print(f"Error starting client {client_number}: {e}")
        return None

def main():
    clear_screen()
    print_header()

    # Ask for test configuration
    start_server = input("Start server? (y/n): ").lower() == 'y'
    num_clients = int(input("Number of clients to start (1-5): "))

    # Validate input
    if num_clients < 1 or num_clients > 5:
        print("Number of clients must be between 1 and 5")
        return

    # Start processes
    processes = []
    if start_server:
        server_process = run_server()
        if server_process:
            processes.append(("Server", server_process))
        time.sleep(1)  # Give the server time to start

    # Start clients
    for i in range(1, num_clients + 1):
        client_process = run_client(i)
        if client_process:
            processes.append((f"Client {i}", client_process))
        time.sleep(0.5)  # Space out client startups

    print("\nAll processes started!")
    print("Close the console windows when you're done testing.")
    print("=" * 50)

    # Wait for user to end test
    input("Press Enter to terminate all processes and end the test...")

    # Clean up processes
    for name, process in processes:
        print(f"Terminating {name}...")
        try:
            process.terminate()
        except:
            pass

    print("Test complete!")

if __name__ == "__main__":
    main()