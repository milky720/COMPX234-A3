import socket
import sys

class TupleSpaceClient:
    def __init__(self, host, port, request_file):
        self.host = host
        self.port = port
        self.request_file = request_file

    def format_request(self, raw_request):
        parts = raw_request.strip().split(maxsplit=2)
        if not parts or parts[0] not in ("PUT", "GET", "READ"):
            return None

        op_char = parts[0][0]

        if op_char == 'P' and len(parts) == 3:
            key, value = parts[1], parts[2]
            if len(key) + len(value) + 1 > 970:
                print(f"Error: The length of the key-value exceeds the limit（{raw_request}）")
                return None
            content = f"{op_char} {key} {value}"

        elif op_char == 'G' and len(parts) == 2:
            key = parts[1]
            if len(key) > 999:
                print(f"Error: The length of the key-value exceeds the limit（{raw_request}）")
                return None
            content = f"{op_char} {key}"

        elif op_char == 'R' and len(parts) == 2:
            key = parts[1]
            if len(key) > 999:
                print(f"Error: The length of the key-value exceeds the limit（{raw_request}）")
                return None
            content = f"{op_char} {key}"

        else:
            return None

        formatted = f"{len(content) + 4:03d} {content}"
        return formatted

    def run(self):
        try:
            with open(self.request_file) as f:
                requests = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: File {self.request_file} not found")
            return

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.host, self.port))
                print(f"Connected to server at {self.host}:{self.port}")

                for req in requests:
                    formatted_msg = self.format_request(req)
                    if not formatted_msg:
                        print(f"Skipping invalid request: {req}")
                        continue

                    s.send(formatted_msg.encode())
                    response = s.recv(1024).decode()
                    print(req)
                    print(response)

            except ConnectionRefusedError:
                print("Error: Could not connect to server")
            except Exception as e:
                print(f"Communication error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <host> <port> <request_file>")
        sys.exit(1)
    client = TupleSpaceClient(sys.argv[1], int(sys.argv[2]), sys.argv[3])
    client.run()