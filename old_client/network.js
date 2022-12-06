const URL = "localhost";
const PORT = 50000;


const server = {
  connection: null,
  msgFromServer: null,
  msgToServer: null,

  connect: function() {
    this.connection = new WebSocket("ws://" + URL + ":" + PORT);
    this.msgToServer = {
      msg_type: "create_player",
      player_name: PLAYER_ID,
    };
    this.connection.onopen = () =>
      this.connection.send(JSON.stringify(this.msgToServer));
  },

  listen: function() {
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

  parseMsg: function() {
    console.log(this.msgFromServer);
    switch (this.msgFromServer.msg_type) {
      case "init_map":
        app.map = this.msgFromServer.map;
        app.displayMap();
        break;
      case "update":
        app.player.pos.y = this.msgFromServer.player_pos.y
        app.player.pos.x = this.msgFromServer.player_pos.x
        for (let i = 0; i < this.msgFromServer.data.length; i++) {
          app.updateMap(this.msgFromServer.data[i]);
        }
        app.displayMap();
        break;
    }
  },
};