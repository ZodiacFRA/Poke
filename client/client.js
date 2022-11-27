"restric mode";

// Create websocket connection
const url = "ws://localhost:50000";
const connection = new WebSocket(url);

// Shoud not be hardcoded
const pixelSize = 16;
const mapWidth = 20;
const mapHeight = 20;

// Get and resize canvas
const canvas = document.getElementById("viewport");
// canvas.width = mapWidth * pixelSize;
// canvas.height = mapHeight * pixelSize;

// Return a drawing context on the canvas
const c = canvas.getContext("2d");

// Create images and import them
const groundImg = new Image();
groundImg.src = "img/ground.png";
const wallImg = new Image();
wallImg.src = "img/wall.png";
const playerImg = new Image();
playerImg.src = "img/player.png";

// Global variables to store received data (sprite unused for now)
let mapJson;
let spriteJson;

// When (and if) a connection is established
connection.onopen = () => {
  connection.send("Matthieu");
  window.addEventListener("keydown", (e) => {
    connection.send(e.key);
  });
};

connection.onerror = (error) => {
  console.log(`WebSocket error: ${error}`);
};

// Each time an update is received, the onmessage event occurs
connection.onmessage = (e) => {
  const msg = JSON.parse(e.data);
  console.log(msg);

  switch (msg.type) {
    case "init_map":
      mapJson = msg.map;
      spriteJson = msg.sprites_table;
      console.log(msg.sprites_table);
      drawMap();
  }
};

var player_pos = [2,2];
var view_distance = 28;

function drawMap() {
  var half_disp_width = viewport_shape[0] / 16 / 2;
  var half_disp_height = viewport_shape[1] / 16 / 2;

  for (let y = Math.floor(player_pos[0] - half_disp_height); y < player_pos[0] + half_disp_height; y++) {
    if (y < 0 || y >= mapJson.bottom.length)
      continue
    for (let x = Math.floor(player_pos[1] - half_disp_width); x < player_pos[1] + half_disp_width; x++) {
      if (x < 0 || x >= mapJson.bottom[y].length)
        continue
      // console.log("dlkajsld;kfj ", mapJson.bottom[y][x], mapJson.top[y][x])
      c.drawImage(db_img[spriteJson[mapJson.bottom[y][x]]], x * pixelSize - pixelSize / 2 + half_disp_width * 16, y * pixelSize - pixelSize / 2 + half_disp_height * 16);
      if (mapJson.top[y][x])
        c.drawImage(db_img[spriteJson[mapJson.top[y][x]]], x * pixelSize - pixelSize / 2 + half_disp_width * 16, y * pixelSize - pixelSize / 2 + half_disp_height * 16);
    }
  }

  console.log("\n\n")
}
