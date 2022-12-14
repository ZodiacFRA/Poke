const SCREEN_WIDTH_TILES = 15;
const SCREEN_HEIGHT_TILES = 9;
const PLAYER_ID = "UnDesSix";
const SCALE = 4;
const TILE_SIZE = 32 * SCALE;
const FPS = 30;

const app = {
  pixiApp: null,
  map: null,
  textures: null,
  containers: {
    bottom: null,
    top: null,
  },
  player_pos: {
    x: -1,
    y: -1,
  },

  computeSprites: function (x, y, topLeftTileIdx) {
    let bottom_idx =
      this.map.bottom[topLeftTileIdx.y + y][topLeftTileIdx.x + x];
    if (bottom_idx >= 0) {
      // idx matches with the images index. If map[y][x] is 0, then idx = 0 and
      // the function will load imgSrc[0] as a texture.
      const sprite = new PIXI.Sprite(this.textures[bottom_idx]);
      sprite.setTransform(0, 0, SCALE, SCALE, 0, 0, 0, 0, 0, 0);
      sprite.x = x * TILE_SIZE;
      sprite.y = y * TILE_SIZE;
      this.containers.bottom.addChild(sprite);
    }
    let top_idx = this.map.top[topLeftTileIdx.y + y][topLeftTileIdx.x + x];
    if (top_idx >= 0) {
      let offsetPlayer = 0;
      if (top_idx > 999 && top_idx < 1004) offsetPlayer = 16 * SCALE;
      const sprite = new PIXI.Sprite(this.textures[top_idx]);
      sprite.setTransform(0, 0, SCALE, SCALE, 0, 0, 0, 0, 0, 0);
      sprite.x = x * TILE_SIZE;
      sprite.y = y * TILE_SIZE - offsetPlayer;
      this.containers.top.addChild(sprite);
    }
  },

  displayMap: function () {
    this.containers.bottom.removeChildren();
    this.containers.top.removeChildren();
    const topLeftTileIdx = {
      x: Math.max(this.player_pos.x - Math.trunc(SCREEN_WIDTH_TILES / 2), 0),
      y: Math.max(this.player_pos.y - Math.trunc(SCREEN_HEIGHT_TILES / 2), 0),
    };
    for (let y = 0; y < Math.min(SCREEN_HEIGHT_TILES, this.map.size_y); y++)
      for (let x = 0; x < Math.min(SCREEN_WIDTH_TILES, this.map.size_x); x++)
        this.computeSprites(x, y, topLeftTileIdx);
  },

  initContainers: function () {
    this.containers.bottom = new PIXI.Container();
    this.containers.top = new PIXI.Container();
    this.pixiApp.stage.addChild(this.containers.bottom);
    this.pixiApp.stage.addChild(this.containers.top);
  },

  initPixiApp: function () {
    this.pixiApp = new PIXI.Application({
      width: SCREEN_WIDTH_TILES * TILE_SIZE,
      height: SCREEN_HEIGHT_TILES * TILE_SIZE,
      background: "#000000",
    });
    PIXI.settings.SCALE_MODE = PIXI.SCALE_MODES.NEAREST;
    document.body.appendChild(this.pixiApp.view);
    imgSrc.buildPathArray();
  },

  init: function () {
    this.initPixiApp();
    this.initContainers();
    const texturesPromise = PIXI.Assets.load(imgSrc.name);
    texturesPromise.then((textures) => {
      this.textures = textures;
      console.log(imgSrc.name[200]);
      server.listen();
    });
  },
};

app.init();
