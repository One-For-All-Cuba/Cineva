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
| GET | `/watch/<type>/<id>/` | Vista reproductor (placeholder) |
| GET | `/health/` | JSON estado (version, catalog, tmdb) |
| GET | `/api/catalog/?kind=&q=&genero=&ano=&orden=` | API JSON del catálogo |
| GET | `/accounts/google/login/` | OAuth Google (allauth) |
| GET | `/qvapay/login/` | Hint SDK mini-app QvaPay |
| POST | `/qvapay/webhook/` | Webhook QvaPay (HMAC) |
| GET | `/static/cineva.css` | Estilos |

### Query params de filtros
- `genero` / `genre`
- `ano` / `year`
- `letra` / `letter` (A–Z)
- `orden`: `rating` \| `year` \| `az` \| `za`

## Externos (preparados, no obligatorios en demo)

| API | Uso |
|-----|-----|
| TMDB | Metadata y portadas reales si `TMDB_API_KEY` |
| Google OAuth | Login vía django-allauth |
| QvaPay mini-app SDK | `QvaPay.auth.requestLogin()` |
| QvaPay webhook | Firma `x-qvapay-signature` HMAC-SHA256 |

## Despliegue Alwaysdata
- Código: `~/apps/Cineva` (+ sync `1gb` vía rclone cuando aplique)
- Gunicorn: `127.0.0.1:8000`
- Caddy servicio: `[fd00::4:84e]:8300` → proxy a `:8000`
- Dominio: Apache → `services-oneforall.alwaysdata.net:8300`
- Arranque: `~/bin/start-cineva-public.sh`
