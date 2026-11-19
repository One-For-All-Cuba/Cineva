# Bitácora Cineva

## 2026-11-19 — v0.8.0 UI estable + reinicio

### Problema reportado
- Al refrescar, la página se veía distinta cada vez.

### Causa
1. El dominio público (`oneforall.alwaysdata.net`) a menudo servía **v0.2** (proceso del panel Alwaysdata), mientras el stack local ya era 0.7+.
2. Portadas vía `picsum.photos` podían variar de percepción; se sustituyen por **SVG data-URI fijos** por título/id.

### Acciones
- Portadas SVG generadas en `demo_catalog.py` (gradiente + título + badge HD) — idénticas en cada recarga.
- VERSION `0.8.0`.
- Deploy a `~/apps/Cineva`, sync `1gb`, reinicio gunicorn 127.0.0.1:8000 + Caddy fd00::4:84e:8300.
- Script `start-cineva-public.sh` actualizado (health no va a MCP).

### Nota panel
Si el dominio sigue en 0.2, reiniciar el sitio/servicio en el panel Alwaysdata (puerto 8300).
