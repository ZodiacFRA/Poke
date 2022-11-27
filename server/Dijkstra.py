import copy
import collections
from operator import attrgetter

from HelperClasses import Position


class Node(object):
    def __init__(self, pos, distance=float('inf')):
        self.pos = pos
        self.distance = distance
        self.neighbors = []

    def __repr__(self):
        return f"[{self.pos}, {self.distance}]"


class Dijkstra(object):
    """ Dijkstra pathfinding algorithm implementation
    TODO: Find a way to avoid top colliding entities as well """
    def __init__(self, map_wrapper):
        self.deltas = (Position(-1, 0), Position(0, 1), Position(1, 0), Position(0, -1))
        self.map_wrapper = map_wrapper

    def get_shortest_path(self, from_pos, target_pos):
        """ A complete re evaluation of the graph is done each time for now, as
        colliding entities can change positions """
        self.root_node = Node(from_pos, 0)
        self.target_pos = target_pos

        self.done_nodes = collections.OrderedDict()
        self.to_do_nodes = collections.OrderedDict()
        # Set the root node as done, we already know its distance (0)
        self.done_nodes[self.root_node.__repr__()] = self.root_node
        self.explore_neighbors(self.root_node)
        return self.compute()

    def explore_neighbors(self, current_node, distance=0):
        if distance > self.map_wrapper.x_size * self.map_wrapper.y_size:
            return 2
        if current_node.pos == self.target_pos:
            return 1
        self.explore_neighbors_2(current_node, distance)
        return 0

    def explore_neighbors_2(self, current_node, distance=0):
        for delta in self.deltas:
            tmp_pos = current_node.pos + delta
            # If is a valid position (is a node)
            if not self.map_wrapper.is_colliding_pos(tmp_pos):
                tmpName = tmp_pos.__repr__()
                # If position has never been visited, create the node object
                if tmpName not in self.to_do_nodes and tmpName not in self.done_nodes:
                    newNode = Node(tmp_pos, distance + 1)
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
            # We found it but the target tile is colliding - Workaround
            if tmp_pos == self.target_pos:
                newNode = Node(tmp_pos, distance + 1)
                current_node.neighbors.append(newNode)
                self.to_do_nodes[tmp_pos.__repr__()] = newNode

    def compute(self):
        while len(self.to_do_nodes) > 0:
            node = self.to_do_nodes.popitem(False)
            flag = self.explore_neighbors(node[1], node[1].distance)
            self.done_nodes[node[0]] = node[1]
            if flag == 1:
                res = []
                # We start from the target
                min_neighbor = node[1]
                self.explore_neighbors_2(min_neighbor, min_neighbor.distance)
                while min_neighbor.distance != 1:
                    # DEBUG:
                    # print('-'*20)
                    # self.dra&w_distances()
                    # print(f"from {min_neighbor}")
                    for neighbor in min_neighbor.neighbors:
                        # print('\t', neighbor)
                        if neighbor.distance < min_neighbor.distance:
                            min_neighbor = neighbor
                    # min_neighbor = min(min_neighbor.neighbors, key=lambda x: x.distance)
                    # print(f" to: {min_neighbor}")
                    res.append(min_neighbor)
                res.reverse()
                return [node.pos for node in res]
            elif flag == 2:
                return []

    def draw_distances(self):
        """ Debug function, will draw an ascii representation of the map,
        containing the distance of each tile from the root node
        (highest value should be the target) """
        tmp = []
        for y_idx in range(self.map_wrapper.y_size):
            line = []
            for x_idx in range(self.map_wrapper.x_size):
                line.append(-1)
            tmp.append(line)

        for key, node in self.done_nodes.items():
            tmp[node.pos.y][node.pos.x] = node.distance

        for y_idx in range(self.map_wrapper.y_size):
            for x_idx in range(self.map_wrapper.x_size):
                print(f"{tmp[y_idx][x_idx]:>3}", end='')
            print()
