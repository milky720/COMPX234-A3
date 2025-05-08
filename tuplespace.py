import threading

class TupleSpace:
    def __init__(self):
        """Initialize the tuple space with statistics tracking"""
        self.store = {}
        self.lock = threading.Lock()
        self.stats = {
            'num_tuples': 0,
            'total_key_size': 0,
            'total_value_size': 0,
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
            self.stats['num_tuples'] += 1
            self.stats['total_key_size'] += len(key)
            self.stats['total_value_size'] += len(value)
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
            self.stats['num_tuples'] -= 1
            self.stats['total_key_size'] -= len(key)
            self.stats['total_value_size'] -= len(value)
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

    def increment_client_count(self):
        """Increment the client counter"""
        with self.lock:
            self.stats['total_clients'] += 1

    def get_stats(self):
        """Return a dictionary of current statistics"""
        with self.lock:
            stats = self.stats.copy()
            if stats['num_tuples'] > 0:
                stats['avg_tuple_size'] = int((stats['total_key_size'] + stats['total_value_size']) / stats['num_tuples'])
                stats['avg_key_size'] = int(stats['total_key_size'] / stats['num_tuples'])
                stats['avg_value_size'] = int(stats['total_value_size'] / stats['num_tuples'])
            else:
                stats['avg_tuple_size'] = 0
                stats['avg_key_size'] = 0
                stats['avg_value_size'] = 0
            return stats