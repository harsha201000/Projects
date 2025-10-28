// Canvas and rendering setup
const canvas = document.getElementById("c");
const ctx = canvas.getContext("2d");

ctx.imageSmoothingEnabled = false;  // Important!

// Pixel and screen variables
const pixels = [];
const pixelMap = new Map();

let offsetX = 0;
let offsetY = 0;

// === INPUT HANDLING ===

// Drawing
let isDragging = false;
let brushDown = false;

let dragStartX = 0;
let dragStartY = 0;
let startOffsetX = 0;
let startOffsetY = 0;

let dragStartPixelX = 0;
let dragStartPixelY = 0;

// Zooming
let zoom = 1;

let mouse = {
  x: 0,
  y: 0,
  size: 1
}

// Prevent right-click context menu on canvas
canvas.addEventListener('contextmenu', (e) => {
  e.preventDefault();
});

// Keyboard zoom handling — canvas needs tabindex="0" in HTML for this to work
// Modify keydown zoom handling:

window.addEventListener('keydown', (e) => {
  if (e.target !== document.body && e.target !== canvas) return; // prevent if focused on inputs
  if (e.key !== "ArrowUp" && e.key !== "ArrowDown") return;

  e.preventDefault();

  const oldZoom = zoom;
  let newZoom = zoom;

  if (e.key === "ArrowUp") {
    newZoom = Math.min(zoom + 0.1, 10);
  } else if (e.key === "ArrowDown") {
    newZoom = Math.max(zoom - 0.1, 0.1);
  }

  // Adjust offset to zoom around mouse position
  // mouse.x and mouse.y are canvas coordinates
  offsetX = mouse.x - (mouse.x - offsetX) * (newZoom / oldZoom);
  offsetY = mouse.y - (mouse.y - offsetY) * (newZoom / oldZoom);

  zoom = newZoom;
});


canvas.addEventListener('mousedown', (e) => {
  if (e.button === 0) { // Left click for brush
    brushDown = true;
  }

  if (e.button !== 2) return; // Right-click only for drag
  e.preventDefault();

  isDragging = true;
  const rect = canvas.getBoundingClientRect();
  const mouseX = e.clientX - rect.left;
  const mouseY = e.clientY - rect.top;

  dragStartX = mouseX;
  dragStartY = mouseY;
  startOffsetX = offsetX;
  startOffsetY = offsetY;

  dragStartPixelX = (mouseX - offsetX) / zoom;
  dragStartPixelY = (mouseY - offsetY) / zoom;
});

window.addEventListener('mouseup', () => {
  isDragging = false;
  brushDown = false;
});

window.addEventListener('mouseleave', () => {
  isDragging = false;
});

canvas.addEventListener('mousemove', (e) => {
  const rect = canvas.getBoundingClientRect();
  mouse.x = e.clientX - rect.left;
  mouse.y = e.clientY - rect.top;

  if (isDragging) {
    // Sync offset so the pixel under the mouse stays consistent during drag
    offsetX = mouse.x - dragStartPixelX * zoom;
    offsetY = mouse.y - dragStartPixelY * zoom;
  }
});

// === BRUSH STUFF ===

let brush = {
  r: 255,
  g: 0,
  b: 0,
  a: 1,

  type: 0,
  /*
     0: Brush
     1: Select
  */

  size: 3
}

const brushConfirm = document.getElementById("brush-update");

brushConfirm.onclick = function() {
    brush.r = document.querySelector("#brush-settings #rin").value;
    brush.g = document.querySelector("#brush-settings #gin").value;
    brush.b = document.querySelector("#brush-settings #bin").value;
    brush.a = document.querySelector("#brush-settings #ain").value;
    brush.size = document.querySelector("#brush-settings #sin").value;
}

// === INITIALIZATION ===

function init() {
  generatePixels(100, 100);
  loop();
}

function generatePixels(rows, cols) {
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      const pixel = { x, y, r: 255, g: 255, b: 255, a: 1 };
      pixels.push(pixel);
      pixelMap.set(`${x},${y}`, pixel);
    }
  }
}

// === MAIN LOOP ===

function loop() {
  try {
    tick();
    render();
    requestAnimationFrame(loop);
  } catch (e) {
    alert(e);
  }
}

function tick() {
  if (brushDown) {
    // Convert mouse pos to pixel coords (integers!)
    const px = Math.floor((mouse.x - offsetX) / zoom);
    const py = Math.floor((mouse.y - offsetY) / zoom);
    placePixel(px, py);
  }
}

// === RENDERING ===

function render() {
  const cellSize = 10;

  // Clear whole canvas first
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  drawCheckerboard(10, 10, cellSize);
  drawPixels();

  // Draw cursor position (small green dot)
  ctx.fillStyle = "green";
  ctx.fillRect(mouse.x, mouse.y, 2, 2);
}

function drawCheckerboard(rows, cols, cellSize) {
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      ctx.fillStyle = (isEven(x) === isEven(y)) ? "gray" : "darkgray";
      ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
    }
  }
}

function drawPixels() {
  const size = Math.max(1, Math.round(zoom)); // Ensure minimum size is 1

  for (const p of pixels) {
    ctx.fillStyle = `rgba(${p.r}, ${p.g}, ${p.b}, ${p.a})`;

    const drawX = Math.round(p.x * zoom + offsetX);
    const drawY = Math.round(p.y * zoom + offsetY);

    ctx.fillRect(drawX, drawY, size, size);
  }
}


//This was done by chatgpt because my brain exploded for this function
function placePixel(centerX, centerY) {
  const half = Math.floor(brush.size / 2);
  for (let y = centerY - half; y <= centerY + half; y++) {
    for (let x = centerX - half; x <= centerX + half; x++) {
      const pixel = pixelMap.get(`${x},${y}`);
      if (pixel) {
        pixel.r = brush.r;
        pixel.g = brush.g;
        pixel.b = brush.b;
        pixel.a = brush.a;
      }
    }
  }
}

// Utility function (could move to util.js if you want)
function isEven(num) {
  return (num % 2 === 0);
}

// Start
init();

document.getElementById("new").onclick = function() {
    document.getElementById("new-screen").style.display = "block";
}

document.getElementById("confirm-new").onclick = function() {
  const width = parseInt(document.getElementById("winput").value);
  const height = parseInt(document.getElementById("hinput").value);

  // Clear existing pixels
  pixels.length = 0;
  pixelMap.clear();

  generatePixels(width, height);
  document.getElementById("new-screen").style.display = "none";
};
