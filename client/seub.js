var viewport_shape = [0, 0];

var set_viewport_size = function () {
  canva_view = document.getElementById("viewport");
  canva_view.width = canva_view.clientWidth;
  canva_view.height = canva_view.clientHeight;
  viewport_shape = [canva_view.clientWidth, canva_view.clientHeight];
};

set_viewport_size();

// RESIZE FOR VIEWPORT
addEventListener("resize", (event) => {
  set_viewport_size();
});

// var player_pos = [2,2];
// var view_distance = 28;

// function drawMap() {
//   var half_disp_width = viewport_shape[0] / 16 / 2;
//   var half_disp_height = viewport_shape[1] / 16 / 2;

//   for (let y = Math.floor(player_pos[0] - half_disp_height); y < player_pos[0] + half_disp_height; y++) {
//     if (y < 0 || y >= mapJson.bottom.length)
//       continue
//     for (let x = Math.floor(player_pos[1] - half_disp_width); x < player_pos[1] + half_disp_width; x++) {
//       if (x < 0 || x >= mapJson.bottom[y].length)
//         continue
//       // console.log("dlkajsld;kfj ", mapJson.bottom[y][x], mapJson.top[y][x])
//       c.drawImage(db_img[spriteJson[mapJson.bottom[y][x]]], x * pixelSize - pixelSize / 2 + half_disp_width * 16, y * pixelSize - pixelSize / 2 + half_disp_height * 16);
//       if (mapJson.top[y][x])
//         c.drawImage(db_img[spriteJson[mapJson.top[y][x]]], x * pixelSize - pixelSize / 2 + half_disp_width * 16, y * pixelSize - pixelSize / 2 + half_disp_height * 16);
//     }
//   }

//   console.log("\n\n")
// }
