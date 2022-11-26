"restric mode";

// Create websocket connection
const url = "ws://localhost:50000";
const connection = new WebSocket(url);

// Shoud not be hardcoded
const pixelSize = 16;
const mapWidth = 20;
const mapHeight = 20;

// Get and resize canvas
const canvas = document.querySelector("canvas");
canvas.width = mapWidth * pixelSize;
canvas.height = mapHeight * pixelSize;

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
      // console.log(mapJson);
      drawMap();
  }
};

function drawMap() {
  for (let y = 0; y < mapJson.bottom.length; y++) {
    for (let x = 0; x < mapJson.bottom[y].length; x++) {
      if (mapJson.bottom[y][x] === 0)
        c.drawImage(groundImg, x * pixelSize, y * pixelSize);
      if (mapJson.top[y][x] === 1)
        c.drawImage(wallImg, x * pixelSize, y * pixelSize);
      else if (mapJson.top[y][x] === 2)
        c.drawImage(playerImg, x * pixelSize, y * pixelSize);
    }
  }
}
