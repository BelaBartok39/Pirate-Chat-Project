import socket
import threading
import sys
import time
from colorama import init, Fore, Style

# TODO: Consider using a buffer mechanism for recieving messages

sys.stdout.reconfigure(encoding='utf-8') # Ensure terminal can handle emojis

init(autoreset=True)  # Initialize colorama
DEBUG = False  # Set to True for debug messages, False to turn off

class MagicalChatClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None
        self.running = True
        self.username_set = False
        self.input_lock = threading.Lock()

    def connect(self):
        try:
            self.socket.connect((self.server_ip, self.server_port))
            print(f"{Fore.GREEN}Connected to the server!")
            
            # Start receiving messages in a separate thread
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            # Wait for username prompt and handle it in receive thread
            while not self.username_set and self.running:
                time.sleep(0.1)
            
            # Handle user input in the main thread once username is set
            if self.running:
                self.handle_user_input()
            
        except Exception as e:
            print(f"{Fore.RED}Connection error: {e}")
    
    def handle_user_input(self):
        try:
            print(f"{Fore.CYAN}You can now chat. Type /quit to exit.")
            while self.running:
                # Wait for user input
                with self.input_lock:
                    message = input()
                
                # Check for quit command
                if message.lower() == '/quit':
                    self.disconnect()
                    break
                
                # Send the message
                if message.strip():
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
        waiting_for_username_prompt = True
        
        while self.running:
            try:
                data = self.socket.recv(1024).decode('utf-8')
                if not data:
                    print(f"{Fore.YELLOW}Server connection closed.")
                    self.running = False
                    break
                
                try:
                    print(data)
                except UnicodeEncodeError as e:
                    print(f"Unicode display error: {e}")
                    print(f"Message (safely encoded): {data.encode('ascii', 'replace').decode('ascii')}")
                
                # Handle username prompt gracefully
                if waiting_for_username_prompt and "Enter your magic name" in data:
                    if DEBUG:
                        print(f"[DEBUG] Username prompt detected")
                    
                    with self.input_lock:
                        self.username = input()
                    
                    if DEBUG:
                        print(f"[DEBUG] Sending username: {self.username}")
                    
                    self.send_message(self.username)
                    waiting_for_username_prompt = False
                    self.username_set = True
                    
                    if DEBUG:
                        print(f"[DEBUG] Username sent, waiting for confirmation...")
                
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
        return


# Example usage
if __name__ == "__main__":
    client = MagicalChatClient("127.0.0.1", 5050)
    client.connect()