import threading
import socket

class TestServer:
  def __init__(self, host='0.0.0.0', port=5050):
    self.host = host
    self.port = port
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.clients = []

  def start(self):
    # First thing we need is to bind to a socket
    self.server_socket.bind((self.host,self.port))
    # Then listen on that bound socket
    self.server_socket.listen()
    print(f"Server listening on {self.host}:{self.port}")
    # Now run a loop that accepts clients 
    while True:
      client_socket, cli_addr = self.server_socket.accept()
      print(f"New connection from {cli_addr}")
      self.clients.append(client_socket)
      # Start a thread for that client 
      client_thread = threading.Thread(
        #target is the handle helper
        target=self.handle_client,
        args=(client_socket, cli_addr)
      )
      client_thread.daemon = False
      client_thread.start()

  def handle_client(self, client_socket, cli_addr):
    welcome_msg = "Hey buddy, welcome!"
    client_socket.send(welcome_msg.encode('utf-8'))
    

if __name__ == "__main__":
  server = TestServer()
  server.start()
  
  