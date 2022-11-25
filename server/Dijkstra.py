import copy
import collections
from operator import attrgetter

from utils import Position


class Node(object):
    def __init__(self, pos, distance=float('inf')):
        self.pos = pos
        self.distance = distance
        self.neighbors = []

    def __repr__(self):
        return f"{self.pos}"


class Dijkstra(object):
    def __init__(self, map_wrapper):
        self.deltas = (Position(-1, 0), Position(0, 1), Position(1, 0), Position(0, -1))
        self.map_wrapper = map_wrapper

    def get_shortest_path(self, from_pos, target_pos):
        if self.map_wrapper.is_colliding_pos(from_pos) or self.map_wrapper.is_colliding_pos(target_pos):
            print(f"[-] - Dijkstra: Position not accessible: either {from_pos} or {target_pos}")
            return None
        self.root_node = Node(from_pos, 0)
        self.target_pos = target_pos

        self.done_nodes = collections.OrderedDict()
        self.to_do_nodes = collections.OrderedDict()
        self.explore_neighbors(self.root_node)
        # self.to_do_nodes[self.root_node.__repr__] = self.root_node
        self.compute()

    def explore_neighbors(self, current_node, distance = 0):
        if distance > self.map_wrapper.x_size * self.map_wrapper.y_size:
            return 2
        if current_node.pos == self.target_pos:
            return 1
        for delta in self.deltas:
            tmpPos = current_node.pos + delta
            # If is a valid position (is a node)
            if not self.map_wrapper.is_colliding_pos(tmpPos):
                tmpName = tmpPos.__repr__()
                # If position has never been visited, create the node object
                if tmpName not in self.to_do_nodes and tmpName not in self.done_nodes:
                    newNode = Node(tmpPos, distance + 1)
                    # Add to todo, we'll do it later
                    self.to_do_nodes[tmpName] = newNode
                # If the node exists
                else:
                    if tmpName in self.to_do_nodes:
                        newNode = self.to_do_nodes[tmpName]
                    else:
                        newNode = self.done_nodes[tmpName]
                    if distance + 1 < newNode.distance:
                        newNode.distance = distance + 1
                current_node.neighbors.append(newNode)
        return 0

    def compute(self):
        while len(self.to_do_nodes) > 0:
            node = self.to_do_nodes.popitem(False)
            # print(f"tour sur {node[1].pos}")
            flag = self.explore_neighbors(node[1], node[1].distance)
            self.done_nodes[node[0]] = node[1]
            if flag == 1:
                # Backtrack
                tmp = None
                min_neighbor = self.root_node
                while min_neighbor.pos != self.target_pos:
                    print("tour", min_neighbor.pos, min_neighbor.distance, min_neighbor.neighbors)
                    if tmp is not None and tmp.pos == min_neighbor.pos:
                        print("Break")
                        break
                    # print(min_neighbor.distance)
                    # Get neighbor with lowest distance
                    tmp = min_neighbor
                    min_neighbor = min(min_neighbor.neighbors, key=lambda x: x.distance)

            elif flag == 2:
                return []
