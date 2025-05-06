import threading

class TupleSpace:
    def __init__(self):
        """Initialize the tuple space"""
        self.store = {}
        self.lock = threading.Lock()
        self.stats = {
            'total_operations': 0,
            'reads': 0,
            'gets': 0,
            'puts': 0,
            'errors': 0,
            'total_clients': 0
        }

    def put(self, key, value):
        """Add a key-value tuple"""
        with self.lock:
            self.stats['total_operations'] += 1
            self.stats['puts'] += 1
            if key in self.store:
                self.stats['errors'] += 1
                return (False, f"ERR {key} already exists")
            self.store[key] = value
            return (True, f"OK ({key}, {value}) added")

    def get(self, key):
        """Fetch and remove the key-value tuple"""
        with self.lock:
            self.stats['total_operations'] += 1
            self.stats['gets'] += 1
            if key not in self.store:
                self.stats['errors'] += 1
                return (False, f"ERR {key} does not exist")
            value = self.store.pop(key)
            return (True, f"OK ({key}, {value}) removed")

    def read(self, key):
        """Read the key-value tuple"""
        with self.lock:
            self.stats['total_operations'] += 1
            self.stats['reads'] += 1
            if key not in self.store:
                self.stats['errors'] += 1
                return (False, f"ERR {key} does not exist")
            return (True, f"OK ({key}, {self.store[key]}) read")
