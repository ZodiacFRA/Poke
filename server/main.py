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
        self.map_wrapper = MapWrapper("./maps/map.txt")
        self.pathfinder = Dijkstra(self.map_wrapper)
        # print(self.pathfinder.get_shortest_path(
        #     from_pos=Position(3, 1),
        #     target_pos=Position(3, 7))
        # )
        self.players = {}
        self.LivingEntities = {}
        # Networking
        self.incoming_messages = []
        self.message_types_functions = {
            "enter_game": self.add_new_player,
            "key_input": self.do_movement
        }

        self.server = WebsocketServer(host='localhost', port=50000, loglevel=logging.INFO)
        # TODO: remove set_fn_new_client as this will be handled by a specific message
        # when the client is ready
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
            self.process_incoming_messages()
            time.sleep(self.delta_time - (time.time() - start_time))

    def process_incoming_messages(self):
        while len(self.incoming_messages) > 0:
            client, msg = self.incoming_messages.pop()
            try:
                msg = json.loads(msg)
            except json.decoder.JSONDecodeError as e:
                print(f"""[-] - Json module: Could not decode "{msg}" """)
            else:
                func = self.message_types_functions.get(msg["msg_type"])
                if func is None:
                    print(f"""[-] - Invalid message type: {msg["msg_type"]} in {msg}""")
                else:
                    func(client, msg)

    ########################################3
    ## Message processing

    def add_new_player(self, client, msg):
        player_pos = Position(1, 1)
        player = Player(Position(1, 1), "jm", client["id"])
        self.players[client["id"]] = player
        self.map_wrapper.add_player(player)

        map = self.map_wrapper.serialize()
        message = {"type": "init_map", "sprites_table": self.map_wrapper.sprites, "map": map}
        self.server.send_message_to_all(json.dumps(message))

    def do_movement(self, client, msg):
        player_pos = self.players[client["id"]].pos
        if msg == "ArrowUp":
            new_pos = Position(player_pos.y - 1, player_pos.x)
        elif msg == "ArrowDown":
            new_pos = Position(player_pos.y + 1, player_pos.x)
        elif msg == "ArrowLeft":
            new_pos = Position(player_pos.y, player_pos.x - 1)
        elif msg == "ArrowRight":
            new_pos = Position(player_pos.y, player_pos.x + 1)
        else:
            # Not a movement
            return

        is_colliding_pos = self.map_wrapper.is_colliding_pos(new_pos)
        if not is_colliding_pos:
            self.map_wrapper.move(player_pos, new_pos)
            self.players[client["id"]].pos = new_pos

        map = self.map_wrapper.serialize()
        msg = {"type": "init_map", "sprites_table": self.map_wrapper.sprites, "map": map}
        self.server.send_message_to_all(json.dumps(msg))

    ########################################3
    ## Networking

    def on_new_client(self, client, server):
        """ TODO: Remove everything here as the player will be created on the reception
        of a special message later on, waiting for the client implementation.
        For now the player is created here """
        player_pos = Position(1, 1)
        player = Player(Position(1, 1), "jm", client["id"])
        self.players[client["id"]] = player
        self.map_wrapper.add_player(player)

        map = self.map_wrapper.serialize()
        message = {"type": "init_map", "sprites_table": self.map_wrapper.sprites, "map": map}
        self.server.send_message_to_all(json.dumps(message))

    def on_client_leave(self, client, server):
        player = self.players.pop(client["id"])
        self.map_wrapper.remove_entity(player.pos)

        map = self.map_wrapper.serialize()
        message = {"type": "init_map", "sprites_table": self.map_wrapper.sprites, "map": map}
        self.server.send_message_to_all(json.dumps(message))

    def on_msg_received(self, client, server, message):
        self.incoming_messages.append((client, message))
        if message[:5] == "Arrow":
            self.do_movement(client, message)
        else:
            print(client["id"], message)


if __name__ == '__main__':
    app = App()
