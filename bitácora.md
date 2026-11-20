# Bitácora Cineva

## 2026-11-19 — v0.9.2

### Hecho
- Eliminada opción/configuración **TMDB**.
- Panel admin reorganizado (config integrada + proveedores).
- Si un proveedor activo tiene `catalog_url`, el sitio **no usa demo**.
- Inicio con **carruseles** (botones ‹ › + scroll).
- Proveedor `custom_json` para API propia legítima.

### No implementado (rechazado)
- Proveedor basado en **cuevana3t.pro** u otros sitios de streaming no autorizados (catálogo + video completo). Viola derechos de autor.

### Alternativa legal
- Configurar `catalog_url` con tu propio JSON.
- `embed_url` / `trailer_url` hacia fuentes que controles o tráilers oficiales (YouTube).

## 2026-11-20 — v0.10.1

### Hecho
- En vista **ver películas** (`/watch/<type>/<id>/`): selector de proveedor (cambia embed de servidores externos configurados).
- Botón **Descargar** si el proveedor o el ítem tiene `download_url` (plantilla o URL directa).
- En portadas (listados, home, detalle, rails): badge en esquina superior izquierda: **Película** / **Serie** / **Animado**.
- Campo `download_url` en modelo ProviderPlugin + migración 0004.
- Panel de proveedor actualizado para configurar URL de descarga.
- Version bump a 0.10.1.

### Notas
- Los servidores externos se configuran desde el panel (embed_url / download_url). No se hardcodean fuentes no autorizadas.
- Al reiniciar el servicio se aplica la migración automáticamente (start.sh ejecuta migrate).
