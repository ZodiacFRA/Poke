import sys


class IdManager(object):
    def __init__(self):
        self.ids = []
        self.network_ids = {}  # Used to match engine IDs and network ids

    def create_new_id(self, network_id=None):
        for i in range(sys.maxsize):
            if i not in self.ids:
                self.ids.append(i)
                if network_id is not None:  # Associate the new id to a network_id
                    self.network_ids[i] = network_id
                return i

    def get_network_id(self, engine_id):
        return self.network_ids.get(engine_id, None)

    def get_engine_id(self, network_id):
        return next(k for k, v in self.network_ids.items() if v == network_id)
