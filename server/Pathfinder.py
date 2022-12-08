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

    def get_next_move(self, entity, target_pos):
        path = self.algo.get_shortest_path(entity.pos, target_pos)
        if not path:
            return None
        if len(path):
            return path.pop(0)

    def get_tiles_at_distance_from(self, target_pos, requested_distance):
        return self.algo.get_tiles_at_distance_from(target_pos, requested_distance)
