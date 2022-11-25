import time
import json
import logging
from pprint import pprint

# https://github.com/Pithikos/python-websocket-server#api
from websocket_server import WebsocketServer

from utils import Position
from Map import MapWrapper
from Entities import Player
from Dijkstra import Dijkstra


class App(object):
    def __init__(self):
        super(App, self).__init__()
        # Game state
        self.map_wrapper = MapWrapper("map.txt")
        self.pathfinder = Dijkstra(self.map_wrapper)
        # print(self.pathfinder.get_shortest_path(
        #     from_pos=Position(3, 1),
        #     target_pos=Position(3, 7))
        # )
        self.players = {}
        self.LivingEntities = {}
        # Networking
        self.server = WebsocketServer(host='localhost', port=50000, loglevel=logging.INFO)
        self.server.set_fn_new_client(self.on_new_client)
        self.server.set_fn_client_left(self.on_client_leave)
        self.server.set_fn_message_received(self.on_msg_received)
        self.server.run_forever(threaded=True)
        # Game loop
        self.delta_time = 1
        self.launch()

    def launch(self):
        while True:
            start_time = time.time()
            print("tick")
            time.sleep(self.delta_time - (time.time() - start_time))

    def do_movement(self, client, message):
        player_pos = self.players[client["id"]].pos
        if message == "ArrowUp":
            new_pos = Position(player_pos.y - 1, player_pos.x)
        elif message == "ArrowDown":
            new_pos = Position(player_pos.y + 1, player_pos.x)
        elif message == "ArrowLeft":
            new_pos = Position(player_pos.y, player_pos.x - 1)
        elif message == "ArrowRight":
            new_pos = Position(player_pos.y, player_pos.x + 1)
        else:
            # Not a movement
            return

        is_colliding_pos = self.map_wrapper.is_colliding_pos(new_pos)
        if not is_colliding_pos:
            self.map_wrapper.move(player_pos, new_pos)
            self.players[client["id"]].pos = new_pos

        map = self.map_wrapper.serialize()
        message = {"type": "init_map", "sprites_table": self.map_wrapper.sprites, "map": map}
        self.server.send_message_to_all(json.dumps(message))

    ########################################3
    ## Networking

    def on_new_client(self, client, server):
        # Create the new player
        player_pos = Position(1, 1)
        player = Player(Position(1, 1), "jm", client["id"])
        self.players[client["id"]] = player
        self.map_wrapper.add_player(player)

        map = self.map_wrapper.serialize()
        message = {"type": "init_map", "sprites_table": self.map_wrapper.sprites, "map": map}
        self.server.send_message_to_all(json.dumps(message))

    def on_client_leave(self, client, server):
        player = self.players.pop(client["id"])
        self.map_wrapper.remove_entity()

        map = self.map_wrapper.serialize()
        message = {"type": "init_map", "sprites_table": self.map_wrapper.sprites, "map": map}
        self.server.send_message_to_all(json.dumps(message))

    def on_msg_received(self, client, server, message):
        if message[:5] == "Arrow":
            self.do_movement(client, message)
        else:
            print(client["id"], message)


if __name__ == '__main__':
    app = App()
