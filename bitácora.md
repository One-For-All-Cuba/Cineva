# Bitácora Cineva

## 2026-11-19 — Reinicio y UI 0.7.0

### Acciones
- Subido a GitHub `master` la UI profesional v0.7 (hover play, chips de género, filtros, sidebar).
- Corregido Caddyfile: `/health` ya no se desvía al MCP; queda en Cineva.
- Sincronizado código en `~/apps/Cineva` desde GitHub.
- Reinicio completo: kill gunicorn/caddy previos, arranque gunicorn `:8000` + Caddy `:8300` (bind `fd00::4:84e`).
- Documentación de endpoints actualizada en `doc_endpoints.md`.

### Problema conocido
- `https://oneforall.alwaysdata.net/` puede seguir respondiendo **0.2** si el proceso del **panel Alwaysdata** (User program / reverse proxy a `services-oneforall:8300`) no se ha reiniciado desde el panel.
- Localmente `127.0.0.1:8000` y `[fd00::4:84e]:8300` sirven **0.7.0**.
- `sites.conf` de Apache no es escribible por el usuario; solo el panel puede reasignar el backend.

### Errores
- Proxy público aún apuntaba a stack antiguo (Via: Caddy + health 0.2) mientras el código en disco ya era 0.6+/0.7.
- `pkill` a veces cierra la sesión SSH (exit 255); usar kill por PID + gunicorn `--daemon`.

### Verificación post-reinicio
```bash
curl -fsS http://127.0.0.1:8000/health/
curl -fsS -g http://[fd00::4:84e]:8300/health/
curl -fsS https://oneforall.alwaysdata.net/health/
```
