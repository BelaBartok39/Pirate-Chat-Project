import socket
import threading
import sys
import time
from colorama import init, Fore, Style

init(autoreset=True)  # Initialize colorama
DEBUG = True  # Set to True for debug messages

class MagicalChatClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None
        self.running = True

    def connect(self):
        try:
            self.socket.connect((self.server_ip, self.server_port))
            print(f"{Fore.GREEN}Connected to the server!")
            
            # Start receiving messages in a separate thread
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            # Handle user input in the main thread
            self.handle_user_input()
            
        except Exception as e:
            print(f"{Fore.RED}Connection error: {e}")
    
    def handle_user_input(self):
        try:
            while self.running:
                # Wait for user input
                message = input("")
                
                # Check for quit command
                if message.lower() == '/quit':
                    self.disconnect()
                    break
                
                # Send the message
                self.send_message(message)
                
        except KeyboardInterrupt:
            self.disconnect()
        except Exception as e:
            print(f"{Fore.RED}Input error: {e}")
            self.disconnect()

    def send_message(self, message):
        try:
            self.socket.sendall(message.encode('utf-8'))
        except Exception as e:
            print(f"{Fore.RED}Message send error: {e}")

    def receive_messages(self):
        while self.running:
            try:
                data = self.socket.recv(1024).decode('utf-8')
                if not data:
                    print(f"{Fore.YELLOW}Server connection closed.")
                    self.running = False
                    break
                
                print(data)
                
                # If we're prompted for a username
                if "Enter your magic name" in data:
                    if DEBUG:
                        print(f"{Fore.CYAN}[DEBUG] Username prompt detected")
                    self.username = input(f"{Fore.CYAN}Enter your magical name: ")
                    if DEBUG:
                        print(f"{Fore.CYAN}[DEBUG] Sending username: {self.username}")
                    self.send_message(self.username)
                    if DEBUG:
                        print(f"{Fore.CYAN}[DEBUG] Username sent, waiting for confirmation...")
                    
            except Exception as e:
                if self.running:  # Only show error if we didn't disconnect intentionally
                    print(f"{Fore.RED}Receive error: {e}")
                break

    def disconnect(self):
        self.running = False
        try:
            self.send_message('/quit')
            self.socket.close()
            print(f"{Fore.YELLOW}Disconnected from server.")
        except Exception as e:
            print(f"{Fore.RED}Disconnection error: {e}")
        sys.exit(0)


# Example usage
if __name__ == "__main__":
    client = MagicalChatClient("127.0.0.1", 5050)
    client.connect()