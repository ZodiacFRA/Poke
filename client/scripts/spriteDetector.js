const spriteDetector = {
  isFlower: function (idx) {
    if ((idx > 14 && idx < 19) || (idx > 26 && idx < 31)) return true;
    return false;
  },
};
