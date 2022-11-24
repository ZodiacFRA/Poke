import copy
import collections


class Node(object):
    def init(self, pos, type, distance = float('inf')):
        self.pos = pos
        self.type = type
        self.distance = distance
        self.neighbours = []


class Dijkstra(object):
    def __init__(self, map_wrapper):
        self.deltas = (Position(-1, 0), Position(0, 1), Position(1, 0), Position(0, -1))
        self.map_wrapper = map_wrapper
        self.rootNode = Node(self.map.ghostPos, 'F', 0)
        self.done_nodes = collections.OrderedDict()
        self.to_do_nodes = collections.OrderedDict()
        self.explore_neighbours(self.rootNode)
        self.compute()

    def explore_neighbours(self, current_node, distance = 0):
        if distance > self.map.x_size * self.map.y_size:
            return 2
        if self.map.get(current_node) == 'P':
            return 1
        for delta in self.deltas:
            tmpPos = current_node.pos + delta
            # If is a valid position (is a node)
            if not self.map_wrapper.is_colliding_pos(tmpPos):
                tmpName = str(tmpPos[0]) + ',' + str(tmpPos[1])
                # If position has never been visited, create the node object
                if tmpName not in self.to_do_nodes and tmpName not in self.done_nodes:
                    newNode = Node(tmpPos, self.map_wrapper.map.get(tmpPos), distance + 1)
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
                current_node.neighbours.append(newNode)
        return 0

    def compute(self):
        while len(self.to_do_nodes) > 0:
            node = self.to_do_nodes.popitem(False)
            flag = self.explore_neighbours(node[1], node[1].distance)
            self.done_nodes[node[0]] = node[1]
            if flag == 1:
                break
            elif flag == 2:
                break
