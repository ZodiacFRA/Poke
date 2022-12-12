const SCREEN_WIDTH_TILES = 15;
const SCREEN_HEIGHT_TILES = 9;
const PLAYER_ID = "UnDesSix";
const TILE_SIZE = 16;
const FPS = 30;

const app = {
  app: null,
  map: null,
  textures: null,
  player: {
    pos: {
      x: -1,
      y: -1,
    },
    direction: -1,
  },

  init: function () {
    this.app = new PIXI.Application({
      width: SCREEN_WIDTH_TILES * TILE_SIZE,
      height: SCREEN_HEIGHT_TILES * TILE_SIZE,
      background: "#000000",
    });
    document.body.appendChild(this.app.view);
    imgSrc.buildPathArray();
    const texturesPromise = PIXI.Assets.load(imgSrc.name);
    texturesPromise.then((textures) => {
      this.textures = textures;
      console.log(imgSrc.name[200]);
      server.listen();
    });
  },

  displayMap: function () {
    bottomContainer = new PIXI.Container();
    topContainer = new PIXI.Container();
    // playerContainer = new PIXI.Container();
    this.app.stage.removeChildren();
    this.app.stage.addChild(bottomContainer);
    this.app.stage.addChild(topContainer);
    // this.app.stage.addChild(playerContainer);

    // // CREATE AND SAVE PLAYER INTO CONTAINERS
    // // offsetPlayer is a paramater to offset the player position
    // // player.height - TILE_SIZE = 48 - 32 = 16;
    // const spriteVal = this.map.top[this.player.pos.y][this.player.pos.x];
    // console.log(spriteVal);
    // const playerSprite = new PIXI.Sprite(this.textures[imgSrc.name[spriteVal]]);
    const playerSprite = { x: -1, y: -1 };
    playerSprite.x = Math.trunc(SCREEN_WIDTH_TILES / 2) * TILE_SIZE;
    playerSprite.y = Math.trunc(SCREEN_HEIGHT_TILES / 2) * TILE_SIZE;
    // playerContainer.addChild(playerSprite);

    // CREATE AND SAVE PLAYER INTO CONTAINERS
    const topLeftTileIdx = { x: -1, y: -1 };
    topLeftTileIdx.x = playerSprite.x - this.player.pos.x * TILE_SIZE;
    topLeftTileIdx.y = playerSprite.y - this.player.pos.y * TILE_SIZE;

    for (let y = 0; y < this.map.size_y; y++) {
      for (let x = 0; x < this.map.size_x; x++) {
        if (this.map.bottom[y][x] >= 0) {
          // idx matches with the images index. If map[y][x] is 0, then idx = 0 and
          // the function will load imgSrc[0] as a texture.
          const idx = this.map.bottom[y][x];
          const sprite = new PIXI.Sprite(this.textures[idx]);
          sprite.x = x * TILE_SIZE + topLeftTileIdx.x;
          sprite.y = y * TILE_SIZE + topLeftTileIdx.y;
          bottomContainer.addChild(sprite);
        }
        if (this.map.top[y][x] >= 0) {
          let offsetPlayer = 0;
          const idx = this.map.top[y][x];
          if (idx > 999 && idx < 2000) {
            offsetPlayer = 8;
          }
          const sprite = new PIXI.Sprite(this.textures[idx]);
          sprite.x = x * TILE_SIZE + topLeftTileIdx.x;
          sprite.y = y * TILE_SIZE + topLeftTileIdx.y - offsetPlayer;
          topContainer.addChild(sprite);
        }
      }
    }
  },
};

app.init();
