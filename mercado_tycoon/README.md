# Mercado Tycoon — v0.1

Juego de gestión 2D en navegador. Backend Flask + SQLite, pensado para correr
en el plan gratuito de PythonAnywhere (sin workers en background, sin
websockets, sin MySQL).

## Alcance de v0.1

- Login / registro (Flask-Login), una tienda por usuario.
- Catálogo de productos fijo (sembrado automáticamente al iniciar la app).
- Compra de inventario y venta manual (el jugador atiende haciendo clic).
- Simulación **catch-up**: cada vez que se carga el dashboard de la tienda,
  `simulation.catchup_store()` resuelve de forma cerrada (sin loops) lo que
  pasó desde `last_update_ts` — en v0.1 esto es la merma de productos
  perecederos. No hay ningún proceso corriendo en segundo plano.

## Correr localmente

```bash
cd mercado_tycoon
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

La app crea `mercado.db` (SQLite) y siembra el catálogo la primera vez que
arranca. Abre `http://127.0.0.1:5000`, regístrate y ya tienes una tienda.

## Siguientes fases

- **v0.2**: empleados, sueldos, automatización con gerente, mermas ligadas a
  reputación, reputación decayendo hacia la media.
- **v0.3**: múltiples tiendas por usuario, dashboard consolidado.

Ver el prompt de construcción original para el detalle de reglas y
restricciones de hosting (no implementar Celery/RQ/websockets/MySQL/cron).
