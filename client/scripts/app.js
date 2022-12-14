const SCREEN_WIDTH_TILES = 15;
const SCREEN_HEIGHT_TILES = 9;
const PLAYER_ID = "UnDesSix";
const SCALE = 4;
const TILE_SIZE = 32 * SCALE;
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

  init: function() {
    this.app = new PIXI.Application({
      width: SCREEN_WIDTH_TILES * TILE_SIZE,
      height: SCREEN_HEIGHT_TILES * TILE_SIZE,
      background: "#000000",
    });
    PIXI.settings.SCALE_MODE = PIXI.SCALE_MODES.NEAREST;
    document.body.appendChild(this.app.view);
    imgSrc.buildPathArray();
    const texturesPromise = PIXI.Assets.load(imgSrc.name);
    texturesPromise.then((textures) => {
      this.textures = textures;
      console.log(imgSrc.name[200]);
      server.listen();
    });
  },

  displayMap: function() {
    bottomContainer = new PIXI.Container();
    topContainer = new PIXI.Container();
    // playerContainer = new PIXI.Container();
    this.app.stage.removeChildren();
    this.app.stage.addChild(bottomContainer);
    this.app.stage.addChild(topContainer);
    const topLeftTileIdx = {
      x: Math.max(this.player.pos.x - Math.trunc(SCREEN_WIDTH_TILES / 2), 0),
      y: Math.max(this.player.pos.y - Math.trunc(SCREEN_HEIGHT_TILES / 2), 0),
    };
    for (let y = 0; y < Math.min(SCREEN_HEIGHT_TILES, this.map.size_y); y++) {
      for (let x = 0; x < Math.min(SCREEN_WIDTH_TILES, this.map.size_x); x++) {
        var bottom_idx =
          this.map.bottom[topLeftTileIdx.y + y][topLeftTileIdx.x + x];
        if (bottom_idx >= 0) {
          // idx matches with the images index. If map[y][x] is 0, then idx = 0 and
          // the function will load imgSrc[0] as a texture.
          const sprite = new PIXI.Sprite(this.textures[bottom_idx]);
          sprite.setTransform(0, 0, SCALE, SCALE, 0, 0, 0, 0, 0, 0);
          sprite.x = x * TILE_SIZE;
          sprite.y = y * TILE_SIZE;
          bottomContainer.addChild(sprite);
        }
        var top_idx = this.map.top[topLeftTileIdx.y + y][topLeftTileIdx.x + x];
        if (top_idx >= 0) {
          let offsetPlayer = 0;
          if (top_idx > 999 && top_idx < 1004) {
            offsetPlayer = 8 * SCALE;
          }
          const sprite = new PIXI.Sprite(this.textures[top_idx]);
          sprite.setTransform(0, 0, SCALE, SCALE, 0, 0, 0, 0, 0, 0);
          sprite.x = x * TILE_SIZE;
          sprite.y = y * TILE_SIZE - offsetPlayer;
          topContainer.addChild(sprite);
        }
      }
    }
  },
};

app.init();