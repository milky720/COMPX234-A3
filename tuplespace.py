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
        """Add a key-value pair"""
        with self.lock:
            self.stats['total_operations'] += 1
            self.stats['puts'] += 1
            if key in self.store:
                self.stats['errors'] += 1
                return (False, f"ERR {key} already exists")
            self.store[key] = value
            return (True, f"OK ({key}, {value}) added")
