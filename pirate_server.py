import threading 
import ssl
import socket
import random
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize colorama
DEBUG = True # Debug messages on/off

WELCOME_ART = [
    """
888888888888888888888888888888888888888888888888888888888888
888888888888888888888888888888888888888888888888888888888888
8888888888888888888888888P""  ""9888888888888888888888888888
8888888888888888P"88888P          988888"9888888888888888888
8888888888888888  "9888            888P"  888888888888888888
888888888888888888bo "9  d8o  o8b  P" od88888888888888888888
888888888888888888888bob 98"  "8P dod88888888888888888888888
888888888888888888888888    db    88888888888888888888888888
88888888888888888888888888      8888888888888888888888888888
88888888888888888888888P"9bo  odP"98888888888888888888888888
88888888888888888888P" od88888888bo "98888888888888888888888
888888888888888888   d88888888888888b   88888888888888888888
8888888888888888888oo8888888888888888oo888888888888888888888
888888888888888888888888888888888888888888888888888888888888
    """
]

class PirateChatServer:
    def __init__(self, host='0.0.0.0', port=5050):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.ssl_context.load_cert_chain(certfile="server.crt", keyfile="server.key")
        self.clients = []
        self.lock = threading.Lock()

    def start(self):
        if DEBUG:
          print("[DEBUG] Starting server")
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        if DEBUG:
            print("[DEBUG] Server started and waiting for connections")
        print(f"{Fore.YELLOW}✨ Server listening on {self.host}:{self.port}")
        print(f"{Fore.CYAN} Waiting for pirates creatures to connect...")
        
        if DEBUG:
            print("[DEBUG] Entering client acceptance loop")
        while True:
            client_socket, addr = self.server_socket.accept()
            client_socket = self.ssl_context.wrap_socket(client_socket, server_side=True)
            print("[DEBUG] SSL handshake completed")
            print(f"{Fore.GREEN}🔗 New connection from {addr}")
            client_thread = threading.Thread(
                target=self.handle_client,
                args=(client_socket, addr)
            )
            client_thread.daemon = True  # Make thread daemon so it exits when main thread exits
            client_thread.start()
            if DEBUG:
                print("[DEBUG] Thread created and running")

    def broadcast(self, message, sender=None):
        with self.lock:
            print(f"{Fore.MAGENTA}📢 Broadcasting: {message}")
            for client in self.clients:
                if client != sender:
                    try:
                        client[0].send(message.encode('utf-8'))
                    except Exception as e:
                        print(f"{Fore.RED}💥 Error broadcasting message: {e}")
                        self.clients.remove(client)
                        if DEBUG:
                            print("[DEBUG] Removing missing/bad client")

    def handle_client(self, client_socket, addr):
        username = "Unknown"
        try:
            # Send welcome message with ASCII art
            art = random.choice(WELCOME_ART)
            welcome_msg = f"\n{Fore.MAGENTA}{art}\n{Fore.GREEN}☠️ Welcome to Pirate Chat! ☠️\n"
            client_socket.send(welcome_msg.encode('utf-8'))
            
            # Get username
            client_socket.send(f"{Fore.CYAN}🔮 Enter your pirate name: ".encode('utf-8'))
            username = client_socket.recv(1024).decode('utf-8').strip()
            print(f"{Fore.GREEN}🧙 User {username} joined from {addr}")
            
            with self.lock:
                self.clients.append((client_socket, username))
            
            join_msg = f"\n{Fore.YELLOW}🌟 {username} has entered the high seas! 🌳\n"
            self.broadcast(join_msg, (client_socket, username))
            
            while True:
                message = client_socket.recv(1024).decode('utf-8').strip()
                if not message:
                    break
                
                print(f"{Fore.BLUE}📩 Message in a bottle from {username}: {message}")
                
                if message.lower() == '.quit':
                    break
                
                # Handle .list command
                if message.lower() == '.list':
                    with self.lock:
                        client_list = [client[1] for client in self.clients]
                    client_list_message = f"{Fore.CYAN}🌊 Connected pirates: {', '.join(client_list)}"
                    client_socket.send(client_list_message.encode('utf-8'))
                    continue
                
                msg = f"{Fore.BLUE}🧚 {username}: {Style.RESET_ALL}{message}"
                self.broadcast(msg, (client_socket, username))
                
        except Exception as e:
            print(f"{Fore.RED}🔥 Connection error with {addr} ({username}): {e}")
        finally:
            leave_msg = f"\n{Fore.YELLOW}🍂 {username} jumped overboard! ✨\n"
            self.broadcast(leave_msg)
            with self.lock:
                try:
                    if (client_socket, username) in self.clients:
                        self.clients.remove((client_socket, username))
                except:
                    pass
                
                try:
                    client_socket.close()
                    print(f"{Fore.YELLOW}👋 Connection closed with {username} ({addr})")
                except:
                    pass

if __name__ == "__main__":
    server = PirateChatServer()
    server.start()