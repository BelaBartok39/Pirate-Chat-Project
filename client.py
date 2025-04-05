import socket
import threading


class ChatClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_id = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.socket.connect((self.server_ip, self.server_port))
            self.client_id = self.socket.recv(1024).decode()
            print(f"Connected as {self.client_id}")
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            print(f"Connection error: {e}")

    def send_message(self, recipient_id, message):
        try:
            msg_data = f"{recipient_id}:{message}"
            self.socket.sendall(msg_data.encode())
        except Exception as e:
            print(f"Message send error: {e}")

    def request_client_list(self):
        try:
            self.socket.sendall(b".list")
        except Exception as e:
            print(f"Client list request error: {e}")

    def receive_messages(self):
        while True:
            try:
                data = self.socket.recv(1024).decode()
                if not data:
                    break
                print(f"Message received: {data}")
            except Exception as e:
                print(f"Receive error: {e}")
                break

    def disconnect(self):
        try:
            self.socket.sendall(b".exit")
            self.socket.close()
            print("Disconnected from server.")
        except Exception as e:
            print(f"Disconnection error: {e}")


# Example usage
if __name__ == "__main__":
    client = ChatClient("127.0.0.1", 5000)
    client.connect()
    # Example commands
    client.request_client_list()
    client.send_message("user123", "Hello!")
    client.disconnect()
