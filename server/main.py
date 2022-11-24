import json
import logging
from pprint import pprint

# https://github.com/Pithikos/python-websocket-server#api
from websocket_server import WebsocketServer

from Map import Map
from Entities import Player
from utils import Position


class App(object):
    def __init__(self):
        super(App, self).__init__()
        self.map = Map(20, 20)
        self.players = {}

        self.server = WebsocketServer(host='localhost', port=50000, loglevel=logging.INFO)
        self.server.set_fn_new_client(self.on_new_client)
        self.server.set_fn_message_received(self.on_msg_received)
        self.server.run_forever()

    def on_new_client(self, client, server):
        # Create the new player
        player_pos = Position(1, 1)
        player = Player(Position(1, 1), "jm", client["id"])
        self.players[client["id"]] = player
        self.map.add_player(player)

        map = self.map.serialize()
        message = {"type": "init_map", "sprites_table": self.map.sprites, "map": map}
        self.server.send_message_to_all(json.dumps(message))

    def on_msg_received(self, client, server, message):
        print(client["id"], message)
        if message == "ArrowUp":
            player_pos = self.players[client["id"]].pos
            new_pos = Position(player_pos.y - 1, player_pos.x)
            is_colliding_pos = self.map.is_colliding_pos(new_pos)
            if not is_colliding_pos:
                self.map.move(player_pos, new_pos)
                self.players[client["id"]].pos.y -= 1
        elif message == "ArrowDown":
            player_pos = self.players[client["id"]].pos
            new_pos = Position(player_pos.y + 1, player_pos.x)
            is_colliding_pos = self.map.is_colliding_pos(new_pos)
            if not is_colliding_pos:
                self.map.move(player_pos, new_pos)
                self.players[client["id"]].pos.y += 1
        elif message == "ArrowLeft":
            player_pos = self.players[client["id"]].pos
            new_pos = Position(player_pos.y, player_pos.x - 1)
            is_colliding_pos = self.map.is_colliding_pos(new_pos)
            if not is_colliding_pos:
                self.map.move(player_pos, new_pos)
                self.players[client["id"]].pos.x -= 1
        elif message == "ArrowRight":
            player_pos = self.players[client["id"]].pos
            new_pos = Position(player_pos.y, player_pos.x + 1)
            is_colliding_pos = self.map.is_colliding_pos(new_pos)
            if not is_colliding_pos:
                self.map.move(player_pos, new_pos)
                self.players[client["id"]].pos.x += 1

        map = self.map.serialize()
        message = {"type": "init_map", "sprites_table": self.map.sprites, "map": map}
        self.server.send_message_to_all(json.dumps(message))


if __name__ == '__main__':
    app = App()
