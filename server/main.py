import time
import json
import copy
import logging
from pprint import pprint

# https://github.com/Pithikos/python-websocket-server#api
from websocket_server import WebsocketServer

import Globals
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
        # self.map_wrapper = MapWrapper("../utils/map_gen1_rot.json")
        self.map_wrapper = MapWrapper("../utils/translateMap/map_loadable.json")
        self.gameplay_events = []

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
        self.start_time = time.time()
        self.delta_time = 1/6  # 1/UpdatePerSecond
        Globals.turn_idx = 0

    def launch(self):
        while True:
            self.process_incoming_messages()
            self.process_living_entities()
            self.send_updates()
            self.tick()

    def process_living_entities(self):
        for id, entity in self.living_entities.items():
            entity.do_turn(self.map_wrapper, self.living_entities)

    def tick(self, debug=False):
        Globals.turn_idx += 1
        to_sleep = self.delta_time - (time.time() - self.start_time)
        if to_sleep <= 0:
            print(f"[-] - Main: Lagging behind: {to_sleep}")
        else:
            time.sleep(to_sleep)
        self.start_time = time.time()
        if debug:
            print('-'*50)

    ########################################
    ### Gameplay
    def check_for_player_interaction(self, player):
        """ Called after any player movement """
        # If another living entity in front of the player
        front_entity = self.map_wrapper.get_tile_in_front(
            player.pos,
            player.direction,
            top_entity_only=True
        )
        if type(front_entity) == Player:
            self.gameplay_events.append([
                player.id,
                {
                "type": "player_interaction",
                "player_1": player.name,
                "player_2": front_entity.name,
                "options": ["talk to", "fight"]
                }
            ])

    ########################################
    ### Message processing

    def add_new_player(self, client, msg):
        self.send_full_map()
        player_pos = self.map_wrapper.get_available_position()
        player_pos = Position(258, 75)
        player = Player(
            self.id_manager.create_new_id(client["id"]),
            player_pos,
            msg["player_name"]
        )
        self.living_entities[player.id] = player
        self.map_wrapper.add_entity(player.pos, player)
        print(f"Player spawned at position {player.pos}")
        self.add_pet(player)

    def add_pet(self, player, position=None):
        availableTiles = self.map_wrapper.pathfinder.get_tiles_at_distance_from(
            player.pos, 10
        )
        if availableTiles:
            tmp_pos = availableTiles[0]
        else:
            self.map_wrapper.get_available_position()
        pet_position = position if position else availableTiles[0]
        pet = Pet(
            id=self.id_manager.create_new_id(),
            pos=pet_position,
            owner=player
        )
        self.living_entities[pet.id] = pet
        self.map_wrapper.add_entity(pet.pos, pet)
        self.living_entities[player.id].pokedex.append(pet)
        print(f"Pet spawned at position {pet_position}")

    def do_movement(self, client, msg):
        engine_id = self.id_manager.get_engine_id(client["id"])
        player = self.living_entities[engine_id]
        old_dir = player.direction
        new_pos = None
        if msg["key"] == "ArrowUp":
            new_pos = player.pos + Globals.deltas[0]
        elif msg["key"] == "ArrowRight":
            new_pos = player.pos + Globals.deltas[1]
        elif msg["key"] == "ArrowDown":
            new_pos = player.pos + Globals.deltas[2]
        elif msg["key"] == "ArrowLeft":
            new_pos = player.pos + Globals.deltas[3]
        else:  # Not a movement nor a dir change
            return
        if self.map_wrapper.move_entity(player.pos, new_pos):
            self.check_for_player_interaction(player)

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

    def send_updates(self):
        """ Send map and gameplay events deltas """
        # TODO: This condition may need to change with the addition of self.gameplay_events
        if len(self.map_wrapper.map_events) == 0:
            return

        # Prepare the base of the message (which will be sent to every player)
        base_msg = {
            "msg_type": "update",
            "turn_idx": Globals.turn_idx,
            "data": [],
            "player_pos": {"y": -1, "x": -1}
        }
        while len(self.map_wrapper.map_events) > 0:
            base_msg["data"].append(self.map_wrapper.map_events.pop(0))

        # Create a dict with each players and their specific message
        clients_messages = {}
        for client in self.server.clients:
            engine_id = self.id_manager.get_engine_id(client["id"])
            if engine_id is None:
                print(f"[-] - Networking system, detected a connected client not linked to a player")
                continue
            msg = copy.copy(base_msg)
            # Add the position and direction of each player
            player = self.living_entities[engine_id]
            msg["player_pos"] = player.pos.get_json_repr()
            msg["player_direction"] = player.direction
            clients_messages[engine_id] = [client, msg]

        # Now add the gameplay events, which are specific to some players
        while len(self.gameplay_events) > 0:
            ge = self.gameplay_events.pop(0)
            # ge = [player engine id, {ge data}]
            # clients_messages[player_engine_id] = [network client object, msg]
            clients_messages[ge[0]][1]["data"].append(ge[1])

        # Now send the message to each player
        for engine_id, (client, msg) in clients_messages.items():
            self.server.send_message(client, json.dumps(msg))

    def send_full_map(self):
        map = self.map_wrapper.serialize()
        message = {"msg_type": "init_map", "map": map}
        self.server.send_message_to_all(json.dumps(message))

    def on_client_leave(self, client, server):
        engine_id = self.id_manager.get_engine_id(client["id"])
        # Remove all messages from this player in the message queue
        tmp = []
        for idx, (tmp_client, msg) in enumerate(self.incoming_messages):
            if tmp_client["id"] != client["id"]:
                tmp.append((tmp_client, msg))
        self.incoming_messages = tmp

        player = self.living_entities.pop(engine_id)
        print(f"[ ] - Networking system: Client left ({player})")
        for pet in player.pokedex:
            self.living_entities.pop(pet.id)
            self.map_wrapper.delete_entity(pet.pos)
        self.map_wrapper.delete_entity(player.pos)

    def on_msg_received(self, client, server, message):
        self.incoming_messages.append((client, message))


if __name__ == '__main__':
    app = App()
    app.launch()
