// Animación puramente cosmética del piso de venta.
// Se genera en el cliente a partir del último snapshot recibido del servidor
// (reputación, cantidad de productos); no depende de eventos en vivo.
function initFloor(canvas, snapshot) {
  const ctx = canvas.getContext('2d');
  const customerCount = Math.max(1, Math.min(8, Math.round(snapshot.reputation / 15)));
  const customers = Array.from({ length: customerCount }, (_, i) => ({
    x: (i * 70) % canvas.width,
    speed: 0.4 + (i % 3) * 0.2,
    y: 40 + (i % 3) * 30,
  }));

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#eef2f0';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = '#8a6d3b';
    for (let shelf = 0; shelf < Math.min(6, snapshot.productCount || 0); shelf++) {
      ctx.fillRect(20 + shelf * 90, 10, 60, 14);
    }

    ctx.fillStyle = '#3a7d44';
    customers.forEach((c) => {
      c.x = (c.x + c.speed) % canvas.width;
      ctx.beginPath();
      ctx.arc(c.x, c.y, 6, 0, Math.PI * 2);
      ctx.fill();
    });

    requestAnimationFrame(draw);
  }

  draw();
}
