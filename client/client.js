"restric mode";

const imagesPath = ["img/ground.png", "img/wall.png", "img/player.png"];
const URL = "localhost";
const PORT = 50000;
const SCREEN_WIDTH = 720;
const SCREEN_HEIGHT = 480;
const PLAYER_ID = "UnDesSix";
const TILE_SIZE = 16;

const keyboard = {
  listen: function () {
    window.addEventListener("keydown", (e) => {
      server.msgToServer = { type: "key_event", content: "e.key" };
      server.connection.send(server.msgToServer);
    });
  },
};

class image {
  constructor(path) {
    this.obj = new Image();
    this.obj.src = path;
    if (obj.height > TILE_SIZE || obj.width > TILE_SIZE)
      this.isForeground = true;
  }
}

const character = {
  image: () => {
    return image();
  },
};

const game = {
  map: {
    content: null,
    width: 0,
    height: null,
    sprites: null,
  },
  playerMoved: true,

  movePlayer: function () {
    this.playerMoved = false;
    for (let i = 0; i < display.tileSize; i++) {
      //
    }
  },
};

const server = {
  connection: new WebSocket("ws://" + URL + ":" + PORT),
  msgFromServer: null,
  msgToServer: null,

  connect: function () {
    this.msgToServer = { type: "new_connection", content: PLAYER_ID };
    this.connection.onopen = () =>
      this.connection.send(JSON.stringify(msgToServer));
  },

  listen: function () {
    this.connect();

    this.connection.onerror = (error) => {
      console.log(`WebSocket error: ${error}`);
    };

    this.connection.onmessage = (event) => {
      try {
        this.msgFromServer = JSON.parse(event.data);
        this.parseMsg();
      } catch (exception) {}
    };
  },

  parseMsg: function () {
    switch (this.msgFromServer.type) {
      case "init_map":
        game.map.content = this.msgFromServer.map;
        game.map.height = game.map.content.bottom.length;
        game.map.width = game.map.content.bottom[0].length;
        game.map.sprites = this.msgFromServer.sprites_table;
        display.drawMap();
    }
  },
};

const display = {
  viewport: null,
  ctx: null,
  images: [],

  init: function () {
    this.setViewport();
    this.setContext();
    this.loadImages();
  },

  setViewport: function () {
    this.viewport = document.getElementById("viewport");
    this.viewport.width = SCREEN_WIDTH;
    this.viewport.height = SCREEN_HEIGHT;
  },

  setContext: function () {
    this.ctx = this.viewport.getContext("2d");
  },

  loadImages: function () {
    for (var i = 0; i < imagesPath.length; i++) {
      this.images.push(new Image());
      this.images[i].src = imagesPath[i];
    }
  },

  // NEED TP INSERT SEUB FUNCTION INSTEAD
  drawMap: function () {
    for (var y = 0; y < game.map.height; y++) {
      for (var x = 0; x < game.map.width; x++) {
        // DRAW BACKGROUND
        this.ctx.drawImage(this.images[1], x * TILE_SIZE, y * TILE_SIZE);
        // DRAW OBJECT

        // DRAW FOREGROUND
      }
    }
  },
};

display.init();
server.listen();
keyboard.listen();
