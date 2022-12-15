const server = {
  url: "localhost",
  port: 50000,
  playerID: "UnDesSix",
  connection: null,
  msgFromServer: null,
  msgToServer: null,

  connect: function () {
    this.connection = new WebSocket("ws://" + this.url + ":" + this.port);
    this.msgToServer = {
      msg_type: "create_player",
      player_name: this.playerID,
    };
    this.connection.onopen = () =>
      this.connection.send(JSON.stringify(this.msgToServer));
  },

  listen: function () {
    this.connect();
    keyboard.listen();

    this.connection.onerror = (error) => {
      console.log("WebSocket error: ${error}");
    };

    this.connection.onmessage = (event) => {
      try {
        this.msgFromServer = JSON.parse(event.data);
        this.parseMsg();
      } catch (exception) {}
    };
  },

  parseMsg: function () {
    console.log(this.msgFromServer);
    switch (this.msgFromServer.msg_type) {
      case "init_map":
        app.map = this.msgFromServer.map;
        app.ticker.start();
        break;
      case "update":
        app.player_pos.x = this.msgFromServer.player_pos.x;
        app.player_pos.y = this.msgFromServer.player_pos.y;
        for (let i = 0; i < this.msgFromServer.data.length; i++) {
          this.updateMap(this.msgFromServer.data[i]);
        }
        app.displayMap();
        break;
    }
  },

  updateMap: function (msgFromServer) {
    switch (msgFromServer.type) {
      case "add_entity":
        app.map.top[msgFromServer.pos.y][msgFromServer.pos.x] =
          msgFromServer.entity;
        break;
      case "delete_entity":
        app.map.top[msgFromServer.pos.y][msgFromServer.pos.x] = -1;
        break;
      case "move_entity":
        var entity =
          app.map.top[msgFromServer.from_pos.y][msgFromServer.from_pos.x];
        app.map.top[msgFromServer.from_pos.y][msgFromServer.from_pos.x] = -1;
        app.map.top[msgFromServer.to_pos.y][msgFromServer.to_pos.x] = entity;
        break;
      case "update_entity":
        app.map.top[msgFromServer.pos.y][msgFromServer.pos.x] =
          msgFromServer.entity;
        break;
    }
  },
};
