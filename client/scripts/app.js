const SCREEN_WIDTH_TILES = 15;
const SCREEN_HEIGHT_TILES = 8;
const PLAYER_ID = "UnDesSix";
const SCALE = 4;
const TILE_SIZE = 32 * SCALE;
const FPS = 30;

const app = {
  renderer: null,
  state: null,

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

  // animateFlowers: function () {
  //   const topLeftTileIdx = {
  //     x: Math.max(this.player_pos.x - Math.trunc(SCREEN_WIDTH_TILES / 2), 0),
  //     y: Math.max(this.player_pos.y - Math.trunc(SCREEN_HEIGHT_TILES / 2), 0),
  //   };
  //   for (let y = 0; y < Math.min(SCREEN_HEIGHT_TILES, this.map.size_y); y++)
  //     for (let x = 0; x < Math.min(SCREEN_WIDTH_TILES, this.map.size_x); x++) {
  //       let bottom_idx =
  //         this.map.bottom[topLeftTileIdx.y + y][topLeftTileIdx.x + x];
  //       if (
  //         (bottom_idx > 14 && bottom_idx < 19) ||
  //         (bottom_idx > 26 && bottom_idx < 31)
  //       ) {
  //         console.log("bottom_idx: ", bottom_idx);
  //         const sprite = new PIXI.Sprite(this.textures[0]);
  //         sprite.setTransform(0, 0, SCALE, SCALE, 0, 0, 0, 0, 0);
  //         sprite.x = x * TILE_SIZE;
  //         sprite.y = y * TILE_SIZE;
  //         this.containers.bottom.addChild(sprite);
  //       }
  //     }
  // },

  computeSprites: function (x, y, topLeftTileIdx) {
    let bottom_idx =
      this.map.bottom[topLeftTileIdx.y + y][topLeftTileIdx.x + x];
    if (
      (bottom_idx > 14 && bottom_idx < 19) ||
      (bottom_idx > 26 && bottom_idx < 31)
    ) {
      const sprite = new PIXI.Sprite(this.textures[214 + this.tickerFlag]); // FLOWERS SPRITES
      sprite.setTransform(0, 0, SCALE, SCALE, 0, 0, 0, 0, 0);
      sprite.x = x * TILE_SIZE;
      sprite.y = y * TILE_SIZE;
      this.containers.bottom.addChild(sprite);
    } else if (bottom_idx > -1) {
      // idx matches with the images index. If map[y][x] is 0, then idx = 0 and
      // the function will load imgSrc[0] as a texture.
      const sprite = new PIXI.Sprite(this.textures[bottom_idx]);
      sprite.setTransform(0, 0, SCALE, SCALE, 0, 0, 0, 0, 0);
      sprite.x = x * TILE_SIZE;
      sprite.y = y * TILE_SIZE;
      this.containers.bottom.addChild(sprite);
    }
    let top_idx = this.map.top[topLeftTileIdx.y + y][topLeftTileIdx.x + x];
    if (top_idx >= 0) {
      let offsetPlayer = 0;
      if (top_idx > 999 && top_idx < 1004) offsetPlayer = 16 * SCALE;
      const sprite = new PIXI.Sprite(this.textures[top_idx]);
      sprite.setTransform(0, 0, SCALE, SCALE, 0, 0, 0, 0, 0);
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
    this.stage.addChild(this.containers.bottom);
    this.stage.addChild(this.containers.top);
  },

  initPixiApp: function () {
    this.renderer = new PIXI.Renderer({
      width: SCREEN_WIDTH_TILES * TILE_SIZE,
      height: SCREEN_HEIGHT_TILES * TILE_SIZE,
      backgroundColor: 0x1099bf,
    });
    document.body.appendChild(this.renderer.view);
    this.stage = new PIXI.Container();
    PIXI.settings.SCALE_MODE = PIXI.SCALE_MODES.NEAREST;

    // TICKER PART
    // ----------------------------------------
    this.ticker = new PIXI.Ticker({
      autoPlay: false,
    });
    let totaltime = 0;
    this.ticker.add(() => {
      totaltime += this.ticker.deltaTime;
      if (totaltime < 20) this.tickerFlag = 0;
      else if (totaltime < 40) this.tickerFlag = 1;
      else if (totaltime < 60) this.tickerFlag = 2;
      else if (totaltime < 80) this.tickerFlag = 3;
      if (totaltime >= 80) totaltime = 0;
      this.displayMap();
      this.renderer.render(this.stage);
    }, PIXI.UPDATE_PRIORITY.LOW);
    // ----------------------------------------

    imgSrc.buildPathArray();
  },

  init: function () {
    this.initPixiApp();
    this.initContainers();
    const texturesPromise = PIXI.Assets.load(imgSrc.name);
    texturesPromise.then((textures) => {
      this.textures = textures;
      server.listen();
    });
  },
};

app.init();
