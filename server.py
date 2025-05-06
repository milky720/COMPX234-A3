import socket
import threading
from tuplespace import TupleSpace

class TupleSpaceServer:
    def __init__(self, port):
        self.port = port
        self.tuple_space = TupleSpace()
        self.running = False

    def start(self):
        self.running = True
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', self.port))
            s.listen()
            print(f"Server started on port {self.port}")
            
            while self.running:
                conn, addr = s.accept()
                threading.Thread(
                    target=self.handle_client,
                    args=(conn, addr)
                ).start()

    def handle_client(self, conn, addr):
        with conn:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                response = self.process_message(data)
                conn.send(response.encode())

    def process_message(self, message):
        # Simple implementation, further submissions will improve it.
        if message.startswith("PUT"):
            _, key, value = message.split(maxsplit=2)
            return self.tuple_space.put(key, value)[1]
        return "ERR invalid command"

if __name__ == "__main__":
    import sys
    server = TupleSpaceServer(51234)
    server.start()
