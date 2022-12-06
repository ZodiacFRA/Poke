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
        break;
      case "update":
        app.player.pos.x = this.msgFromServer.player_pos.x;
        app.player.pos.y = this.msgFromServer.player_pos.y;
        app.player.direction = this.msgFromServer.player_direction;
        app.displayMap();
        break;
    }
  },
};
