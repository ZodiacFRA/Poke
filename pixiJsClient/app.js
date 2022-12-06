const SCREEN_WIDTH_TILES = 15;
const SCREEN_HEIGHT_TILES = 9;
const PLAYER_ID = "UnDesSix";
const TILE_SIZE = 32;
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

    this.addSprites();
    const texturesPromise = PIXI.Assets.load(imgSrc.name);
    texturesPromise.then((textures) => {
      this.textures = textures;
      server.listen();
    });
  },

  addSprites: function () {
    for (let i = 0; i < imgSrc.path.length; i++) {
      imgSrc.name[i] = imgSrc.path[i].split("/")[1].split(".")[0];
      PIXI.Assets.add(imgSrc.name[i], imgSrc.path[i]);
    }
  },

  buildMap: function () {
    bottomContainer = new PIXI.Container();
    topContainer = new PIXI.Container();
    playerContainer = new PIXI.Container();
    this.app.stage.removeChildren();
    this.app.stage.addChild(bottomContainer);
    this.app.stage.addChild(topContainer);
    this.app.stage.addChild(playerContainer);

    // Create player
    const playerSprite = new PIXI.Sprite(
      this.textures[imgSrc.name[3 + this.player.direction]]
    );
    playerSprite.x = Math.trunc(SCREEN_WIDTH_TILES / 2) * TILE_SIZE;
    playerSprite.y = Math.trunc(SCREEN_HEIGHT_TILES / 2) * TILE_SIZE;
    playerContainer.addChild(playerSprite);

    // Create MAP
    const topLeftTileIdx = { x: -1, y: -1 };
    topLeftTileIdx.x = playerSprite.x - this.player.pos.x * TILE_SIZE;
    topLeftTileIdx.y = playerSprite.y - this.player.pos.y * TILE_SIZE;

    for (let y = 0; y < this.map.size_y; y++) {
      for (let x = 0; x < this.map.size_x; x++) {
        if (this.map.bottom[y][x] >= 0) {
          const idx = this.map.bottom[y][x];
          const ground = new PIXI.Sprite(this.textures[imgSrc.name[idx]]);
          ground.x = x * TILE_SIZE + topLeftTileIdx.x;
          ground.y = y * TILE_SIZE + topLeftTileIdx.y;
          bottomContainer.addChild(ground);
        }
        if (this.map.top[y][x] >= 0) {
          const idx = this.map.top[y][x];
          const ground = new PIXI.Sprite(this.textures[imgSrc.name[idx]]);
          ground.x = x * TILE_SIZE + topLeftTileIdx.x;
          ground.y = y * TILE_SIZE + topLeftTileIdx.y;
          topContainer.addChild(ground);
        }
      }
    }
  },
};

app.init();
