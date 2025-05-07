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
        if len(message) < 7:
            return "000 ERR invalid message"

        try:
            msg_len = int(message[:3])
            if msg_len != len(message):
                return "000 ERR invalid message length"

            op = message[4]
            content = message[5:]

            if op == 'P':
                try:
                    key, value = content.split(maxsplit=1)
                    if len(key) + len(value) > 970:
                        return "000 ERR key+value too long"
                    success, response = self.tuple_space.put(key, value)
                    return f"{len(response) + 4:03d} {response}"
                except ValueError:
                    return "000 ERR PUT requires key and value"

            elif op == 'G':
                if not content.strip():
                    return "000 ERR GET requires key"
                key = content.strip()
                if len(key) > 999:
                    return "000 ERR key too long"
                success, response = self.tuple_space.get(key)
                return f"{len(response) + 4:03d} {response}"

            elif op == 'R':
                if not content.strip():
                    return "000 ERR READ requires key"
                key = content.strip()
                if len(key) > 999:
                    return "000 ERR key too long"
                success, response = self.tuple_space.read(key)
                return f"{len(response) + 4:03d} {response}"

            else:
                return "000 ERR unknown operation"

        except ValueError:
            return "000 ERR protocol format error"
        except Exception as e:
            print(f"Server error: {str(e)}")
            return "000 ERR server internal error"

if __name__ == "__main__":
    import sys
    server = TupleSpaceServer(51234)
    server.start()