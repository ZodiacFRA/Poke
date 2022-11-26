import time
import json
import random
import logging
from pprint import pprint

# https://github.com/Pithikos/python-websocket-server#api
from websocket_server import WebsocketServer

import Global
from Entities import *
from Map import MapWrapper
from IdManager import IdManager
from HelperClasses import Position


class App(object):
    def __init__(self):
        super(App, self).__init__()
        ### Game state
        self.id_manager = IdManager()
        self.living_entities = {}
        self.map_wrapper = MapWrapper("./maps/pathfinding_demo_map.txt")

        ### Networking
        self.incoming_messages = []
        self.message_types_functions = {
            "enter_game": self.add_new_player,
            "key_input": self.do_movement
        }
        self.delta_messages = []

        self.server = WebsocketServer(host='localhost', port=50000, loglevel=logging.INFO)
        # TODO: remove set_fn_new_client as this will be handled by a specific message
        # when the client is ready
        self.server.set_fn_new_client(self.add_new_player)
        self.server.set_fn_client_left(self.on_client_leave)
        self.server.set_fn_message_received(self.on_msg_received)
        self.server.run_forever(threaded=True)
        ### Game loop
        self.delta_time = 1/10  # 1/FPS
        Global.turn_idx = 0
        self.launch()

    def launch(self):
        while True:
            start_time = time.time()
            # print("tick")
            self.process_incoming_messages()

            self.process_living_entities()

            self.send_deltas()
            # TODO: Remove this whole map update, client should use deltas now
            map = self.map_wrapper.serialize()
            message = {"type": "init_map", "sprites_table": self.map_wrapper.sprites, "map": map}
            self.server.send_message_to_all(json.dumps(message))

            Global.turn_idx += 1
            time.sleep(self.delta_time - (time.time() - start_time))

    def process_living_entities(self):
        for id, entity in self.living_entities.items():
            entity.do_turn(self.map_wrapper, self.living_entities)

    ########################################
    ### Message processing

    def add_new_player(self, client, msg):
        player_pos = self.map_wrapper.get_available_position()
        player_pos = Position(1, 6)
        player = Player(
            self.id_manager.create_new_id(client["id"]),
            player_pos,
            "jean michel"
        )
        self.living_entities[player.id] = player
        self.map_wrapper.add_entity(player.pos, player)
        print(f"Player spawned at position {player.pos}")

        ##### TMP, give the player a pet
        pet_position = self.map_wrapper.get_available_position()
        pet_position = Position(3, 7)
        print(f"Pet spawning at position {pet_position}")
        pet = Pet(
            id=self.id_manager.create_new_id(),
            pos=pet_position,
            owner_id=player.id
        )
        self.living_entities[pet.id] = pet
        self.map_wrapper.add_entity(pet.pos, pet)

    def do_movement(self, client, msg):
        engine_id = self.id_manager.get_engine_id(client["id"])
        player_pos = self.living_entities[engine_id].pos
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
        # No need to check for collisions
        # we just ignore if the move isn't possible
        self.map_wrapper.move_entity(player_pos, new_pos)

    ########################################3
    ### Networking

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

    def send_deltas(self):
        """ Send map and game events deltas """
        while len(self.map_wrapper.map_events_deltas) > 0:
            delta = self.map_wrapper.map_events_deltas.pop(0)
            delta["turn_idx"] = Global.turn_idx
            # DEBUG:
            print("\tDelta: ", end='')
            pprint(delta)

            self.server.send_message_to_all(json.dumps(delta))

    def on_client_leave(self, client, server):
        player = self.players.pop(client["id"])
        self.map_wrapper.delete_entity(player.pos)

    def on_msg_received(self, client, server, message):
        self.incoming_messages.append((client, message))
        if message[:5] == "Arrow":
            self.do_movement(client, message)


if __name__ == '__main__':
    app = App()
