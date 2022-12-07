from pprint import pprint

import Global
from Dijkstra import Dijkstra


class Pathfinder(object):
    """ Class wrapping our pathfinding algorithm (Dijkstra) and provides an
    easy to use interface.
    KISS
    """
    def __init__(self, map_wrapper):
        self.map_wrapper = map_wrapper
        self.algo = Dijkstra(map_wrapper)
        self.queries = {}

    def get_next_move(self, entity, to_pos, requested_distance_from_target):
        path = self.algo.get_shortest_path(entity.pos, to_pos)
        if not path:
            print(f"""[ ] - Pathfinding system - Could not find path from {entity.pos} to {to_pos}""")
            return None
        path = path[:len(path) - requested_distance_from_target - 1]
        if len(path):
            return path.pop(0)
            
