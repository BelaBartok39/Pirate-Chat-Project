import threading 
import socket
import random
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize colorama

WELCOME_ART = [
    r"""
    (\\_/)
    (o.o)
    (> <)
    """,
    r"""
     /\_/\\
    ( o.o )
     > ^ <
    """,
    r"""
    .--. 
    |o_o | 
    |:_/ | 
    //   \ \ 
    (|     | ) 
    /'\_   _/`\ 
    \___)=(___/ 
    """
]

class MagicalChatServer:
    def __init__(self, host='0.0.0.0', port=5050):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.lock = threading.Lock()

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"{Fore.YELLOW}✨ Server listening on {self.host}:{self.port}")
        print(f"{Fore.CYAN}🐾 Waiting for magical creatures to connect...")
        
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"{Fore.GREEN}🔗 New connection from {addr}")
            client_thread = threading.Thread(
                target=self.handle_client,
                args=(client_socket, addr)
            )
            client_thread.daemon = True  # Make thread daemon so it exits when main thread exits
            client_thread.start()

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

    def handle_client(self, client_socket, addr):
        username = "Unknown"
        try:
            # Send welcome message with random ASCII art
            art = random.choice(WELCOME_ART)
            welcome_msg = f"\n{Fore.MAGENTA}{art}\n{Fore.GREEN}🌌 Welcome to the Magical Chat! 🌠\n"
            client_socket.send(welcome_msg.encode('utf-8'))
            
            # Get username
            client_socket.send(f"{Fore.CYAN}🔮 Enter your magic name: ".encode('utf-8'))
            username = client_socket.recv(1024).decode('utf-8').strip()
            print(f"{Fore.GREEN}🧙 User {username} joined from {addr}")
            
            with self.lock:
                self.clients.append((client_socket, username))
            
            join_msg = f"\n{Fore.YELLOW}🌟 {username} has entered the enchanted forest! 🌳\n"
            self.broadcast(join_msg, (client_socket, username))
            
            while True:
                message = client_socket.recv(1024).decode('utf-8').strip()
                if not message:
                    break
                
                print(f"{Fore.BLUE}📩 Message from {username}: {message}")
                
                if message.lower() == '/quit':
                    break
                
                msg = f"{Fore.BLUE}🧚 {username}: {Style.RESET_ALL}{message}"
                self.broadcast(msg, (client_socket, username))
                
        except Exception as e:
            print(f"{Fore.RED}🔥 Connection error with {addr} ({username}): {e}")
        finally:
            with self.lock:
                try:
                    if (client_socket, username) in self.clients:
                        self.clients.remove((client_socket, username))
                        leave_msg = f"\n{Fore.YELLOW}🍂 {username} vanished in a puff of glitter! ✨\n"
                        self.broadcast(leave_msg)
                except:
                    pass
                
                try:
                    client_socket.close()
                    print(f"{Fore.YELLOW}👋 Connection closed with {username} ({addr})")
                except:
                    pass

if __name__ == "__main__":
    server = MagicalChatServer()
    server.start()