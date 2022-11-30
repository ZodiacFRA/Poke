"restric mode";

const URL = "localhost";
const PORT = 50000;
const SCREEN_WIDTH = 720;
const SCREEN_HEIGHT = 480;
const PLAYER_ID = "UnDesSix";
const TILE_SIZE = 32;
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
    for (let i = 0; i < display.tileSize; i++) {
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
      server.connection.send(JSON.stringify(server.msgToServer));
    });
  },
};

const server = {
  connection: new WebSocket("ws://" + URL + ":" + PORT),
  msgFromServer: null,
  msgToServer: null,

  connect: function () {
    this.msgToServer = {
      msg_type: "create_player",
      player_name: PLAYER_ID,
    };
    this.connection.onopen = () =>
      this.connection.send(JSON.stringify(this.msgToServer));
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
    switch (this.msgFromServer.msg_type) {
      case "init_map":
        map.content = this.msgFromServer.map;
        map.height = map.content.bottom.length;
        map.width = map.content.bottom[0].length;
        display.setViewport(map.width, map.height); // Temporary as viewport should be always fix
        // if (player.isUninitialized()) player.initPosition();
        // else player.getDirection();
        display.drawMap();
        break;
      case "delta":
        console.log(this.msgFromServer);
        display.updateMap(this.msgFromServer);
        break;
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
    this.loadImages().then(() => display.drawMap());
  },

  setViewport: function (width, height) {
    this.viewport = document.getElementById("viewport");
    this.viewport.width = width * TILE_SIZE;
    this.viewport.height = height * TILE_SIZE;
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
    return this.images;
  },

  drawMap: function () {
    for (var y = 0; y < map.height; y++) {
      for (var x = 0; x < map.width; x++) {
        if (map.content.bottom[y][x] === 0)
          this.ctx.drawImage(this.images[0].obj, x * TILE_SIZE, y * TILE_SIZE);
        if (map.content.top[y][x] == 1)
          this.ctx.drawImage(this.images[1].obj, x * TILE_SIZE, y * TILE_SIZE);
      }
    }
  },

  updateMap: function (msgFromServer) {
    switch (msgFromServer.type) {
      case "add_entity":
        const tmp = msgFromServer.entity + 1; // + 1 is temporary using pikachu instead of player (32x32 is better)
        map.content.top[msgFromServer.pos.y][msgFromServer.pos.x] = tmp;
        this.ctx.drawImage(
          this.images[tmp].obj, // + 1 is temporary using pikachu instead of player (32x32 is better)
          msgFromServer.pos.x * TILE_SIZE,
          msgFromServer.pos.y * TILE_SIZE
        );
        break;
      case "delete_entity":
        this.ctx.drawImage(
          this.images[0].obj,
          msgFromServer.pos.x * TILE_SIZE,
          msgFromServer.pos.y * TILE_SIZE
        );
        break;
      case "move_entity":
        const entityBot =
          map.content.bottom[msgFromServer.from_pos.y][
            msgFromServer.from_pos.x
          ];
        const entityTop =
          map.content.top[msgFromServer.from_pos.y][msgFromServer.from_pos.x];
        console.log(entityBot, entityTop);
        map.content.top[msgFromServer.to_pos.y][msgFromServer.to_pos.x] =
          map.content.top[msgFromServer.from_pos.y][msgFromServer.from_pos.x];
        map.content.top[msgFromServer.from_pos.y][msgFromServer.from_pos.x] =
          "";
        this.ctx.drawImage(
          this.images[entityBot].obj,
          msgFromServer.from_pos.x * TILE_SIZE,
          msgFromServer.from_pos.y * TILE_SIZE
        );
        this.ctx.drawImage(
          this.images[entityTop].obj,
          msgFromServer.to_pos.x * TILE_SIZE,
          msgFromServer.to_pos.y * TILE_SIZE
        );
        break;
    }
  },
};

const player = {
  position: {
    x: -1,
    y: -1,
  },

  initPosition: function () {
    this.position = this.getPosition();
  },

  isUninitialized: function () {
    if (this.position.x === -1) return true;
    else return false;
  },

  getPosition: function () {
    position = { x: 0, y: 0 };
    for (var y = 0; y < map.height; y++) {
      for (var x = 0; x < map.width; x++) {
        if (map.content.top[y][x] == 2) {
          position.x = x;
          position.y = y;
          return position;
        }
      }
    }
  },

  getDirection: function () {
    xOffset = this.getPosition().x - this.position.x;
    yOffset = this.getPosition().y - this.position.y;
    console.log(xOffset, yOffset);

    if (yOffset === 1) return "down";
    else if (yOffset === -1) return "up";
    else if (xOffset === 1) return "right";
    else if (xOffset === -1) return "left";
    else return "";
  },
};

display.init();

server.listen();
keyboard.listen();
