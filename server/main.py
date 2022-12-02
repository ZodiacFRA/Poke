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
        self.map_wrapper = MapWrapper("./maps/map")

        ### Networking
        self.incoming_messages = []
        self.message_types_functions = {
            "create_player": self.add_new_player,
            "key_input": self.do_movement
        }
        self.delta_messages = []
        self.server = WebsocketServer(
            host='localhost',
            port=50000,
            loglevel=logging.INFO
        )
        self.server.set_fn_client_left(self.on_client_leave)
        self.server.set_fn_message_received(self.on_msg_received)
        self.server.run_forever(threaded=True)
        ### Game loop
        self.delta_time = 1/4  # 1/UpdatePerSecond
        Global.turn_idx = 0
        ### Utils
        self.pos_deltas = (
            Position(-1, 0),
            Position(0, 1),
            Position(1, 0),
            Position(0, -1)
        )

        self.launch()

    def launch(self):
        while True:
            # print('-'*50)  # DEBUG:
            start_time = time.time()
            self.process_incoming_messages()

            self.process_living_entities()

            self.send_update()
            # self.map_wrapper.display_ascii()  # DEBUG:
            Global.turn_idx += 1
            time.sleep(self.delta_time - (time.time() - start_time))

    def process_living_entities(self):
        for id, entity in self.living_entities.items():
            entity.do_turn(self.map_wrapper, self.living_entities)

    ########################################
    ### Message processing

    def add_new_player(self, client, msg):
        self.send_full_map()
        player_pos = self.map_wrapper.get_available_position()
        player = Player(
            self.id_manager.create_new_id(client["id"]),
            player_pos,
            msg["player_name"]
        )
        self.living_entities[player.id] = player
        self.map_wrapper.add_entity(player.pos, player)
        print(f"Player spawned at position {player.pos}")
        # self.add_pet(player)  # (Matthieu: I hate animals)

    def add_pet(self, player, position=None):
        pet_position = position if position else self.map_wrapper.get_available_position()
        pet = Pet(
            id=self.id_manager.create_new_id(),
            pos=pet_position,
            owner=player
        )
        self.living_entities[pet.id] = pet
        self.map_wrapper.add_entity(pet.pos, pet)
        self.living_entities[player.id].pets.append(pet)
        print(f"Pet spawned at position {pet_position}")

    def do_movement(self, client, msg):
        engine_id = self.id_manager.get_engine_id(client["id"])
        player = self.living_entities[engine_id]
        if msg["key"] == "ArrowUp":
            new_pos = player.pos + self.pos_deltas[0]
            player.direction = 0
        elif msg["key"] == "ArrowRight":
            new_pos = player.pos + self.pos_deltas[1]
            player.direction = 1
        elif msg["key"] == "ArrowDown":
            new_pos = player.pos + self.pos_deltas[2]
            player.direction = 2
        elif msg["key"] == "ArrowLeft":
            new_pos = player.pos + self.pos_deltas[3]
            player.direction = 3
        else:  # Not a movement
            return
        # No need to check for collisions
        # we just ignore if the move isn't possible
        self.map_wrapper.move_entity(player.pos, new_pos)

    ########################################3
    ### Networking

    def process_incoming_messages(self):
        # Clients can only do one input per turn, use the first one
        done_clients = []
        while len(self.incoming_messages) > 0:
            client, msg = self.incoming_messages.pop()
            if client["id"] in done_clients:
                continue
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
                    done_clients.append(client["id"])

    def send_update(self):
        """ Send map and game events deltas """
        if len(self.map_wrapper.map_events) == 0:
            return
        # Prepare the base of the message (which will be sent to every player)
        delta = {
            "msg_type": "update",
            "turn_idx": Global.turn_idx,
            "data": [],
            "player_pos": {"y": -1, "x": -1}
        }
        while len(self.map_wrapper.map_events) > 0:
            delta["data"].append(self.map_wrapper.map_events.pop(0))
        # Add the position of each player and send him the full message
        for client in self.server.clients:
            engine_id = self.id_manager.get_engine_id(client["id"])
            if engine_id is None:
                continue
            pos = self.living_entities[engine_id].pos
            delta["player_pos"]["y"] = pos.y
            delta["player_pos"]["x"] = pos.x
            self.server.send_message(client, json.dumps(delta))

    def send_full_map(self):
        map = self.map_wrapper.serialize()
        message = {"msg_type": "init_map", "map": map}
        self.server.send_message_to_all(json.dumps(message))

    def on_client_leave(self, client, server):
        print("left")
        engine_id = self.id_manager.get_engine_id(client["id"])
        # Remove all messages from this player in the message queue
        tmp = []
        for idx, (tmp_client, msg) in enumerate(self.incoming_messages):
            if tmp_client["id"] != client["id"]:
                tmp.append((tmp_client, msg))
        self.incoming_messages = tmp

        player = self.living_entities.pop(engine_id)
        self.map_wrapper.delete_entity(player.pos)

    def on_msg_received(self, client, server, message):
        # print(message)  # DEBUG:
        self.incoming_messages.append((client, message))


if __name__ == '__main__':
    app = App()
