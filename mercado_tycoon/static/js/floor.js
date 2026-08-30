// Animación puramente cosmética del piso de venta, generada en el cliente a
// partir del último snapshot recibido del servidor (reputación, categorías
// en inventario). No depende de eventos en vivo ni de un servidor push.
const CATEGORY_EMOJI = {
  abarrotes: '📦',
  lacteos: '🥛',
  panaderia: '🍞',
  frutas: '🍎',
  bebidas: '🥤',
};

function initFloor(canvas, snapshot) {
  const ctx = canvas.getContext('2d');
  const width = canvas.width;
  const height = canvas.height;

  const customerCount = Math.max(1, Math.min(6, Math.round(snapshot.reputation / 18)));
  const customers = Array.from({ length: customerCount }, (_, i) => ({
    x: width - 40 - i * 90,
    y: height - 36,
    speed: 0.5 + (i % 3) * 0.15,
    emoji: snapshot.hasStock ? '🧍' : '🚶',
  }));

  const shelfIcons = (snapshot.categories && snapshot.categories.length
    ? snapshot.categories
    : ['abarrotes']
  ).map((c) => CATEGORY_EMOJI[c] || '🛍️');

  function drawFloorTiles() {
    ctx.fillStyle = '#eef6ee';
    ctx.fillRect(0, 0, width, height);
    ctx.fillStyle = '#e2efe2';
    const tile = 40;
    for (let y = 60; y < height; y += tile) {
      for (let x = (y / tile) % 2 === 0 ? 0 : tile; x < width; x += tile * 2) {
        ctx.fillRect(x, y, tile, tile);
      }
    }
  }

  function drawShelves() {
    const shelfWidth = 70;
    const gap = 16;
    const startX = 20;
    shelfIcons.slice(0, 7).forEach((emoji, i) => {
      const x = startX + i * (shelfWidth + gap);
      ctx.fillStyle = '#a9784a';
      ctx.fillRect(x, 10, shelfWidth, 34);
      ctx.fillStyle = '#7a5735';
      ctx.fillRect(x, 40, shelfWidth, 6);
      ctx.font = '22px system-ui, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(emoji, x + shelfWidth / 2, 33);
    });
  }

  function drawCounter() {
    const counterX = width - 130;
    const counterY = height - 60;
    ctx.fillStyle = '#c9a06a';
    ctx.fillRect(counterX, counterY, 100, 40);
    ctx.fillStyle = '#8a6d3b';
    ctx.fillRect(counterX, counterY, 100, 8);

    ctx.font = '30px system-ui, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('🧑‍💼', counterX + 50, counterY - 8);
    ctx.font = '12px system-ui, sans-serif';
    ctx.fillStyle = '#555';
    ctx.fillText('Tú (cajero/a)', counterX + 50, counterY + 55);
  }

  function drawCustomers() {
    ctx.font = '26px system-ui, sans-serif';
    ctx.textAlign = 'center';
    customers.forEach((c) => {
      c.x -= c.speed;
      if (c.x < 40) {
        c.x = width - 40;
      }
      ctx.fillText(c.emoji, c.x, c.y);
    });
  }

  function draw() {
    drawFloorTiles();
    drawShelves();
    drawCounter();
    drawCustomers();
    requestAnimationFrame(draw);
  }

  draw();
}
