from pprint import pprint

import Global
from Dijkstra import Dijkstra


class PathfindingQuery(object):
    def __init__(self, entity, to_pos, path, turn_idx, priority=1):
        self.entity = entity
        self.to_pos = to_pos
        self.path = path
        self.last_refresh = turn_idx
        self.priority = priority


class Pathfinder(object):
    """ Class wrapping our pathfinding algorithm (Dijkstra) and provides an
    easy to use interface.
    Maintain a map of the queries for each entity (max 1 / entity)
    and returns the next move, automatically rerun the pathfinding algorithm
    if needed (last update too old for the set priority or not existing)
    """
    def __init__(self, map_wrapper):
        self.map_wrapper = map_wrapper
        self.algo = Dijkstra(map_wrapper)
        self.queries = {}

    # Maybe add a priority number
    def get_next_move(self, entity, to_pos, priority=1, debug=False):
        if entity.pos == to_pos:
            print(f"{entity} already arrived")
            return None

        if entity.id not in self.queries:  # First pathfinding query, create the entry
            next_move = self.init_new_query(entity, to_pos, priority)
            if next_move is None:
                return

        elif entity.id in self.queries and self.queries[entity.id].to_pos != to_pos:  # Outdated query, delete and recreate
            del self.queries[entity.id]
            next_move = self.init_new_query(entity, to_pos, priority)
            if next_move is None:
                return

        else:  # Query is usable
            query = self.queries[entity.id]
            # Check if we need to rerun the algorithm based on priority and path age
            if Global.turn_idx - query.last_refresh > query.priority:
                path = self.algo.get_shortest_path(entity.pos, to_pos)
                if not path:
                    if debug:
                        print(f"""[ ] - Pathfinding system - Could not find path""")
                    return None
                query.path = path
                query.last_refresh = Global.turn_idx
                next_move = query.path.pop(0)
            else:  # Just return the next available move
                next_move = query.path.pop(0)

        # Delete query if finished (no more moves available) and the pathfinding is done
        if len(self.queries[entity.id].path) <= 0:
            del self.queries[entity.id]

        return next_move

    def init_new_query(self, entity, to_pos, priority, debug=False):
        if debug:
            print(f"new query from {entity.pos} to {to_pos}")
        path = self.algo.get_shortest_path(entity.pos, to_pos)
        if not path:
            if debug:
                print(f"""[ ] - Pathfinding system - Could not find path""")
            return None
        self.queries[entity.id] = PathfindingQuery(
            entity, to_pos, path, Global.turn_idx, priority
        )
        return self.queries[entity.id].path.pop(0)
