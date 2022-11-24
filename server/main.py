import json
import logging
from pprint import pprint

# https://github.com/Pithikos/python-websocket-server#api
from websocket_server import WebsocketServer

from Map import Map


class App(object):
    def __init__(self):
        super(App, self).__init__()
        self.map = Map(20, 20)
        self.server = WebsocketServer(host='localhost', port=50000, loglevel=logging.INFO)
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_message_received(self.msg_received)
        self.server.run_forever()

    def new_client(self, client, server):
        self.server.send_message_to_all("Hfey all, a new client has joined us")
        self.server.send_message(client, json.dumps(self.map.sprites))
        self.server.send_message(client, json.dumps(self.map.serialize()))

    def msg_received(self, client, server, message):
        print(client, message)


if __name__ == '__main__':
    app = App()
