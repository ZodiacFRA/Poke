const player = {
  position: {
    x: -1,
    y: -1,
  },

  setPosition: function (position) {
    this.position.x = position.x;
    this.position.y = position.y;
    // console.log("position: ", this.position.x, this.position.y);
  },

  getDirection: function (fromPos, toPos) {
    xOffset = toPos.x - fromPos.x;
    yOffset = toPos.y - fromPos.y;
    // console.log("offset: ", xOffset, yOffset);

    if (yOffset === 1) return "down";
    else if (yOffset === -1) return "up";
    else if (xOffset === 1) return "right";
    else if (xOffset === -1) return "left";
    else return "";
  },
};
