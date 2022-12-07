const imgSrc = {
  name: [],
  path: [
    "sprites/ground.png",
    "sprites/ground2.png",
    "sprites/wall.png",
    "sprites/player_up.png",
    "sprites/player_right.png",
    "sprites/player_down.png",
    "sprites/player_left.png",
    "sprites/pet.png",
  ],
};

class image {
  constructor(path) {
    this.obj = new Image();
    this.obj.src = path;
    if (this.obj.height > TILE_SIZE || this.obj.width > TILE_SIZE)
      this.isForeground = true;
  }
}

const keyboard = {
  listen: function () {
    window.addEventListener("keydown", (e) => {
      server.msgToServer = {
        msg_type: "key_input",
        key: e.key,
      };
      if (server.connection)
        server.connection.send(JSON.stringify(server.msgToServer));
    });
  },
};
