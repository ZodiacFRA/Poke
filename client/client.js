"restric mode";

const imgPathArray = [
  "img/ground.png",
  "img/wall.png",
  "img/scientist.png",
  "img/pet.png",
  "img/player.png",
];

const URL = "localhost";
const PORT = 50000;
const SCREEN_WIDTH = 720;
const SCREEN_HEIGHT = 480;
const PLAYER_ID = "UnDesSix";
const TILE_SIZE = 32;

// WORK IN PROGRESS
const character = {
  image: () => {
    return image();
  },
};

// WORK IN PROGRESS
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
    switch (this.msgFromServer.type) {
      case "init_map":
        map.content = this.msgFromServer.map;
        map.height = map.content.bottom.length;
        map.width = map.content.bottom[0].length;
        display.setViewport(map.width, map.height);
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
    console.log("all images loaded");
    return this.images;
  },

  drawMap: function () {
    for (var y = 0; y < map.height; y++) {
      for (var x = 0; x < map.width; x++) {
        if (map.content.bottom[y][x] === 0)
          this.ctx.drawImage(this.images[0].obj, x * TILE_SIZE, y * TILE_SIZE);
        if (map.content.top[y][x] == 1)
          this.ctx.drawImage(this.images[1].obj, x * TILE_SIZE, y * TILE_SIZE);
        else if (map.content.top[y][x] == 2)
          this.ctx.drawImage(this.images[2].obj, x * TILE_SIZE, y * TILE_SIZE);
        else if (map.content.top[y][x] == 3)
          this.ctx.drawImage(this.images[3].obj, x * TILE_SIZE, y * TILE_SIZE);
      }
    }
  },
};

display.init();

server.listen();
keyboard.listen();
