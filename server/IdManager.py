import sys


class IdManager(object):
    def __init__(self):
        self.ids = []
        self.network_ids = {}  # engine IDs -> network id

    def create_new_id(self, network_id=None):
        for i in range(sys.maxsize):
            if i not in self.ids:
                self.ids.append(i)
                if network_id is not None:  # Associate the new id to a network_id
                    self.network_ids[i] = network_id
                return i

    def get_network_client(self, engine_id):
        return self.network_ids.get(engine_id, None)

    def get_engine_id(self, network_id):
        try:
            engine_id = next(k for k, v in self.network_ids.items() if v == network_id)
        except StopIteration:
            return None
        return engine_id

    def get_players_ids(self):
        return self.network_ids
