"restric mode";

const URL = "localhost";
const PORT = 50000;
const SCREEN_WIDTH = 15;
const SCREEN_HEIGHT = 9;
const PLAYER_ID = "UnDesSix";
const TILE_SIZE = 32;
const FPS = 30;

const imgPathArray = [
  "img/ground.png",
  "img/wall.png",
  "img/scientist.png",
  "img/pet.png",
  "img/player.png",
];

class image {
  constructor(path) {
    this.obj = new Image();
    this.obj.src = path;
    if (this.obj.height > TILE_SIZE || this.obj.width > TILE_SIZE)
      this.isForeground = true;
  }
}

const map = {
  content: null,
  width: 0,
  height: null,
  playerMoved: true,

  movePlayer: function () {
    this.playerMoved = false;
    for (let i = 0; i < app.tileSize; i++) {
      //
    }
  },
};

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

const server = {
  connection: null,
  msgFromServer: null,
  msgToServer: null,

  connect: function () {
    this.connection = new WebSocket("ws://" + URL + ":" + PORT);
    this.msgToServer = {
      msg_type: "create_player",
      player_name: PLAYER_ID,
    };
    this.connection.onopen = () =>
      this.connection.send(JSON.stringify(this.msgToServer));
  },

  listen: function () {
    this.connect();
    keyboard.listen();

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
    console.log(this.msgFromServer);
    switch (this.msgFromServer.msg_type) {
      case "init_map":
        map.content = this.msgFromServer.map;
        map.height = map.content.bottom.length;
        map.width = map.content.bottom[0].length;
        break;
      case "delta":
        app.updateMap(this.msgFromServer);
        break;
    }
  },
};

const app = {
  viewport: null,
  ctx: null,
  images: [],

  init: function () {
    this.setViewport();
    this.setContext();
    this.loadImages().then(() => server.listen());
  },

  setViewport: function () {
    this.viewport = document.getElementById("viewport");
    this.viewport.width = SCREEN_WIDTH * TILE_SIZE;
    this.viewport.height = SCREEN_HEIGHT * TILE_SIZE;
  },

  setContext: function () {
    this.ctx = this.viewport.getContext("2d");
  },

  loadImages: async function () {
    // create an array for promises
    const promiseArray = [];

    for (let imgPath of imgPathArray) {
      promiseArray.push(
        new Promise((resolve) => {
          const img = new image(imgPath);
          img.obj.onload = function () {
            resolve();
          };
          this.images.push(img);
        })
      );
    }
    await Promise.all(promiseArray); // wait for all the images to be loaded
    console.log("loaded images");
    return this.images;
  },

  displayPlayer: function (direction) {
    const coord = {
      x: Math.trunc(SCREEN_WIDTH / 2) * TILE_SIZE,
      y: Math.trunc(SCREEN_HEIGHT / 2) * TILE_SIZE - 16,
    };
    const img = this.images[4].obj;
    switch (direction) {
      case "spawn":
      case "down":
        this.ctx.drawImage(img, 0, 0, 32, 48, coord.x, coord.y, 32, 48);
        break;
      case "up":
        this.ctx.drawImage(img, 0, 144, 32, 48, coord.x, coord.y, 32, 48);
        break;
      case "left":
        this.ctx.drawImage(img, 0, 48, 32, 48, coord.x, coord.y, 32, 48);
        break;
      case "right":
        this.ctx.drawImage(img, 0, 96, 32, 48, coord.x, coord.y, 32, 48);
        break;
    }
    // console.log("player displayed");
  },

  displayMap: function () {
    const topLeft = {
      x: player.position.x - Math.trunc(SCREEN_WIDTH / 2),
      y: player.position.y - Math.trunc(SCREEN_HEIGHT / 2),
    };

    for (let y = 0; y < SCREEN_HEIGHT; y++) {
      for (let x = 0; x < SCREEN_WIDTH; x++) {
        if (map.content.bottom[topLeft.y + y][topLeft.x + x] === 0)
          this.ctx.drawImage(this.images[0].obj, x * TILE_SIZE, y * TILE_SIZE);
        if (map.content.top[topLeft.y + y][topLeft.x + x] == 1)
          this.ctx.drawImage(this.images[1].obj, x * TILE_SIZE, y * TILE_SIZE);
      }
    }
    // console.log("map displayed");
  },

  updateMap: function (msgFromServer) {
    switch (msgFromServer.type) {
      case "add_entity":
        player.setPosition(msgFromServer.pos);
        this.displayMap();
        this.displayPlayer("spawn");
        break;
      case "delete_entity":
        player.setPosition({ x: -1, y: -1 });
        break;
      case "move_entity":
        player.setPosition(msgFromServer.to_pos);
        this.displayMap();
        this.displayPlayer(
          player.getDirection(msgFromServer.from_pos, msgFromServer.to_pos)
        );
        break;
    }
  },
};

app.init();
