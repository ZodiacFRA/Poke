const imgSrc = {
  name: [],
  pathArray: [],

  fillNames: function(i) {
    tmp_str = "../sprites/" + i + ".png";
    this.pathArray.push(tmp_str);
    this.name.push(i.toString());
  },

  buildPathArray: function() {
    // Base sprites
    for (let i = 0; i <= 211; i++)
      this.fillNames(i)
    // Characters sprites
    for (let i = 1000; i <= 1007; i++)
      this.fillNames(i)
    // Debug sprites
    for (let i = 2000; i <= 2003; i++)
      this.fillNames(i)
    // Add to asset pool
    for (let i = 0; i < this.name.length; i++)
      PIXI.Assets.add(this.name[i], this.pathArray[i]);
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
  listen: function() {
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