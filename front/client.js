"restric mode";

// const url = "ws://localhost:50000";
// const connection = new WebSocket(url);
const canvas = document.querySelector("canvas");
const c = canvas.getContext("2d");

const groundImg = new Image();
groundImg.src = "img/ground.png";
const wallImg = new Image();
wallImg.src = "img/wall.png";
const playerImg = new Image();
playerImg.src = "img/player.png";

const pixelSize = 16;
const mapWidth = 15;
const mapHeight = 9;

// connection.onopen = () => {
//   window.addEventListener("keydown", (e) => {
//     connection.send(e.key);
//   });
// };
// connection.onerror = (error) => {
//   console.log(`WebSocket error: ${error}`);
// };
// connection.onmessage = (e) => {
//   console.log(e.data);
// };

const map = [];
function generateMap() {
  for (let i = 0; i < mapWidth * mapHeight; i++) {
    map.push(Math.floor(Math.random() * 2));
  }
}
generateMap();

canvas.width = mapWidth * pixelSize;
canvas.height = mapHeight * pixelSize;

playerImg.onload = drawImageActualSize; // Draw when image has loaded

function drawImageActualSize() {
  //   c.drawImage(groundImg, 12 * 16, 0);
  for (let i = 0; i < mapHeight; i++) {
    for (let j = 0; j < mapWidth; j++) {
      index = i * mapWidth + j;
      if (map[index] === 0)
        c.drawImage(groundImg, j * pixelSize, i * pixelSize);
      else c.drawImage(wallImg, j * pixelSize, i * pixelSize);
    }
  }
  c.drawImage(playerImg, 0, 0);
}
