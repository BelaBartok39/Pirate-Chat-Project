import threading
import socket

class TestClient:
  def __init__(self, server_ip,server_port):
    self.server_ip = server_ip
    self.server_port = server_port
    self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    self.username = None
  
  def connect(self):
    self.socket.connect((self.server_ip,self.server_port))
    print("Connected to server!")
    receive_thread = threading.Thread(
      target = self.receive_messages
    )
    receive_thread.daemon = False
    receive_thread.start()

  def receive_messages(self):
    while True:
      data = self.socket.recv(1024).decode('utf-8')
      # if not data:
      #   print("Connection lost :(")
      #   break
      
      print(data)


if __name__ == "__main__":
  client = TestClient("127.0.0.1",5050)
  client.connect()


