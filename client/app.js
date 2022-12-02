const SCREEN_WIDTH_TILES = 15;
const SCREEN_HEIGHT_TILES = 9;
const PLAYER_ID = "UnDesSix";
const TILE_SIZE = 32;
const FPS = 30;


const app = {
  sprites: [],
  // display
  viewport: null,
  ctx: null,
  // data
  player: {
    pos: {
      x: 0,
      y: 0
    },
  },
  map: null,

  init: function() {
    this.loadSprites().then(() => server.listen());
    this.setViewport();
    this.ctx = this.viewport.getContext("2d");
  },

  loadSprites: async function() {
    const promiseArray = [];
    for (let imgPath of imgPathArray) {
      promiseArray.push(
        new Promise((resolve) => {
          const sprite = new image(imgPath);
          sprite.obj.onload = function() {
            resolve();
          };
          this.sprites.push(sprite);
        })
      );
    }
    await Promise.all(promiseArray); // wait for all the sprites to be loaded
    console.log(this.sprites.length, "sprites loaded");
    return this.sprites;
  },

  setViewport: function() {
    this.viewport = document.getElementById("viewport");
    this.viewport.width = Math.trunc(SCREEN_WIDTH_TILES * TILE_SIZE);
    this.viewport.height = Math.trunc(SCREEN_HEIGHT_TILES * TILE_SIZE);
  },

  updateMap: function(msgFromServer) {
    switch (msgFromServer.type) {
      case "add_entity":
        this.map.top[msgFromServer.pos.y][msgFromServer.pos.x] = msgFromServer.entity
        console.log("added entity", msgFromServer)
        break;
      case "delete_entity":
        this.map.top[msgFromServer.pos.y][msgFromServer.pos.x] = ""
        console.log("deleted entity", msgFromServer)
        break;
      case "move_entity":
        var entity = this.map.top[msgFromServer.from_pos.y][msgFromServer.from_pos.x]
        this.map.top[msgFromServer.from_pos.y][msgFromServer.from_pos.x] = ""
        this.map.top[msgFromServer.to_pos.y][msgFromServer.to_pos.x] = entity
        break;
    }
  },

  displayMap: function() {
    const topLeftTileIdx = {
      x: Math.max(this.player.pos.x - Math.trunc(SCREEN_WIDTH_TILES / 2), 0),
      y: Math.max(this.player.pos.y - Math.trunc(SCREEN_HEIGHT_TILES / 2), 0)
    };
    console.log("top left tile idxs:", topLeftTileIdx.y, topLeftTileIdx.x);
    for (let y = 0; y < Math.min(SCREEN_HEIGHT_TILES, this.map.size_y); y++) {
      for (let x = 0; x < Math.min(SCREEN_WIDTH_TILES, this.map.size_x); x++) {
        // console.log('-------------', "y:", topLeftTileIdx.y + y, "x:", topLeftTileIdx.x + x);
        var bottom_idx = this.map.bottom[topLeftTileIdx.y + y][topLeftTileIdx.x + x]
        if (!isNaN(bottom_idx) && bottom_idx <= this.sprites.length) {
          // console.log("bottom img path:", this.sprites[bottom_idx].obj.src);
          this.ctx.drawImage(this.sprites[bottom_idx].obj, x * TILE_SIZE, y * TILE_SIZE);
        }
        var top_idx = this.map.top[topLeftTileIdx.y + y][topLeftTileIdx.x + x]
        if (top_idx != "" && top_idx <= this.sprites.length) {
          // Here request the animation frames to the frame manager
          if (top_idx > 1) {
            console.log("top img path:", this.sprites[top_idx].obj.src);
            this.ctx.drawImage(this.sprites[top_idx].obj, 0, 0, 32, 48, x * TILE_SIZE, y * TILE_SIZE - 16, 32, 48);
          } else {
            this.ctx.drawImage(this.sprites[top_idx].obj, x * TILE_SIZE, y * TILE_SIZE);
          }
        }
      }
    }
  }

  // displayPlayer: function(direction) {
  //   const coord = {
  //     x: Math.trunc(SCREEN_WIDTH_TILES / 2) * TILE_SIZE,
  //     y: Math.trunc(SCREEN_HEIGHT_TILES / 2) * TILE_SIZE - 16,
  //   };
  //   const img = this.sprites[4].obj;
  //   switch (direction) {
  //     case "spawn":
  //     case "down":
  //       this.ctx.drawImage(img, 0, 0, 32, 48, coord.x, coord.y, 32, 48);
  //       break;
  //     case "up":
  //       this.ctx.drawImage(img, 0, 144, 32, 48, coord.x, coord.y, 32, 48);
  //       break;
  //     case "left":
  //       this.ctx.drawImage(img, 0, 48, 32, 48, coord.x, coord.y, 32, 48);
  //       break;
  //     case "right":
  //       this.ctx.drawImage(img, 0, 96, 32, 48, coord.x, coord.y, 32, 48);
  //       break;
  //   }
  //   // console.log("player displayed");
  // },
};


app.init();