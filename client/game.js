const player = {
  position: {
    x: -1,
    y: -1,
  },

  initPosition: function () {
    this.position = this.getPosition();
  },

  getPosition: function () {
    for (var y = 0; y < map.height; y++) {
      for (var x = 0; x < map.width; x++) {
        if (map.content.top[y][x] == 2) {
          position.x = x;
          position.y = y;
          return { x: 0, y: 0 };
        }
      }
    }
  },

  getDirection: function () {
    const newPosition = this.getPosition();
    xOffset = newPosition.x - this.position.x;
    yOffset = newPosition.y - this.position.y;
    this.position = newPosition;
    console.log(xOffset, yOffset);

    if (yOffset === 1) return "down";
    else if (yOffset === -1) return "up";
    else if (xOffset === 1) return "right";
    else if (xOffset === -1) return "left";
    else return "";
  },
};
