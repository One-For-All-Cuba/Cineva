# Cineva — Endpoints y APIs

**Versión:** 0.10.2

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
| GET | `/watch/<type>/<id>/` | Vista reproductor: **selector de servidores alternativos** (`?provider=key`), iframe del embed, botón **Descargar** si hay `download_url` |
| GET | `/health/` | JSON estado (version, catalog, items) |
| GET | `/api/catalog/?kind=&q=&genero=&ano=&orden=` | API JSON del catálogo |
| GET | `/accounts/google/login/` | OAuth Google (allauth) |
| GET | `/qvapay/login/` | Hint SDK mini-app QvaPay |
| POST | `/qvapay/webhook/` | Webhook QvaPay (HMAC) |
| GET | `/static/cineva.css` | Estilos (type-badge, server-bar, etc.) |
| GET/POST | `/panel/` | Panel admin (staff) |
| GET/POST | `/panel/plugin/<key>/` | Editar proveedor |

### Query params de filtros
- `genero` / `genre`
- `ano` / `year`
- `letra` / `letter` (A–Z)
- `orden`: `rating` \| `year` \| `az` \| `za`

### Query en watch
- `provider`: key del ProviderPlugin para cambiar el embed/descarga (ej. `vidlink`, `vsembed`, `vidapi`, `videasy`).

## Servidores de reproducción (ProviderPlugin)

Sembrados por defecto en `bootstrap.ensure_defaults()`:

| key | Nombre | embed_url (plantilla) |
|-----|--------|------------------------|
| vidlink | VidLink | `https://vidlink.pro/{type}/{id}?sub_label=Spanish&player=jw&autoplay=true` |
| vsembed | VSEmbed | `https://vsembed.ru/embed/{type}?tmdb={id}&ds_lang=es` |
| vidapi | VidAPI | `https://vidapi.xyz/embed/{type}/{id}` |
| videasy | Videasy | `https://player.videasy.net/{type}/{id}` |
| youtube_trailer | YouTube tráilers | (solo trailer) |
| custom_json | API JSON propia | configurable |

Variables de plantilla: `{id}`, `{type}` (movie\|tv), `{slug}`, `{title}`, `{trailer_key}`.

Descarga: campo `download_url` del ítem o plantilla del proveedor.

## Externos

| API | Uso |
|-----|-----|
| Proveedores custom | Catálogo JSON + embed_url / download_url / trailer_url en panel |
| Google OAuth | Login vía django-allauth |
| QvaPay mini-app SDK | `QvaPay.auth.requestLogin()` |
| QvaPay webhook | Firma `x-qvapay-signature` HMAC-SHA256 |

## Despliegue Alwaysdata
- Código: `~/apps/Cineva` o `/home/oneforall/mnt/1gb/Cineva` (udocker namespace)
- Gunicorn: `127.0.0.1:8000` o 0.0.0.0:8000
- Caddy servicio: proxy
- Dominio: oneforall.alwaysdata.net
- Arranque: scripts en bin/ y start.sh (ejecuta migrate + ensure_defaults)
- Tras pull: reiniciar gunicorn / script udocker-ns para cargar proveedores y plantillas nuevas.
