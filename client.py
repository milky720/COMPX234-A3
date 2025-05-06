import socket
import sys

class TupleSpaceClient:
    def __init__(self, host, port, request_file):
        self.host = host
        self.port = port
        self.request_file = request_file

    def run(self):
        try:
            with open(self.request_file) as f:
                requests = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: File {self.request_file} not found")
            return

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            for req in requests:
                s.send(req.encode())
                print(f"{req}: {s.recv(1024).decode()}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <host> <port> <request_file>")
        sys.exit(1)
    client = TupleSpaceClient(sys.argv[1], int(sys.argv[2]), sys.argv[3])
    client.run()
