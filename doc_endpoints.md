# Cineva — Endpoints y APIs

## Internos (app Django)

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Home: hero + rails películas/series/anime + sidebar populares |
| GET | `/peliculas/` | Catálogo películas + filtros género/año/letra/orden |
| GET | `/series/` | Catálogo series + filtros |
| GET | `/anime/` | Catálogo anime + filtros |
| GET | `/search/?q=` | Búsqueda (+ mismos filtros) |
| GET | `/movie/<id>/` | Ficha película |
| GET | `/tv/<id>/` | Ficha serie/anime |
| GET | `/watch/<type>/<id>/` | Vista reproductor: selector de proveedor (`?provider=key`), embed de servidores externos, botón descargar si hay download_url |
| GET | `/health/` | JSON estado (version, catalog, items) |
| GET | `/api/catalog/?kind=&q=&genero=&ano=&orden=` | API JSON del catálogo |
| GET | `/accounts/google/login/` | OAuth Google (allauth) |
| GET | `/qvapay/login/` | Hint SDK mini-app QvaPay |
| POST | `/qvapay/webhook/` | Webhook QvaPay (HMAC) |
| GET | `/static/cineva.css` | Estilos (incluye type-badge en portadas) |

### Query params de filtros
- `genero` / `genre`
- `ano` / `year`
- `letra` / `letter` (A–Z)
- `orden`: `rating` \| `year` \| `az` \| `za`

### Query en watch
- `provider`: key del ProviderPlugin para cambiar el embed/descarga.

## Externos (preparados, no obligatorios en demo)

| API | Uso |
|-----|-----|
| Proveedores custom | Catálogo JSON + embed_url / download_url / trailer_url configurables en panel |
| Google OAuth | Login vía django-allauth |
| QvaPay mini-app SDK | `QvaPay.auth.requestLogin()` |
| QvaPay webhook | Firma `x-qvapay-signature` HMAC-SHA256 |

## Despliegue Alwaysdata
- Código: `~/apps/Cineva` o `/home/oneforall/mnt/1gb/Cineva` (udocker namespace)
- Gunicorn: `127.0.0.1:8000` o 0.0.0.0:8000
- Caddy servicio: proxy
- Dominio: oneforall.alwaysdata.net
- Arranque: scripts en bin/ y start.sh (ejecuta migrate)
